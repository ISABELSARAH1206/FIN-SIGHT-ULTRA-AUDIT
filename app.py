import streamlit as st
import pandas as pd
import json
import os
import plotly.express as px

# ======================================================
# LANGUAGE PACK
# ======================================================

TRANSLATIONS = {
    "English": {
        "title": "FIN-SIGHT ULTRA PRO",
        "login": "Login",
        "register": "Register",
        "username": "Username",
        "pin": "PIN",
        "authorize": "Authorize",
        "logout": "Logout",
        "audit": "Audit Identity",
        "module": "Select Module",
        "features": [
            "Health Overview",
            "Fraud Alerts",
            "Spending Analytics",
            "Transaction Logs",
            "Subscription Leaks",
            "Savings Goal Tracker",
            "Capital Impact Simulator",
            "Neural Wealth Forecast",
            "GST Audit",
            "Financial Health Score",
            "Smart Expense Advisor",
            "Emergency Risk Predictor",
            "Family Expense Alert",
            "Merchant Intelligence",
            "Monthly Summary"
        ]
    },

    "Hindi": {
        "title": "फिन-साइट अल्ट्रा प्रो",
        "login": "लॉगिन",
        "register": "पंजीकरण",
        "username": "उपयोगकर्ता नाम",
        "pin": "पिन",
        "authorize": "प्रवेश",
        "logout": "लॉग आउट",
        "audit": "पहचान खोजें",
        "module": "मॉड्यूल चुनें",
        "features": [
            "स्वास्थ्य अवलोकन",
            "धोखाधड़ी अलर्ट",
            "व्यय विश्लेषण",
            "लेनदेन लॉग",
            "सदस्यता लीकेज",
            "बचत लक्ष्य ट्रैकर",
            "पूंजी प्रभाव सिम्युलेटर",
            "धन पूर्वानुमान",
            "जीएसटी ऑडिट",
            "वित्तीय स्कोर",
            "व्यय सलाहकार",
            "जोखिम पूर्वानुमान",
            "पारिवारिक खर्च अलर्ट",
            "व्यापारी विश्लेषण",
            "मासिक सारांश"
        ]
    },

    "Tamil": {
        "title": "பின்-சைட் அல்ட்ரா ப்ரோ",
        "login": "உள்நுழை",
        "register": "பதிவு",
        "username": "பயனர் பெயர்",
        "pin": "பின்",
        "authorize": "அனுமதி",
        "logout": "வெளியேறு",
        "audit": "அடையாள தேடல்",
        "module": "தொகுதியைத் தேர்ந்தெடுக்கவும்",
        "features": [
            "சுகாதார கண்ணோட்டம்",
            "மோசடி எச்சரிக்கை",
            "செலவு பகுப்பாய்வு",
            "பரிவர்த்தனை பதிவு",
            "சந்தா கசிவு",
            "சேமிப்பு இலக்கு கண்காணிப்பு",
            "மூலதன தாக்க சிமுலேட்டர்",
            "செல்வ முன்னறிவிப்பு",
            "ஜிஎஸ்டி ஆய்வு",
            "நிதி மதிப்பெண்",
            "செலவு ஆலோசகர்",
            "அபாய கணிப்பு",
            "குடும்ப செலவு எச்சரிக்கை",
            "வணிக பகுப்பாய்வு",
            "மாத சுருக்கம்"
        ]
    }
}

# ======================================================
# AUTH SYSTEM
# ======================================================

USER_DB = "users.json"

def load_db():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {"admin": "1234"}

def save_db(db):
    with open(USER_DB, "w") as f:
        json.dump(db, f)

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(page_title="FIN-SIGHT ULTRA PRO", layout="wide")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

# ======================================================
# LANGUAGE SIDEBAR
# ======================================================

st.sidebar.title("Language")

st.session_state["lang"] = st.sidebar.selectbox(
    "",
    ["English", "Hindi", "Tamil"]
)

curr = TRANSLATIONS[st.session_state["lang"]]

# ======================================================
# LOGIN
# ======================================================

