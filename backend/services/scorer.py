"""
scorer.py — Phase 3 implementation.
Implements the weighted scoring formula from SPECS.md:

  NormalizedScore(model, benchmark) = RawScore / MaxScoreAcrossAllModels
  FinalScore(model, usecase) = Σ [ weight(benchmark, usecase) × NormalizedScore(model, benchmark) ]

Stub for Phase 1. Full implementation in Phase 3.
"""


def normalize_scores(scores: list[dict]) -> dict:
    """Normalize raw scores per benchmark across all models. Returns dict[benchmark][model_id]."""
    raise NotImplementedError("Implemented in Phase 3")


def compute_final_scores(model_scores: dict, use_case: str, weights: dict) -> list[dict]:
    """Compute FinalScore(model, usecase) for all models. Returns ranked list."""
    raise NotImplementedError("Implemented in Phase 3")
