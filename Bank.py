import json
import random
import string
from pathlib import Path
from abc import ABC, abstractmethod

# ================= ABSTRACT ACCOUNT =================
class Account(ABC):
    def __init__(self, data: dict):
        self.name = data["name"]
        self.age = data["age"]
        self.email = data["email"]
        self.pin = data["pin"]
        self.accountno = data["accountno"]
        self._balance = data["balance"]

    def deposit(self, amount: int):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount

    @abstractmethod
    def withdraw(self, amount: int):
        pass

    def get_balance(self):
        return self._balance


class SavingsAccount(Account):
    MIN_BALANCE = 500

    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")
        if self._balance - amount < self.MIN_BALANCE:
            raise ValueError("Minimum balance of 500 required")
        self._balance -= amount


class CurrentAccount(Account):
    def withdraw(self, amount: int):
        if amount <= 0:
            raise ValueError("Invalid withdrawal amount")
        if amount > self._balance:
            raise ValueError("Insufficient balance")
        self._balance -= amount


# ================= BANK SYSTEM =================
class BankSystem:
    def __init__(self, database="data.json"):
        self.database = database
        self.data = self._load_data()

    # ---------- FILE HANDLING ----------
    def _load_data(self):
        if Path(self.database).exists():
            with open(self.database, "r") as f:
                return json.load(f)
        return []

    def _save_data(self):
        with open(self.database, "w") as f:
            json.dump(self.data, f, indent=4)

    # ---------- PUBLIC HELPERS (FOR STREAMLIT) ----------
    def save(self):
        self._save_data()

    def generate_account(self):
        return ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=8)
        )

    def find_user(self, accno, pin):
        for user in self.data:
            if user["accountno"] == accno and user["pin"] == pin:
                return user
        return None

    def get_account_object(self, user):
        if user["type"] == "Savings":
            return SavingsAccount(user)
        return CurrentAccount(user)

    # ---------- CORE OPERATIONS ----------
    def create_account(self, name, age, email, pin, acc_type):
        if age < 18 or len(str(pin)) != 4:
            raise ValueError("Invalid age or PIN")

        account = {
            "name": name,
            "age": age,
            "email": email,
            "pin": pin,
            "accountno": self.generate_account(),
            "balance": 0,
            "type": acc_type
        }

        self.data.append(account)
        self._save_data()
        return account["accountno"]

    def deposit(self, user, amount):
        acc = self.get_account_object(user)
        acc.deposit(amount)
        user["balance"] = acc.get_balance()
        self._save_data()

    def withdraw(self, user, amount):
        acc = self.get_account_object(user)
        acc.withdraw(amount)
        user["balance"] = acc.get_balance()
        self._save_data()

    def update_details(self, user, name=None, email=None):
        if name:
            user["name"] = name
        if email:
            user["email"] = email
        self._save_data()

    def delete_account(self, user):
        self.data.remove(user)
        self._save_data()
