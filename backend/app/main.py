from fastapi import FastAPI
from app.routers import files, search
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

# Routers
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(search.router, prefix="/search", tags=["Search"])

@app.get("/")
def root():
    return {"message": "Welcome to the Senatus Resolutions API"}

# CORS engedélyezése a frontend számára
origins = [
    "http://localhost:5173",  # Frontend alkalmazás helye
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Engedélyezett origin-ek
    allow_credentials=True,
    allow_methods=["*"],  # Engedélyezett HTTP-módszerek
    allow_headers=["*"],  # Engedélyezett fejlécek
)
