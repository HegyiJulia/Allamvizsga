import os
import fitz 
from elasticsearch import Elasticsearch

# Kapcsolódás az Elasticsearch szerverhez HTTP-n keresztül
es = Elasticsearch("http://localhost:9200")

# Ellenőrizd a kapcsolatot
if es.ping():
    print("Kapcsolódás sikeres!")
else:
    print("Kapcsolódás sikertelen!")

# PDF-ek mappájának elérési útja
pdf_directory = "C:/Allamvizsga/downloaded_files/pdf_files"

# Elasticsearch index neve
index_name = "senatus_határozatok"

# Index létrehozása (ha még nem létezik)
if not es.indices.exists(index=index_name):
    es.indices.create(index=index_name)

# PDF-ek beolvasása és feltöltése
for filename in os.listdir(pdf_directory):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(pdf_directory, filename)
        doc = fitz.open(pdf_path)
        
        # Szöveg beolvasása minden oldalról
        content = ""
        for page in doc:
            content += page.get_text()

        # Dokumentum bejegyzés Elasticsearch-be
        doc_body = {
            "filename": filename,
            "content": content
        }
        res = es.index(index=index_name, document=doc_body)
        print(f"Feltöltve: {filename}, ID: {res['_id']}")

print("Minden PDF dokumentum sikeresen indexelve!")


