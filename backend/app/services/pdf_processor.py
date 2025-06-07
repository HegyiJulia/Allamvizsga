import os
import fitz  # PyMuPDF
from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL
import re
import requests
from sentence_transformers import SentenceTransformer, util
#from PyPDF2 import PdfReader
import json
import datetime

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

def normalize_date(date_str):
    try:
        dt = datetime.datetime.strptime(date_str.strip(), "%Y. %B %d.")
        return dt.strftime("%Y-%m-%d")
    except Exception:
        return date_str  # fallback, ha nem ismeri fel


# Csatlakozás az Elasticsearch szerverhez
# Elasticsearch csatlakozás
def get_elasticsearch_client():
    es_host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")  # Elasticsearch neve a docker-compose.yml-ben
    es_url = f"http://{es_host}:9200"
    
    # es_url = f"http://elasticsearch:9200"
    try:
        es = Elasticsearch([es_url], )
        print(es.ping(), es.info())
        response = requests.get(es_url, timeout=5)
        if response.status_code == 200:
            print(f"✅ OK: {es_url} elérhető.")
            return es
        else:
            print(f"⚠️ Válaszkód: {response.status_code} a {es_url}-ről.")
            return False
    except requests.RequestException as e:
        print(f"❌ Hiba történt: {e}")
        return False
    es = Elasticsearch([es_url])
    print(f"Elasticsearch URL: {es_url}") 
    try:
        if not es.ping():
            raise ValueError("Elasticsearch nem elérhető!")
    except Exception as e:
        print(f"Elasticsearch hiba: {e}")
        raise ValueError("Elasticsearch nem elérhető!")
    return es


# Csatlakozás Elasticsearch-hez
es = get_elasticsearch_client()
print(es)
#Index neve
INDEX_NAME = "senatus_resolutions"
INDEX_DECISIONS = "senatus_decisions"

# Index létrehozása, ha nem létezik
def create_index_if_not_exists():
    if not es.indices.exists(index=INDEX_NAME):
        print("create index")
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
                date = extract_date(content)
                # Elasticsearch dokumentum létrehozása
                doc_body = {
                    "filename": filename,
                    "content": content,
                    "date": date
                }
                
                # Határozatok keresése és indexelése
                res = es.index(index=INDEX_NAME, document=doc_body)
                
                process_and_index_decisions(content, filename, date)
                # JSON mentés
                json_output_dir = os.path.join("downloaded_files", "json_outputs")
                os.makedirs(json_output_dir, exist_ok=True)

                senate_data = extract_senate_data(pdf_path)
                json_filename = os.path.splitext(filename)[0] + ".json"
                json_output_path = os.path.join(json_output_dir, json_filename)

                with open(json_output_path, "w", encoding="utf-8") as f:
                    json.dump(senate_data, f, indent=2, ensure_ascii=False)

               
                print(f"Indexelt dokumentum: {filename}, ID: {res['_id']}")
            except Exception as e:
                print(f"Hiba történt a PDF feldolgozása során: {filename}, Hiba: {e}")
    
    print("Minden PDF dokumentum sikeresen feldolgozva és indexelve!")


# Dátum kinyerése a szövegből
def extract_date(text: str):
    date_match = re.search(r"Ikt\. sz\. \d+/([\d]{4}\.\d{2}\.\d{2})", text)
    return date_match.group(1) if date_match else "Ismeretlen dátum"

# Határozatok kinyerése és indexelése
def process_and_index_decisions(text: str, filename: str, date: str):
    pattern = re.compile(r"(\d{3,4})\. határozat\s*(.*?)(?=\n\d{3,4}\. határozat|\Z)", re.DOTALL)
    matches = pattern.findall(text)

    for match in matches:
        decision_number = match[0]
        decision_text = match[1].strip()

        # embedding kiszámítása
        embedding = model.encode(decision_text).tolist()  # numpy array -> list kell az ES-nek

        doc_body = {
            "decision_number": decision_number,
            "content": decision_text,
            "filename": filename,
            "date": date,
            "embedding": embedding
        }
        es.index(index=INDEX_DECISIONS, document=doc_body)
        print(f"Határozat indexelve: {decision_number}")


#pdf-> json

# def extract_senate_data(pdf_path):
#     reader = PdfReader(pdf_path)
#     text = "\n".join(page.extract_text() for page in reader.pages if page.extract_text())

#     title_match = re.search(r"A Szenátus .*?ülésének határozatai", text)
#     date_match = re.search(r"\d{4}\. szeptember \d{2}\.", text)
#     president_match = re.search(r"Dr\. .+?egyetemi tanár", text)
#     secretary_match = re.search(r"Hauer Melinda", text)

#     decision_matches = re.findall(r"(\d{4})\.? határozat\s+(.*?)(?=\n\d{4}\.|Dr\.|$)", text, re.DOTALL)

#     decisions = []
#     for number, content in decision_matches:
#         decisions.append({
#             "number": int(number),
#             "content": " ".join(content.strip().split())
#         })

#     return {
#         "session_title": title_match.group(0) if title_match else None,
#         "date": normalize_date(date_match.group(0)) if date_match else None,
#         "decisions": decisions,
#         "senate_president": president_match.group(0) if president_match else None,
#         "secretary_general": secretary_match.group(0) if secretary_match else None
#     }
