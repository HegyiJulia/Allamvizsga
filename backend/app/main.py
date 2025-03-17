from fastapi import FastAPI
from app.routers import files, search

app = FastAPI()

# Routers
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(search.router, prefix="/search", tags=["Search"])

@app.get("/")
def root():
    return {"message": "Welcome to the Senatus Resolutions API"}

