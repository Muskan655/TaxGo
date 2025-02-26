import streamlit as st
import pandas as pd
import openai

# Set Streamlit Page Config
st.set_page_config(page_title="TaxGo AI", page_icon="💰", layout="wide")
st.markdown("""
    <style>
        /* Global Text Color - White (Except Inputs & Buttons) */
        html, body, [class*="st-"] {
            color: white !important;
        }

        /* Background Image & Overlay */
        .stApp {
            background: linear-gradient(to right, rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("images.jpg") no-repeat center center fixed;
            background-size: cover;
        }

        /* Sidebar Text Color */
        [data-testid="stSidebar"] {
            background-color: rgba(20, 20, 20, 0.95) !important;
            color: white !important;
        }

        /* Section Headers */
        .section-title {
            font-size: 2rem;
            font-weight: bold;
            color: #FFD700 !important;
            text-align: center;
            margin-bottom: 2rem;
            margin-top: 1rem;
        }

        /* Buttons */
        .stButton > button {
            background-color: #FFB74D !important;
            color: black !important;
            font-size: 16px;
            font-weight: bold;
            padding: 12px 24px;
            border-radius: 10px;
            transition: 0.3s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #FF9800 !important;
            transform: scale(1.08);
        }

        /* Input Fields & Textareas - White Text */
        input, textarea, select {
            color: white !important;
            background-color: black !important;
            border: 1px solid white !important;
        }

        /* File Uploader Fix - Ensure Text is White */
        div[data-testid="stFileUploader"] * {
            color: black !important;
        }

        /* Force the Browse Button in File Uploader to be Visible */
        div[data-testid="stFileUploader"] button {
            background-color: #FFB74D !important;
            color: black !important;
            font-weight: bold !important;
        }

        /* Force Black Placeholder Text */
        [data-testid="stTextInput"] input::placeholder,
        [data-testid="stTextArea"] textarea::placeholder {
            color: black !important;
            opacity: 1 !important;
        }

        /* Increase Section Spacing */
        .spacer { margin-bottom: 200px; }
    </style>
""", unsafe_allow_html=True)

    

# 🔹 Sidebar Navigation
st.sidebar.title("📌 TaxGo AI Navigation")
section = st.sidebar.radio("Select a section:", [
    "🏠 Home",
    "🔑 Login / Signup",
    "📰 News & Updates",
    "📊 Expense Bucket",
    "📈 Dashboard",
    "🧮 Income Tax Calculator",
    "📝 E-Filing Tool",
    "📚 Library",
    "🤖 AI Chatbot",
    "👨‍👩‍👧 Family Tax Planner"
])

# 🔹 Home Section
if section == "🏠 Home":
    st.title("💰 TaxGo AI - Your Smart Tax Assistant")
    st.markdown("""
        Welcome to **TaxGo AI** - your personal AI-powered tax assistant! 🚀  
        This platform helps you **track expenses, calculate taxes, e-file returns, and optimize savings**.  
        
        ### 🌟 Features:
        - **Automated Tax Calculation** ✅  
        - **Smart Expense Tracking** 📊  
        - **Tax-Saving Investment Insights** 📈  
        - **AI Chatbot for Tax Queries** 🤖  
        - **Family Tax Planning** 👨‍👩‍👧  
    """)

# 🔹 Login / Signup
elif section == "🔑 Login / Signup":
    st.subheader("🔐 Secure Access")
    choice = st.radio("Select an option:", ["Login", "Signup"])
    
    if choice == "Login":
        st.text_input("📧 Email")
        st.text_input("🔑 Password", type="password")
        st.button("Login")
    
    elif choice == "Signup":
        st.text_input("📧 Email")
        st.text_input("👤 Full Name")
        st.text_input("🔑 Password", type="password")
        st.button("Signup")

# 🔹 News & Updates
elif section == "📰 News & Updates":
    st.subheader("📢 Latest Tax News")
    st.markdown("🟢 **Budget 2025 Update**: New tax slabs introduced for salaried professionals!")
    st.markdown("🔵 **80C Limit**: Govt. may increase deduction limit to ₹2,00,000.")
    st.markdown("🟠 **GST Reforms**: New simplified GST rules for small businesses.")

# 🔹 Expense Bucket
elif section == "📊 Expense Bucket":
    st.subheader("💳 Track Your Tax-Deductible Expenses")
    
    uploaded_file = st.file_uploader("Upload Expense CSV", type=["csv"])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

# 🔹 Dashboard
elif section == "📈 Dashboard":
    st.subheader("📊 Tax Overview Dashboard")
    st.metric("Total Income", "₹12,00,000")
    st.metric("Tax Paid", "₹1,80,000")
    st.metric("Deductions", "₹2,00,000")

# 🔹 Income Tax Calculator
elif section == "🧮 Income Tax Calculator":
    st.subheader("🧮 Calculate Your Income Tax")
    
    income = st.number_input("Enter Your Annual Income (₹)", value=500000)
    deductions = st.number_input("Enter Eligible Deductions (₹)", value=50000)
    
    taxable_income = max(0, income - deductions)
    
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.2
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.3

    st.write(f"**Estimated Tax: ₹{tax:,.2f}**")

# 🔹 E-Filing Tool
elif section == "📝 E-Filing Tool":
    st.subheader("📝 File Your Income Tax Return Online")
    st.markdown("Upload your **Form-16**, investment proofs, and salary slips to auto-file your tax return.")
    st.file_uploader("Upload Form-16 (PDF)", type=["pdf"])
    st.file_uploader("Upload Investment Proofs (PDF)", type=["pdf"])
    st.button("Proceed to Filing")

# 🔹 Library
elif section == "📚 Library":
    st.subheader("📚 Tax Documents & Guides")
    st.markdown("📄 **Income Tax Act PDF** - [Download](#)")
    st.markdown("📘 **80C Deduction Guide** - [Download](#)")
    st.markdown("📙 **GST Filing Guide** - [Download](#)")

# 🔹 AI Chatbot
elif section == "🤖 AI Chatbot":
    st.subheader("🤖 Ask TaxGo AI")
    
    openai.api_key = "your-api-key-here"  # Replace with your actual API key
    user_input = st.text_input("Ask your tax question:")
    
    if st.button("Get Answer"):
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": user_input}],
            temperature=0.2
        )
        st.markdown(f"**AI Response:** {response['choices'][0]['message']['content']}")

# 🔹 Family Tax Planner
elif section == "👨‍👩‍👧 Family Tax Planner":
    st.subheader("👨‍👩‍👧 Plan Taxes for Your Family")
    
    num_members = st.number_input("Number of Family Members", min_value=1, max_value=10, value=2)
    
    income_list = []
    deduction_list = []
    
    for i in range(num_members):
        st.markdown(f"### Member {i+1}")
        income = st.number_input(f"Income (₹) - Member {i+1}", value=500000)
        deduction = st.number_input(f"Deductions (₹) - Member {i+1}", value=50000)
        income_list.append(income)
        deduction_list.append(deduction)
    
    total_income = sum(income_list)
    total_deductions = sum(deduction_list)
    taxable_family_income = max(0, total_income - total_deductions)
    
    st.markdown(f"**Total Family Income:** ₹{total_income:,.2f}")
    st.markdown(f"**Total Deductions:** ₹{total_deductions:,.2f}")
    st.markdown(f"**Taxable Family Income:** ₹{taxable_family_income:,.2f}")

# Footer
st.markdown("---")
st.markdown("© 2025 TaxGo AI | Your Smart Tax Assistant 💰")
