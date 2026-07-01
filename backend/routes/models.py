from fastapi import APIRouter, Depends
import os, json
from config import settings

router = APIRouter(prefix="/models", tags=["models"])

MODEL_PATH = settings.MODEL_PATH

@router.get("/metrics")
def get_model_metrics():
    metrics_file = os.path.join(MODEL_PATH, "metrics.json")
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            return json.load(f)
    return {"error": "Metrics not found. Train models first."}

@router.get("/list")
def list_models():
    metrics_file = os.path.join(MODEL_PATH, "metrics.json")
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            data = json.load(f)
        return [{"name": k, **v} for k, v in data.items()]
    return []