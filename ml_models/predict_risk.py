
import joblib
import pandas as pd

# Load trained model
model = joblib.load("ml_models/loan_risk_model.pkl")

# New applicant details
applicant = pd.DataFrame([{
    "income": 60000,
    "loan_amount": 1000000,
    "credit_score": 750,
    "loan_tenure": 15,
    "existing_loans": 1,
    "employment_years": 5,
    "loan_income_ratio": 1000000 / (60000 * 12)
}])

# Predict risk
prediction = model.predict(applicant)

# Prediction probabilities
probabilities = model.predict_proba(applicant)

print("Loan Risk Prediction:", prediction[0])

print("\nPrediction Probabilities:")

for category, probability in zip(
    model.classes_,
    probabilities[0]
):
    print(category, ":", round(probability * 100, 2), "%")
