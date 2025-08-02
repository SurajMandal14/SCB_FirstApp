import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from models.ml_models import detect_anomalies, segment_users, detect_fraud_rules, train_forecasting_model
import numpy as np

st.set_page_config(layout="wide")

st.title("Smart Transaction Insight Dashboard")

# File Uploader
uploaded_file = st.sidebar.file_uploader("Upload your transaction CSV", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.sidebar.success("File uploaded successfully!")
    
    st.header("Raw Data")
    st.dataframe(df.head())

    # Basic Dashboard
    st.header("Basic Dashboard")
    col1, col2 = st.columns(2)

    with col1:
        # Total Spend
        total_spend = df[df['txn_type'] == 'DEBIT']['amount'].sum()
        st.metric("Total Spend", f"₹{total_spend:,.2f}")

        # Merchant-wise Spend
        st.subheader("Spend by Merchant")
        merchant_spend = df[df['txn_type'] == 'DEBIT'].groupby('merchant')['amount'].sum().sort_values(ascending=False)
        fig, ax = plt.subplots()
        merchant_spend.plot(kind='bar', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

    with col2:
        # Daily Spend
        st.subheader("Daily Spend")
        df['date'] = pd.to_datetime(df['date'])
        daily_spend = df[df['txn_type'] == 'DEBIT'].groupby('date')['amount'].sum()
        fig, ax = plt.subplots()
        daily_spend.plot(kind='line', ax=ax)
        plt.xticks(rotation=45)
        st.pyplot(fig)

        # Payment Method Usage
        st.subheader("Payment Method Usage")
        payment_method_counts = df['payment_method'].value_counts()
        fig, ax = plt.subplots()
        payment_method_counts.plot(kind='pie', autopct='%1.1f%%', ax=ax)
        plt.ylabel('')
        st.pyplot(fig)

    # ML Insights
    st.header("Machine Learning Insights")
    if st.button("Run ML Analysis"):
        # Anomaly Detection
        st.subheader("Anomaly Detection")
        anomalies = detect_anomalies(df.copy())
        st.write(f"Found {len(anomalies)} anomalous transactions.")
        st.dataframe(anomalies)

        # User Segmentation
        st.subheader("User Segmentation")
        segmented_df = segment_users(df.copy())
        fig, ax = plt.subplots()
        sns.countplot(x='segment', data=segmented_df, ax=ax)
        st.pyplot(fig)
        st.dataframe(segmented_df[['user_id', 'segment']].drop_duplicates().head())

        # Fraud Signals
        st.subheader("Fraud Signals")
        fraud_signals = detect_fraud_rules(df.copy())
        st.write(f"Found {len(fraud_signals)} transactions with fraud signals.")
        st.dataframe(fraud_signals)

        # Spend Forecasting
        st.subheader("Spend Forecasting (Next 30 Days)")
        forecasting_model = train_forecasting_model(df.copy())
        future_days = np.array(range(1, 366))[-30:].reshape(-1, 1)
        predictions = forecasting_model.predict(future_days)
        
        fig, ax = plt.subplots()
        ax.plot(future_days, predictions, label="Forecasted Spend")
        ax.set_xlabel("Day of Year")
        ax.set_ylabel("Predicted Spend")
        ax.legend()
        st.pyplot(fig)

    # Download Report
    if st.button("Generate and Download Report"):
        # In a real app, this would generate a PDF or a more detailed CSV
        st.download_button(
            label="Download Report (CSV)",
            data=df.to_csv(index=False).encode('utf-8'),
            file_name='transaction_report.csv',
            mime='text/csv',
        )
else:
    st.info("Please upload a CSV file to get started.")
