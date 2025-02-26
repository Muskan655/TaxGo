import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import random
import os

def generate_mock_expenses_csv(num_rows=100):
    """Generates a mock expenses DataFrame for dashboard showcasing."""

    categories = [
        "Food", "Travel", "Grocery", "Entertainment", "Healthcare",
        "Household", "Clothing", "Transportation", "Personal Care",
        "Gifts & Donations", "Electronics", "Business Expenses",
        "Education", "Investment"
    ]

    data = []
    start_date = datetime.now() - timedelta(days=365)  # Start from a year ago

    for _ in range(num_rows):
        category = random.choice(categories)
        amount = round(random.uniform(10, 500), 2)  # Random amount between 10 and 500
        date = start_date + timedelta(days=random.randint(0, 365))  # Random date within the year
        date_str = date.strftime("%Y-%m-%d")

        data.append([date_str, category, amount])

    df = pd.DataFrame(data, columns=["Date", "Category", "Amount"])
    return df

def load_dataframe_from_csv(filename="processed_expenses.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return None

def run():
    st.subheader("📊 Expense Dashboard & Analysis")

    col1, col2 = st.columns(2)

    # --- Real Expenses ---
    with col1:
        st.subheader("Real Expenses")
        real_df = load_dataframe_from_csv()

        if real_df is not None and 'Category' in real_df.columns and 'Amount' in real_df.columns:
            real_category_totals = real_df.groupby('Category')['Amount'].sum().reset_index()
            real_category_totals = real_category_totals.sort_values(by='Amount', ascending=False)

            fig_real_bar = px.bar(real_category_totals, x='Category', y='Amount', title='Real Expenses by Category', color='Category')
            st.plotly_chart(fig_real_bar)

            if not real_category_totals.empty:
                top_real_category = real_category_totals.iloc[0]
                try:
                    amount_float = float(top_real_category['Amount'])
                    st.write(f"Top Real Expense: **{top_real_category['Category']}** (₹{amount_float:.2f})")
                except ValueError:
                    st.write(f"Top Real Expense: **{top_real_category['Category']}** (Amount: {top_real_category['Amount']})")
        else:
            st.write("No real expense data available.")

    # --- Mock Expenses ---
    with col2:
        st.subheader("Mock Expenses")
        mock_df = generate_mock_expenses_csv()

        if mock_df is not None and 'Category' in mock_df.columns and 'Amount' in mock_df.columns and 'Date' in mock_df.columns:
            mock_category_totals = mock_df.groupby('Category')['Amount'].sum().reset_index()
            mock_category_totals = mock_category_totals.sort_values(by='Amount', ascending=False)

            fig_mock_bar = px.bar(mock_category_totals, x='Category', y='Amount', title='Mock Expenses by Category', color='Category')
            st.plotly_chart(fig_mock_bar)

            if not mock_category_totals.empty:
                top_mock_category = mock_category_totals.iloc[0]
                try:
                    amount_float = float(top_mock_category['Amount'])
                    st.write(f"Top Mock Expense: **{top_mock_category['Category']}** (₹{amount_float:.2f})")
                except ValueError:
                    st.write(f"Top Mock Expense: **{top_mock_category['Category']}** (Amount: {top_mock_category['Amount']})")

            # Monthly Expense Analysis (Mock Data)
            st.subheader("Monthly Mock Expenses")
            mock_df['Date'] = pd.to_datetime(mock_df['Date'])
            monthly_expenses = mock_df.resample('M', on='Date')['Amount'].sum().reset_index()
            monthly_expenses['Month'] = monthly_expenses['Date'].dt.strftime('%Y-%m')

            fig_monthly = px.line(monthly_expenses, x='Month', y='Amount', title='Monthly Mock Expenses')
            st.plotly_chart(fig_monthly)

        else:
            st.write("Mock expense data could not be generated.")

    # --- Recommendations ---
    st.subheader("Expense Analysis & Recommendations")

    if real_df is not None and 'Category' in real_df.columns and 'Amount' in real_df.columns:
        real_category_totals = real_df.groupby('Category')['Amount'].sum().reset_index()
        real_category_totals = real_category_totals.sort_values(by='Amount', ascending=False)

        if not real_category_totals.empty:
            top_real_category = real_category_totals.iloc[0]
            st.write(f"Based on your real expenses, your highest category is **{top_real_category['Category']}**.")
            st.write("Here are some recommendations:")

            if top_real_category['Category'] == "Food":
                st.write("- Consider cooking more meals at home to reduce restaurant expenses.")
                st.write("- Plan your grocery shopping to avoid impulse purchases.")
            elif top_real_category['Category'] == "Travel":
                st.write("- Look for travel deals and discounts.")
                st.write("- Plan trips in advance to avoid last-minute expenses.")
            elif top_real_category['Category'] == "Entertainment":
                st.write("- Explore free or low-cost entertainment options.")
                st.write("- Limit subscriptions and memberships.")
            elif top_real_category['Category'] == "Business Expenses":
                st.write("- Review your business expenses regularly and cut unnecessary costs.")
                st.write("- Negotiate better deals with suppliers and service providers.")
            else:
                st.write("- Review your spending in this category and identify areas for potential savings.")
    else:
        st.write("No real expense data to provide recommendations.")