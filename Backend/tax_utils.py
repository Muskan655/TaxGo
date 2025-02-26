import re
import PyPDF2
import openai
import pandas as pd
import tempfile
import os
import pytesseract
from PIL import Image
from pdf2image import convert_from_path
import cv2
import fitz
from datetime import datetime
from Data.categories import CATEGORY_KEYWORDS

# Function to extract text from image receipts
def extract_text_from_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)
    return text

# Function to extract text from PDF receipts
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)
    for page in doc:
        text += page.get_text()
    return text

# Function to extract date from text
def extract_date(text):
    date_patterns = [
        r'\b(\d{1,2}[-/.]\d{1,2}[-/.]\d{2,4})\b',  
        r'\b(\d{4}[-/.]\d{1,2}[-/.]\d{1,2})\b',  
        r'\b([A-Za-z]{3,9}\s\d{1,2},\s\d{4})\b', 
        r'\b(\d{1,2}\s[A-Za-z]{3,9}\s\d{4})\b' 
    ]
    for pattern in date_patterns:
        dates = re.findall(pattern, text)
        if dates:
            date_str = dates[0]
            try:
                
                for fmt in ["%d/%m/%Y", "%d-%m-%Y", "%d.%m.%Y", "%Y/%m/%d", "%Y-%m-%d", "%Y.%m.%d", "%B %d, %Y", "%d %B %Y"]:
                    try:
                        return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
                    except ValueError:
                        pass
                return date_str 
            except ValueError:
                pass
    return "Unknown"

# Function to extract amount from text
def extract_amount(text):
    amount_patterns = [
        r'₹\s?([\d,]+\.\d{2})',  
        r'\$\s?([\d,]+\.\d{2})',  
        r'([\d,]+\.\d{2})\s?₹',  
        r'([\d,]+\.\d{2})\s?\$',  
        r'([\d,]+\.\d{2})' 
    ]
    for pattern in amount_patterns:
        amounts = re.findall(pattern, text)
        if amounts:
            amount = amounts[-1].replace(",","") 
            try:
                float(amount) 
                return amounts[-1]
            except:
                pass
    return "Unknown"

# Function to categorize expense based on keywords
def categorize_expense(text):
    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword.lower() in text.lower() for keyword in keywords):
            return category
    return "Other"

# Function to process receipts (Image/PDF) and return a DataFrame
def process_receipt(file_path):
    try:
        if file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
            text = extract_text_from_image(file_path)
        else:
            text = extract_text_from_pdf(file_path)

        date = extract_date(text)
        amount = extract_amount(text)
        category = categorize_expense(text)

        df = pd.DataFrame([[date, category, amount]], columns=["Date", "Category", "Amount"])
        return df
    except Exception as e:
        return f"Error processing receipt: {e}"
def find_matching_tax_laws(expense_description, tax_laws_text, openai_api_key):
    """Uses OpenAI to find matching tax laws for an expense."""
    openai.api_key = openai_api_key
    prompt = f"Given the expense description: '{expense_description}', find relevant tax laws from the following text:\n\n{tax_laws_text}\n\nProvide the relevant tax law excerpts and a brief explanation of why they might apply."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error using OpenAI: {e}")
        return "Could not determine matching tax laws."

def is_expense_deductible(expense_description, tax_laws_text, openai_api_key):
    """Uses OpenAI to determine if an expense is deductible."""
    openai.api_key = openai_api_key
    prompt = f"Based on the expense description: '{expense_description}' and the following tax laws:\n\n{tax_laws_text}\n\ndetermine if the expense is deductible. Answer with only 'Yes' or 'No' and a short explanation."
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
        )
        answer = response['choices'][0]['message']['content']
        if "yes" in answer.lower():
            return True, answer
        else:
            return False, answer
    except Exception as e:
        print(f"Error using OpenAI: {e}")
        return False, "Could not determine deductibility."

def calculate_tax(income, deductions):
    """Calculates income tax based on income and deductions."""
    taxable_income = max(0, income - deductions)
    if taxable_income <= 250000:
        tax = 0
    elif taxable_income <= 500000:
        tax = (taxable_income - 250000) * 0.05
    elif taxable_income <= 1000000:
        tax = 12500 + (taxable_income - 500000) * 0.2
    else:
        tax = 112500 + (taxable_income - 1000000) * 0.3
    return tax