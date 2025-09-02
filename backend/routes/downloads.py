from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from backend.interactors.downloads import DownloadInteractor

router = APIRouter(prefix="/papers", tags=["download"])

@router.get("/download/{filename}")
async def download_pdf(filename: str) -> FileResponse:
    try:
        download_interactor = DownloadInteractor()
        return download_interactor.get_pdf_file(filename)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error downloading PDF: {str(e)}")