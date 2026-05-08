"""
services/scorer.py  —  Phase 3: Scoring Engine

Implements the two-step weighted scoring formula from SPECS.md:

    NormalizedScore(model, benchmark) = RawScore / MaxScoreAcrossAllModels

    FinalScore(model, usecase) = Σ [ weight(benchmark, usecase)
                                     × NormalizedScore(model, benchmark) ]

Public API
----------
    normalize_scores(db)
        → dict[model_name, dict[benchmark_name, float]]   (values 0–1)

    compute_final_score(model_name, use_case, normalized_scores)
        → float   (0–1)

    rank_models(use_case, db)
        → list[dict]  sorted descending by final_score
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any

from sqlalchemy.orm import Session

from models.benchmark import BenchmarkScore, LLMModel

logger = logging.getLogger(__name__)

# ── Weights file ───────────────────────────────────────────────────────────────
_WEIGHTS_PATH = Path(__file__).resolve().parent.parent / "data" / "benchmark_weights.json"

VALID_USE_CASES = {
    "code_generation",
    "math_reasoning",
    "general_qa",
    "document_analysis",
    "creative_writing",
    "science_research",
}


def _load_weights() -> dict[str, dict[str, float]]:
    """Load and return the benchmark_weights.json mapping."""
    with open(_WEIGHTS_PATH, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ── Step 1: Normalize ──────────────────────────────────────────────────────────

def normalize_scores(db: Session) -> dict[str, dict[str, float]]:
    """
    For every benchmark, divide each model's raw score by the maximum
    score recorded across *all* models for that benchmark.

    Parameters
    ----------
    db : SQLAlchemy Session

    Returns
    -------
    dict mapping  model_name → { benchmark_name → normalized_score (0–1) }

    Notes
    -----
    - Models with no score for a given benchmark receive 0.0 for that benchmark.
    - If the max score for a benchmark is 0 (data error), all values stay 0.0
      to avoid division by zero.
    """
    # Pull every (model_name, benchmark_name, score) row in one query
    rows: list[tuple[str, str, float]] = (
        db.query(LLMModel.name, BenchmarkScore.benchmark_name, BenchmarkScore.score)
        .join(BenchmarkScore, BenchmarkScore.model_id == LLMModel.id)
        .all()
    )

    if not rows:
        logger.warning("normalize_scores: no benchmark rows found in database.")
        return {}

    # --- build raw lookup: { benchmark_name → { model_name → raw_score } }
    raw: dict[str, dict[str, float]] = {}
    for model_name, bench_name, score in rows:
        raw.setdefault(bench_name, {})[model_name] = float(score)

    # --- compute per-benchmark max
    bench_max: dict[str, float] = {
        bench: max(scores.values()) for bench, scores in raw.items()
    }

    # --- gather complete model list
    all_models: set[str] = {r[0] for r in rows}

    # --- build normalized output
    normalized: dict[str, dict[str, float]] = {m: {} for m in all_models}

    for bench_name, model_scores in raw.items():
        max_val = bench_max[bench_name]
        for model_name in all_models:
            raw_score = model_scores.get(model_name, 0.0)
            normalized[model_name][bench_name] = (
                raw_score / max_val if max_val > 0 else 0.0
            )

    logger.debug(
        "normalize_scores: normalized %d benchmarks across %d models.",
        len(raw),
        len(all_models),
    )
    return normalized


# ── Step 2: Weighted final score ───────────────────────────────────────────────

def compute_final_score(
    model_name: str,
    use_case: str,
    normalized_scores: dict[str, dict[str, float]],
) -> float:
    """
    Apply the weighted sum formula for a single model / use-case pair.

        FinalScore = Σ (weight_i × normalized_score_i)

    Benchmarks listed in the weights file but missing from normalized_scores
    for this model contribute 0.0 (treated as no data).

    Parameters
    ----------
    model_name        : exact name matching an llm_models row
    use_case          : one of the six VALID_USE_CASES keys
    normalized_scores : output of normalize_scores()

    Returns
    -------
    float in [0, 1]

    Raises
    ------
    ValueError  if use_case is not a recognised category
    """
    if use_case not in VALID_USE_CASES:
        raise ValueError(
            f"Unknown use_case {use_case!r}. "
            f"Must be one of: {sorted(VALID_USE_CASES)}"
        )

    weights = _load_weights().get(use_case, {})
    model_normalized = normalized_scores.get(model_name, {})

    final: float = 0.0
    for bench_name, weight in weights.items():
        norm_val = model_normalized.get(bench_name, 0.0)
        final += weight * norm_val

    # Clamp to [0, 1] as a safety net against floating-point edge cases
    return max(0.0, min(1.0, final))


# ── Step 3: Rank all models ────────────────────────────────────────────────────

def rank_models(
    use_case: str,
    db: Session,
) -> list[dict[str, Any]]:
    """
    Rank all models in the database for the given use_case.

    Workflow
    --------
    1. normalize_scores(db)   — one DB query, O(models × benchmarks)
    2. compute_final_score()  — per model
    3. Sort descending by final_score

    Parameters
    ----------
    use_case : one of the six VALID_USE_CASES keys
    db       : SQLAlchemy Session

    Returns
    -------
    List of dicts, sorted best → worst:
    [
        {
            "model":        "Gemini 2.5 Pro",
            "final_score":  0.91,
            "breakdown": {
                "MMLU":      0.35,   # weight × normalized_score contribution
                "GSM8K":     0.40,
                ...
            }
        },
        ...
    ]

    Raises
    ------
    ValueError  if use_case is not recognised
    """
    if use_case not in VALID_USE_CASES:
        raise ValueError(
            f"Unknown use_case {use_case!r}. "
            f"Must be one of: {sorted(VALID_USE_CASES)}"
        )

    normalized = normalize_scores(db)
    weights = _load_weights().get(use_case, {})

    results: list[dict[str, Any]] = []

    for model_name, model_normalized in normalized.items():
        final_score = compute_final_score(model_name, use_case, normalized)

        # Per-benchmark contribution for transparent score breakdown
        breakdown: dict[str, float] = {}
        for bench_name, weight in weights.items():
            norm_val = model_normalized.get(bench_name, 0.0)
            breakdown[bench_name] = round(weight * norm_val, 6)

        results.append(
            {
                "model": model_name,
                "final_score": round(final_score, 6),
                "breakdown": breakdown,
            }
        )

    # Sort descending — highest final_score first
    results.sort(key=lambda x: x["final_score"], reverse=True)

    # Make scores relative to top model (highest scorer = 100%, others proportionally lower)
    if results and results[0]["final_score"] > 0:
        max_score = results[0]["final_score"]
        for res in results:
            res["final_score"] = round(res["final_score"] / max_score, 6)

    logger.info(
        "rank_models: ranked %d models for use_case=%r. Top: %s (%.4f)",
        len(results),
        use_case,
        results[0]["model"] if results else "N/A",
        results[0]["final_score"] if results else 0.0,
    )
    return results
