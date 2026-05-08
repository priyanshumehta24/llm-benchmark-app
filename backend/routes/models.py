from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db
from models.benchmark import LLMModel, BenchmarkScore

router = APIRouter(prefix="/api/models", tags=["models"])

# --- Pydantic Schemas ---

class ModelResponse(BaseModel):
    id: int
    name: str
    family: Optional[str]
    provider: Optional[str]
    is_open_source: bool
    description: Optional[str]

    class Config:
        from_attributes = True

class ScoreResponse(BaseModel):
    benchmark: str
    score: float
    score_type: str
    fetched_at: str

class ModelDetailResponse(ModelResponse):
    scores: List[ScoreResponse]

# --- Routes ---

@router.get("", response_model=List[ModelResponse])
def get_models(
    family: Optional[str] = Query(None, description="Filter by model family"),
    open_source: Optional[bool] = Query(None, description="Filter by open_source"),
    db: Session = Depends(get_db)
):
    query = db.query(LLMModel)
    
    if family is not None:
        query = query.filter(LLMModel.family == family)
    if open_source is not None:
        query = query.filter(LLMModel.is_open_source == open_source)
        
    return query.all()

@router.get("/{model_id}", response_model=ModelDetailResponse)
def get_model_detail(model_id: int, db: Session = Depends(get_db)):
    model = db.query(LLMModel).filter(LLMModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail=f"Model with id {model_id} not found")
        
    scores = db.query(BenchmarkScore).filter(BenchmarkScore.model_id == model_id).all()
    
    score_list = [
        ScoreResponse(
            benchmark=s.benchmark_name,
            score=s.score,
            score_type=s.score_type,
            fetched_at=s.fetched_at.isoformat() + "Z" if s.fetched_at else ""
        )
        for s in scores
    ]
    
    return ModelDetailResponse(
        id=model.id,
        name=model.name,
        family=model.family,
        provider=model.provider,
        is_open_source=model.is_open_source,
        description=model.description,
        scores=score_list
    )
