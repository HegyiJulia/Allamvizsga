from fastapi import APIRouter, HTTPException
from app.services.elastic_handler import search_documents
from app.models.search import SearchRequest, SearchResponse
#from app.services.pdf_processor import  process_and_index_pdfs
router = APIRouter()

@router.post("/")
def search_endpoint(request: SearchRequest):
    try:
        results = search_documents(request.query)
        return SearchResponse(results=results)  # A válasz csak a fájlneveket tartalmazza
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/process_pdfs")
def process_pdfs_endpoint():
    pdf_directory = "downloaded_files/pdf_files"  # Relatív útvonal
    try:
        process_and_index_pdfs(pdf_directory)
        return {"message": "PDF-ek feldolgozása és indexelése sikeres!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hiba történt: {e}")
