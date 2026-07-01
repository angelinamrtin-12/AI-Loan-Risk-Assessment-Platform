import joblib
import os
import numpy as np
from config import settings

MODEL_PATH = settings.MODEL_PATH

MODEL_FILE = os.path.join(MODEL_PATH, "xgboost_model.pkl")
SCALER_FILE = os.path.join(MODEL_PATH, "scaler.pkl")
FEATURE_FILE = os.path.join(MODEL_PATH, "features.pkl")

model = None
scaler = None
features = None

def load_model():
    global model, scaler, features
    if model is None:
        model = joblib.load(MODEL_FILE)
        scaler = joblib.load(SCALER_FILE)
        features = joblib.load(FEATURE_FILE)
    return model, scaler, features

def predict_risk(data: dict):
    model, scaler, features = load_model()

    input_arr = np.array([[
        data["age"], data["income"], data["credit_score"],
        data["loan_amount"], data["loan_term"],
        data["employment_years"], data["debt_to_income"]
    ]])
    input_scaled = scaler.transform(input_arr)

    proba = model.predict_proba(input_scaled)[0][1]  # probability of default
    risk_score = round(proba * 100, 2)

    if risk_score < 40:
        label = "Low Risk"
    elif risk_score < 70:
        label = "Medium Risk"
    else:
        label = "High Risk"

    confidence = round(max(proba, 1 - proba) * 100, 2)

    return {
        "risk_score": risk_score,
        "risk_label": label,
        "confidence": confidence,
        "raw_proba": float(proba)
    }