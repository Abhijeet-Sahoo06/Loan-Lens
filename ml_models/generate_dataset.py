
import pandas as pd
import numpy as np

# Generate synthetic loan applicant data
np.random.seed(42)

n = 1000

data = {
    "income": np.random.randint(15000, 150000, n),
    "loan_amount": np.random.randint(50000, 2000000, n),
    "credit_score": np.random.randint(300, 851, n),
    "loan_tenure": np.random.randint(1, 31, n),
    "existing_loans": np.random.randint(0, 6, n),
    "employment_years": np.random.randint(0, 31, n)
}

df = pd.DataFrame(data)

# Calculate loan-to-income ratio
df["loan_income_ratio"] = (
    df["loan_amount"] / (df["income"] * 12)
)

# Assign synthetic risk categories
def calculate_risk(row):

    score = 0

    if row["credit_score"] < 550:
        score += 3
    elif row["credit_score"] < 650:
        score += 2
    elif row["credit_score"] < 700:
        score += 1

    if row["loan_income_ratio"] > 5:
        score += 3
    elif row["loan_income_ratio"] > 3:
        score += 2
    elif row["loan_income_ratio"] > 2:
        score += 1

    if row["existing_loans"] >= 4:
        score += 2
    elif row["existing_loans"] >= 2:
        score += 1

    if row["employment_years"] < 1:
        score += 2
    elif row["employment_years"] < 3:
        score += 1

    if score >= 6:
        return "High Risk"
    elif score >= 3:
        return "Medium Risk"
    else:
        return "Low Risk"


df["risk_category"] = df.apply(calculate_risk, axis=1)

# Save dataset
df.to_csv("ml_models/loan_dataset.csv", index=False)

print("Loan dataset created successfully!")
print("\nDataset Preview:")
print(df.head())

print("\nRisk Category Distribution:")
print(df["risk_category"].value_counts())

print("\nDataset Shape:", df.shape)
