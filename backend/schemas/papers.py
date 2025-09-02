from pydantic import BaseModel
from typing import List

class PaperInfo(BaseModel):
    filename: str
    title: str
    created_at: str
    file_size: int
    download_url: str

class PapersListResponse(BaseModel):
    papers: List[PaperInfo]
    total_count: int