import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Fraud Intelligence Platform",
    page_icon="🏦",
    layout="wide"
)

# Sidebar
# Sidebar
st.sidebar.title("🏦 Fraud Intelligence")

st.sidebar.markdown("---")

st.sidebar.info("🤖 Model: Random Forest")

st.sidebar.success("🟢 Status: Active")

st.sidebar.markdown("---")

st.sidebar.write("Developer")
st.sidebar.write("Rishabh Dwivedi")

st.sidebar.markdown("---")

st.sidebar.write("Version 1.0")
# Main Title
st.markdown("""
<h1 style='text-align: center; color: #1f77b4;'>
🏦 Fraud Intelligence Platform
</h1>
<h4 style='text-align: center;'>
Machine Learning Powered Fraud Detection Dashboard
</h4>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.info("🤖 Model: Random Forest")

with col2:
    st.success("🛡️ Platform: Fraud Detection")

with col3:
    st.warning("🟢 Status: Active")
st.markdown("---")
# Load Model
@st.cache_resource
def load_model():
    return joblib.load("fraud_model.pkl")

model = load_model()
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Dashboard", "🔍 Single Transaction"])

with tab1:

    st.subheader("📂 Upload Transactions CSV")
    
    uploaded_file = st.file_uploader(
         "Choose a file",
        type=["csv", "xlsx"]
    )

    if uploaded_file is not None:
    

       if uploaded_file.name.endswith(".csv"):
           csv_data = pd.read_csv(uploaded_file)
       else:
           csv_data = pd.read_excel(uploaded_file)

       st.subheader("Uploaded Data")
       st.dataframe(csv_data.head())

       predictions = model.predict(csv_data)

       csv_data["Prediction"] = predictions

       csv_data["Prediction"] = csv_data["Prediction"].map(
            {0: "Legitimate", 1: "Fraud"}
        )

       fraud_count = (csv_data["Prediction"] == "Fraud").sum()
       legit_count = (csv_data["Prediction"] == "Legitimate").sum()

       st.subheader("📊 Summary")

       col1, col2 = st.columns(2)

       with col1:
            st.metric("Fraud Transactions", fraud_count)

       with col2:
            st.metric("Legitimate Transactions", legit_count)

       st.dataframe(csv_data)
       total_transactions = fraud_count + legit_count
       fraud_rate = (fraud_count / total_transactions) * 100

       st.metric("Fraud Rate (%)", f"{fraud_rate:.1f}%")

       if fraud_count > 0:
          st.warning(f"⚠️ {fraud_count} suspicious transaction(s) detected!")
       else:
          st.success("✅ No suspicious transactions detected.")

       col3, col4, col5 = st.columns(3)

       with col3:
          st.metric("Total Transactions", len(csv_data))

       with col4:
         st.metric(
            "Highest Amount",
            f"₹{csv_data['amount'].max()/10000000:.1f} Cr"
        )

       with col5:
         st.metric(
        "Average Amount",
        f"₹{csv_data['amount'].mean()/10000000:.1f} Cr"
        )

       st.markdown("---")

       st.markdown("---")
       st.subheader("🏦 Financial Risk Metrics")

       st.subheader("📊 Executive Risk Summary")

       risk1, risk2, risk3, risk4 = st.columns(4)
    
       fraud_rows = csv_data[csv_data["Prediction"] == "Fraud"]
       legit_rows = csv_data[csv_data["Prediction"] == "Legitimate"]

       colA, colB = st.columns(2)

       with colA:
         st.metric(
          "Fraud Amount",
           f"₹{fraud_rows['amount'].sum()/10000000:.1f} Cr"
        )

       with colB:
         legit_rows = csv_data[csv_data["Prediction"] == "Legitimate"]

         st.metric(
            "Legitimate Amount",
            f"₹{legit_rows['amount'].sum()/10000000:.1f} Cr"
        )

       with risk1:
          st.metric("Transactions", len(csv_data))

       with risk2:
         st.metric("Frauds", fraud_count)

       with risk3:
         st.metric("Fraud Rate", f"{fraud_rate:.1f}%")

       with risk4:
           st.metric(
           "Highest Amount",
           f"₹{csv_data['amount'].max()/10000000:.1f} Cr"
        )

       st.markdown("---")

       st.subheader("📊 Fraud Analytics Dashboard")

       chart1, chart2 = st.columns([3,2])

       with chart1:
         fig2, ax2 = plt.subplots()

         ax2.bar(
            ["Fraud", "Legitimate"],
            [fraud_count, legit_count]
         )

         ax2.set_title("Fraud vs Legitimate Transactions")
         st.pyplot(fig2)

       with chart2:
         fig3, ax3 = plt.subplots(figsize=(3,3))

         ax3.pie(
           [fraud_count, legit_count],
           labels=["Fraud", "Legitimate"],
           autopct="%1.1f%%",
           radius=0.6
        )

         ax3.set_title("Fraud Distribution")

         fig3.tight_layout()

         st.pyplot(fig3, use_container_width=False)

    
       st.subheader("🚨 Top Suspicious Transactions")

       fraud_rows = csv_data[csv_data["Prediction"] == "Fraud"]
   
       st.metric(
          "Suspicious Transactions",
          len(fraud_rows)
        )

    

       fraud_rows = fraud_rows.sort_values(
            by="amount",
            ascending=False
        )

        
       st.dataframe(
         fraud_rows.head(10),
         use_container_width=True
        )
       csv_file = csv_data.to_csv(index=False).encode("utf-8")

       st.download_button(
            "📥 Download Fraud Analysis Report",
            data=csv_file,
            file_name="fraud_predictions.csv",
            mime="text/csv"
        )

  
with tab2:
 
    # Inputs
    amount = st.number_input("Transaction Amount", min_value=0.0)
    oldbalanceOrg = st.number_input("Old Balance Origin", min_value=0.0)
    newbalanceOrig = st.number_input("New Balance Origin", min_value=0.0)
    oldbalanceDest = st.number_input("Old Balance Destination", min_value=0.0)
    newbalanceDest = st.number_input("New Balance Destination", min_value=0.0)

    # Prediction Button
    if st.button("Check Risk"):

        st.subheader("Transaction Summary")

        st.write("Amount:", amount)
        st.write("Old Balance Origin:", oldbalanceOrg)
        st.write("New Balance Origin:", newbalanceOrig)
        st.write("Old Balance Destination:", oldbalanceDest)
        st.write("New Balance Destination:", newbalanceDest)

        data = pd.DataFrame({
            'amount': [amount],
            'oldbalanceOrg': [oldbalanceOrg],
            'newbalanceOrig': [newbalanceOrig],
            'oldbalanceDest': [oldbalanceDest],
            'newbalanceDest': [newbalanceDest]
        })

        prediction = model.predict(data)[0]
        probability = model.predict_proba(data)[0]

        st.subheader("Prediction Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Amount", f"₹{amount:,.0f}")

        with col2:
            if prediction == 1:
                st.metric("Confidence", f"{probability[1]*100:.1f}%")
            else:
                st.metric("Confidence", f"{probability[0]*100:.1f}%")

        with col3:
            if prediction == 1:
                st.metric("Risk Level", "HIGH")
            else:
                st.metric("Risk Level", "LOW")

                

        


        if prediction == 1:
            st.error("🚨 Fraud Transaction Detected")
            st.progress(float(probability[1]))
            st.write(f"Risk Score: {probability[1]*100:.2f}%")
            st.warning("Risk Level: HIGH")
        else:
            st.success("✅ Legitimate Transaction")
            st.progress(float(probability[0]))
            st.write(f"Confidence: {probability[0]*100:.2f}%")
            st.info("Risk Level: LOW")
        colA, colB = st.columns(2)

        with colA:
            st.metric(
                "Fraud Probability",
                f"{probability[1]*100:.2f}%"
            )

        with colB:
            st.metric(
                "Legitimate Probability",
                f"{probability[0]*100:.2f}%"
            )

        st.subheader("🥧 Fraud Probability Distribution")

        fig2, ax2 = plt.subplots(figsize=(3,3))

        ax2.pie(
            [probability[0] * 100, probability[1] * 100],
            labels=["Legitimate", "Fraud"],
            autopct="%1.1f%%",
            radius=0.55
        )
        


        ax2.set_title("Probability Distribution")

        fig2.tight_layout()

        st.pyplot(fig2, use_container_width=False)
# End of file
st.markdown("---")
st.caption("Developed by Rishabh Dwivedi | Fraud Intelligence Platform v1.0")    

   