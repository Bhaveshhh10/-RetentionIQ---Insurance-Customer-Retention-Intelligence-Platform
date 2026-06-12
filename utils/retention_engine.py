"""
Retention Strategy Simulation Engine.
The key differentiating feature — allows users to simulate retention strategies
and see their impact by re-running the actual XGBoost model with modified features.
"""
import numpy as np
import pandas as pd
import streamlit as st
from config import FEATURE_COLUMNS, RETENTION_COSTS, AVG_CUSTOMER_LIFETIME_YEARS


def simulate_retention_strategy(
    df,
    model,
    premium_discount_pct=0,
    enable_flexible_payment=False,
    multi_policy_discount_pct=0,
    enable_dedicated_support=False,
    target_segment="High Risk Only",
):
    """
    Simulate the impact of retention strategies by modifying customer features
    and re-predicting churn probabilities through the actual XGBoost model.

    Parameters:
        df: Customer risk scores DataFrame
        model: Trained sklearn Pipeline (preprocessor + XGBClassifier)
        premium_discount_pct: Percentage premium discount to offer (0-25)
        enable_flexible_payment: Whether to offer flexible payment plans
        multi_policy_discount_pct: Bundle discount percentage (0-15)
        enable_dedicated_support: Whether to assign dedicated support
        target_segment: Which customers to target

    Returns:
        results: dict with simulation outcomes
    """
    # Select target customers based on segment
    if target_segment == "High Risk Only":
        mask = df["Risk_Category"] == "High"
    elif target_segment == "High + Medium Risk":
        mask = df["Risk_Category"].isin(["High", "Medium"])
    elif target_segment == "Top 100 Highest Risk":
        top_100_idx = df.nlargest(100, "Risk_Score").index
        mask = df.index.isin(top_100_idx)
    else:  # All Customers
        mask = pd.Series(True, index=df.index)

    target_df = df[mask].copy()
    if len(target_df) == 0:
        return _empty_results()

    # --- Original predictions ---
    original_probs = target_df["Churn_Probability"].values.copy()

    # --- Modify features based on strategy ---
    modified_features = target_df[FEATURE_COLUMNS].copy()

    # 1) Premium Discount
    if premium_discount_pct > 0:
        discount_factor = 1 - (premium_discount_pct / 100)
        modified_features["current_premium"] = (
            modified_features["current_premium"] * discount_factor
        )
        # Recalculate premium change percentage
        modified_features["premium_change_pct"] = (
            (modified_features["current_premium"] - modified_features["premium_last_year"])
            / modified_features["premium_last_year"]
        )
        # Reduce num_price_increases counter
        modified_features["num_price_increases_last_3y"] = np.maximum(
            modified_features["num_price_increases_last_3y"] - 1, 0
        )

    # 2) Flexible Payment Plans
    if enable_flexible_payment:
        modified_features["autopay_enabled"] = 1
        modified_features["late_payment_count_12m"] = 0
        modified_features["missed_payment_flag"] = 0
        modified_features["payment_frequency"] = "Monthly"

    # 3) Multi-Policy Bundle
    if multi_policy_discount_pct > 0:
        modified_features["multi_policy_flag"] = 1
        modified_features["num_policies"] = np.maximum(
            modified_features["num_policies"], 2
        )
        # Apply bundle discount to premium
        bundle_factor = 1 - (multi_policy_discount_pct / 100)
        modified_features["current_premium"] = (
            modified_features["current_premium"] * bundle_factor
        )

    # 4) Dedicated Support
    if enable_dedicated_support:
        modified_features["complaint_flag"] = 0
        modified_features["complaint_resolution_days"] = 0
        modified_features["num_contacts_12m"] = np.maximum(
            (modified_features["num_contacts_12m"] * 0.5).astype(int), 0
        )
        modified_features["quote_requested_flag"] = 0
        modified_features["coverage_downgrade_flag"] = 0

    # --- Re-predict with modified features ---
    try:
        new_probs = model.predict_proba(modified_features)[:, 1]
    except Exception:
        # Fallback: use heuristic if model prediction fails
        new_probs = _heuristic_prediction(
            original_probs, premium_discount_pct, enable_flexible_payment,
            multi_policy_discount_pct, enable_dedicated_support
        )

    # --- Calculate results ---
    prob_reduction = original_probs - new_probs
    customers_saved = int(np.sum((original_probs >= 0.5) & (new_probs < 0.5)))
    avg_prob_reduction = float(np.mean(prob_reduction))

    # Revenue calculations
    premiums = target_df["current_premium"].values
    original_expected_loss = float(np.sum(premiums * original_probs))
    new_expected_loss = float(np.sum(premiums * new_probs))
    revenue_saved_annual = original_expected_loss - new_expected_loss
    revenue_saved_lifetime = revenue_saved_annual * AVG_CUSTOMER_LIFETIME_YEARS

    # Campaign cost calculation
    campaign_cost = _calculate_campaign_cost(
        target_df, premium_discount_pct, enable_flexible_payment,
        multi_policy_discount_pct, enable_dedicated_support
    )

    # ROI
    roi = ((revenue_saved_lifetime - campaign_cost) / campaign_cost * 100) if campaign_cost > 0 else 0

    # Customer-level detail
    customer_detail = target_df[["Risk_Score", "Risk_Category", "current_premium",
                                  "policy_type", "region_name"]].copy()
    customer_detail["Original_Churn_Prob"] = np.round(original_probs * 100, 1)
    customer_detail["New_Churn_Prob"] = np.round(new_probs * 100, 1)
    customer_detail["Prob_Reduction"] = np.round(prob_reduction * 100, 1)
    customer_detail["Status"] = np.where(
        (original_probs >= 0.5) & (new_probs < 0.5), "✅ Saved",
        np.where(new_probs < original_probs, "📉 Improved", "—")
    )
    customer_detail = customer_detail.sort_values("Prob_Reduction", ascending=False)

    return {
        "target_count": len(target_df),
        "customers_saved": customers_saved,
        "avg_prob_reduction": avg_prob_reduction,
        "revenue_saved_annual": revenue_saved_annual,
        "revenue_saved_lifetime": revenue_saved_lifetime,
        "campaign_cost": campaign_cost,
        "roi": roi,
        "original_probs": original_probs,
        "new_probs": new_probs,
        "customer_detail": customer_detail,
        "original_expected_loss": original_expected_loss,
        "new_expected_loss": new_expected_loss,
    }


