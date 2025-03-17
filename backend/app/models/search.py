from pydantic import BaseModel
from typing import List, Dict, Optional

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    results: List[str]