from pathlib import Path
from datetime import datetime
from backend.schemas.papers import PaperInfo, PapersListResponse

class PapersInteractor:
    def get_papers_list(self) -> PapersListResponse:
        output_dir = Path("output").absolute()
        
        if not output_dir.exists():
            output_dir.mkdir(exist_ok=True)
            return PapersListResponse(papers=[], total_count=0)
        
        papers = []
        
        for pdf_file in output_dir.glob("*.pdf"):
            stat = pdf_file.stat()
            title = pdf_file.stem.replace("paper_", "").replace("_", " ").title()
            
            papers.append(PaperInfo(
                filename=pdf_file.name,
                title=title,
                created_at=datetime.fromtimestamp(stat.st_ctime).isoformat(),
                file_size=stat.st_size,
                download_url=f"/papers/download/{pdf_file.name}"
            ))
        
        papers.sort(key=lambda x: x.created_at, reverse=True)
        return PapersListResponse(papers=papers, total_count=len(papers))
