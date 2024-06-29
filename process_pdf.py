import re
import pdfplumber
import pandas as pd
from datetime import datetime

# Function to check if a string can be converted to float
def is_number(s):
    try:
        float(s.replace(',', ''))
        return True
    except ValueError:
        return False

# Function to process each PDF file and extract df and tf
def process_pdf(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text()

    # Extracting date range
    date_range_pattern = re.compile(r"Date Range:(\d{2}/\d{2}/\d{4}) to (\d{2}/\d{2}/\d{4})")
    date_match = date_range_pattern.search(text)
    
    if date_match:
        start_date_str = date_match.group(1)
        start_date = datetime.strptime(start_date_str, "%m/%d/%Y")
        first_of_month_date = start_date.replace(day=1)
    else:
        raise ValueError(f"Date Range not found in {pdf_path}")

    # Cleaning and structuring the text
    lines = text.split('\n')
    data = []
    datat = []
    current_account = None

    # Process lines for df
    for line in lines[:36]:
        parts = line.split()
        if len(parts) >= 5 and is_number(parts[-4]) and is_number(parts[-3]) and is_number(parts[-2]) and is_number(parts[-1]):
            account_name = " ".join(parts[:-4])
            period_value = float(parts[-4].replace(',', ''))
            period_percent = float(parts[-3])
            ytd_value = float(parts[-2].replace(',', ''))
            ytd_percent = float(parts[-1])
            data.append([account_name, period_value, period_percent, ytd_value, ytd_percent])
        elif len(parts) == 1:
            current_account = parts[0]
        elif len(parts) > 1:
            if current_account:
                account_name = current_account + " " + " ".join(parts[:-4])
                current_account = None
            else:
                account_name = " ".join(parts[:-4])
            if len(parts) >= 4 and is_number(parts[-4]) and is_number(parts[-3]) and is_number(parts[-2]) and is_number(parts[-1]):
                period_value = float(parts[-4].replace(',', ''))
                period_percent = float(parts[-3])
                ytd_value = float(parts[-2].replace(',', ''))
                ytd_percent = float(parts[-1])
                data.append([account_name, period_value, period_percent, ytd_value, ytd_percent])

    # Process lines for tf
    for line in lines[36:]:
        parts = line.split()
        if len(parts) >= 3 and is_number(parts[-2]) and is_number(parts[-1]):
            account_name = " ".join(parts[:-2])
            period_value = float(parts[-2].replace(',', ''))
            ytd_value = float(parts[-1].replace(',', ''))
            datat.append([account_name, period_value, ytd_value])

    # Creating DataFrames
    columns = ["Account Name", "Selected Period Value", "Selected Period %", "Fiscal Year To Date Value", "Fiscal Year To Date %"]
    df = pd.DataFrame(data, columns=columns)
    
    columnst = ["Account Name", "Selected Period Value", "Fiscal Year To Date Value"]
    tf = pd.DataFrame(datat, columns=columnst)

    # Adding the Extract Date column
    tf['Extract Date'] = first_of_month_date
    df['Extract Date'] = first_of_month_date

    return df, tf, first_of_month_date