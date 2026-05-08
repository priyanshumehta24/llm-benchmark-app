"""
services/scraper.py

Fetches benchmark scores from three external APIs:
  1. fetch_hf_leaderboard()    — Hugging Face Open LLM Leaderboard
  2. fetch_papers_with_code()  — Papers With Code REST API
  3. fetch_arena_elo()         — LMSYS Chatbot Arena (HTML scrape / leaderboard)

Every function:
  - Loads API credentials from backend/.env via python-dotenv
  - Wraps network calls in try/except
  - Returns cached DB data as a fallback if the live fetch fails
"""

import logging
import os
from typing import Any

import requests
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from models.benchmark import BenchmarkScore, LLMModel

load_dotenv()

logger = logging.getLogger(__name__)

# ── ENV ────────────────────────────────────────────────────────────────────────
HF_API_TOKEN: str = os.getenv("HF_API_TOKEN", "")
# Papers With Code is publicly accessible; key is optional but honoured if set
PWC_API_KEY: str = os.getenv("PAPERS_WITH_CODE_API_KEY", "")

# ── Hugging Face ───────────────────────────────────────────────────────────────
_HF_LEADERBOARD_URL = (
    "https://huggingface.co/datasets/open-llm-leaderboard/"
    "results/resolve/main/results.json"
)
# Benchmarks we care about from HF leaderboard
_HF_BENCHMARKS = {"mmlu", "arc", "hellaswag", "truthfulqa", "winogrande"}


def fetch_hf_leaderboard(db: Session) -> list[dict[str, Any]]:
    """
    Fetch the latest benchmark scores from the Hugging Face Open LLM Leaderboard.

    Returns a list of dicts, each containing:
        {
            "model_name": str,
            "benchmark_name": str,   # e.g. "MMLU"
            "score": float,
            "score_type": "percent",
            "source_url": str,
        }

    Falls back to cached BenchmarkScore rows from the database if the
    request fails for any reason.
    """
    source_url = "https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard"
    try:
        headers = {}
        if HF_API_TOKEN:
            headers["Authorization"] = f"Bearer {HF_API_TOKEN}"

        # The public HF leaderboard exposes a dataset with aggregated results.
        # We hit the dataset viewer API which requires no special token for public data.
        api_url = (
            "https://datasets-server.huggingface.co/rows"
            "?dataset=open-llm-leaderboard%2Fresults&config=default&split=train&offset=0&length=100"
        )
        response = requests.get(api_url, headers=headers, timeout=15)
        response.raise_for_status()

        payload = response.json()
        rows = payload.get("rows", [])

        results: list[dict[str, Any]] = []
        for row_wrapper in rows:
            row = row_wrapper.get("row", {})
            model_name: str = row.get("model_name_for_query") or row.get("model", "")
            if not model_name:
                continue
            # Each benchmark is a top-level key; collect only the ones we need
            for bench_key in _HF_BENCHMARKS:
                raw_score = row.get(bench_key) or row.get(bench_key.upper())
                if raw_score is None:
                    continue
                results.append(
                    {
                        "model_name": model_name,
                        "benchmark_name": bench_key.upper().replace("TRUTHFULQA", "TruthfulQA")
                                                               .replace("HELLASWAG", "HellaSwag")
                                                               .replace("WINOGRANDE", "Winogrande")
                                                               .replace("MMLU", "MMLU")
                                                               .replace("ARC", "ARC"),
                        "score": float(raw_score),
                        "score_type": "percent",
                        "source_url": source_url,
                    }
                )

        logger.info("fetch_hf_leaderboard: fetched %d score rows from HF.", len(results))
        return results

    except Exception as exc:
        logger.warning(
            "fetch_hf_leaderboard: live fetch failed (%s). Falling back to DB cache.", exc
        )
        return _fallback_from_db(
            db,
            benchmark_names=["MMLU", "ARC", "HellaSwag", "TruthfulQA", "Winogrande"],
        )


# ── Papers With Code ───────────────────────────────────────────────────────────
_PWC_API_BASE = "https://paperswithcode.com/api/v1"
_PWC_BENCHMARKS = {
    "GSM8K": "gsm8k",
    "HumanEval": "humaneval",
    "MATH": "math",
}


