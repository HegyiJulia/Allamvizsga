# services/semantic_search.py
from sentence_transformers import SentenceTransformer
from elasticsearch import Elasticsearch
import numpy as np
from app.services.elastic_handler import get_elasticsearch_client


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

es = get_elasticsearch_client()
INDEX_DECISIONS = "senatus_decisions"

def search_semantic(query: str, top_k: int = 5):
    query_embedding = model.encode(query).tolist()

    body = {
        "size": top_k,
        "knn": {
            "field": "embedding",
            "query_vector": query_embedding,
            "k": top_k,
            "num_candidates": 100  
        }
    }


    res = es.search(index=INDEX_DECISIONS, body=body)

    results = []
    for hit in res['hits']['hits']:
        source = hit['_source']
        score = hit['_score']  
        results.append({
            "id": hit['_id'],
            "content": source['content'],
            "decision_number": source.get('decision_number', ''),
            "score": score,
            "filename": source.get('filename', ''),
            "date": source.get('date', '')
        })



    return results
