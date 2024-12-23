import os
import subprocess
from pdf2image import convert_from_path
from pytesseract import image_to_string
from PyPDF2 import PdfWriter
import re

def convert_pcl_to_pdf(pcl_path, pdf_path):
    """Convert PCL to PDF using GhostPCL."""
    command = [
        "gpcl6win64",  # Replace with the correct GhostPCL executable
        "-dNOPAUSE",
        "-sDEVICE=pdfwrite",
        f"-sOutputFile={pdf_path}",
        pcl_path
    ]
    try:
        subprocess.run(command, check=True)
        print(f"Converted {pcl_path} to {pdf_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to convert {pcl_path}: {e}")

def perform_ocr_on_pdf(image_pdf_path):
    """Extract text from an image-based PDF using OCR."""
    images = convert_from_path(image_pdf_path)
    text = ""
    for image in images:
        text += image_to_string(image)
    return text

def save_text_as_pdf(text, output_pdf_path):
    """Save extracted text as a searchable PDF."""
    writer = PdfWriter()
    writer.add_blank_page(width=72 * 8.5, height=72 * 11)  # Standard A4 size
    writer.add_metadata({'/Title': 'Converted Text PDF'})
    with open(output_pdf_path, 'wb') as f:
        writer.write(f)
    print(f"Text saved as PDF: {output_pdf_path}")

def extract_fields(text):
    """Extract relevant fields from OCR text."""
    work_order_match = re.search(r"Work Order\s*(\d{1,9})", text)
    description_match = re.search(r"Work Order\d+\s+([\w\s]+)", text)
    assigned_to_match = re.findall(r"Assigned To\s*([\w\s]+)", text)
    work_order = work_order_match.group(1) if work_order_match else None
    description = description_match.group(1).strip() if description_match else None
    assigned_to = assigned_to_match if assigned_to_match else []
    return work_order, description, assigned_to

def process_pcl_file(pcl_path, output_dir, electricians):
    """Full pipeline: PCL -> Image PDF -> OCR -> Text PDF -> Rename."""
    base_name = os.path.splitext(os.path.basename(pcl_path))[0]
    image_pdf_path = os.path.join(output_dir, f"{base_name}_image.pdf")
    text_pdf_path = os.path.join(output_dir, f"{base_name}_text.pdf")

    # Step 1: Convert PCL to Image-Based PDF
    convert_pcl_to_pdf(pcl_path, image_pdf_path)

    # Step 2: Perform OCR and extract text
    ocr_text = perform_ocr_on_pdf(image_pdf_path)

    # Step 3: Save Text as a Searchable PDF
    save_text_as_pdf(ocr_text, text_pdf_path)

    # Step 4: Extract fields and rename
    work_order, description, assigned_to = extract_fields(ocr_text)
    electrician_name = next((name for name in assigned_to if name in electricians), "NoElectrician")
    new_filename = f"{work_order or 'Unknown'}_{description or 'Untitled'}_{electrician_name}.pdf".replace(" ", "_")
    new_pdf_path = os.path.join(output_dir, new_filename)
    os.rename(text_pdf_path, new_pdf_path)
    print(f"Final renamed PDF: {new_pdf_path}")

# Directory and electrician list configuration
pcl_directory = "path_to_pcl_folder"  # Replace with your folder containing PCL files
output_directory = "path_to_output_folder"  # Replace with your output folder
os.makedirs(output_directory, exist_ok=True)

electricians = ["David Morancie", "David Buonassisi"]

# Process each PCL file
for pcl_file in os.listdir(pcl_directory):
    if pcl_file.endswith(".pcl"):
        process_pcl_file(os.path.join(pcl_directory, pcl_file), output_directory, electricians)