def fetch_papers_with_code(db: Session) -> list[dict[str, Any]]:
    """
    Fetch GSM8K, HumanEval, and MATH scores from the Papers With Code API.

    Returns a list of dicts in the same format as fetch_hf_leaderboard().
    Falls back to cached DB data on any error.
    """
    source_url = "https://paperswithcode.com/sota"
    results: list[dict[str, Any]] = []

    try:
        headers: dict[str, str] = {}
        if PWC_API_KEY:
            headers["Authorization"] = f"Token {PWC_API_KEY}"

        for display_name, sota_slug in _PWC_BENCHMARKS.items():
            try:
                url = f"{_PWC_API_BASE}/sota/?task={sota_slug}&ordering=-score&page_size=20"
                resp = requests.get(url, headers=headers, timeout=15)
                resp.raise_for_status()

                data = resp.json()
                for entry in data.get("results", []):
                    model_name: str = entry.get("model_name", "").strip()
                    score_val = entry.get("best_metric") or entry.get("score")
                    if not model_name or score_val is None:
                        continue
                    results.append(
                        {
                            "model_name": model_name,
                            "benchmark_name": display_name,
                            "score": float(score_val),
                            "score_type": "percent",
                            "source_url": source_url,
                        }
                    )
            except Exception as inner_exc:
                logger.warning(
                    "fetch_papers_with_code: failed for benchmark %r (%s).",
                    display_name,
                    inner_exc,
                )
                # Continue to next benchmark rather than bailing entirely

        if not results:
            raise RuntimeError("No results retrieved from Papers With Code.")

        logger.info("fetch_papers_with_code: fetched %d score rows from PWC.", len(results))
        return results

    except Exception as exc:
        logger.warning(
            "fetch_papers_with_code: live fetch failed (%s). Falling back to DB cache.", exc
        )
        return _fallback_from_db(db, benchmark_names=["GSM8K", "HumanEval", "MATH"])


# ── LMSYS Chatbot Arena ────────────────────────────────────────────────────────
_ARENA_LEADERBOARD_URL = (
    "https://raw.githubusercontent.com/lm-sys/FastChat/main/fastchat/serve/leaderboard.json"
)


def fetch_arena_elo(db: Session) -> list[dict[str, Any]]:
    """
    Fetch human-preference Elo ratings from the LMSYS Chatbot Arena leaderboard.

    The leaderboard JSON is cached publicly on the FastChat GitHub repo.

    Returns a list of dicts:
        {
            "model_name": str,
            "benchmark_name": "Chatbot Arena Elo",
            "score": float,
            "score_type": "elo",
            "source_url": str,
        }

    Falls back to cached DB rows on any error.
    """
    source_url = "https://chat.lmsys.org"
    try:
        resp = requests.get(_ARENA_LEADERBOARD_URL, timeout=15)
        resp.raise_for_status()

        data = resp.json()
        # The JSON structure varies; handle both list-of-dicts and nested formats.
        entries = data if isinstance(data, list) else data.get("leaderboard_table_df", [])

        results: list[dict[str, Any]] = []
        for entry in entries:
            model_name: str = (
                entry.get("model_name") or entry.get("Model") or entry.get("model", "")
            ).strip()
            elo = entry.get("rating") or entry.get("Elo") or entry.get("elo")
            if not model_name or elo is None:
                continue
            results.append(
                {
                    "model_name": model_name,
                    "benchmark_name": "Chatbot Arena Elo",
                    "score": float(elo),
                    "score_type": "elo",
                    "source_url": source_url,
                }
            )

        if not results:
            raise RuntimeError("Arena leaderboard JSON returned no usable rows.")

        logger.info("fetch_arena_elo: fetched Elo for %d models.", len(results))
        return results

    except Exception as exc:
        logger.warning(
            "fetch_arena_elo: live fetch failed (%s). Falling back to DB cache.", exc
        )
        return _fallback_from_db(db, benchmark_names=["Chatbot Arena Elo"])


# ── Shared DB fallback ─────────────────────────────────────────────────────────

def _fallback_from_db(
    db: Session,
    benchmark_names: list[str],
) -> list[dict[str, Any]]:
    """
    Query the local database for cached scores when a live fetch fails.

    Returns results in the same dict format used by all three fetcher functions.
    """
    try:
        rows = (
            db.query(BenchmarkScore, LLMModel.name)
            .join(LLMModel, LLMModel.id == BenchmarkScore.model_id)
            .filter(BenchmarkScore.benchmark_name.in_(benchmark_names))
            .all()
        )
        cached: list[dict[str, Any]] = []
        for score_row, model_name in rows:
            cached.append(
                {
                    "model_name": model_name,
                    "benchmark_name": score_row.benchmark_name,
                    "score": score_row.score,
                    "score_type": score_row.score_type,
                    "source_url": score_row.source_url or "",
                }
            )
        logger.info(
            "_fallback_from_db: returned %d cached rows for benchmarks %s.",
            len(cached),
            benchmark_names,
        )
        return cached
    except Exception as db_exc:
        logger.error("_fallback_from_db: DB query also failed: %s", db_exc)
        return []
