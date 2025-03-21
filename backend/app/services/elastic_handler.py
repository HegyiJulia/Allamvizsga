from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL

# Csatlakozás az Elasticsearch szerverhez
def get_elasticsearch_client():
    # Csatlakozás az Elasticsearch szerverhez
    try:
        es = Elasticsearch(["http://localhost:9200"])
        if not es.ping():
            raise ValueError("Elasticsearch nem elérhető!")
        return es
    except ConnectionError:
        raise ValueError("Nem lehet csatlakozni az Elasticsearch-hoz. Ellenőrizd, hogy fut-e!")



# Keresési függvény
def search_documents(query: str, mode: str):
    es = get_elasticsearch_client()

    # Különböző keresési lekérdezések
    if mode == "phrase":
        query_body = {
            "query": {
                "match_phrase": {  # Pontos kifejezést keres
                    "content": query
                }
            }
        }
    elif mode == "word":
        query_body = {
            "query": {
                "match": {  # Szavas keresés
                    "content": query
                }
            }
        }
    else:
        raise ValueError("Érvénytelen keresési mód!")  # Hibakezelés

    # Elasticsearch keresés
    try:
        response = es.search(
            index="senatus_resolutions",
            body={
                **query_body,
                "highlight": {
                    "fields": {
                        "content": {
                            "fragment_size": 150,
                            "number_of_fragments": 1
                        }
                    }
                },
                "_source": ["filename", "content"]
            }
        )
    except Exception as e:
        raise ValueError(f"Hiba az Elasticsearch keresés során: {e}")
    
    results = []
    for hit in response["hits"]["hits"]:
        filename = hit["_source"]["filename"]
        content = hit["_source"]["content"]

        
        snippet = hit.get("highlight", {}).get("content", [content[:150]])[0]

        results.append({
            "filename": filename,
            "snippet": snippet,
            "content": content
        })

    return results

