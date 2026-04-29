import os
import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from django.shortcuts import render
from django.contrib import messages
from .models import CropPrediction, TAMILNADU_DISTRICTS


# ==============================
# 1. LOAD MODEL
# ==============================
MODEL_PATH = os.path.join(
    settings.BASE_DIR,
    'Model',
    'Data',
    'Crop',
    'crop_model.pkl'
)

loaded = joblib.load(MODEL_PATH)

ann_model = loaded['ann_model']
gb_model = loaded['gb_model']
scaler = loaded['scaler']
label_encoder = loaded['label_encoder']
w_ann = loaded['w_ann']
w_gb = loaded['w_gb']
feature_columns = loaded['feature_columns']


# ==============================
# 2. PREDICTION FUNCTION
# ==============================
def predict_crop(input_dict):

    # Convert input to DataFrame
    df = pd.DataFrame([input_dict])

    # Ensure correct column order
    df = df[feature_columns]

    # Scale input (VERY IMPORTANT)
    df_scaled = scaler.transform(df)

    # ANN prediction
    ann_prob = ann_model.predict(df_scaled)
    if len(ann_prob.shape) == 1:
        ann_prob = np.expand_dims(ann_prob, axis=0)

    # XGBoost prediction
    gb_prob = gb_model.predict_proba(df_scaled)

    # Fusion
    final_prob = (w_ann * ann_prob) + (w_gb * gb_prob)

    # Final class
    pred_index = np.argmax(final_prob, axis=1)[0]
    prediction = label_encoder.inverse_transform([pred_index])[0]

    confidence = round(float(np.max(final_prob) * 100), 2)

    # Top 3 crops
    top3_idx = final_prob[0].argsort()[-3:][::-1]
    top3 = label_encoder.inverse_transform(top3_idx)
    top3_scores = [round(float(final_prob[0][i] * 100), 2) for i in top3_idx]

    return {
        "prediction": prediction,
        "confidence": confidence,
        "top3": list(zip(top3, top3_scores))
    }


# ---------------------------------------------------------------------------------------------


def crop_prediction(request):

    if request.method == 'POST':

        # ==========================
        # 1. USER INFO
        # ==========================
        name = request.POST.get('name')
        district = request.POST.get('district')
        place = request.POST.get('place')

        # ==========================
        # 2. SAFE FLOAT CONVERTER
        # ==========================
        def get_float(value):
            try:
                if value is None or value == "":
                    return 0.0
                return float(value)
            except:
                return 0.0

        # ==========================
        # 3. INPUT FEATURES
        # ==========================
        input_dict = {
            'cation_exchange_capacity': get_float(request.POST.get('cation_exchange_capacity')),
            'humidity': get_float(request.POST.get('humidity')),
            'nitrogen': get_float(request.POST.get('nitrogen')),
            'phosphorus': get_float(request.POST.get('phosphorus')),
            'potassium': get_float(request.POST.get('potassium')),
            'rainfall': get_float(request.POST.get('rainfall')),
            'soil_moisture': get_float(request.POST.get('soil_moisture')),
            'soil_ph': get_float(request.POST.get('soil_ph')),
            'temperature': get_float(request.POST.get('temperature')),
        }

        # ==========================
        # 4. 🔥 USE PROPER PIPELINE (IMPORTANT FIX)
        # ==========================
        result = predict_crop(input_dict)

        # ==========================
        # 5. SAVE TO DATABASE
        # ==========================
        CropPrediction.objects.create(
            name=name,
            district=district,
            place=place,
            cation_exchange_capacity=input_dict['cation_exchange_capacity'],
            humidity=input_dict['humidity'],
            nitrogen=input_dict['nitrogen'],
            phosphorus=input_dict['phosphorus'],
            potassium=input_dict['potassium'],
            rainfall=input_dict['rainfall'],
            soil_moisture=input_dict['soil_moisture'],
            soil_ph=input_dict['soil_ph'],
            temperature=input_dict['temperature'],
            prediction=result["prediction"],
            probability=result["confidence"],
            user=request.user if request.user.is_authenticated else None
        )

        # ==========================
        # 6. RESULT PAGE
        # ==========================
        return render(request, 'crop_result.html', {
            "prediction": result["prediction"],
            "probability": result["confidence"],
            "top3": result["top3"],
            "name": name,
            "district": district,
            "place": place
        })

    return render(request, 'crop_form.html', {
        'TAMILNADU_DISTRICTS': TAMILNADU_DISTRICTS
    })