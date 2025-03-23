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

def extract_snippet(content: str, query: str, snippet_length: int = 300):
    """
    Ha van highlight, azt használja. Ha nincs, akkor a query első előfordulásától ad egy snippetet.
    """
    query_lower = query.lower()
    content_lower = content.lower()

    index = content_lower.find(query_lower)
    if index == -1:
        # Ha a keresett szó nincs benne, akkor az első 300 karaktert adja vissza
        return content[:snippet_length]
    
    # Ha a keresett szó megtalálható, akkor előtte és utána is adunk szöveget
    start = max(0, index - snippet_length // 2)
    end = min(len(content), index + snippet_length // 2)

    return content[start:end] + "..."


def semantic_search_documents(query: str):
    es = get_elasticsearch_client()

    query_body = {
        "query": {
            "more_like_this": {
                "fields": ["content"],
                "like": query,
                "min_term_freq": 1,
                "max_query_terms": 20
            }
        }
    }

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

        
        snippet = hit.get("highlight", {}).get("content", [])
        if snippet:
            snippet = " ... ".join(snippet)  
        else:
            snippet = extract_snippet(content, query)   


        results.append({
            "filename": filename,
            "snippet": snippet,
            "content": content
        })

    return results

