import streamlit as st
import pandas as pd
import tempfile
import os
import traceback
from Backend.tax_utils import process_receipt

def save_dataframe_to_csv(df, filename="processed_expenses.csv"):
    df.to_csv(filename, index=False)
    st.success(f"Data saved to {filename}")
    
    
def run(): 
    st.subheader("💳 Track Your Tax-Deductible Expenses")
    uploaded_files = st.file_uploader("Upload Expense Receipts (Images/PDFs)", type=["png", "jpg", "jpeg", "pdf"], accept_multiple_files=True)
    
    if uploaded_files:
        all_dfs = []
        errors = []
        for uploaded_file in uploaded_files:
            try:
                with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp_file:
                    temp_file.write(uploaded_file.read())
                    temp_file_path = temp_file.name

                result = process_receipt(temp_file_path)
                if isinstance(result, pd.DataFrame):
                    all_dfs.append(result)
                else:
                    errors.append(f"Error processing {uploaded_file.name}: {result}")
            except Exception as e:
                errors.append(f"Error processing {uploaded_file.name}: {e}\n{traceback.format_exc()}")
            finally:
                if 'temp_file_path' in locals():
                    os.unlink(temp_file_path)

        if all_dfs:
            combined_df = pd.concat(all_dfs, ignore_index=True)
            st.dataframe(combined_df)
            save_dataframe_to_csv(combined_df) #save the df.
            st.session_state.processed_df = combined_df
        if errors:
            for error in errors:
                st.error(error)

        if not all_dfs and not errors:
            st.error("No data could be extracted from any files.")