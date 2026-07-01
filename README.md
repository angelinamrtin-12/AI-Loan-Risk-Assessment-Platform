# AI Loan Risk Assessment Platform

**Intelligent Loan Decisions with Explainable AI**

An advanced fintech platform that predicts loan default probability using Machine Learning and provides transparent, explainable AI decisions using SHAP values. Designed with a 100% Neomorphic UI inspired by Apple VisionOS and Stripe Dashboard.

---

## Key Features

- **Explainable AI (XAI):** Goes beyond simple predictions by showing exactly *why* a loan was approved/rejected using SHAP feature importance.
- **Role-Based Dashboards:** Dynamic views for Applicants, Loan Officers, and Admins.
- **Officer Action Center:** Loan officers can view pending applications and approve/reject them directly from the dashboard.
- **Admin Analytics:** Neomorphic charts showing applications per month, approval rates, risk distribution, and model accuracy.
- **Model Comparison:** A clean table comparing 5 ML models (Logistic Regression, Random Forest, XGBoost, SVM, Naive Bayes) on Accuracy, Precision, Recall, F1, and ROC-AUC.
- **Neomorphic Design Language:** Soft UI, floating panels, circular gauges, and consistent 24px border radii. No Material UI or Bootstrap.

---

## 🛠 Tech Stack

**Backend**
- FastAPI (Python web framework)
- SQLAlchemy + SQLite (Database)
- JWT (Authentication)
- Uvicorn (Server)

**Machine Learning**
- Scikit-Learn, XGBoost (Models)
- SHAP (Explainability)
- Pandas, NumPy (Data processing)

**Frontend**
- Next.js 14 (App Router)
- TailwindCSS (Styling)
- Recharts (Data Visualization)
- Lucide Icons
- Axios (API Calls)

---

## 📁 Project Structure

```
loan-risk-platform/
├── backend/     # FastAPI server, Auth, DB, Routes
├── ml/          # ML pipeline, training, saved models, SHAP
└── frontend/    # Next.js Neomorphic UI
```

---

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/loan-risk-platform.git
cd loan-risk-platform
```

### 2. Backend & ML Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Mac/Linux | venv\Scripts\activate (Windows)

pip install -r requirements.txt
```

Train the ML models (generates the `.pkl` files and metrics):

```bash
cd ../ml
python training/train.py
```

Run the backend server:

```bash
cd ../backend
uvicorn main:app --reload --port 8000
```

> Backend runs on `http://localhost:8000`

### 3. Frontend Setup

Open a new terminal:

```bash
cd loan-risk-platform/frontend
npm install
npm run dev
```

> Frontend runs on `http://localhost:3000`

---

##  Environment Variables

Create a `.env` file inside the `backend/` folder:

```env
SECRET_KEY=your_super_secret_key_change_me_12345
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
DATABASE_URL=sqlite:///./loan_platform.db
MODEL_PATH=../ml/saved_models
```

---

## 🧪 Usage Guide

1. **Sign Up** — Create an account as an applicant, officer, or admin.
2. **Apply for Loan** — As an applicant, fill out the 3-step loan application form.
3. **View Prediction** — See your risk score (0–100%), confidence level, and SHAP feature impacts.
4. **Officer Dashboard** — Log in as a Loan Officer to view global stats and approve/reject pending loans.
5. **Admin Dashboard** — Log in as Admin to view advanced analytics, charts, and model performance metrics.
6. **ML Page** — Visit `/ml` to compare the performance metrics of all 5 trained machine learning models.

---

## 🗺 Future Roadmap

- **Smart Loan Application OCR** — Auto-extract salary slips and bank statements to autofill the application form.
- **Confusion Matrix & ROC Curves** — Add visual charts to the ML Models page.
- **Cloud Deployment** — Deploy backend to Render, frontend to Vercel.

---

## Push to GitHub

Open your terminal in the root folder (`loan-risk-platform`) and run:

```bash
# 1. Initialize git in the root folder
git init

# 2. Add all files (respecting .gitignore)
git add .

# 3. Make your first commit
git commit -m "Initial commit: AI Loan Risk Platform with FastAPI, Next.js, ML & SHAP"

# 4. Set the main branch
git branch -M main

# 5. Go to GitHub and create a NEW EMPTY repository (don't add README or .gitignore on GitHub)
# Then copy your repo URL and paste it below:
git remote add origin https://github.com/YOUR_USERNAME/loan-risk-platform.git

# 6. Push it up!
git push -u origin main
```
