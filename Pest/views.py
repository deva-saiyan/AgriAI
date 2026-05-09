import os
import numpy as np
import tensorflow as tf
import traceback
from PIL import Image

from django.shortcuts import render
from django.conf import settings
from .models import PestClass


# ==============================
# GLOBAL CACHE
# ==============================
_model = None
_class_names = None


# ==============================
# LOAD MODEL
# ==============================
def get_model():
    global _model
    if _model is None:
        model_path = os.path.join(settings.BASE_DIR, "Pest", "Data", "f2.keras")
        print("Loading model from:", model_path)
        _model = tf.keras.models.load_model(model_path)
    return _model


# ==============================
# LOAD CLASS NAMES (VALID DATASET)
# ==============================
def get_class_names():
    global _class_names
    if _class_names is None:
        valid_dir = os.path.join(settings.BASE_DIR, "Pest", "Data", "Valid")

        # Read folder names directly (SAFE + FAST)
        _class_names = sorted([
            d for d in os.listdir(valid_dir)
            if os.path.isdir(os.path.join(valid_dir, d))
        ])

        print("Loaded classes:", _class_names)

    return _class_names


# ==============================
# PREPROCESS IMAGE
# ==============================
def preprocess(img_path):
    img = Image.open(img_path).convert("RGB")
    img = img.resize((224, 224))  # MUST match model

    img = np.array(img) / 255.0   # match training
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
            # SAVE IMAGE
            # ==============================
            record = PestClass(
                name=name,
                district=district,
                location=location,
                plant_type=plant_type,
                image=image_file
            )
            record.save()

            img_path = record.image.path
            print("Image Path:", img_path)

            # ==============================
            # LOAD MODEL + CLASSES
            # ==============================
            model = get_model()
            class_names = get_class_names()

            # ==============================
            # PREPROCESS
            # ==============================
            input_img = preprocess(img_path)

            # ==============================
            # PREDICT
            # ==============================
            preds = model.predict(input_img)[0]

            index = int(np.argmax(preds))
            confidence = float(preds[index]) * 100

            predicted_class = (
                class_names[index] if index < len(class_names) else "Unknown"
            )

            # ==============================
            # DEBUG (VERY IMPORTANT)
            # ==============================
            print("Raw Predictions:", preds)
            print("Predicted Index:", index)
            print("Predicted Class:", predicted_class)
            print("Confidence:", confidence)

            # ==============================
            # MESSAGE
            # ==============================
            message = f"🕷 Hello {name}, your pest image is detected."

            # ==============================
            # SAVE RESULT
            # ==============================
            record.predicted_disease = predicted_class
            record.confidence = round(confidence, 2)
            record.save()

            # ==============================
            # RESPONSE
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
            print(traceback.format_exc())
            return render(request, "pest_form.html", {
                "error": f"Prediction failed: {str(e)}"
            })

    return render(request, "pest_form.html")