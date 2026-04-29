from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *
import numpy as np
import joblib

# -----------------------------
# Load ML model once
# -----------------------------
MODEL_PATH = "Data/Chronic model.pkl"
Train_model = joblib.load(MODEL_PATH)


def prediction(request):
    if request.method == 'POST':
        form = PredictionForm(request.POST, request.FILES)
        if form.is_valid():
            # ---- Save patient data temporarily ----
            patient = form.save(commit=False)  # Do not commit yet

            # ---- Encode categorical values ----
            appetite_map = {'Good': 1, 'Poor': 0}

            # ---- Prepare input features (must match model training order) ----
            input_data = np.array([[
                float(patient.age),
                float(patient.blood_pressure),
                float(patient.specific_gravity),
                float(patient.albumin),
                float(patient.sugar),
                int(patient.red_blood_cells),
                int(patient.pus_cell),
                int(patient.pus_cell_clumps),
                int(patient.bacteria),
                float(patient.blood_glucose_random),
                float(patient.blood_urea),
                float(patient.serum_creatinine),
                float(patient.sodium),
                float(patient.potassium),
                float(patient.hemoglobin),
                float(patient.packed_cell_volume),
                float(patient.white_blood_cell_count),
                float(patient.red_blood_cell_count),
                int(patient.hypertension),
                int(patient.diabetes_mellitus),
                int(patient.coronary_artery_disease),
                int(appetite_map.get(patient.appetite, 0)),
                int(patient.pedal_edema),
                int(patient.anemia)
            ]])

            # ---- Predict CKD using XGBClassifier ----
            prediction_result = Train_model.predict(input_data)[0]  # 0 = No CKD, 1 = CKD

            # ---- Get prediction probability ----
            try:
                prediction_prob = Train_model.predict_proba(input_data)[0][int(prediction_result)]
            except AttributeError:
                prediction_prob = None  # If regressor, no proba available

            # ---- Save prediction in the patient record ----
            patient.ckd_prediction = int(prediction_result)
            patient.prediction_prob = round(float(prediction_prob * 100), 2) if prediction_prob else None

            # ---- Save patient details + prediction to DB ----
            patient.save()

            # ---- Render result page ----
            return render(request, 'result.html', {'patient': patient})

    else:
        form = PredictionForm()

    return render(request, 'prediction.html', {'form': form})


# Patients List ================================================================================

def patients(request):
    data = Prediction_Model.objects.all()
    return render(request, 'patients.html', {'register_data': data})


# View Patient ==============================================================================

def view_patient(request, id):
    view_patient = get_object_or_404(Prediction_Model, id=id)
    return render(request, 'view_patient.html', {'view_patient': view_patient})



# Update Patient ===========================================================================

def update_patient(request, id):
    data = get_object_or_404(Prediction_Model, id=id)
    
    if request.method == 'POST':
        form = PredictionForm(request.POST, request.FILES, instance=data)
        if form.is_valid():
            form.save()
            messages.success(request, "User updated successfully!")
            return redirect('ML_Model:patients')
    else:
        form = PredictionForm(instance=data)

    return render(request, 'update_patient.html', {'update_form': form})


# Delete Patient ===========================================================================

def delete_patient(request, id):
    user_data = get_object_or_404(Prediction_Model, id=id)
    user_data.delete()
    messages.success(request, "User deleted successfully!")
    return redirect('ML_Model:patients')


# Search Patient =========================================================================

from django.db.models import Q

def patients(request):
    query = request.GET.get('q', '').strip()

    register_data = Prediction_Model.objects.all()

    if query:
        register_data = register_data.filter(
            Q(name__icontains=query) 
        )

    return render(
        request,
        'patients.html',
        {
            'register_data': register_data,
            'query': query
        }
    )


# New Patients =====================================================================================

def new_patient(request):

    if request.method == 'POST':
        form = PredictionForm(request.POST, request.FILES)
        if form.is_valid():
            # ---- Save patient data temporarily ----
            patient = form.save(commit=False)  # Do not commit yet

            # ---- Encode categorical values ----
            appetite_map = {'Good': 1, 'Poor': 0}

            # ---- Prepare input features (must match model training order) ----
            input_data = np.array([[
                float(patient.age),
                float(patient.blood_pressure),
                float(patient.specific_gravity),
                float(patient.albumin),
                float(patient.sugar),
                int(patient.red_blood_cells),
                int(patient.pus_cell),
                int(patient.pus_cell_clumps),
                int(patient.bacteria),
                float(patient.blood_glucose_random),
                float(patient.blood_urea),
                float(patient.serum_creatinine),
                float(patient.sodium),
                float(patient.potassium),
                float(patient.hemoglobin),
                float(patient.packed_cell_volume),
                float(patient.white_blood_cell_count),
                float(patient.red_blood_cell_count),
                int(patient.hypertension),
                int(patient.diabetes_mellitus),
                int(patient.coronary_artery_disease),
                int(appetite_map.get(patient.appetite, 0)),
                int(patient.pedal_edema),
                int(patient.anemia)
            ]])

            # ---- Predict CKD using XGBClassifier ----
            prediction_result = Train_model.predict(input_data)[0]  # 0 = No CKD, 1 = CKD

            # ---- Get prediction probability ----
            try:
                prediction_prob = Train_model.predict_proba(input_data)[0][int(prediction_result)]
            except AttributeError:
                prediction_prob = None  # If regressor, no proba available

            # ---- Save prediction in the patient record ----
            patient.ckd_prediction = int(prediction_result)
            patient.prediction_prob = round(float(prediction_prob * 100), 2) if prediction_prob else None

            # ---- Save patient details + prediction to DB ----
            patient.save()

            # ---- Render result page ----
            messages.success(request, 'Patient created successfully')
            return redirect("ML_Model:patients")

    else:
        form = PredictionForm()

    return render(request, 'new_patient.html', {'form': form})
from django.test import TestCase

# Create your tests here.
