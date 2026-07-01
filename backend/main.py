from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import auth, predict, applications, models, dashboard

app = FastAPI(title="AI Loan Risk Assessment Platform",
              description="Intelligent Loan Decisions with Explainable AI",
              version="1.0.0")

# CORS - allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router)
app.include_router(predict.router)
app.include_router(applications.router)
app.include_router(models.router)
app.include_router(dashboard.router)

@app.get("/")
def root():
    return {"message": "AI Loan Risk API is running 🚀"}

@app.get("/health")
def health():
    return {"status": "healthy"}