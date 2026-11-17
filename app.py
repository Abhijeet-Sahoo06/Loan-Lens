import joblib
from pathlib import Path

import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="LoanLens | Smart Financial Advisor",
    page_icon="💰",
    layout="wide"
)

# Custom styling
st.markdown("""
<style>
/* Fix invisible text in search and dropdown fields */
input, textarea {
    color: #FFFFFF !important;
    background-color: #1C2B40 !important;
    caret-color: #FFFFFF !important;
}

[data-baseweb="select"] > div {
    background-color: #1C2B40 !important;
    color: #FFFFFF !important;
}

[data-baseweb="select"] input {
    color: #FFFFFF !important;
}

[role="listbox"] {
    background-color: #1C2B40 !important;
}

[role="option"] {
    color: #FFFFFF !important;
    background-color: #1C2B40 !important;
}

[role="option"]:hover {
    background-color: #29435D !important;
    color: #FFFFFF !important;
}
</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.title("💰 LoanLens")
st.sidebar.caption("Smart Loan & Property Advisor")

page = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "EMI Calculator",
        "Loan Eligibility",
        "Property Advisor",
        "Smart Recommendations",
        "ML Risk Prediction",
        "About LoanLens"
    ]
)


# Dashboard
if page == "Dashboard":

    
    st.divider()

    st.subheader("📊 Loan Dataset Analytics")

    dataset_path = Path(__file__).parent / "ml_models" / "loan_dataset.csv"

    if dataset_path.exists():

        df = pd.read_csv(dataset_path)

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Applicants", len(df))

        col2.metric(
            "Low Risk Applicants",
            len(df[df["risk_category"] == "Low Risk"])
        )

        col3.metric(
            "High Risk Applicants",
            len(df[df["risk_category"] == "High Risk"])
        )

        st.subheader("Risk Category Distribution")

        risk_counts = df["risk_category"].value_counts()

        st.bar_chart(risk_counts)

    else:
        st.warning("Loan dataset not found.")


    st.title("Welcome to LoanLens 👋")
    st.write("Your personal smart financial advisor.")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Loan Tools", "03")

    with col2:
        st.metric("Financial Analysis", "Active")

    with col3:
        st.metric("Platform", "LoanLens")

    st.subheader("Explore Our Services")

    c1, c2 = st.columns(2)

    with c1:
        st.info("💳 EMI Calculator\n\nCalculate monthly loan payments.")

    with c2:
        st.info("📊 Loan Eligibility\n\nEstimate your loan affordability.")

    c3, c4 = st.columns(2)

    with c3:
        st.info("🏠 Property Advisor\n\nEstimate your affordable property budget.")

    with c4:
        st.info("🧠 Smart Recommendations\n\nUnderstand your financial position.")


# EMI Calculator
elif page == "EMI Calculator":

    st.title("💳 EMI Calculator")
    st.write("Calculate your monthly loan payments instantly.")

    st.divider()

    with st.form("emi_form"):

        st.subheader("Enter Loan Details")

        col1, col2 = st.columns(2)

        with col1:
            loan_amount = st.number_input(
                "Loan Amount (₹)",
                min_value=1000,
                max_value=100000000,
                value=1000000,
                step=10000
            )

            interest_rate = st.number_input(
                "Annual Interest Rate (%)",
                min_value=0.0,
                max_value=30.0,
                value=8.5,
                step=0.1
            )

        with col2:
            tenure = st.number_input(
                "Loan Tenure (Years)",
                min_value=1,
                max_value=30,
                value=20,
                step=1
            )

        calculate = st.form_submit_button(
            "Calculate EMI",
            use_container_width=True
        )

    if calculate:

        monthly_rate = interest_rate / (12 * 100)
        months = tenure * 12

        if monthly_rate == 0:
            emi = loan_amount / months
        else:
            emi = (
                loan_amount * monthly_rate *
                (1 + monthly_rate) ** months
            ) / ((1 + monthly_rate) ** months - 1)

        total_payment = emi * months
        total_interest = total_payment - loan_amount

        st.divider()

        st.subheader("📊 Your Loan Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Monthly EMI",
                f"₹{emi:,.2f}"
            )

        with col2:
            st.metric(
                "Total Interest",
                f"₹{total_interest:,.2f}"
            )

        with col3:
            st.metric(
                "Total Payment",
                f"₹{total_payment:,.2f}"
            )

        st.divider()

        st.subheader("Loan Repayment Breakdown")

        chart_data = pd.DataFrame({
            "Amount": [loan_amount, total_interest]
        }, index=["Principal Amount", "Interest Amount"])

        st.bar_chart(chart_data)

        # Amortization schedule
        st.subheader("📅 Monthly Repayment Schedule")

        balance = float(loan_amount)
        schedule = []

        for month in range(1, months + 1):

            interest = balance * monthly_rate
            principal = emi - interest

            if month == months:
                principal = balance

            payment = principal + interest
            balance = max(0, balance - principal)

            schedule.append({
                "Month": month,
                "EMI (₹)": round(payment, 2),
                "Principal (₹)": round(principal, 2),
                "Interest (₹)": round(interest, 2),
                "Remaining Balance (₹)": round(balance, 2)
            })

        df = pd.DataFrame(schedule)

        with st.expander("View Complete Repayment Schedule"):
            st.dataframe(df, use_container_width=True)

        st.success("EMI calculated successfully!")



# Loan Eligibility
elif page == "Loan Eligibility":

    st.title("📊 Loan Eligibility Analyzer")
    st.write("Estimate your loan eligibility based on your income and financial obligations.")

    st.divider()

    with st.form("eligibility_form"):

        st.subheader("Enter Your Financial Details")

        col1, col2 = st.columns(2)

        with col1:
            monthly_income = st.number_input(
                "Monthly Net Income (₹)",
                min_value=1000,
                value=50000,
                step=5000
            )

            existing_emi = st.number_input(
                "Existing Monthly EMIs (₹)",
                min_value=0,
                value=5000,
                step=1000
            )

            interest_rate = st.number_input(
                "Expected Interest Rate (%)",
                min_value=0.0,
                max_value=30.0,
                value=9.0,
                step=0.1
            )

        with col2:
            tenure = st.number_input(
                "Loan Tenure (Years)",
                min_value=1,
                max_value=30,
                value=20
            )

            foir = st.slider(
                "FOIR Limit (%)",
                min_value=30,
                max_value=70,
                value=50
            )

        submit = st.form_submit_button(
            "Check Loan Eligibility",
            use_container_width=True
        )

    if submit:

        if existing_emi >= monthly_income:
            st.error("Existing EMIs must be lower than monthly income.")

        else:

            # Calculate maximum EMI capacity
            max_emi = (monthly_income * foir / 100) - existing_emi

            monthly_rate = interest_rate / (12 * 100)
            months = tenure * 12

            # Calculate eligible loan amount
            if monthly_rate == 0:
                eligible_amount = max_emi * months
            else:
                eligible_amount = (
                    max_emi *
                    ((1 + monthly_rate) ** months - 1)
                    / (monthly_rate * (1 + monthly_rate) ** months)
                )

            total_obligations = existing_emi + max_emi

            st.divider()

            st.subheader("📊 Your Eligibility Results")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Estimated Loan Eligibility",
                    f"₹{eligible_amount:,.0f}"
                )

            with col2:
                st.metric(
                    "Available EMI Capacity",
                    f"₹{max_emi:,.0f}"
                )

            with col3:
                st.metric(
                    "FOIR",
                    f"{foir}%"
                )

            st.divider()

            st.subheader("Financial Analysis")

            st.write(f"Monthly Income: ₹{monthly_income:,.0f}")
            st.write(f"Existing EMI: ₹{existing_emi:,.0f}")
            st.write(f"Proposed EMI Capacity: ₹{max_emi:,.0f}")

            st.progress(foir / 100)

            st.success(
                "Eligibility estimation completed successfully!"
            )

            st.warning(
                "This is an indicative estimate based on the selected FOIR. "
                "Actual eligibility depends on lender policies, credit score, "
                "income verification and other factors."
            )



# Property Advisor
# Property Advisor
elif page == "Property Advisor":

    st.title("🏡 Property Affordability Advisor")
    st.write("Calculate your estimated home loan eligibility and property budget.")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💰 Financial Details")

        monthly_income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=60000,
            step=5000
        )

        existing_emi = st.number_input(
            "Existing Monthly EMIs (₹)",
            min_value=0,
            value=5000,
            step=1000
        )

        down_payment = st.number_input(
            "Available Down Payment (₹)",
            min_value=0,
            value=1000000,
            step=50000
        )

    with col2:
        st.subheader("🏦 Loan Preferences")

        interest_rate = st.number_input(
            "Home Loan Interest Rate (%)",
            min_value=0.0,
            value=8.5,
            step=0.1
        )

        tenure = st.slider(
            "Loan Tenure (Years)",
            min_value=5,
            max_value=30,
            value=20
        )

        foir = st.slider(
            "FOIR (%)",
            min_value=30,
            max_value=70,
            value=50
        )

    st.markdown("---")

    if st.button("🔍 Calculate Property Budget", use_container_width=True):

        max_emi = (monthly_income * foir / 100) - existing_emi

        if max_emi <= 0:
            st.error("Your available income is insufficient for an additional EMI.")

        else:
            monthly_rate = interest_rate / 1200
            months = tenure * 12

            if monthly_rate == 0:
                eligible_loan = max_emi * months
            else:
                eligible_loan = (
                    max_emi *
                    (1 - (1 + monthly_rate) ** (-months))
                    / monthly_rate
                )

            property_budget = eligible_loan + down_payment

            st.subheader("📊 Your Property Affordability Results")

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Estimated Loan Amount",
                f"₹{eligible_loan:,.0f}"
            )

            c2.metric(
                "Available Down Payment",
                f"₹{down_payment:,.0f}"
            )

            c3.metric(
                "Estimated Property Budget",
                f"₹{property_budget:,.0f}"
            )

            st.markdown("---")

            st.subheader("📈 Financial Breakdown")

            col3, col4 = st.columns(2)

            with col3:
                st.metric("Maximum Affordable EMI", f"₹{max_emi:,.0f}")
                st.metric("Loan Tenure", f"{tenure} Years")

            with col4:
                st.metric("Interest Rate", f"{interest_rate}%")
                st.metric("FOIR", f"{foir}%")

            st.success(
                f"Based on your inputs, your estimated property budget is "
                f"₹{property_budget:,.0f}."
            )

            st.info(
                "Note: This is an approximate affordability calculation, "
                "not a loan approval. Actual eligibility depends on lender "
                "policies, credit score, property valuation, LTV limits, "
                "registration charges, stamp duty and other expenses."
            )


# Smart Financial Recommendations
elif page == "Smart Recommendations":

    st.title("🧠 Smart Financial Recommendations")

    st.write(
        "Analyze your financial position and receive "
        "personalized financial suggestions."
    )

    st.divider()

    with st.form("financial_analysis_form"):

        st.subheader("Your Financial Information")

        col1, col2 = st.columns(2)

        with col1:
            income = st.number_input(
                "Monthly Net Income (₹)",
                min_value=1000,
                value=60000,
                step=5000
            )

            expenses = st.number_input(
                "Monthly Living Expenses (₹)",
                min_value=0,
                value=20000,
                step=1000
            )

        with col2:
            existing_emi = st.number_input(
                "Existing Monthly EMIs (₹)",
                min_value=0,
                value=10000,
                step=1000
            )

            savings = st.number_input(
                "Total Available Savings (₹)",
                min_value=0,
                value=200000,
                step=10000
            )

        analyze = st.form_submit_button(
            "Analyze My Financial Health",
            use_container_width=True
        )

    if analyze:

        st.divider()

        st.subheader("📊 Financial Health Analysis")

        total_obligations = expenses + existing_emi
        monthly_surplus = income - total_obligations

        debt_ratio = (existing_emi / income) * 100
        expense_ratio = (expenses / income) * 100

        recommended_emi = max(
            0,
            (income * 0.40) - existing_emi
        )

        if expenses > 0:
            emergency_months = savings / expenses
        else:
            emergency_months = 0

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Monthly Surplus",
                f"₹{monthly_surplus:,.0f}"
            )

        with col2:
            st.metric(
                "Debt-to-Income Ratio",
                f"{debt_ratio:.1f}%"
            )

        with col3:
            st.metric(
                "Recommended Additional EMI",
                f"₹{recommended_emi:,.0f}"
            )

        st.divider()

        st.subheader("Financial Health Score")

        score = 100

        if debt_ratio > 40:
            score -= 30
        elif debt_ratio > 30:
            score -= 15

        if monthly_surplus < 0:
            score -= 40
        elif monthly_surplus < income * 0.10:
            score -= 20

        if emergency_months < 3:
            score -= 20

        score = max(0, score)

        st.metric("Financial Health Score", f"{score}/100")

        st.progress(score / 100)

        if score >= 80:
            st.success("Good financial position!")
        elif score >= 50:
            st.warning("Moderate financial position. Some improvements are needed.")
        else:
            st.error("Your finances need attention.")

        st.divider()

        st.subheader("💡 Smart Recommendations")

        if debt_ratio > 40:
            st.warning(
                "Your existing EMI burden is high. "
                "Consider reducing outstanding debt."
            )
        elif debt_ratio > 30:
            st.info(
                "Your EMI obligations are moderately high. "
                "Avoid taking unnecessary loans."
            )
        else:
            st.success(
                "Your existing EMI burden is within the suggested range."
            )

        if monthly_surplus <= 0:
            st.warning(
                "Your monthly expenses and EMIs equal or exceed your income. "
                "Review your spending."
            )
        elif monthly_surplus < income * 0.10:
            st.info(
                "Your monthly savings potential is low. "
                "Try reducing non-essential expenses."
            )
        else:
            st.success(
                "You have a positive monthly surplus. "
                "Maintain a consistent savings habit."
            )

        if emergency_months < 3:
            st.warning(
                "Build an emergency fund covering at least "
                "3 to 6 months of essential expenses."
            )
        else:
            st.success(
                "Your savings cover at least 3 months of living expenses."
            )

        st.info(
            "Recommended additional EMI is an illustrative estimate "
            "using a 40% income-based obligation limit. "
            "The health score is a rule-based indicator, not a "
            "credit score or lender approval."
        )


# ML Risk Prediction

elif page == "ML Risk Prediction":

    st.title("🤖 ML-Based Loan Risk Prediction")

    st.write("Enter applicant details to predict loan risk.")

    col1, col2 = st.columns(2)

    with col1:
        income = st.number_input(
            "Monthly Income (₹)",
            min_value=0,
            value=50000
        )

        loan_amount = st.number_input(
            "Loan Amount (₹)",
            min_value=0,
            value=1000000
        )

        credit_score = st.number_input(
            "Credit Score",
            min_value=0,
            max_value=1000,
            value=750
        )

    with col2:
        loan_tenure = st.number_input(
            "Loan Tenure (Years)",
            min_value=0,
            max_value=30,
            value=15
        )

        existing_loans = st.number_input(
            "Existing Loans",
            min_value=0,
            value=1
        )

        employment_years = st.number_input(
            "Employment Years",
            min_value=0,
            value=5
        )

    if st.button("Predict Loan Risk"):

        if (
            income <= 0
            or loan_amount <= 0
            or credit_score < 300
            or credit_score > 850
            or loan_tenure <= 0
        ):
            st.error("Please enter valid applicant details.")

        else:

            model_path = Path(__file__).parent / "ml_models" / "loan_risk_model.pkl"

            model = joblib.load(model_path)

            applicant = pd.DataFrame([{
                "income": income,
                "loan_amount": loan_amount,
                "credit_score": credit_score,
                "loan_tenure": loan_tenure,
                "existing_loans": existing_loans,
                "employment_years": employment_years,
                "loan_income_ratio": loan_amount / (income * 12)
            }])

            prediction = model.predict(applicant)
            probabilities = model.predict_proba(applicant)

            st.divider()

            st.subheader("Prediction Result")

            risk = prediction[0]

            if risk == "Low Risk":
                st.success(f"Predicted Category: {risk}")

            elif risk == "Medium Risk":
                st.warning(f"Predicted Category: {risk}")

            else:
                st.error(f"Predicted Category: {risk}")

            st.subheader("Prediction Probabilities")

            for category, probability in zip(model.classes_, probabilities[0]):
                st.write(f"{category}: {probability * 100:.2f}%")

            st.divider()

            st.subheader("📊 Model Feature Importance")


            report = pd.DataFrame([{
                "Monthly Income": income,
                "Loan Amount": loan_amount,
                "Credit Score": credit_score,
                "Loan Tenure": loan_tenure,
                "Existing Loans": existing_loans,
                "Employment Years": employment_years,
                "Predicted Risk": risk,
                "Loan Income Ratio": loan_amount / (income * 12)
            }])

            st.download_button(
                label="📥 Download Loan Risk Report",
                data=report.to_csv(index=False),
                file_name="LoanLens_Risk_Report.csv",
                mime="text/csv"
            )


            chart_path = Path(__file__).parent / "ml_models" / "feature_importance.png"

            if chart_path.exists():
                st.image(
                    str(chart_path),
                    caption="Factors influencing model predictions",
                    use_container_width=True
                )
            else:
                st.warning("Feature importance chart not found.")

            st.caption(
                "This is an educational prediction using a synthetic dataset. "
                "It does not represent actual loan approval or default probability."
            )

# About LoanLens
elif page == "About LoanLens":

    st.title("🚀 About LoanLens")

    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #101c35, #172c4d);
        padding: 30px;
        border-radius: 18px;
        border: 1px solid #25cce8;
        margin-bottom: 25px;
    ">
        <h1 style="color: #39dce9; font-size: 38px;">
            LoanLens
        </h1>
        <h3 style="color: white;">
            Smart Loan & Property Advisor
        </h3>
        <p style="color: #b8c9df; font-size: 16px;">
            Making smarter financial decisions through data,
            machine learning and intelligent financial insights.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("💡 What is LoanLens?")

    st.write("""
    LoanLens is a FinTech-based web application developed using
    Python, Streamlit and Machine Learning.

    It helps users understand their loan affordability, estimate
    property budgets, calculate EMIs and explore financial insights
    through an interactive dashboard.
    """)

    st.markdown("---")

    st.subheader("⚡ Key Features")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        ### 🏦 Loan Analysis
        - EMI Calculator
        - Loan Eligibility Estimator
        - Loan Risk Prediction
        - Financial Insights
        """)

    with col2:
        st.markdown("""
        ### 🏡 Property Intelligence
        - Property Affordability
        - Estimated Loan Amount
        - Property Budget Calculation
        - Down Payment Analysis
        """)

    st.markdown("---")

    st.subheader("🧠 Technology Stack")

    technologies = [
        ("Python", "Core programming language"),
        ("Streamlit", "Interactive web application"),
        ("Pandas & NumPy", "Data processing and analysis"),
        ("Scikit-learn", "Machine Learning model"),
        ("Matplotlib", "Data visualization"),
        ("Joblib", "Model serialization")
    ]

    for tech, description in technologies:
        st.markdown(f"**{tech}** — {description}")

    st.markdown("---")

    st.subheader("🤖 Machine Learning")

    st.write("""
    LoanLens uses a Random Forest Classification model to categorize
    loan applicants into three risk categories:

    - 🟢 Low Risk
    - 🟡 Medium Risk
    - 🔴 High Risk

    The current model is trained on a synthetic dataset generated
    for educational and demonstration purposes. Its predictions
    should not be treated as actual loan approval decisions or
    real-world default probabilities.
    """)

    st.markdown("---")

    st.subheader("🎯 Project Objective")

    st.write("""
    The objective of LoanLens is to combine financial calculations,
    property affordability analysis and machine learning into one
    user-friendly digital platform.

    It demonstrates how technology and data science can support
    smarter financial planning.
    """)

    st.markdown("---")

    st.markdown("""
    <div style="text-align:center; padding:20px;">
        <h3 style="color:#39dce9;">LOANLENS</h3>
        <p style="color:#9aacc5;">
            Smart Decisions. Better Financial Futures.
        </p>
        <p style="color:#71839c; font-size:12px;">
            Developed as a FinTech & Machine Learning Project
        </p>
    </div>
    """, unsafe_allow_html=True)