import os
from datetime import datetime
from typing import Dict, Any, List
from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.benchmark import LLMModel, BenchmarkScore, UpdateLog
from services import scorer

router = APIRouter(prefix="/api", tags=["meta"])

# --- Pydantic Schemas ---

class HealthResponse(BaseModel):
    status: str
    timestamp: str

class LastUpdatedResponse(BaseModel):
    last_updated: str
    models_count: int
    scores_count: int

class UseCaseInfo(BaseModel):
    id: str
    label: str
    description: str
    icon: str
    weights: Dict[str, float]

class TriggerUpdateResponse(BaseModel):
    status: str
    started_at: str

# --- Static Use Case Info ---
USE_CASE_STATIC = [
    {
        "id": "code_generation",
        "label": "Code Generation & Review",
        "description": "Writing, debugging, and reviewing code",
        "icon": "code"
    },
    {
        "id": "math_reasoning",
        "label": "Math & Reasoning",
        "description": "Mathematical problem solving and logical reasoning",
        "icon": "calculator"
    },
    {
        "id": "general_qa",
        "label": "General Q&A Assistant",
        "description": "Wide-ranging question answering and knowledge tasks",
        "icon": "chat"
    },
    {
        "id": "document_analysis",
        "label": "Document Analysis & Summarization",
        "description": "Reading, extracting, and summarizing long documents",
        "icon": "document"
    },
    {
        "id": "creative_writing",
        "label": "Creative Writing & Content",
        "description": "Generating creative, engaging written content",
        "icon": "pen"
    },
    {
        "id": "science_research",
        "label": "Science & Research",
        "description": "PhD-level scientific reasoning and research assistance",
        "icon": "flask"
    }
]

# --- Routes ---

@router.get("/health", response_model=HealthResponse)
def health():
    return HealthResponse(
        status="ok",
        timestamp=datetime.utcnow().isoformat() + "Z"
    )

@router.get("/last-updated", response_model=LastUpdatedResponse)
def last_updated(db: Session = Depends(get_db)):
    last_log = db.query(UpdateLog).filter(UpdateLog.status == "success").order_by(UpdateLog.run_at.desc()).first()
    
    # If no update log, use the latest fetched_at from benchmark_scores
    last_updated_time = None
    if last_log:
        last_updated_time = last_log.run_at
    else:
        latest_score = db.query(BenchmarkScore).order_by(BenchmarkScore.fetched_at.desc()).first()
        if latest_score and latest_score.fetched_at:
            last_updated_time = latest_score.fetched_at
            
    # Default if db is empty
    if not last_updated_time:
        last_updated_time = datetime.utcnow()
        
    models_count = db.query(LLMModel).count()
    scores_count = db.query(BenchmarkScore).count()
    
    return LastUpdatedResponse(
        last_updated=last_updated_time.isoformat() + "Z",
        models_count=models_count,
        scores_count=scores_count
    )

@router.get("/usecases", response_model=List[UseCaseInfo])
def usecases():
    weights = scorer._load_weights()
    
    result = []
    for info in USE_CASE_STATIC:
        usecase_id = info["id"]
        result.append(UseCaseInfo(
            id=usecase_id,
            label=info["label"],
            description=info["description"],
            icon=info["icon"],
            weights=weights.get(usecase_id, {})
        ))
        
    return result

@router.post("/trigger-update", response_model=TriggerUpdateResponse)
def trigger_update(x_admin_secret: str = Header(None)):
    expected_secret = os.getenv("ADMIN_SECRET")
    if not expected_secret or x_admin_secret != expected_secret:
        raise HTTPException(status_code=403, detail="Invalid or missing admin secret")
        
    # In a real system, this would enqueue a background job.
    # For now, we return immediate success response per API_CONTRACTS.md
    return TriggerUpdateResponse(
        status="update triggered",
        started_at=datetime.utcnow().isoformat() + "Z"
    )
