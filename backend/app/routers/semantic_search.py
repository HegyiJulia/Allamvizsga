from fastapi import APIRouter, HTTPException

from app.models.semantic_search_documents import SemanticSearchRequest
from app.services.elastic_handler import semantic_search_documents

router = APIRouter()
@router.post("/")
def semantic_search_endpoint(request: SemanticSearchRequest):
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="A keresési lekérdezés nem lehet üres!")

        results = semantic_search_documents(request.query)

        return {"results": results}

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Szerverhiba: {str(e)}")
