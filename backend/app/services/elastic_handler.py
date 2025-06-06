from datetime import datetime
from typing import Optional, List
from elasticsearch import Elasticsearch
from app.config import ELASTICSEARCH_URL
import requests
import os
# Csatlakozás az Elasticsearch szerverhez
def get_elasticsearch_client():
    es_host = os.getenv("ELASTICSEARCH_HOST", "elasticsearch")  # Elasticsearch neve a docker-compose.yml-ben
    es_url = f"http://{es_host}:9200"
    
    # es_url = f"http://elasticsearch:9200"
    try:
        es = Elasticsearch([es_url])
        # print(es.ping(), es.info())
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

def validate_date(date_str: str) -> Optional[str]:
    try:
        # Ellenőrizzük, hogy a dátum formátuma helyes-e (yyyy.MM)
        datetime.strptime(date_str, "%Y.%m")
        return date_str
    except ValueError:
        return None
# Keresési függvény

def search_documents(query: str, mode: str, start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[dict]:
    # Létrehozzuk az Elasticsearch query-t
    must_clauses = []

    # Ha van keresési kifejezés
    if query:
        if mode == "phrase":
            must_clauses.append({"match_phrase": {"content": query}})
        else:
            must_clauses.append({"match": {"content": query}})

    if start_date:
        valid_start_date = validate_date(start_date)
        if not valid_start_date:
            raise ValueError(f"Hibás kezdő dátum formátum: {start_date}. A helyes formátum: yyyy.MM")
        start_date = valid_start_date
    
    if end_date:
        valid_end_date = validate_date(end_date)
        if not valid_end_date:
            raise ValueError(f"Hibás végső dátum formátum: {end_date}. A helyes formátum: yyyy.MM")
        end_date = valid_end_date

    # Dátum szűrés hozzáadása, ha megadjuk a dátumokat
    if start_date and end_date:
        must_clauses.append({
            "range": {
                "date": {
                    "gte": start_date,
                    "lte": end_date
                }
            }
        })
    
    # Elasticsearch lekérdezés
    search_query = {
        "query": {
            "bool": {
                "must": must_clauses
            }
        },
        "highlight": {
            "fields": {
                "content": {}
            }
        }
    }

    es = get_elasticsearch_client()
    response = es.search(index="senatus_resolutions", body=search_query)

    results = []
    for hit in response["hits"]["hits"]:
        source = hit["_source"]
        highlight = hit.get("highlight", {}).get("content", [source["content"][:300]])[0]
        results.append({
            "filename": source.get("filename"),
            "snippet": highlight,
            "content": source.get("content")
        })

    return results

