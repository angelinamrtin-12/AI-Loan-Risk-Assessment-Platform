import shap
import joblib
import numpy as np
import os
from config import settings

MODEL_PATH = settings.MODEL_PATH
MODEL_FILE = os.path.join(MODEL_PATH, "xgboost_model.pkl")
SCALER_FILE = os.path.join(MODEL_PATH, "scaler.pkl")

explainer = None
scaler = None
model = None

def load_explainer():
    global explainer, scaler, model
    if explainer is None:
        model = joblib.load(MODEL_FILE)
        scaler = joblib.load(SCALER_FILE)
        explainer = shap.TreeExplainer(model)
    return explainer, scaler, model

def get_shap_values(data: dict):
    explainer, scaler, model = load_explainer()

    input_arr = np.array([[
        data["age"], data["income"], data["credit_score"],
        data["loan_amount"], data["loan_term"],
        data["employment_years"], data["debt_to_income"]
    ]])
    input_scaled = scaler.transform(input_arr)
    shap_values = explainer.shap_values(input_scaled)

    feature_names = ["Age", "Income", "Credit Score", "Loan Amount",
                     "Loan Term", "Employment Years", "Debt to Income"]

    shap_dict = {}
    for name, val in zip(feature_names, shap_values[0]):
        shap_dict[name] = round(float(val), 3)

    # Generate explanation
    explanation = []
    sorted_features = sorted(shap_dict.items(), key=lambda x: abs(x[1]), reverse=True)
    for name, val in sorted_features[:4]:
        direction = "increases" if val > 0 else "decreases"
        explanation.append(f"{name} {direction} default probability")

    return {"shap_values": shap_dict, "explanation": explanation}