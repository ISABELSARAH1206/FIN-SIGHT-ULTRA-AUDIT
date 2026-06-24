import pandas as pd
import numpy as np

class NeuralAuditEngine:
    def __init__(self, df):
        self.df = df
        # Clean numeric columns
        cols = ['Account Balance', 'Loan Amount', 'Transaction Amount', 'Interest Rate']
        for col in cols:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)

    def run_audit(self, query, nudge=0):
        # 1. Identity Search
        match = self.df[self.df['First Name'].str.contains(query, case=False) | 
                        self.df['Last Name'].str.contains(query, case=False)]
        if match.empty: return None
        u = match.iloc[0]

        # 2. Logic Metrics
        balance = float(u['Account Balance'])
        avg_spend = self.df['Transaction Amount'].mean() * 30
        survival_days = (balance / avg_spend) * 30 if avg_spend > 0 else 365

        interest_leak = (float(u['Loan Amount']) * (float(u['Interest Rate'])/100)) / 12
        tax_leak = balance * 0.015 

        # 3. 60-Month Wealth Simulation
        projection = [balance]
        for _ in range(60):
            projection.append((projection[-1] + nudge) * 1.0066)

        return {
            "name": f"{u['First Name']} {u['Last Name']}",
            "balance": balance,
            "survival": int(survival_days),
            "leak": round(interest_leak + tax_leak, 2),
            "risk": 100 - (self.df[self.df['Anomaly'] == 1].shape[0] * 5),
            "projection": projection
        }