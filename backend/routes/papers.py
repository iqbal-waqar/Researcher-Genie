from fastapi import APIRouter, HTTPException
from backend.schemas.papers import PapersListResponse
from backend.interactors.papers import PapersInteractor

router = APIRouter(prefix="/papers", tags=["papers"])

@router.get("/", response_model=PapersListResponse)
async def list_research_papers() -> PapersListResponse:
    try:
        papers_interactor = PapersInteractor()
        return papers_interactor.get_papers_list()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing papers: {str(e)}")