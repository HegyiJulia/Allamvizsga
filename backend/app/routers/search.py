from fastapi import APIRouter, HTTPException
from app.services.elastic_handler import search_documents
from app.services.semantic_search import search_semantic
from app.models.search import SearchRequest, SearchResponse
from app.models.search import SemanticSearchRequest, SemanticSearchResponse
#from app.services.pdf_processor import  process_and_index_pdfs
router = APIRouter()



@router.post("/semantic-search", response_model=SemanticSearchResponse)
def semantic_search(query: SemanticSearchRequest):
    results = search_semantic(query.query, query.top_k)
    return {"results": results}

@router.post("/")
def search_endpoint(request: SearchRequest):
    try:
        if not request.query.strip():
            raise HTTPException(status_code=400, detail="A keresési lekérdezés nem lehet üres!")

        # Validáljuk a módot (word/phrase)
        mode = request.mode if request.mode in ["word", "phrase"] else "word"
        
        # A kereséshez hozzuk a dátum intervallumot is, ha van
        results = search_documents(request.query, mode, request.startDate, request.endDate)

        return {"results": results}  

    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Szerverhiba: {str(e)}")

