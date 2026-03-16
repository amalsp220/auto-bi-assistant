import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.analytics.data_profiler import profile_dataframe
import pandas as pd
import io

router = APIRouter()

# In-memory storage for uploaded dataframes (session-based)
_store: dict = {}

@router.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    """Upload a CSV file and return its profile."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are supported.")

    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.MAX_FILE_SIZE_MB}MB limit.")

    try:
        df = pd.read_csv(io.BytesIO(content))
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Could not parse CSV: {str(e)}")

    session_id = str(uuid.uuid4())
    _store[session_id] = df

    profile = profile_dataframe(df)
    return JSONResponse({
        "session_id": session_id,
        "filename": file.filename,
        "rows": len(df),
        "columns": len(df.columns),
        "profile": profile,
    })

def get_dataframe(session_id: str) -> pd.DataFrame:
    """Retrieve a stored dataframe by session ID."""
    df = _store.get(session_id)
    if df is None:
        raise HTTPException(status_code=404, detail="Session not found. Please re-upload your file.")
    return df
