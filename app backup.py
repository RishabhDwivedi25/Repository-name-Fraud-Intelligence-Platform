import streamlit as st

st.title("Fraud Intelligence Platform")

amount = st.number_input("Transaction Amount")

if st.button("Check Risk"):
    if amount > 100000:
        st.error("High Risk Transaction")
    else:
        st.success("Low Risk Transaction")