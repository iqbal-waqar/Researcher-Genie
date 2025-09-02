from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routes.chat import router as chat_router
from backend.routes.papers import router as papers_router
from backend.routes.downloads import router as downloads_router

app = FastAPI(
    title="Research-Genie API",
    description="An AI-powered research paper generation system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router)
app.include_router(papers_router)
app.include_router(downloads_router)
