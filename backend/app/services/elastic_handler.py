from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL

# Csatlakozás az Elasticsearch szerverhez
def get_elasticsearch_client():
    # Csatlakozás az Elasticsearch szerverhez
    es = Elasticsearch(["http://localhost:9200"])  # Adja meg a helyi Elasticsearch elérhetőséget
    if not es.ping():
        raise ValueError("Elasticsearch nem elérhető!")
    return es

# Az index létrehozása, ha nem létezik
def create_index_if_not_exists():
    index_name = "senatus_resolutions"
    es = get_elasticsearch_client()
    if not es.indices.exists(index=index_name):
        # Az index létrehozása, ha nem létezik
        es.indices.create(index=index_name)
        #print(f"Index '{index_name}' sikeresen létrehozva.")
    #else:
        #print(f"Index '{index_name}' már létezik.")

# Indexelés PDF fájlokhoz
def index_pdf(file_path, content):
    # Ellenőrizzük, hogy létezik-e az index, ha nem, létrehozzuk
    create_index_if_not_exists()

    filename = os.path.basename(file_path)  # Csak a fájl neve
    doc_body = {"file_path": file_path, "filename": filename, "content": content}
    es.index(index="senatus_resolutions", document=doc_body)
    print(f"Dokumentum indexelve: {filename}")

# Keresési függvény
def search_documents(query: str):
    # Csatlakozás az Elasticsearch-hez
    es = get_elasticsearch_client()

    # Lekérdezés összeállítása
    response = es.search(
        index="senatus_resolutions",  # Használni kell az index nevét
        body={
            "query": {
                "match": {
                    "content": query
                }
            },
            "_source": ["filename"]  # Csak a filename mezőt kérjük vissza
        }
    )

    # A válaszban lévő találatok kigyűjtése
    filenames = [hit["_source"]["filename"] for hit in response["hits"]["hits"]]

    return filenames
