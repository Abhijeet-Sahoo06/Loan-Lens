
import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix
)

# Load dataset
df = pd.read_csv("ml_models/loan_dataset.csv")

# Separate features and target
X = df.drop("risk_category", axis=1)
y = df["risk_category"]

# Split dataset (same split used during training)
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Load trained model
model = joblib.load("ml_models/loan_risk_model.pkl")

# Predictions
predictions = model.predict(X_test)

# Evaluation
print("\n========== MODEL EVALUATION ==========")

print(
    "\nAccuracy:",
    round(accuracy_score(y_test, predictions) * 100, 2),
    "%"
)

print(
    "Balanced Accuracy:",
    round(balanced_accuracy_score(y_test, predictions) * 100, 2),
    "%"
)

print("\nClassification Report:")
print(classification_report(y_test, predictions))

print("\nConfusion Matrix:")
print(
    confusion_matrix(
        y_test,
        predictions,
        labels=model.classes_
    )
)

# Feature importance
importance = pd.DataFrame({
    "Feature": X.columns,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n========== FEATURE IMPORTANCE ==========")
print(importance.to_string(index=False))

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.barh(
    importance["Feature"],
    importance["Importance"]
)

plt.xlabel("Importance Score")
plt.ylabel("Loan Features")
plt.title("Loan Risk Prediction - Feature Importance")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("ml_models/feature_importance.png")
plt.show()

print("\nFeature importance chart saved successfully!")

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.barh(
    importance["Feature"],
    importance["Importance"]
)

plt.xlabel("Importance Score")
plt.ylabel("Loan Features")
plt.title("Loan Risk Prediction - Feature Importance")

plt.gca().invert_yaxis()
plt.tight_layout()

plt.savefig("ml_models/feature_importance.png")
plt.show()

print("\nFeature importance chart saved successfully!")