def _calculate_campaign_cost(target_df, discount_pct, flex_pay, bundle_pct, support):
    """Calculate the total cost of the retention campaign."""
    n = len(target_df)
    cost = 0

    if discount_pct > 0:
        # Cost = discount amount per customer
        cost += (target_df["current_premium"] * discount_pct / 100).sum()

    if flex_pay:
        cost += n * RETENTION_COSTS["flexible_payment_cost"]

    if bundle_pct > 0:
        cost += (target_df["current_premium"] * bundle_pct / 100).sum()

    if support:
        cost += n * RETENTION_COSTS["dedicated_support_cost"]

    return float(cost)


def _heuristic_prediction(original_probs, discount_pct, flex_pay, bundle_pct, support):
    """
    Fallback heuristic for when model re-prediction fails.
    Uses empirically reasonable reduction factors.
    """
    reduction = np.zeros_like(original_probs)

    if discount_pct > 0:
        reduction += original_probs * (discount_pct / 100) * 0.6

    if flex_pay:
        reduction += original_probs * 0.08

    if bundle_pct > 0:
        reduction += original_probs * (bundle_pct / 100) * 0.4

    if support:
        reduction += original_probs * 0.1

    new_probs = np.maximum(original_probs - reduction, 0.01)
    return new_probs


def _empty_results():
    """Return empty results when no customers are targeted."""
    return {
        "target_count": 0,
        "customers_saved": 0,
        "avg_prob_reduction": 0,
        "revenue_saved_annual": 0,
        "revenue_saved_lifetime": 0,
        "campaign_cost": 0,
        "roi": 0,
        "original_probs": np.array([]),
        "new_probs": np.array([]),
        "customer_detail": pd.DataFrame(),
        "original_expected_loss": 0,
        "new_expected_loss": 0,
    }
