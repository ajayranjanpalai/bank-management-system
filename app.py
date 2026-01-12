import streamlit as st
from Bank import BankSystem

st.set_page_config(page_title="Bank System", layout="centered")
st.title("🏦 Bank Management System")

bank = BankSystem()

menu = st.sidebar.radio(
    "Menu",
    ["Create Account", "Deposit", "Withdraw", "Show Details", "Delete Account"]
)

def auth():
    accno = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    return accno, pin

# ---------------- CREATE ACCOUNT ----------------
if menu == "Create Account":
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=18, step=1)
    email = st.text_input("Email")
    pin = st.text_input("4-digit PIN", type="password")
    acc_type = st.selectbox("Account Type", ["Savings", "Current"])

    if st.button("Create"):
        if not name or len(pin) != 4:
            st.error("Invalid input")
        else:
            accno = bank.generate_account()
            bank.data.append({
                "name": name,
                "age": age,
                "email": email,
                "pin": int(pin),
                "accountno": accno,
                "balance": 0,
                "type": acc_type
            })
            bank.save()
            st.success(f"Account Created ✅\nAccount No: {accno}")

# ---------------- DEPOSIT ----------------
elif menu == "Deposit":
    accno, pin = auth()
    amount = st.number_input("Amount", min_value=1)

    if st.button("Deposit"):
        user = bank.find_user(accno, int(pin))
        if user:
            user["balance"] += amount
            bank.save()
            st.success("Deposit Successful")
        else:
            st.error("Invalid credentials")

# ---------------- WITHDRAW ----------------
elif menu == "Withdraw":
    accno, pin = auth()
    amount = st.number_input("Amount", min_value=1)

    if st.button("Withdraw"):
        user = bank.find_user(accno, int(pin))
        if user and user["balance"] >= amount:
            user["balance"] -= amount
            bank.save()
            st.success("Withdrawal Successful")
        else:
            st.error("Invalid user or insufficient balance")

# ---------------- SHOW DETAILS ----------------
elif menu == "Show Details":
    accno, pin = auth()

    if st.button("Show"):
        user = bank.find_user(accno, int(pin))
        if user:
            st.json({k: v for k, v in user.items() if k != "pin"})
        else:
            st.error("Invalid credentials")

# ---------------- DELETE ----------------
elif menu == "Delete Account":
    accno, pin = auth()

    if st.button("Delete"):
        user = bank.find_user(accno, int(pin))
        if user:
            bank.data.remove(user)
            bank.save()
            st.success("Account Deleted")
        else:
            st.error("Invalid credentials")
