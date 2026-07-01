from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---- Auth ----
class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str = "applicant"

class UserLogin(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserOut

# ---- Loan Application ----
class LoanApplicationIn(BaseModel):
    name: str
    email: str
    age: int
    income: float
    credit_score: int
    loan_amount: float
    loan_term: int
    employment_years: float
    debt_to_income: float

class PredictionOut(BaseModel):
    risk_score: float
    risk_label: str
    confidence: float
    shap_values: dict
    explanation: List[str]

class ApplicationOut(BaseModel):
    id: int
    name: str
    email: str
    age: int
    income: float
    credit_score: int
    loan_amount: float
    loan_term: int
    employment_years: float
    debt_to_income: float
    risk_score: Optional[float]
    risk_label: Optional[str]
    confidence: Optional[float]
    status: str
    created_at: datetime
    class Config:
        from_attributes = True

# ---- ML Model Info ----
class ModelMetrics(BaseModel):
    name: str
    accuracy: float
    precision: float
    recall: float
    f1: float
    training_time: float