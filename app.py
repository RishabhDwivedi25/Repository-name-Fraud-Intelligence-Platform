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

# Load Model
@st.cache_resource
def load_model():
    return joblib.load("fraud_model.pkl")

model = load_model()

# CSV Upload
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

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Fraud Transactions", fraud_count)


    fig2, ax2 = plt.subplots()
    with col2:
        st.metric("Legitimate Transactions", legit_count)

    st.subheader("Prediction Results for Uploaded File")
    ax2.bar(
        ["Fraud", "Legitimate"],
        [fraud_count, legit_count]
    )

    ax2.set_title("Fraud vs Legitimate Transactions")
    ax2.set_ylabel("Number of Transactions")

    st.pyplot(fig2)

    st.dataframe(csv_data)



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