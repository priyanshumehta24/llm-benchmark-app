"""
Stub route files for Phases 2–5 — these will be fully implemented in later phases.
They are registered here so the router tree is complete from Phase 1.
"""
from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["models"])


@router.get("/models")
def get_models():
    return {"message": "Phase 2 — not yet implemented"}


@router.get("/models/{model_id}")
def get_model(model_id: int):
    return {"message": f"Phase 2 — model {model_id} not yet implemented"}
