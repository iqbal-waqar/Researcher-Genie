from pathlib import Path
from fastapi.responses import FileResponse

class DownloadInteractor:
    def get_pdf_file(self, filename: str) -> FileResponse:
        if ".." in filename or "/" in filename or "\\" in filename:
            raise ValueError("Invalid filename")
        
        if not filename.endswith(".pdf"):
            raise ValueError("Only PDF files can be downloaded")
        
        pdf_path = Path("output").absolute() / filename
        
        if not pdf_path.exists():
            raise FileNotFoundError("PDF file not found")
        
        return FileResponse(
            path=str(pdf_path), 
            filename=filename, 
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
