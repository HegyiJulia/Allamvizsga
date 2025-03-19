import os
import fitz  # PyMuPDF
from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL


# Csatlakozás az Elasticsearch szerverhez
def get_elasticsearch_client():
    # Csatlakozás az Elasticsearch szerverhez
    es = Elasticsearch(["http://localhost:9200"])  # Adja meg a helyi Elasticsearch elérhetőséget
    if not es.ping():
        raise ValueError("Elasticsearch nem elérhető!")
    return es

# Csatlakozás Elasticsearch-hez
es = get_elasticsearch_client()

#Index neve
INDEX_NAME = "senatus_resolutions"


# Index létrehozása, ha nem létezik
def create_index_if_not_exists():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME)
        print(f"Index '{INDEX_NAME}' sikeresen létrehozva.")
    else:
        print(f"Index '{INDEX_NAME}' már létezik.")

# PDF-ek feldolgozása és Elasticsearch-be való feltöltése
def process_and_index_pdfs(pdf_directory: str):
    # Ellenőrizzük, hogy az index létezik-e
    create_index_if_not_exists()

    # PDF fájlok feldolgozása
    for filename in os.listdir(pdf_directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(pdf_directory, filename)
            print(f"Feldolgozás: {pdf_path}")

            try:
                # PDF tartalmának kinyerése
                doc = fitz.open(pdf_path)
                content = ""
                for page in doc:
                    content += page.get_text()

                # Elasticsearch dokumentum létrehozása
                doc_body = {
                    "filename": filename,
                    "content": content
                }
                res = es.index(index=INDEX_NAME, document=doc_body)
                print(f"Indexelt dokumentum: {filename}, ID: {res['_id']}")
            except Exception as e:
                print(f"Hiba történt a PDF feldolgozása során: {filename}, Hiba: {e}")
    
    print("Minden PDF dokumentum sikeresen feldolgozva és indexelve!")


