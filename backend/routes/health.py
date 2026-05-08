from datetime import datetime, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
from models.benchmark import BenchmarkScore, LLMModel

router = APIRouter(prefix="/api", tags=["meta"])


@router.get("/health")
def health_check():
    """Returns server health status."""
    return {
        "status": "ok",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


@router.get("/last-updated")
def last_updated(db: Session = Depends(get_db)):
    """Returns timestamp of the most recent data fetch, model count, and score count."""
    models_count = db.query(func.count(LLMModel.id)).scalar() or 0
    scores_count = db.query(func.count(BenchmarkScore.id)).scalar() or 0

    # Find the most recent fetched_at timestamp across all scores
    latest = db.query(func.max(BenchmarkScore.fetched_at)).scalar()

    return {
        "last_updated": latest.isoformat() if latest else None,
        "models_count": models_count,
        "scores_count": scores_count
    }