if not st.session_state["auth"]:

    st.title(curr["title"])

    tab1, tab2 = st.tabs([curr["login"], curr["register"]])

    db = load_db()

    with tab1:
        u = st.text_input(curr["username"])
        p = st.text_input(curr["pin"], type="password")

        if st.button(curr["authorize"]):
            if u in db and db[u] == p:
                st.session_state["auth"] = True
                st.rerun()
            else:
                st.error("Access Denied")

    with tab2:
        nu = st.text_input("New Username")
        np = st.text_input("New PIN", type="password")

        if st.button(curr["register"]):
            db[nu] = np
            save_db(db)
            st.success("Registered")

# ======================================================
# DASHBOARD
# ======================================================

else:

    df = pd.read_csv("UPI_Transactions.csv")

    with st.sidebar:
        target = st.text_input(curr["audit"], value="Sanaa")

        option = st.radio(curr["module"], curr["features"])

        if st.button(curr["logout"]):
            st.session_state["auth"] = False
            st.rerun()

    u_df = df[df['Customer_Name'].str.contains(target, case=False, na=False)]

    if u_df.empty:
        st.error("No user found")
        st.stop()

    balance = float(u_df['Account_Balance'].iloc[-1])

    st.header(f"{option}: {target}")

    feature = curr["features"]

    # ======================================================
    # SAVINGS GOAL TRACKER FIXED
    # ======================================================

    if option == feature[5]:

        goal = st.number_input("Goal Amount", min_value=1000, value=500000)

        monthly_save = st.number_input("Monthly Saving", min_value=500, value=5000)

        current = max(balance, 0)

        progress = current / goal

        if progress > 1:
            progress = 1.0

        months_needed = (goal - current) / monthly_save if monthly_save > 0 else 0

        st.progress(progress)

        st.metric("Current Savings", f"₹{current:,.2f}")
        st.metric("Completion", f"{progress*100:.2f}%")
        st.metric("Months Needed", f"{months_needed:.1f}")

    # ======================================================
    # CAPITAL IMPACT SIMULATOR FIXED
    # ======================================================

    elif option == feature[6]:

        cost = st.number_input("Purchase Cost", min_value=1, value=10000)

        remaining = balance - cost

        impact = (cost / balance)*100 if balance > 0 else 100

        if impact > 100:
            impact = 100

        st.metric("Current Balance", f"₹{balance:,.2f}")
        st.metric("Remaining Balance", f"₹{remaining:,.2f}")
        st.metric("Capital Impact", f"{impact:.2f}%")

        st.progress(impact/100)

        if remaining < 0:
            st.error("Purchase exceeds available balance")

    # ======================================================
    # OTHER FEATURES
    # ======================================================

    elif option == feature[0]:
        st.metric("Balance", f"₹{balance:,.2f}")
        st.line_chart(u_df['Amount'])

    elif option == feature[1]:
        st.dataframe(u_df[u_df['Is_Anomaly'] == 1])

    elif option == feature[2]:
        fig = px.pie(u_df, values='Amount', names='Category')
        st.plotly_chart(fig)

    elif option == feature[3]:
        st.dataframe(u_df[['Transaction_Date','Description','Amount']])

    elif option == feature[4]:
        subs = u_df[u_df['Description'].str.contains(
            'netflix|spotify|amazon|prime|youtube',
            case=False,
            na=False
        )]
        st.dataframe(subs)

    elif option == feature[7]:
        forecast = [balance*(1.01**i) for i in range(12)]
        st.area_chart(forecast)

    elif option == feature[8]:
        st.metric("GST Paid", f"₹{u_df['GST_Paid'].sum():,.2f}")

    elif option == feature[9]:
        score = 100
        if balance < 5000:
            score -= 20
        st.metric("Score", f"{score}/100")

    elif option == feature[10]:
        category = u_df.groupby("Category")["Amount"].sum()
        st.write(category)

    elif option == feature[11]:
        avg = u_df['Amount'].mean()
        days = balance/avg if avg > 0 else 0
        st.metric("Safe Days", f"{days:.1f}")

    elif option == feature[12]:
        family = u_df[u_df['Category'].astype(str).str.contains(
            'grocery|medical|education|food',
            case=False,
            na=False
        )]
        st.dataframe(family)

    elif option == feature[13]:
        merchant = u_df.groupby('Description')['Amount'].sum()
        st.dataframe(merchant.sort_values(ascending=False).head(10))

    elif option == feature[14]:
        st.write("Top Expense:", u_df.groupby("Category")['Amount'].sum().idxmax())
        st.write("Fraud Count:", len(u_df[u_df['Is_Anomaly']==1]))