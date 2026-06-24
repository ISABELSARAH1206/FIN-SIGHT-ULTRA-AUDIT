import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def create_advanced_ledger():

    names = ["Sanaa", "Rahul", "Priya", "Arjun", "Anjali"]

    categories = [
        "UPI", "Merchant", "Rent", "Subscription",
        "Tax", "Investment", "EMI", "Dining",
        "Medical", "Education", "Grocery", "Salary"
    ]

    merchants = [
        "Amazon", "Flipkart", "Swiggy", "Zomato",
        "Netflix", "Spotify", "Apollo", "Uber",
        "Myntra", "BigBasket"
    ]

    cities = ["Chennai", "Bangalore", "Mumbai", "Delhi", "Hyderabad"]

    payment_modes = ["UPI", "Card", "NetBanking"]

    data = []

    for name in names:

        base_bal = random.randint(200000, 500000)
        credit_score = random.randint(680, 850)

        for i in range(150):

            date = (datetime.now() - timedelta(days=random.randint(0, 180))).strftime('%Y-%m-%d')

            category = random.choice(categories)

            merchant = random.choice(merchants)

            city = random.choice(cities)

            payment = random.choice(payment_modes)

            fraud = 0

            if i == 20 and name == "Sanaa":
                fraud = 1
                amount = 120000
                merchant = "Unknown Transfer"

            else:
                if category == "Salary":
                    amount = random.randint(40000, 90000)
                else:
                    amount = random.randint(100, 15000)

            if category == "Subscription":
                merchant = random.choice(["Netflix", "Spotify", "Amazon Prime"])

            if category == "Medical":
                merchant = random.choice(["Apollo", "MedPlus"])

            if category == "Education":
                merchant = random.choice(["Udemy", "Coursera"])

            if category == "Grocery":
                merchant = random.choice(["BigBasket", "DMart"])

            if category == "Dining":
                merchant = random.choice(["Swiggy", "Zomato"])

            gst = round(amount * 0.18, 2) if category in ["Merchant", "Dining", "Grocery"] else 0

            txn_type = "Credit" if category == "Salary" else "Debit"

            if txn_type == "Debit":
                base_bal -= amount
            else:
                base_bal += amount

            data.append({

                "Customer_Name": name,
                "Account_Balance": round(base_bal, 2),
                "Credit_Score": credit_score,
                "Transaction_Date": date,
                "Amount": round(amount, 2),
                "Category": category,
                "Merchant": merchant,
                "Payment_Mode": payment,
                "City": city,
                "Transaction_Type": txn_type,
                "Is_Anomaly": fraud,
                "Description": merchant,
                "GST_Paid": gst

            })

    df = pd.DataFrame(data)

    df.to_csv("UPI_Transactions.csv", index=False)

    print("✅ Advanced Ledger Created Successfully")

if __name__ == "__main__":
    create_advanced_ledger()