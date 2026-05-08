from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["benchmarks"])


@router.get("/benchmarks")
def get_benchmarks():
    return {"message": "Phase 4 — not yet implemented"}


@router.get("/benchmarks/{benchmark_name}/scores")
def get_benchmark_scores(benchmark_name: str):
    return {"message": f"Phase 4 — {benchmark_name} scores not yet implemented"}
