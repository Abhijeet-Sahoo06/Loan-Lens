
# 🏦 LoanLens – Smart Loan & Property Advisor

LoanLens is a project I built to explore how technology and machine learning can be used in the financial domain.

The idea behind this project is simple: getting a loan or planning to buy a property involves a lot of calculations. I wanted to bring some of those things together in one application so users can get a better idea of their financial position before making a decision.

With LoanLens, users can calculate EMIs, check estimated loan eligibility, plan a property budget, and explore loan risk predictions using a machine learning model.

## 🚀 What can you do with LoanLens?

- **EMI Calculator:** Calculate monthly EMIs, total interest, and total repayment.
- **Loan Eligibility:** Get an estimate of how much loan you may be eligible for based on your income and existing EMIs.
- **Property Advisor:** Get an estimated property budget based on your income, savings, and loan affordability.
- **Smart Recommendations:** Understand your monthly savings and existing financial commitments.
- **Loan Risk Prediction:** Predict whether an applicant falls into the Low, Medium, or High Risk category.
- **Model Evaluation:** Check model performance through accuracy, balanced accuracy, and a confusion matrix.
- **Feature Importance:** See which factors have more influence on the model's predictions.
- **Download Report:** Download the loan risk prediction details in CSV format.

## 🤖 Machine Learning

For the machine learning part, I used a Random Forest Classifier.

I created a synthetic dataset containing 1,000 applicant records with different income levels, loan amounts, credit scores, employment years, and other details.

The model uses these features to classify applicants into three categories:

- Low Risk
- Medium Risk
- High Risk

I also worked on model evaluation and feature importance to understand how the model performs and which input features matter most.

## 🛠️ Tools and Technologies

- Python
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Joblib

## 📁 Project Structure

```text
LoanLens Project/
│
├── app.py
├── requirements.txt
├── README.md
│
└── ml_models/
    ├── generate_dataset.py
    ├── train_model.py
    ├── predict_risk.py
    ├── evaluate_model.py
    ├── loan_dataset.csv
    ├── loan_risk_model.pkl
    └── feature_importance.png
```

## 💻 How to Run the Project

First, clone the repository:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
```

Move into the project folder:

```bash
cd LoanLens
```

Install the required libraries:

```bash
pip install -r requirements.txt
```

Finally, start the application:

```bash
streamlit run app.py
```

## 📊 Train the ML Model

If you want to generate the dataset and train the model again, run these commands:

```bash
python ml_models/generate_dataset.py
python ml_models/train_model.py
python ml_models/evaluate_model.py
```

## ⚠️ A Note About the Predictions

The dataset used in this project is synthetically generated, and the risk categories are assigned using predefined rules.

The model is mainly built to demonstrate a machine learning workflow. Its predictions should not be treated as actual loan approval decisions or real-world credit risk assessments.

## 👨‍💻 About Me

**Abhijeet Sahoo**  
Computer Science and Engineering Student

I built LoanLens as a project to apply my knowledge of Python, data analysis, machine learning, and web application development to a practical FinTech use case.
