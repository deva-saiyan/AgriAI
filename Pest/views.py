import os
import numpy as np
import tensorflow as tf
import traceback

from django.shortcuts import render
from django.conf import settings
from .models import PestClass


# ==============================
# LAZY LOADERS
# ==============================
_cnn_model = None
_class_names = None


def get_model():
    global _cnn_model
    if _cnn_model is None:
        model_path = os.path.join(settings.BASE_DIR, "Pest", "Data", "pest_2.keras")
        _cnn_model = tf.keras.models.load_model(model_path)
    return _cnn_model


def get_class_names():
    global _class_names
    if _class_names is None:
        valid_path = os.path.join(settings.BASE_DIR, "Pest", "Data", "Valid")
        valid_data = tf.keras.utils.image_dataset_from_directory(
    valid_path,
    label_mode="categorical",
    image_size=(224, 224),   # 🔥 FIXED
    batch_size=32,
    shuffle=False
)
        _class_names = valid_data.class_names
    return _class_names


# ==============================
# PREPROCESS
# ==============================
def preprocess(img_path):
    img = tf.keras.preprocessing.image.load_img(
        img_path,
        target_size=(224, 224)   # 🔥 FIXED
    )
    img = tf.keras.preprocessing.image.img_to_array(img)
    img = img / 255.0
    img = np.expand_dims(img, axis=0)
    return img

# ==============================
# VIEW
# ==============================
def pest_prediction(request):

    if request.method == "POST":

        try:
            # ==============================
            # USER INPUT
            # ==============================
            name       = request.POST.get("name", "").strip()
            district   = request.POST.get("district", "").strip()
            location   = request.POST.get("location", "").strip()
            plant_type = request.POST.get("plant_type", "").strip()
            image_file = request.FILES.get("image")

            if not image_file:
                return render(request, "pest_form.html", {
                    "error": "Please upload an image."
                })

            # ==============================
            # SAVE IMAGE (FIXED)
            # ==============================
            record = PestClass(
                name=name,
                district=district,
                location=location,
                plant_type=plant_type,
                image=image_file   # ✅ direct assign
            )
            record.save()  # 🔥 MUST SAVE FIRST

            img_path = record.image.path

            # Debug
            print("Image Path:", img_path)

            # ==============================
            # PREDICTION
            # ==============================
            model       = get_model()
            class_names = get_class_names()

            input_img   = preprocess(img_path)

            prediction  = np.squeeze(model.predict(input_img))
            index       = int(np.argmax(prediction))
            confidence  = float(np.max(prediction)) * 100

            predicted_class = class_names[index] if index < len(class_names) else "Unknown"

            # ==============================
            # CONFIDENCE FILTER
            # ==============================
            if confidence < 80:
                predicted_class = "Invalid Image / Not a Plant"
                message = f"❌ Sorry {name}, please upload a valid plant leaf image."
            else:
                message = f"🌿 Hello {name}, your plant disease is detected successfully."

            # ==============================
            # SAVE RESULT
            # ==============================
            record.predicted_disease = predicted_class
            record.confidence        = round(confidence, 2)
            record.save()

            # ==============================
            # RESULT PAGE
            # ==============================
            return render(request, "pest_result.html", {
                "name": name,
                "district": district,
                "location": location,
                "plant_type": plant_type,
                "prediction": predicted_class,
                "confidence": round(confidence, 2),
                "message": message,
                "image_url": record.image.url,
            })

        except Exception as e:
            print(traceback.format_exc())  # 🔥 full error log
            return render(request, "pest_form.html", {
                "error": f"Prediction failed: {str(e)}"
            })

    return render(request, "pest_form.html")