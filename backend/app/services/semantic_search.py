# services/semantic_search.py
from sentence_transformers import SentenceTransformer, util
from elasticsearch import Elasticsearch
import numpy as np
from app.services.elastic_handler import get_elasticsearch_client

model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
es = get_elasticsearch_client()
INDEX_DECISIONS = "senatus_decisions"

def search_semantic(query: str, top_k: int = 5):
    query_embedding = model.encode(query)

    # Lekérjük a dokumentumokat
    results = es.search(index=INDEX_DECISIONS, query={"match_all": {}}, size=1000)

    docs = []
    embeddings = []
    for hit in results['hits']['hits']:
        doc_id = hit['_id']
        content = hit['_source'].get('content', '')
        if content:
            embedding = model.encode(content)
            docs.append({
                "id": doc_id,
                "content": content,
                "score": 0.0
            })
            embeddings.append(embedding)

    # Cosine similarity
    cos_scores = util.cos_sim(query_embedding, embeddings)[0]
    top_indices = np.argsort(-cos_scores)[:top_k]

    for i in range(top_k):
        docs[top_indices[i]]["score"] = float(cos_scores[top_indices[i]])

    return [docs[i] for i in top_indices]
