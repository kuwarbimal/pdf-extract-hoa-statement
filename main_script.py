import os
import pandas as pd
from process_pdf import process_pdf

# Main script to process all PDF files in the HOA folder
HOA_folder = r'C:\Users\bkunwor\OneDrive - RPCC\Desktop\Bimal\HOA-PDF'  # Replace with your actual folder path

details_folder = os.path.join(HOA_folder, 'details')
summary_folder = os.path.join(HOA_folder, 'summary')

# Create folders if they don't exist
os.makedirs(details_folder, exist_ok=True)
os.makedirs(summary_folder, exist_ok=True)

# Process each PDF file
for filename in os.listdir(HOA_folder):
    if filename.endswith('.pdf'):
        pdf_path = os.path.join(HOA_folder, filename)
        
        try:
            df, tf, extract_date = process_pdf(pdf_path)
            
            # Format the output filenames
            extract_month = extract_date.strftime("%m")
            extract_year = extract_date.strftime("%Y")
            df_filename = f"details_{extract_month}_{extract_year}.csv"
            tf_filename = f"summary_{extract_month}_{extract_year}.csv"
            
            # Save df and tf as CSV files without index
            df.to_csv(os.path.join(details_folder, df_filename), index=False)
            tf.to_csv(os.path.join(summary_folder, tf_filename), index=False)
            
            print(f"Processed {filename} successfully.")
        
        except Exception as e:
            print(f"Error processing {filename}: {e}")
