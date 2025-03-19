from fastapi import APIRouter, HTTPException
from app.services.file_downloader import download_files
from app.services.pdf_processor import process_and_index_pdfs
import os
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/download")
def download_files_endpoint():
    try:
        file_links = download_files()
        return {"message": "Files downloaded successfully", "files": file_links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/process_pdfs")
def process_pdfs_endpoint():
    pdf_directory = "downloaded_files/pdf_files"  
    try:
        process_and_index_pdfs(pdf_directory)
        return {"message": "PDF-ek feldolgozása és indexelése sikeres!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hiba történt: {e}")
    
