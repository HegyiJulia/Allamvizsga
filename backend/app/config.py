import os
from dotenv import load_dotenv

load_dotenv()

ELASTICSEARCH_URL = os.getenv("ELASTICSEARCH_URL", "http://elasticsearch:9200")
PDF_DIRECTORY = os.getenv("PDF_DIRECTORY", "downloaded_files/pdf_files")
