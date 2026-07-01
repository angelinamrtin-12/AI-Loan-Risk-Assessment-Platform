from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime
import os, json
from models.database import get_db, Application, User
from api.deps import get_current_user
from config import settings

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/stats")
def get_stats(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Application)
    if user.role == "applicant":
        query = query.filter(Application.user_id == user.id)

    total_apps = query.count()
    total_predictions = query.filter(Application.risk_score.isnot(None)).count()
    avg_risk = query.with_entities(func.avg(Application.risk_score)).scalar() or 0
    
    pending = query.filter(Application.status == "Pending").count()
    approved = query.filter(Application.status == "Approved").count()
    rejected = query.filter(Application.status == "Rejected").count()

    today_predictions = 0
    default_rate = 0
    total_users = 0

    if user.role in ["officer", "admin"]:
        total_users = db.query(User).count()
        
    if user.role == "admin":
        today = datetime.utcnow().date()
        today_predictions = query.filter(func.date(Application.created_at) == today).count()
        
        if total_predictions > 0:
            # Using High Risk as a proxy for Default Rate
            high_risk_count = query.filter(Application.risk_label == "High Risk").count()
            default_rate = round((high_risk_count / total_predictions) * 100, 2)

    return {
        "total_applications": total_apps,
        "total_predictions": total_predictions,
        "average_risk": round(avg_risk, 2),
        "pending": pending,
        "approved": approved,
        "rejected": rejected,
        "total_users": total_users,
        "role": user.role,
        "name": user.name,
        "today_predictions": today_predictions,
        "default_rate": default_rate
    }

@router.get("/charts")
def get_charts(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin access only")
    
    # 1. Apps per month
    apps_per_month = db.query(
        extract('month', Application.created_at).label('month'),
        func.count(Application.id).label('count')
    ).group_by('month').all()
    
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    apps_data = [{"name": months[int(m)-1], "value": c} for m, c in apps_per_month]

    # 2. Approval Rate
    approved = db.query(Application).filter(Application.status == "Approved").count()
    rejected = db.query(Application).filter(Application.status == "Rejected").count()
    pending = db.query(Application).filter(Application.status == "Pending").count()
    approval_data = [
        {"name": "Approved", "value": approved},
        {"name": "Rejected", "value": rejected},
        {"name": "Pending", "value": pending}
    ]

    # 3. Risk Distribution
    low = db.query(Application).filter(Application.risk_label == "Low Risk").count()
    med = db.query(Application).filter(Application.risk_label == "Medium Risk").count()
    high = db.query(Application).filter(Application.risk_label == "High Risk").count()
    risk_data = [
        {"name": "Low Risk", "value": low},
        {"name": "Medium Risk", "value": med},
        {"name": "High Risk", "value": high}
    ]

    # 4. Model Accuracy
    metrics_file = os.path.join(settings.MODEL_PATH, "metrics.json")
    model_acc = []
    if os.path.exists(metrics_file):
        with open(metrics_file, "r") as f:
            data = json.load(f)
        for k, v in data.items():
            model_acc.append({"name": k.replace("_", " ").title(), "value": v["accuracy"]})
            
    return {
        "apps_per_month": apps_data,
        "approval_rate": approval_data,
        "risk_distribution": risk_data,
        "model_accuracy": model_acc
    }