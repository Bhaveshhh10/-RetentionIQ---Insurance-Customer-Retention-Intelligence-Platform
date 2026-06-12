"""
Page 4 — Model Insights
Model performance analysis with confusion matrix, feature importance,
SHAP global summary, and SHAP dependence plots.
Translates ML metrics into business-friendly language.
"""
import streamlit as st
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, confusion_matrix,
)
from utils.data_loader import load_risk_data, load_training_data, load_model
from utils.shap_engine import get_global_shap_importance, get_shap_dependence_data
from ui.components.metrics import (
    render_hero_section, render_section_header, render_metric_card,
    render_info_box, clean_html,
)
from ui.components.charts import (
    confusion_matrix_heatmap, feature_importance_bar, shap_dependence_scatter,
)
from config import FEATURE_COLUMNS, FEATURE_DISPLAY_NAMES


@st.cache_data
def _compute_model_metrics(_model, _train_df):
    """Compute classification metrics on the training dataset."""
    X = _train_df[FEATURE_COLUMNS]
    y_true = _train_df["churn_flag"].values

    y_prob = _model.predict_proba(X)[:, 1]
    y_pred = (y_prob >= 0.5).astype(int)

    return {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
        "roc_auc": roc_auc_score(y_true, y_prob),
        "y_true": y_true,
        "y_pred": y_pred,
        "y_prob": y_prob,
    }


