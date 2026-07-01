import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import joblib
import os

def generate_synthetic_data(n=2000, save_path="ml/dataset/loan_data.csv"):
    np.random.seed(42)
    age = np.random.randint(21, 65, n)
    income = np.random.normal(60000, 25000, n).clip(15000, 200000)
    credit_score = np.random.randint(300, 850, n)
    loan_amount = np.random.normal(20000, 12000, n).clip(2000, 80000)
    loan_term = np.random.choice([12, 24, 36, 48, 60], n)
    employment_years = np.random.exponential(5, n).clip(0, 30)
    debt_to_income = np.random.normal(0.3, 0.15, n).clip(0.05, 0.8)

    # Create a strict mathematical risk score (0 to 100)
    # Lower credit score = higher risk
    risk_score = (850 - credit_score) / 5.5  # Max ~100
    # Higher DTI = higher risk
    risk_score += (debt_to_income * 100)     # Max ~80
    # Higher loan amount = higher risk
    risk_score += (loan_amount / 1000)       # Max ~80
    # Lower income = higher risk
    risk_score += ((200000 - income) / 4000) # Max ~46
    # Lower employment = higher risk
    risk_score += ((5 - employment_years).clip(0) * 4) # Max ~20

    # Add a little bit of noise (real life isn't perfect)
    risk_score += np.random.normal(0, 10, n)

    # If risk score is above a threshold, they default
    default = (risk_score > 110).astype(int)

    df = pd.DataFrame({
        "age": age, "income": income, "credit_score": credit_score,
        "loan_amount": loan_amount, "loan_term": loan_term,
        "employment_years": employment_years, "debt_to_income": debt_to_income,
        "default": default
    })
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    df.to_csv(save_path, index=False)
    print(f"✅ Dataset saved: {save_path} shape={df.shape}")
    print(f"Default distribution:\n{df['default'].value_counts()}")
    return df

def preprocess(df):
    X = df[["age", "income", "credit_score", "loan_amount",
            "loan_term", "employment_years", "debt_to_income"]]
    y = df["default"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, y, scaler, X.columns.tolist()

if __name__ == "__main__":
    df = generate_synthetic_data()
    print(df.head())
    print(df["default"].value_counts())