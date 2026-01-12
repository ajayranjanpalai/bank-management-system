import streamlit as st
from Bank import BankSystem

# BASIC PAGE RENDER (VERY IMPORTANT)
st.set_page_config(page_title="Bank Management System")
st.title("🏦 Bank Management System")
st.write("App is running successfully 🚀")

bank = BankSystem()

st.sidebar.title("Menu")
menu = st.sidebar.radio(
    "Choose option",
    ["Create Account", "View Accounts"]
)

if menu == "Create Account":
    st.subheader("Create Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")

    if st.button("Create"):
        if name and len(pin) == 4:
            acc_no = bank.generate_account()
            bank.data.append({
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "accountno": acc_no,
                "balance": 0,
                "type": "Savings"
            })
            bank.save()
            st.success(f"Account created ✅ Account No: {acc_no}")
        else:
            st.error("Invalid input")

elif menu == "View Accounts":
    st.subheader("All Accounts")
    st.json(bank.data)
