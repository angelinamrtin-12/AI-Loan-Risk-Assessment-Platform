from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.database import get_db, User
from models.schemas import UserCreate, UserLogin, Token, UserOut
from auth.auth_service import hash_password, verify_password
from auth.jwt_handler import create_access_token
from api.deps import get_current_user  # <--- MAKE SURE THIS LINE IS HERE

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=user.name,
        email=user.email,
        hashed_password=hash_password(user.password),
        role=user.role
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    token = create_access_token({"sub": new_user.email, "role": new_user.role})
    return {"access_token": token, "token_type": "bearer",
            "user": UserOut.model_validate(new_user, from_attributes=True)}

@router.post("/login", response_model=Token)
def login(creds: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == creds.email).first()
    if not user or not verify_password(creds.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token({"sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer",
            "user": UserOut.model_validate(user, from_attributes=True)}

@router.post("/logout")
def logout(user: User = Depends(get_current_user)):
    # JWT is stateless, so we just return success. 
    # The frontend will handle deleting the token from localStorage.
    return {"message": "Successfully logged out"}