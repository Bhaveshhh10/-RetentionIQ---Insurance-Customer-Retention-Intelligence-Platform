# app_v2.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="Insurance Customer Retention Intelligence Platform", page_icon="🛡️", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("customer_risk_scores.csv")

df = load_data()

st.markdown("<h1>🛡️ Insurance Customer Retention Intelligence Platform</h1>", unsafe_allow_html=True)

page = st.sidebar.radio("Navigation", ["🏠 Executive Dashboard","👤 Customer Explorer","🚨 High Risk Customers"])

total_customers = len(df)
high_risk = len(df[df['Risk_Category']=='High'])
medium_risk = len(df[df['Risk_Category']=='Medium'])
avg_risk = round(df['Risk_Score'].mean(),2)

if page == "🏠 Executive Dashboard":
    st.info(f"Portfolio Summary: {high_risk} high-risk customers out of {total_customers}. Average risk score: {avg_risk}%")

    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Customers", total_customers)
    c2.metric("High Risk", high_risk)
    c3.metric("Medium Risk", medium_risk)
    c4.metric("ROC-AUC", "0.785")

    left,right = st.columns(2)

    with left:
        risk_counts = df['Risk_Category'].value_counts().reset_index()
        risk_counts.columns=['Risk','Count']
        fig = px.pie(risk_counts, names='Risk', values='Count', hole=0.6)
        st.plotly_chart(fig, use_container_width=True)

    with right:
        drivers = pd.DataFrame({
            'Feature':['Premium Change','Late Payments','Multi Policy','Complaints','Quote Request'],
            'Importance':[0.24,0.20,0.22,0.11,0.11]
        })
        fig2 = px.bar(drivers,x='Importance',y='Feature',orientation='h')
        st.plotly_chart(fig2,use_container_width=True)

elif page == "👤 Customer Explorer":
    idx = st.selectbox("Select Customer", df.index)
    customer = df.loc[idx]

    col1,col2 = st.columns(2)

    with col1:
        st.write(customer[['age','region_name','policy_type','customer_tenure_months']])

    with col2:
        fig = go.Figure(go.Indicator(mode='gauge+number', value=float(customer['Risk_Score'])))
        st.plotly_chart(fig, use_container_width=True)

elif page == "🚨 High Risk Customers":
    st.dataframe(df[df['Risk_Category']=='High'], use_container_width=True)
