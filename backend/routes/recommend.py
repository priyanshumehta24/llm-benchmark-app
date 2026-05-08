from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["recommend"])


@router.post("/recommend")
def recommend():
    return {"message": "Phase 4 — not yet implemented"}


@router.get("/compare")
def compare():
    return {"message": "Phase 4 — not yet implemented"}


@router.get("/usecases")
def usecases():
    return {"message": "Phase 4 — not yet implemented"}
