from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.benchmark import LLMModel, BenchmarkScore

router = APIRouter(prefix="/api/compare", tags=["compare"])

# --- Pydantic Schemas ---

class CompareResponse(BaseModel):
    models: List[str]
    benchmarks: List[str]
    data: Dict[str, Dict[str, float]]
    radar_data: List[Dict[str, Any]]

# --- Routes ---

@router.get("", response_model=CompareResponse)
def compare_models(
    models: str = Query(..., description="Comma-separated model IDs"),
    benchmarks: Optional[str] = Query(None, description="Comma-separated benchmark names"),
    db: Session = Depends(get_db)
):
    try:
        model_ids = [int(m.strip()) for m in models.split(",") if m.strip()]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid model IDs provided")

    if not (2 <= len(model_ids) <= 4):
        raise HTTPException(status_code=400, detail="Please provide between 2 and 4 model IDs")

    # Fetch models
    db_models = db.query(LLMModel).filter(LLMModel.id.in_(model_ids)).all()
    if len(db_models) != len(model_ids):
        found_ids = [m.id for m in db_models]
        missing = set(model_ids) - set(found_ids)
        raise HTTPException(status_code=404, detail=f"Models not found: {missing}")

    model_names = [m.name for m in db_models]

    # Fetch scores
    query = db.query(BenchmarkScore).filter(BenchmarkScore.model_id.in_(model_ids))
    
    benchmark_list = []
    if benchmarks:
        benchmark_list = [b.strip() for b in benchmarks.split(",") if b.strip()]
        query = query.filter(BenchmarkScore.benchmark_name.in_(benchmark_list))
    
    scores = query.all()
    
    if not benchmark_list:
        # If not specified, get all unique benchmarks from the results
        benchmark_list = sorted(list(set(s.benchmark_name for s in scores)))

    # Structure data
    data: Dict[str, Dict[str, float]] = {name: {} for name in model_names}
    
    # Map model ID to name
    id_to_name = {m.id: m.name for m in db_models}
    
    for s in scores:
        model_name = id_to_name[s.model_id]
        data[model_name][s.benchmark_name] = s.score

    # Structure radar_data
    radar_data = []
    for bench in benchmark_list:
        radar_entry = {"benchmark": bench}
        for model_name in model_names:
            radar_entry[model_name] = data[model_name].get(bench, 0.0)
        radar_data.append(radar_entry)

    return CompareResponse(
        models=model_names,
        benchmarks=benchmark_list,
        data=data,
        radar_data=radar_data
    )
