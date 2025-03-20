from fastapi import APIRouter, HTTPException
from app.services.elastic_handler import search_documents
from app.models.search import SearchRequest, SearchResponse
#from app.services.pdf_processor import  process_and_index_pdfs
router = APIRouter()

@router.post("/")
def search_endpoint(request: SearchRequest):
    try:
        mode = request.mode if request.mode in ["word", "phrase"] else "word"
        
        results = search_documents(request.query, mode)
        return {"results": results}  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


