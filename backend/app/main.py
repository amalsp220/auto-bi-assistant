from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, ask
from app.core.config import settings

app = FastAPI(
    title="Auto-BI Assistant API",
    description="Open-source agentic data analyst powered by OpenAI + FastAPI",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(ask.router, prefix="/api", tags=["ask"])

@app.get("/")
async def root():
    return {"message": "Auto-BI Assistant API is running", "docs": "/docs"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
