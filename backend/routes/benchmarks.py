from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
from models.benchmark import LLMModel, BenchmarkScore

router = APIRouter(prefix="/api/benchmarks", tags=["benchmarks"])

# --- Static Benchmark Dictionary ---
BENCHMARKS_INFO = [
    {
        "name": "MMLU",
        "full_name": "Massive Multitask Language Understanding",
        "description": "Tests knowledge across 57 academic subjects. Higher = better general knowledge.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "ARC",
        "full_name": "AI2 Reasoning Challenge",
        "description": "Grade-school science questions requiring logic and reasoning.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "HellaSwag",
        "full_name": "HellaSwag",
        "description": "Commonsense reasoning around everyday events.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "TruthfulQA",
        "full_name": "TruthfulQA",
        "description": "Measures the model's propensity to produce falsehoods or conspiracy theories.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "Winogrande",
        "full_name": "WinoGrande",
        "description": "Adversarial winograd schema challenge testing pronoun resolution and commonsense.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "HumanEval",
        "full_name": "HumanEval Code Generation",
        "description": "Measures ability to generate correct Python functions from docstrings.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "GSM8K",
        "full_name": "Grade School Math 8K",
        "description": "High quality grade school math word problems.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "MATH",
        "full_name": "MATH",
        "description": "Challenging competition mathematics problems.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "SWE-Bench",
        "full_name": "Software Engineering Benchmark",
        "description": "Resolving real-world GitHub issues in Python repositories.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "GPQA",
        "full_name": "Google-Proof Q&A",
        "description": "Extremely difficult PhD-level questions in biology, physics, and chemistry.",
        "score_type": "percent",
        "max_score": 100
    },
    {
        "name": "Chatbot Arena Elo",
        "full_name": "LMSYS Chatbot Arena Elo Rating",
        "description": "Human preference-based Elo rating from head-to-head model battles.",
        "score_type": "elo",
        "max_score": None
    }
]

# --- Pydantic Schemas ---

class BenchmarkInfoResponse(BaseModel):
    name: str
    full_name: str
    description: str
    score_type: str
    max_score: Optional[int] = None

class ModelScoreItem(BaseModel):
    model_id: int
    model_name: str
    score: float

class BenchmarkScoresResponse(BaseModel):
    benchmark: str
    scores: List[ModelScoreItem]

# --- Routes ---

@router.get("", response_model=List[BenchmarkInfoResponse])
def get_benchmarks():
    return BENCHMARKS_INFO

@router.get("/{benchmark_name}/scores", response_model=BenchmarkScoresResponse)
def get_benchmark_scores(benchmark_name: str, db: Session = Depends(get_db)):
    scores = (
        db.query(BenchmarkScore, LLMModel.name)
        .join(LLMModel, LLMModel.id == BenchmarkScore.model_id)
        .filter(BenchmarkScore.benchmark_name == benchmark_name)
        .order_by(BenchmarkScore.score.desc())
        .all()
    )
    
    if not scores:
        raise HTTPException(status_code=404, detail=f"Benchmark '{benchmark_name}' not found")
        
    result_scores = [
        ModelScoreItem(
            model_id=s.BenchmarkScore.model_id,
            model_name=s.name,
            score=s.BenchmarkScore.score
        )
        for s in scores
    ]
    
    return BenchmarkScoresResponse(
        benchmark=benchmark_name,
        scores=result_scores
    )
