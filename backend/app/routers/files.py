from fastapi import APIRouter, HTTPException
from app.services.file_downloader import download_files

router = APIRouter()

@router.get("/download")
def download_files_endpoint():
    try:
        file_links = download_files()
        return {"message": "Files downloaded successfully", "files": file_links}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
