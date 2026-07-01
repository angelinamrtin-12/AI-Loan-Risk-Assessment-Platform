from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from models.database import get_db, Application, User
from models.schemas import ApplicationOut
from api.deps import get_current_user

router = APIRouter(prefix="/applications", tags=["applications"])

@router.get("", response_model=List[ApplicationOut])
def list_applications(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    query = db.query(Application)
    
    # If applicant, only fetch their applications
    if user.role == "applicant":
        query = query.filter(Application.user_id == user.id)
        
    return query.order_by(Application.created_at.desc()).all()

@router.get("/{app_id}", response_model=ApplicationOut)
def get_application(app_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    # Applicant can only see their own app
    if user.role == "applicant" and app.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this application")
        
    return app

@router.put("/{app_id}/status")
def update_status(app_id: int, status: str, db: Session = Depends(get_db),
                  user: User = Depends(get_current_user)):
    # Only officers and admins can change status
    if user.role not in ["officer", "admin"]:
        raise HTTPException(status_code=403, detail="Not authorized")
        
    if status not in ["Approved", "Rejected", "Pending"]:
         raise HTTPException(status_code=400, detail="Invalid status")
         
    app = db.query(Application).filter(Application.id == app_id).first()
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")
        
    app.status = status
    db.commit()
    return {"message": "Status updated", "status": status}