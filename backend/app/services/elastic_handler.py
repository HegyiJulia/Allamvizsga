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
    es = get_elasticsearch_client()

    response = es.search(
        index="senatus_resolutions",
        body={
            "query": {
                "match": {
                    "content": query
                }
            },
            "highlight": {
                "fields": {
                    "content": {
                        "fragment_size": 150,  # A visszaadott szövegrész hossza
                        "number_of_fragments": 1  # Csak az első találatot adja vissza
                    }
                }
            },
            "_source": ["filename", "content"]
        }
    )

    results = []
    for hit in response["hits"]["hits"]:
        filename = hit["_source"]["filename"]
        content = hit["_source"]["content"]

        # Ha van highlight, akkor azt használjuk, ha nincs, akkor az első 150 karaktert
        snippet = hit.get("highlight", {}).get("content", [content[:150]])[0]

        results.append({
            "filename": filename,
            "snippet": snippet,
            "content": content
        })

    return results

