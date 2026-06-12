"""
Data loading utilities with Streamlit caching for optimal performance.
Handles loading of risk scores, training data, and the ML model pipeline.
"""
import streamlit as st
import pandas as pd
import joblib
import numpy as np
from config import FEATURE_COLUMNS, AVG_CUSTOMER_LIFETIME_YEARS


@st.cache_data(ttl=3600)
def load_risk_data():
    """Load the customer risk scores dataset (10,000 scored customers)."""
    df = pd.read_csv("customer_risk_scores.csv")
    return df


@st.cache_data(ttl=3600)
def load_training_data():
    """Load the full synthetic training dataset (50,000 customers)."""
    df = pd.read_csv("insurance_policyholder_churn_synthetic.csv")
    return df


@st.cache_resource
def load_model():
    """Load the trained XGBoost pipeline (ColumnTransformer + XGBClassifier)."""
    return joblib.load("models/churn_model.pkl")


def get_feature_data(df):
    """
    Extract the feature columns from a DataFrame in the correct order
    for the model pipeline.
    """
    return df[FEATURE_COLUMNS].copy()


def compute_portfolio_metrics(df):
    """
    Compute key portfolio-level metrics for the executive dashboard.
    Returns a dict of all KPI values.
    """
    total = len(df)
    high_risk = len(df[df["Risk_Category"] == "High"])
    medium_risk = len(df[df["Risk_Category"] == "Medium"])
    low_risk = total - high_risk - medium_risk

    # Portfolio Health Score: weighted average (Low=100, Medium=50, High=0)
    health_score = round(
        (low_risk * 100 + medium_risk * 50 + high_risk * 0) / total, 1
    )

    # Churn rate approximation from probabilities
    avg_churn_prob = df["Churn_Probability"].mean()
    churn_rate = round(avg_churn_prob * 100, 1)

    # Revenue calculations
    total_premium = df["current_premium"].sum()
    high_risk_df = df[df["Risk_Category"] == "High"]
    revenue_at_risk = high_risk_df["current_premium"].sum()

    # Predicted annual revenue loss = sum(premium * churn_probability) for all customers
    predicted_loss = (df["current_premium"] * df["Churn_Probability"]).sum()

    # Average risk score
    avg_risk = round(df["Risk_Score"].mean(), 1)

    return {
        "total_customers": total,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "health_score": health_score,
        "churn_rate": churn_rate,
        "avg_risk": avg_risk,
        "total_premium": total_premium,
        "revenue_at_risk": revenue_at_risk,
        "predicted_loss": predicted_loss,
        "model_confidence": 78.5,  # ROC-AUC as percentage
    }


def compute_clv(customer_row):
    """
    Estimate Customer Lifetime Value (CLV) for a single customer.
    CLV = annual_premium × expected_remaining_years × retention_probability
    """
    premium = customer_row["current_premium"]
    tenure_years = customer_row["customer_tenure_months"] / 12
    remaining_years = max(AVG_CUSTOMER_LIFETIME_YEARS - tenure_years, 1)
    retention_prob = 1 - customer_row["Churn_Probability"]

    clv = premium * remaining_years * retention_prob
    return round(clv, 2)
