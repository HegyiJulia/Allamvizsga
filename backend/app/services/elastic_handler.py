from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL

# Csatlakozás az Elasticsearch szerverhez
def get_elasticsearch_client():
    # Csatlakozás az Elasticsearch szerverhez
    es = Elasticsearch(["http://localhost:9200"])  # Adja meg a helyi Elasticsearch elérhetőséget
    if not es.ping():
        raise ValueError("Elasticsearch nem elérhető!")
    return es

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
