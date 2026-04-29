import os
import numpy as np
import tensorflow as tf

from django.shortcuts import render
from django.conf import settings

from .models import PlantDisease


# ==============================
# LAZY LOADERS
# ==============================
_cnn_model = None
_class_names = None


def get_model():
    global _cnn_model
    if _cnn_model is None:
        model_path = os.path.join(settings.BASE_DIR, "Leaf", "Data", "leafs.keras")
        _cnn_model = tf.keras.models.load_model(model_path)
    return _cnn_model


def get_class_names():
    global _class_names
    if _class_names is None:
        valid_path = os.path.join(settings.BASE_DIR, "Leaf", "Data", "Valid")
        valid_data = tf.keras.utils.image_dataset_from_directory(
            valid_path,
            label_mode="categorical",
            image_size=(128, 128),   # ✅ must match preprocess target_size
            batch_size=32,
            shuffle=False
        )
        _class_names = valid_data.class_names
    return _class_names


# ==============================
# IMAGE PREPROCESSING
# ==============================
def preprocess(img_path):
    img = tf.keras.preprocessing.image.load_img(
        img_path,
        target_size=(128, 128)   # ✅ matches training
    )
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = np.expand_dims(img, axis=0)   # shape: (1, 128, 128, 3)
    return img


# ==============================
# VIEW
# ==============================
def leaf_prediction(request):

    if request.method == "POST":

        # ==============================
        # USER INPUT
        # ==============================
        name       = request.POST.get("name", "").strip()
        district   = request.POST.get("district", "").strip()
        location   = request.POST.get("location", "").strip()
        plant_type = request.POST.get("plant_type", "").strip()
        image_file = request.FILES.get("image")

        if not image_file:
            return render(request, "leaf_form.html", {"error": "Please upload an image."})

        # ==============================
        # SAVE IMAGE VIA ImageField
        # ==============================
        record = PlantDisease(
            name=name,
            district=district,
            location=location,
            plant_type=plant_type,
        )
        record.image.save(image_file.name, image_file, save=False)
        img_path = record.image.path   # real filesystem path for TF

        # ==============================
        # PREDICTION
        # ==============================
        try:
            model       = get_model()
            class_names = get_class_names()

            input_img   = preprocess(img_path)
            prediction  = model.predict(input_img)
            index       = int(np.argmax(prediction))
            confidence  = float(np.max(prediction)) * 100

            predicted_class = class_names[index] if index < len(class_names) else "Unknown"

        except Exception as e:
            return render(request, "leaf_form.html", {
                "error": f"Prediction failed: {str(e)}"
            })

        # ==============================
        # CONFIDENCE FILTER
        # ==============================
        if confidence < 60:
            predicted_class = "Unknown"
            message = f"❌ Sorry {name}, your leaf disease could not be identified."
        else:
            message = f"🌿 Hello {name}, your plant disease is detected successfully."

        # ==============================
        # SAVE TO DATABASE
        # ==============================
        record.predicted_disease = predicted_class
        record.confidence        = round(confidence, 2)
        record.save()

        # ==============================
        # RESULT PAGE
        # ==============================
        return render(request, "leaf_result.html", {
            "name"       : name,
            "district"   : district,
            "location"   : location,
            "plant_type" : plant_type,
            "prediction" : predicted_class,
            "confidence" : round(confidence, 2),
            "message"    : message,
            "image_url"  : record.image.url,
        })

    return render(request, "leaf_form.html")