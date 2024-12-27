import os
import subprocess
from pdf2image import convert_from_path
from PyPDF2 import PdfWriter, PdfReader
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

def rasterize_pdf_to_images(image_pdf_path, output_folder):
    """Rasterize PDF to individual images using pdf2image."""
    try:
        images = convert_from_path(image_pdf_path, dpi=400)
        image_paths = []
        for idx, image in enumerate(images):
            image_path = os.path.join(output_folder, f"page_{idx+1}.png")
            image.save(image_path, "PNG")
            image_paths.append(image_path)
        print(f"Rasterized PDF to images: {image_paths}")
        return image_paths
    except Exception as e:
        print(f"Failed to rasterize PDF {image_pdf_path}: {e}")
        return []

def merge_pdfs(pdf_files, output_pdf_path):
    """Merge multiple PDFs into a single PDF."""
    writer = PdfWriter()
    for pdf_file in pdf_files:
        reader = PdfReader(pdf_file)
        for page in reader.pages:
            writer.add_page(page)
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
    print(f"Merged PDF saved to: {output_pdf_path}")

def perform_ocr_on_images(image_paths, output_pdf_path):
    """Perform OCR on rasterized images and combine results into a searchable PDF."""
    temp_pdf_files = []
    try:
        for image_path in image_paths:
            temp_output_path = os.path.splitext(image_path)[0] + ".pdf"  # Output PDF for each image
            command = [
                "tesseract",
                image_path,
                temp_output_path.replace(".pdf", ""),  # Remove .pdf as Tesseract appends it
                "-l", "eng", "--psm", "6", "pdf"
            ]
            print("Running Tesseract Command:", " ".join(command))  # Debugging
            subprocess.run(command, check=True)
            temp_pdf_files.append(temp_output_path)
        print(f"Generated individual PDFs: {temp_pdf_files}")

        # Merge individual PDFs into one
        merge_pdfs(temp_pdf_files, output_pdf_path)
    except subprocess.CalledProcessError as e:
        print(f"Failed to perform OCR on images: {e}")
    finally:
        # Optionally, clean up temporary files
        for temp_pdf in temp_pdf_files:
            if os.path.exists(temp_pdf):
                os.remove(temp_pdf)
    return output_pdf_path

def extract_fields(ocr_text):
    """Extract relevant fields from OCR text."""
    work_order_match = re.search(r"Work Order\s*(\d{1,9})", ocr_text)
    description_match = re.search(r"Work Order\d+\s+([\w\s]+)", ocr_text)
    assigned_to_match = re.findall(r"Assigned To\s*([\w\s]+)", ocr_text, re.IGNORECASE)
    
    work_order = work_order_match.group(1) if work_order_match else None
    description = description_match.group(1).strip() if description_match else None
    assigned_to = assigned_to_match if assigned_to_match else []
    return work_order, description, assigned_to

def sanitize_filename(filename):
    """Remove invalid characters from filenames."""
    return re.sub(r'[\/:*?"<>|\\\n\r]', '_', filename)

def process_pcl_file(pcl_path, output_dir, electricians):
    """Full pipeline: PCL -> Image PDF -> OCR PDF -> Rename."""
    base_name = os.path.splitext(os.path.basename(pcl_path))[0]
    image_pdf_path = os.path.join(output_dir, f"{base_name}_image.pdf")
    ocr_pdf_path = os.path.join(output_dir, f"{base_name}_ocr.pdf")
    rasterized_images_folder = os.path.join(output_dir, "rasterized_images")
    os.makedirs(rasterized_images_folder, exist_ok=True)

    # Step 1: Convert PCL to Image-Based PDF
    convert_pcl_to_pdf(pcl_path, image_pdf_path)

    # Step 2: Rasterize PDF to Images
    image_paths = rasterize_pdf_to_images(image_pdf_path, rasterized_images_folder)
    if not image_paths:
        print(f"Skipping file {pcl_path} due to rasterization failure.")
        return

    # Step 3: Perform OCR on Images and Merge into a Single PDF
    perform_ocr_on_images(image_paths, ocr_pdf_path)

    # Step 4: Extract text for renaming
    reader = PdfReader(ocr_pdf_path)
    ocr_text = "\n".join(page.extract_text() for page in reader.pages)
    print("OCR Text Extracted:\n", ocr_text)  # Debugging
    work_order, description, assigned_to = extract_fields(ocr_text)
    electrician_name = next((name for name in assigned_to if name in electricians), "NoElectrician")

    # Step 5: Rename the OCR PDF
    work_order = sanitize_filename(work_order or "Unknown")
    description = sanitize_filename(description or "Untitled")
    electrician_name = sanitize_filename(electrician_name or "NoElectrician")
    new_filename = f"{work_order}_{description}_{electrician_name}.pdf"
    new_pdf_path = os.path.join(output_dir, new_filename)

    os.rename(ocr_pdf_path, new_pdf_path)
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
