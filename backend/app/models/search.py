from pydantic import BaseModel
from typing import List, Dict, Optional
from pydantic import BaseModel
from typing import Optional

class SearchRequest(BaseModel):
    query: str
    mode: str
    startDate: Optional[str] = None  
    endDate: Optional[str] = None

class SearchResponse(BaseModel):
    results: List[str]