from PyPDF2 import PdfReader
import os
import re

def extract_work_order_and_rename(pdf_path):
    reader = PdfReader(pdf_path)
    work_order_number = None

    for page in reader.pages:
        text = page.extract_text()

        # Extract Work Order number using regex
        work_order_match = re.search(r"Work Order(\d{1,9})", text)
        if work_order_match:
            work_order_number = work_order_match.group(1)
            break  # Stop after finding the first match

    # Rename file if Work Order number is found
    if work_order_number:
        directory, filename = os.path.split(pdf_path)
        new_filename = f"{work_order_number}.pdf"
        new_path = os.path.join(directory, new_filename)
        os.rename(pdf_path, new_path)
        print(f"Renamed to: {new_filename}")
    else:
        print(f"No Work Order found in: {pdf_path}")

# Process all PDFs in the specified directory
def process_pdfs_in_directory(directory):
    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            extract_work_order_and_rename(pdf_path)

# Specify the absolute path to the folder containing the PDFs
pdf_directory = r"D:\path_to\PDF-12212024"  # Replace with your full folder path
process_pdfs_in_directory(pdf_directory)
