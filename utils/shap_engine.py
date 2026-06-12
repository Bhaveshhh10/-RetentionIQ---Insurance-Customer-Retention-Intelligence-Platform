"""
SHAP Explainability Engine.
Computes and caches SHAP values for individual and global explanations.
Handles the XGBoost pipeline structure (ColumnTransformer → XGBClassifier).
"""
import streamlit as st
import numpy as np
import pandas as pd
import shap
from config import CATEGORICAL_COLUMNS, FEATURE_DISPLAY_NAMES, FEATURE_COLUMNS


@st.cache_resource
def _get_explainer(_model):
    """Create a cached SHAP TreeExplainer for the XGBoost model."""
    xgb_model = _model.named_steps["model"]
    return shap.TreeExplainer(xgb_model)


def _get_clean_feature_names(model):
    """
    Get human-readable feature names from the pipeline's preprocessor.
    Maps encoded feature names (cat__region_name_Auckland, remainder__age)
    to clean display names.
    """
    preprocessor = model.named_steps["preprocessor"]
    raw_names = preprocessor.get_feature_names_out().tolist()

    clean = []
    for name in raw_names:
        if name.startswith("cat__"):
            # e.g., "cat__region_name_Auckland" → "Region: Auckland"
            parts = name.replace("cat__", "").split("_", 1)
            col = parts[0]
            # Handle multi-word column names
            for cat_col in CATEGORICAL_COLUMNS:
                if name.replace("cat__", "").startswith(cat_col + "_"):
                    col = cat_col
                    val = name.replace("cat__", "").replace(cat_col + "_", "")
                    break
            else:
                val = parts[1] if len(parts) > 1 else ""
            display_col = FEATURE_DISPLAY_NAMES.get(col, col.replace("_", " ").title())
            clean.append(f"{display_col}: {val}")
        elif name.startswith("remainder__"):
            col = name.replace("remainder__", "")
            clean.append(FEATURE_DISPLAY_NAMES.get(col, col.replace("_", " ").title()))
        else:
            clean.append(name)

    return clean


def _aggregate_shap_to_original(shap_values_row, raw_feature_names):
    """
    Aggregate one-hot encoded SHAP values back to original categorical features.
    For each categorical column, sums SHAP values of all its one-hot encoded features.
    Returns a dict of {display_name: shap_value}.
    """
    aggregated = {}

    # Group categorical features
    for cat_col in CATEGORICAL_COLUMNS:
        prefix = f"cat__{cat_col}_"
        cat_indices = [
            i for i, name in enumerate(raw_feature_names) if name.startswith(prefix)
        ]
        if cat_indices:
            display_name = FEATURE_DISPLAY_NAMES.get(
                cat_col, cat_col.replace("_", " ").title()
            )
            aggregated[display_name] = sum(shap_values_row[i] for i in cat_indices)

    # Add remainder (numerical) features
    for i, name in enumerate(raw_feature_names):
        if name.startswith("remainder__"):
            col = name.replace("remainder__", "")
            display_name = FEATURE_DISPLAY_NAMES.get(
                col, col.replace("_", " ").title()
            )
            aggregated[display_name] = shap_values_row[i]

    return aggregated


@st.cache_data(ttl=600)
def get_customer_shap(customer_idx, _model, _df):
    """
    Compute SHAP values for a single customer.
    Returns:
        - aggregated: dict of {display_name: shap_value} (original features)
        - base_value: the expected value (base prediction)
    """
    explainer = _get_explainer(_model)
    preprocessor = _model.named_steps["preprocessor"]
    raw_feature_names = preprocessor.get_feature_names_out().tolist()

    # Get feature data for this customer
    X = _df[FEATURE_COLUMNS].iloc[[customer_idx]]
    X_transformed = preprocessor.transform(X)

    # Compute SHAP values
    shap_vals = explainer.shap_values(X_transformed)
    base_value = explainer.expected_value

    # Handle binary classification — shap_values might be a list of 2 arrays
    if isinstance(shap_vals, list):
        shap_vals = shap_vals[1]  # Use class 1 (churn) SHAP values
    if isinstance(base_value, (list, np.ndarray)):
        base_value = base_value[1] if len(base_value) > 1 else base_value[0]

    shap_row = shap_vals[0]

    # Aggregate to original features
    aggregated = _aggregate_shap_to_original(shap_row, raw_feature_names)

    return aggregated, float(base_value)


@st.cache_data(ttl=1800)
def get_global_shap_importance(_model, _df, n_samples=500):
    """
    Compute global SHAP feature importance by averaging |SHAP values|
    across a sample of customers. Returns a DataFrame sorted by importance.
    """
    explainer = _get_explainer(_model)
    preprocessor = _model.named_steps["preprocessor"]
    raw_feature_names = preprocessor.get_feature_names_out().tolist()

    # Sample customers for efficiency
    sample_size = min(n_samples, len(_df))
    sample_df = _df.sample(n=sample_size, random_state=42)
    X = sample_df[FEATURE_COLUMNS]
    X_transformed = preprocessor.transform(X)

    # Compute SHAP values
    shap_vals = explainer.shap_values(X_transformed)
    if isinstance(shap_vals, list):
        shap_vals = shap_vals[1]

    # Aggregate each sample to original features, then average
    all_aggregated = []
    for row_idx in range(len(shap_vals)):
        agg = _aggregate_shap_to_original(shap_vals[row_idx], raw_feature_names)
        all_aggregated.append(agg)

    agg_df = pd.DataFrame(all_aggregated)
    importance = agg_df.abs().mean().sort_values(ascending=False)

    result = pd.DataFrame({
        "Feature": importance.index,
        "Importance": importance.values,
        "Avg_SHAP": agg_df.mean().reindex(importance.index).values,
    })

    return result


@st.cache_data(ttl=1800)
def get_shap_dependence_data(_model, _df, feature_col, n_samples=500):
    """
    Compute SHAP dependence data for a specific feature.
    Returns a DataFrame with columns: feature_value, shap_value.
    """
    explainer = _get_explainer(_model)
    preprocessor = _model.named_steps["preprocessor"]
    raw_feature_names = preprocessor.get_feature_names_out().tolist()

    # Sample
    sample_size = min(n_samples, len(_df))
    sample_df = _df.sample(n=sample_size, random_state=42).reset_index(drop=True)
    X = sample_df[FEATURE_COLUMNS]
    X_transformed = preprocessor.transform(X)

    # Compute SHAP
    shap_vals = explainer.shap_values(X_transformed)
    if isinstance(shap_vals, list):
        shap_vals = shap_vals[1]

    # Find the feature column index in transformed features
    target_name = f"remainder__{feature_col}"
    if target_name in raw_feature_names:
        feat_idx = raw_feature_names.index(target_name)
        feature_values = sample_df[feature_col].values
        shap_values_feat = shap_vals[:, feat_idx]

        return pd.DataFrame({
            "feature_value": feature_values,
            "shap_value": shap_values_feat,
        })

    return None
