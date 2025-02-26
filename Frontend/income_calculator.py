import streamlit as st
import pandas as pd
import tempfile
import os
import traceback
from Backend.tax_utils import extract_text_from_pdf, find_matching_tax_laws, is_expense_deductible, calculate_tax
import openai

def load_dataframe_from_csv(filename="processed_expenses.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return None  
 
def load_mock_dataframe_from_csv(filename="mock_expenses.csv"):
    if os.path.exists(filename):
        return pd.read_csv(filename)
    return None

def run():
    st.subheader("🧮 Calculate Your Income Tax")
    tax_laws_pdf = st.file_uploader("Upload Tax Laws PDF", type=["pdf"])
    openai_api_key = st.text_input("Enter your OpenAI API Key", type="password")

    loaded_df = load_dataframe_from_csv()

    if loaded_df is not None and tax_laws_pdf and openai_api_key:
        df = loaded_df

        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(tax_laws_pdf.read())
            temp_file_path = temp_file.name

        tax_laws_text = extract_text_from_pdf(temp_file_path)

        if 'Category' in df.columns:
            df['Deductible'] = False
            df['Explanation'] = ''
            for index, row in df.iterrows():
                expense_description = str(row['Category'])

                
                prompt_matching_laws = f"""
                Given the expense category: '{expense_description}', find relevant tax laws from the following text:

                {tax_laws_text}

                Provide the relevant tax law excerpts and a brief explanation of why they might apply. If the provided tax laws do not contain information related to the expense, then answer with 'Could not determine matching tax laws'.
                """
                try:
                    matching_laws = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt_matching_laws}],
                        temperature=0.3,
                        api_key=openai_api_key,
                    )['choices'][0]['message']['content']
                except openai.error.OpenAIError as e:
                    matching_laws = f"Error finding matching laws: {e}"

                
                prompt_deductibility = f"""
                Given the expense category: '{expense_description}', and the following tax laws:

                {matching_laws}

                Determine if the expense is deductible. Provide a 'Yes' or 'No' answer, followed by a detailed explanation. If the provided tax laws do not contain information related to the expense, then answer with 'Could not determine deductibility'.
                """
                try:
                    deductibility_response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt_deductibility}],
                        temperature=0.3,
                        api_key=openai_api_key,
                    )['choices'][0]['message']['content']
                except openai.error.OpenAIError as e:
                    deductibility_response = f"Error determining deductibility: {e}"

                if "yes" in deductibility_response.lower():
                    deductible = True
                elif "no" in deductibility_response.lower():
                    deductible = False
                else:
                    deductible = False  # Default to False if undetermined

                df.loc[index, 'Deductible'] = deductible
                df.loc[index, 'Explanation'] = deductibility_response

            st.dataframe(df)

            if 'Amount' in df.columns and 'Deductible' in df.columns:
                deductible_expenses = df[df['Deductible'] == True]['Amount'].sum()
                st.write(f"Total Deductible Expenses: ₹{deductible_expenses:,.2f}")

                income = st.number_input("Enter your annual income:", value=500000)
                tax = calculate_tax(income, deductible_expenses)
                st.write(f"Calculated Tax: ₹{tax:,.2f}")
        else:
            st.error("The extracted data does not contain a 'Category' column.")
    elif loaded_df is None:
        st.write("Please upload your expense receipts in the 'Expense Bucket' section first.")