import os
import zipfile
import shutil
import re
import logging

# Settings
downloaded_files_dir = 'downloaded_files/zip_files'  # Directory containing ZIP files
DOWNLOAD_FOLDER = 'downloaded_files'  # Main directory for downloaded files
PDF_FOLDER = os.path.join(DOWNLOAD_FOLDER, 'pdf_files')  # Directory for PDF files
temp_dir = 'temp_files'  # Temporary directory for file storage

# Create directories if they don't exist
os.makedirs(PDF_FOLDER, exist_ok=True)
os.makedirs(temp_dir, exist_ok=True)

# Set up logging to only show errors
logging.basicConfig(level=logging.ERROR)

def is_pdf_valid(pdf_path):
    """Check if the PDF file can be opened."""
    try:
        with open(pdf_path, 'rb') as f:
            # Check the first few bytes for a valid PDF header
            header = f.read(4)
            return header == b'%PDF'
    except Exception:
        return False

# Set to keep track of already logged invalid PDFs
logged_invalid_pdfs = set()

# Process each ZIP file in the specified directory
for zip_filename in os.listdir(downloaded_files_dir):
    if zip_filename.endswith('.zip'):
        zip_file_path = os.path.join(downloaded_files_dir, zip_filename)

        try:
            with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                has_valid_pdf = False
                
                for file_info in zip_file.infolist():
                    if file_info.filename.endswith('.pdf'):
                        if re.search(r'hatarozatok[ _\d]*\.pdf$', file_info.filename.lower()):
                            zip_file.extract(file_info.filename, temp_dir)
                            has_valid_pdf = True

                if has_valid_pdf:
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            source_path = os.path.join(root, file)
                            # Check if the extracted PDF is valid
                            if is_pdf_valid(source_path):
                                destination_path = os.path.join(PDF_FOLDER, file)
                                
                                # Move the file
                                shutil.move(source_path, destination_path)
                            else:
                                # Only log once for each invalid PDF
                                if source_path not in logged_invalid_pdfs:
                                    logging.error(f"Skipped invalid PDF: {source_path}")
                                    logged_invalid_pdfs.add(source_path)  # Mark as logged

        except zipfile.BadZipFile:
            logging.error(f"A ZIP fajl serult: {zip_file_path}")
            continue  # Skip processing for corrupted ZIP files
        except Exception as e:
            logging.error(f"Hiba történt a(z) {zip_filename} fájl feldolgozása közben: {e}")
            continue  # Skip the current ZIP file if an error occurs

# Delete temporary directory if it contains files
if os.path.exists(temp_dir) and os.listdir(temp_dir):
    shutil.rmtree(temp_dir)

print(f'A PDF fajlok a "{PDF_FOLDER}" mappaba kerultek.')
