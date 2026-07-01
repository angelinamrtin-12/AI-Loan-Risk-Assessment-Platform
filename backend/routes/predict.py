from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db, Application, User
from models.schemas import LoanApplicationIn, PredictionOut
from api.deps import get_current_user
from services.ml_service import predict_risk
from services.shap_service import get_shap_values

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("", response_model=PredictionOut)
def predict(application: LoanApplicationIn, db: Session = Depends(get_db),
            user: User = Depends(get_current_user)):
    data = application.dict()

    risk = predict_risk(data)
    shap_result = get_shap_values(data)

    # Save application
    new_app = Application(
        user_id=user.id,
        risk_score=risk["risk_score"],
        risk_label=risk["risk_label"],
        confidence=risk["confidence"],
        status="Pending",
        **data
    )
    db.add(new_app)
    db.commit()

    return {
        "risk_score": risk["risk_score"],
        "risk_label": risk["risk_label"],
        "confidence": risk["confidence"],
        "shap_values": shap_result["shap_values"],
        "explanation": shap_result["explanation"]
    }