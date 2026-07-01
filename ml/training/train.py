import os, sys, time, json
import joblib
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
import xgboost as xgb

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from preprocessing.preprocess import generate_synthetic_data, preprocess

SAVE_DIR = "ml/saved_models"
os.makedirs(SAVE_DIR, exist_ok=True)

def train_all_models():
    df = generate_synthetic_data()
    X, y, scaler, features = preprocess(df)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    models = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=100, random_state=42),
        "xgboost": xgb.XGBClassifier(use_label_encoder=False, eval_metric="logloss", random_state=42),
        "svm": SVC(probability=True, random_state=42),
        "naive_bayes": GaussianNB()
    }

    metrics = {}

    for name, model in models.items():
        print(f"\nTraining {name}...")
        start = time.time()
        model.fit(X_train, y_train)
        train_time = time.time() - start

        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)
        roc = roc_auc_score(y_test, y_proba)

        metrics[name] = {
            "accuracy": round(acc * 100, 2),
            "precision": round(prec * 100, 2),
            "recall": round(rec * 100, 2),
            "f1": round(f1 * 100, 2),
            "roc_auc": round(roc, 3),
            "training_time": round(train_time, 3)
        }

        joblib.dump(model, os.path.join(SAVE_DIR, f"{name}_model.pkl"))
        print(f"{name}: acc={acc*100:.2f}% f1={f1*100:.2f}% roc={roc:.3f}")

    joblib.dump(scaler, os.path.join(SAVE_DIR, "scaler.pkl"))
    joblib.dump(features, os.path.join(SAVE_DIR, "features.pkl"))

    with open(os.path.join(SAVE_DIR, "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    print(f"\nAll models trained and saved to {SAVE_DIR}")

if __name__ == "__main__":
    train_all_models()