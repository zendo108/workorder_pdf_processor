# OCR and PDF Automation Project

This project automates the conversion of PCL files to searchable PDFs, extracts key information from the PDFs, and renames them based on the extracted data. It combines several tools and libraries to achieve the functionality.

## Prerequisites

To run this project, you need the following:

### Programs

1. **Python**
   - Version: Python 3.12 or later.
   - [Download Python](https://www.python.org/downloads/)
   - Make sure to check the option to add Python to your system PATH during installation.

2. **GhostPCL**
   - Required to convert PCL files to PDFs.
   - [Download GhostPCL](https://ghostscript.com/releases/gpcldnld.html)
   - Install GhostPCL and add its `bin` directory to your system PATH.

3. **Tesseract OCR**
   - Required to perform OCR on image-based PDFs.
   - [Download Tesseract](https://github.com/tesseract-ocr/tesseract)
   - Install Tesseract and add its `bin` directory to your system PATH.
   - Verify installation by running: `tesseract -v`

4. **Poppler for Windows**
   - Required for rasterizing PDFs into images.
   - [Download Poppler](https://github.com/oschwartz10612/poppler-windows/releases)
   - Extract the downloaded zip file to a folder (e.g., `C:\Poppler`).
   - Add the `bin` directory of the extracted folder to your system PATH.

### Python Packages

Install the required Python libraries using `pip`. Run the following command:

```bash
pip install pdf2image PyPDF2 pillow
```

## Setup Instructions

1. Clone or download the project to your local machine.
2. Ensure all prerequisites are installed and properly configured.
3. Update the following paths in the script:
   - `pcl_directory`: The folder containing PCL files.
   - `output_directory`: The folder where output PDFs will be saved.
4. Customize the `electricians` list in the script to include relevant names for filtering.

## How to Run

1. Open a terminal or command prompt.
2. Navigate to the folder containing the project.
3. Run the script:

```bash
python ocr_pdf_automation.py
```

The script will:
- Convert PCL files to image-based PDFs using GhostPCL.
- Rasterize the PDFs into images.
- Perform OCR on the images using Tesseract to create searchable PDFs.
- Extract key fields (e.g., Work Order number, description, electrician's name) from the text.
- Rename the PDFs based on the extracted fields.

## Troubleshooting

1. **Tesseract or Poppler Not Found**:
   - Ensure their `bin` directories are added to your system PATH.
   - Restart your terminal after updating PATH.

2. **OCR Accuracy Issues**:
   - Increase DPI in the `rasterize_pdf_to_images` function (default is 400).
   - Experiment with Tesseract's Page Segmentation Modes (`--psm` argument).

3. **Missing Electrician Names**:
   - Verify the `electricians` list matches the names extracted from the PDFs.
   - Normalize names (e.g., strip whitespace, lowercase) for better matching.

## Example Output

- Input: `503367364.pcl`
- Output: `503367364_Replace_temperature_probe_NoElectrician.pdf`

---

Feel free to modify the script and README file as per your requirements.
