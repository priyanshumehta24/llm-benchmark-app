from typing import List, Dict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field

from database import get_db
from models.benchmark import LLMModel
from services import gemini_service, scorer

router = APIRouter(prefix="/api", tags=["recommend"])

# --- Pydantic Schemas ---

class RecommendRequest(BaseModel):
    use_case_text: str = Field(..., min_length=10, max_length=500)
    top_n: int = Field(5, ge=1, le=10)

class BreakdownItem(BaseModel):
    raw: float
    normalized: float
    weight: float
    contribution: float

class Recommendation(BaseModel):
    rank: int
    model_id: int
    model_name: str
    provider: str
    is_open_source: bool
    final_score: float
    score_breakdown: Dict[str, BreakdownItem]
    reasoning: str

class RecommendResponse(BaseModel):
    detected_category: str
    category_confidence: float
    use_case_text: str
    recommendations: List[Recommendation]
    weights_used: Dict[str, float]

# --- Routes ---

@router.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest, db: Session = Depends(get_db)):
    # 1. Classify use case
    category = gemini_service.classify_use_case(req.use_case_text)
    
    if not category:
        # If the service raises an exception internally that isn't caught,
        # or if it's completely down, we return 503. The gemini service 
        # is supposed to fallback to general_qa though.
        raise HTTPException(
            status_code=503, 
            detail="Use-case classification service temporarily unavailable. Please try again."
        )

    # 2. Rank models
    try:
        ranked_models = scorer.rank_models(category, db)
    except ValueError as e:
        # Fallback if something weird happens with category string
        category = gemini_service.FALLBACK_CATEGORY
        ranked_models = scorer.rank_models(category, db)

    # 3. Load weights used for this category
    weights = scorer._load_weights().get(category, {})

    # 4. Format response
    # We need the normalized scores to construct the detailed breakdown,
    # or we can reconstruct them from raw + breakdown contribution. 
    # Since rank_models returns just breakdown (contribution), we also need raw scores.
    # To keep it efficient, we can fetch all models first.
    
    models_dict = {m.name: m for m in db.query(LLMModel).all()}
    normalized_scores = scorer.normalize_scores(db)
    
    # Also fetch all raw scores to populate the 'raw' field
    from models.benchmark import BenchmarkScore
    raw_scores = db.query(BenchmarkScore).all()
    raw_score_dict = {}
    for s in raw_scores:
        if s.model_id not in raw_score_dict:
            raw_score_dict[s.model_id] = {}
        raw_score_dict[s.model_id][s.benchmark_name] = s.score

    recommendations = []
    
    for i, rm in enumerate(ranked_models[:req.top_n]):
        model_name = rm["model"]
        model_obj = models_dict.get(model_name)
        
        if not model_obj:
            continue
            
        final_score = rm["final_score"]
        breakdown_dict = {}
        
        for bench_name, weight in weights.items():
            raw_val = raw_score_dict.get(model_obj.id, {}).get(bench_name, 0.0)
            norm_val = normalized_scores.get(model_name, {}).get(bench_name, 0.0)
            contribution = rm["breakdown"].get(bench_name, 0.0)
            
            breakdown_dict[bench_name] = BreakdownItem(
                raw=raw_val,
                normalized=round(norm_val, 4),
                weight=weight,
                contribution=round(contribution, 4)
            )
            
        # Basic reasoning generation
        top_benchmarks = sorted(breakdown_dict.items(), key=lambda x: x[1].contribution, reverse=True)
        reasoning = f"{model_name} is a strong choice for {category}."
        if top_benchmarks:
            top_b = top_benchmarks[0][0]
            reasoning = f"{model_name} leads on {top_b} ({top_benchmarks[0][1].raw}), making it a strong choice."

        recommendations.append(Recommendation(
            rank=i + 1,
            model_id=model_obj.id,
            model_name=model_name,
            provider=model_obj.provider or "",
            is_open_source=model_obj.is_open_source,
            final_score=round(final_score, 3),
            score_breakdown=breakdown_dict,
            reasoning=reasoning
        ))

    return RecommendResponse(
        detected_category=category,
        category_confidence=0.90, # gemini_service current implementation doesn't return confidence, so we mock it
        use_case_text=req.use_case_text,
        recommendations=recommendations,
        weights_used=weights
    )