def render():
    """Render the Model Insights page."""
    df = load_risk_data()
    model = load_model()

    # ── Hero ──
    render_hero_section(
        title="Model Insights",
        subtitle="XGBoost churn prediction model performance, explainability, and feature analysis.",
        badge_text="XGBoost · 300 Trees · SHAP Explainability",
    )

    # ── Model Performance Metrics ──
    render_section_header("📊 Model Performance", "Evaluation metrics computed on 50,000 customers")

    with st.spinner("Computing model metrics..."):
        try:
            train_df = load_training_data()
            metrics = _compute_model_metrics(model, train_df)
            metrics_computed = True
        except Exception as e:
            metrics_computed = False
            st.warning(f"Could not compute metrics on training data: {e}")

    if metrics_computed:
        c1, c2, c3, c4, c5 = st.columns(5)
        with c1:
            render_metric_card(
                "📈", "ROC-AUC",
                f"{metrics['roc_auc']:.3f}",
                delta="Model discrimination",
                delta_type="positive",
                accent="cyan",
            )
        with c2:
            render_metric_card(
                "🎯", "Accuracy",
                f"{metrics['accuracy'] * 100:.1f}%",
                accent="blue",
            )
        with c3:
            render_metric_card(
                "🔎", "Precision",
                f"{metrics['precision'] * 100:.1f}%",
                delta="Churn prediction reliability",
                delta_type="neutral",
                accent="purple",
            )
        with c4:
            render_metric_card(
                "📡", "Recall",
                f"{metrics['recall'] * 100:.1f}%",
                delta="Churn detection rate",
                delta_type="neutral",
                accent="warning",
            )
        with c5:
            render_metric_card(
                "⚖️", "F1 Score",
                f"{metrics['f1'] * 100:.1f}%",
                delta="Precision-Recall balance",
                delta_type="neutral",
                accent="success",
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Business translation
        render_info_box(
            f"<strong>What this means for the business:</strong> "
            f"Our model correctly identifies <strong>{metrics['recall'] * 100:.0f}%</strong> of customers "
            f"who will actually churn (Recall), and when it predicts churn, it's correct "
            f"<strong>{metrics['precision'] * 100:.0f}%</strong> of the time (Precision). "
            f"The ROC-AUC of <strong>{metrics['roc_auc']:.3f}</strong> means the model is significantly "
            f"better than random chance (0.5) at distinguishing between churners and non-churners."
        )

        # ── Confusion Matrix & Feature Importance ──
        col_cm, col_fi = st.columns(2)

        with col_cm:
            fig_cm = confusion_matrix_heatmap(metrics["y_true"], metrics["y_pred"])
            st.plotly_chart(fig_cm, use_container_width=True, key="confusion_matrix")

            # Business interpretation
            cm = confusion_matrix(metrics["y_true"], metrics["y_pred"])
            tp = cm[1][1]
            fn = cm[1][0]
            fp = cm[0][1]
            st.markdown(clean_html(f"""
            <div style="padding: 12px 16px; background: rgba(17,24,39,0.6);
                        border: 1px solid rgba(255,255,255,0.05); border-radius: 10px;
                        font-size: 13px; color: #94a3b8; line-height: 1.7;">
                <strong style="color: #f8fafc;">Reading the Matrix:</strong><br>
                ✅ <strong style="color: #10b981;">{tp:,}</strong> churners correctly identified<br>
                ❌ <strong style="color: #ef4444;">{fn:,}</strong> churners missed (false negatives)<br>
                ⚠️ <strong style="color: #f59e0b;">{fp:,}</strong> false alarms (false positives)
            </div>
            """), unsafe_allow_html=True)

        with col_fi:
            with st.spinner("Computing SHAP feature importance..."):
                try:
                    importance_df = get_global_shap_importance(model, df)
                    fig_fi = feature_importance_bar(importance_df, top_n=15)
                    st.plotly_chart(fig_fi, use_container_width=True, key="feature_importance")
                except Exception as e:
                    st.warning(f"Could not compute SHAP importance: {e}")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── SHAP Dependence ──
    render_section_header(
        "🔬 SHAP Dependence Analysis",
        "Explore how individual feature values influence the model's predictions",
    )

    numerical_features = [
        col for col in FEATURE_COLUMNS
        if col not in ['region_name', 'age_band', 'marital_status', 'policy_type', 'payment_frequency']
    ]
    feature_display = {col: FEATURE_DISPLAY_NAMES.get(col, col) for col in numerical_features}

    dep_col1, dep_col2 = st.columns([1, 3])
    with dep_col1:
        selected_feature_display = st.selectbox(
            "Select Feature",
            options=list(feature_display.values()),
            index=list(feature_display.values()).index("Customer Tenure") if "Customer Tenure" in feature_display.values() else 0,
        )
        # Reverse map to column name
        selected_col = [k for k, v in feature_display.items() if v == selected_feature_display][0]

    with dep_col2:
        with st.spinner("Computing SHAP dependence..."):
            try:
                dep_data = get_shap_dependence_data(model, df, selected_col)
                if dep_data is not None:
                    fig_dep = shap_dependence_scatter(dep_data, selected_feature_display)
                    st.plotly_chart(fig_dep, use_container_width=True, key="shap_dep")
                else:
                    st.info("Dependence data not available for categorical features.")
            except Exception as e:
                st.warning(f"Could not compute dependence plot: {e}")

    # ── Model Architecture ──
    with st.expander("🏗️ Model Architecture Details"):
        st.markdown(clean_html("""
        <div style="line-height: 1.8; color: #94a3b8; font-size: 14px;">
            <table style="width: 100%; border-collapse: collapse;">
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px 0; color: #64748b; width: 40%;">Algorithm</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">XGBoost Classifier</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px 0; color: #64748b;">Estimators</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">300 trees</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px 0; color: #64748b;">Max Depth</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">6</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px 0; color: #64748b;">Learning Rate</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">0.05</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px 0; color: #64748b;">Preprocessing</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">OneHotEncoder (5 categorical) + Passthrough (30 numerical)</td>
                </tr>
                <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
                    <td style="padding: 8px 0; color: #64748b;">Training Data</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">50,000 customers</td>
                </tr>
                <tr>
                    <td style="padding: 8px 0; color: #64748b;">Explainability</td>
                    <td style="padding: 8px 0; color: #f8fafc; font-weight: 600;">SHAP TreeExplainer v0.52</td>
                </tr>
            </table>
        </div>
        """), unsafe_allow_html=True)
