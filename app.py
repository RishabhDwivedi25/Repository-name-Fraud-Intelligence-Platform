import streamlit as st
import joblib
import pandas as pd
import matplotlib.pyplot as plt

# Sidebar
st.sidebar.title("Fraud Intelligence Platform")
st.sidebar.write("Machine Learning Based Fraud Detection System")

# Main Title
st.title("🏦 Fraud Intelligence Platform")
st.write("Analyze transactions using Machine Learning")
st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Model", "Random Forest")

with col2:
    st.metric("Platform", "Fraud Detection")

with col3:
    st.metric("Status", "Active")

st.markdown("---")
# Load Model
@st.cache_resource
def load_model():
    return joblib.load("fraud_model.pkl")

model = load_model()
st.markdown("---")

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
        st.metric("Highest Amount", f"₹{csv_data['amount'].max():,.0f}")

    with col5:
        st.metric("Average Amount", f"₹{csv_data['amount'].mean():,.0f}")

    st.markdown("---")

    st.subheader("📊 Risk Summary")

    st.write(f"Total Transactions: {len(csv_data)}")
    st.write(f"Fraud Transactions: {fraud_count}")
    st.write(f"Fraud Rate: {fraud_rate:.1f}%")
    st.write(f"Highest Amount: ₹{csv_data['amount'].max():,.0f}")

    st.markdown("---")

    st.subheader("📊 Fraud Analytics")

    chart1, chart2 = st.columns(2)

    with chart1:
        fig2, ax2 = plt.subplots()

        ax2.bar(
            ["Fraud", "Legitimate"],
            [fraud_count, legit_count]
        )

        ax2.set_title("Fraud vs Legitimate")
        st.pyplot(fig2)

    with chart2:
        fig3, ax3 = plt.subplots()

        ax3.pie(
            [fraud_count, legit_count],
            labels=["Fraud", "Legitimate"],
            autopct="%1.1f%%"
        )

        st.pyplot(fig3)

    st.subheader("🚨 Top Suspicious Transactions")

    fraud_rows = csv_data[csv_data["Prediction"] == "Fraud"]

    fraud_rows = fraud_rows.sort_values(
        by="amount",
        ascending=False
    )

    st.dataframe(fraud_rows)

    csv_file = csv_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "📥 Download Results",
        data=csv_file,
        file_name="fraud_predictions.csv",
        mime="text/csv"
    )

  

tab1, tab2 = st.tabs(["📊 Dashboard", "🔍 Single Transaction"])
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

    st.subheader("Fraud Probability Chart")

    fig, ax = plt.subplots()

    ax.bar(
        ["Legitimate %", "Fraud %"],
        [probability[0] * 100, probability[1] * 100]
    )
    st.pyplot(fig)