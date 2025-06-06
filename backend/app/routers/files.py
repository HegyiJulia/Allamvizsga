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
        print (e)
        raise HTTPException(status_code=500, detail=f"Hiba történt: {e}")
    
@router.get("/get_pdf/{filename}")
def get_pdf(filename: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # <== elmegy az app/routers/ szintről a backend/ szintre
    filepath = os.path.join(base_dir, "../../downloaded_files/pdf_files")
    filepath = os.path.join(filepath, filename)
    filepath = os.path.abspath(filepath)

    if os.path.exists(filepath):
        response =  FileResponse(
            filepath,
            media_type="application/pdf", 
            filename=filename)
    
        response.headers["Content-Disposition"] = f'inline; filename="{filename}"'
        return response
    
    else:
        raise HTTPException(status_code=404, detail="Fájl nem található")

@router.get("/list_pdfs")
def list_pdfs():
    base_dir = os.path.dirname(os.path.abspath(__file__))  # <== elmegy az app/routers/ szintről a backend/ szintre
    # directory = os.path.join(base_dir, "downloaded_files", "pdf_files")
    directory = os.path.join(base_dir, "../../downloaded_files/pdf_files")
    directory = os.path.abspath(directory)
    # directory = "../../downloaded_files/pdf_files"
    try:
        if not os.path.exists(directory):
            raise HTTPException(status_code=404, detail=f"A könyvtár nem található: {directory}")

        files = [
            {
                "filename": f,
                "url": f"/files/get_pdf/{f}"
            }
            for f in os.listdir(directory)
            if f.lower().endswith(".pdf")
        ]
        return {"pdfs": files}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hiba a fájlok listázása közben: {e}")



@router.get("/_test")
def test():
    return {"message": "Router működik"}
