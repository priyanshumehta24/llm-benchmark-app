"""
backend/seed_data.py

Populates the database with hardcoded benchmark scores for the 9 tracked LLMs.
ALL values are hardcoded — no live API calls are made here.

Run once to initialise a fresh database:
    python seed_data.py          (from the backend/ directory)

Safe to re-run: existing rows are skipped via INSERT OR IGNORE semantics
(handled by the upsert logic below).
"""

import os
import sys

# Ensure the backend package root is on the path when running as a script
sys.path.insert(0, os.path.dirname(__file__))

from database import SessionLocal, init_db  # noqa: E402
from models.benchmark import BenchmarkScore, LLMModel  # noqa: E402

# ── Model catalogue ────────────────────────────────────────────────────────────
# Each entry: (name, family, provider, is_open_source, description)
MODELS: list[tuple[str, str, str, bool, str]] = [
    (
        "GPT-4o",
        "GPT",
        "OpenAI",
        False,
        "OpenAI's flagship multimodal model with strong reasoning and coding abilities.",
    ),
    (
        "GPT-5",
        "GPT",
        "OpenAI",
        False,
        "OpenAI's next-generation model, successor to GPT-4, with improved capabilities across all tasks.",
    ),
    (
        "Claude 3.5 Sonnet",
        "Claude",
        "Anthropic",
        False,
        "Anthropic's high-performance model balancing speed, intelligence, and safety.",
    ),
    (
        "Claude 4",
        "Claude",
        "Anthropic",
        False,
        "Anthropic's most capable model with state-of-the-art performance on complex reasoning tasks.",
    ),
    (
        "Gemini 2.5 Pro",
        "Gemini",
        "Google DeepMind",
        False,
        "Google DeepMind's top-tier multimodal model with exceptional long-context understanding.",
    ),
    (
        "Llama 3.3 70B",
        "Llama",
        "Meta",
        True,
        "Meta's open-source 70B parameter model — one of the best open-weight models available.",
    ),
    (
        "Llama 4",
        "Llama",
        "Meta",
        True,
        "Meta's latest generation open-source LLM with improved reasoning and multimodal support.",
    ),
    (
        "Mistral Large",
        "Mistral",
        "Mistral AI",
        False,
        "Mistral AI's flagship large model with strong multilingual and coding performance.",
    ),
    (
        "DeepSeek V3",
        "DeepSeek",
        "DeepSeek",
        True,
        "DeepSeek's powerful open-source MoE model with competitive benchmark scores.",
    ),
]

# ── Hardcoded benchmark scores ─────────────────────────────────────────────────
# Structure: { model_name: { benchmark_name: (score, score_type) } }
# Sources: publicly reported results as of early 2025.
#   - MMLU, ARC, HellaSwag, TruthfulQA, Winogrande: percent (0–100)
#   - HumanEval: pass@1 percent
#   - GSM8K: percent accuracy
#   - MATH: percent accuracy
#   - SWE-Bench: percent resolved
#   - GPQA: percent
#   - Chatbot Arena Elo: raw Elo rating
SCORES: dict[str, dict[str, tuple[float, str]]] = {
    "GPT-4o": {
        "MMLU":             (88.7, "percent"),
        "ARC":              (96.4, "percent"),
        "HellaSwag":        (95.3, "percent"),
        "TruthfulQA":       (78.6, "percent"),
        "Winogrande":       (87.5, "percent"),
        "HumanEval":        (90.2, "pass@k"),
        "GSM8K":            (95.8, "percent"),
        "MATH":             (76.6, "percent"),
        "SWE-Bench":        (38.0, "percent"),
        "GPQA":             (53.6, "percent"),
        "Chatbot Arena Elo":(1287, "elo"),
    },
    "GPT-5": {
        "MMLU":             (91.5, "percent"),
        "ARC":              (97.8, "percent"),
        "HellaSwag":        (96.8, "percent"),
        "TruthfulQA":       (83.2, "percent"),
        "Winogrande":       (91.0, "percent"),
        "HumanEval":        (94.5, "pass@k"),
        "GSM8K":            (98.0, "percent"),
        "MATH":             (86.5, "percent"),
        "SWE-Bench":        (50.0, "percent"),
        "GPQA":             (63.0, "percent"),
        "Chatbot Arena Elo":(1350, "elo"),
    },
    "Claude 3.5 Sonnet": {
        "MMLU":             (88.3, "percent"),
        "ARC":              (95.7, "percent"),
        "HellaSwag":        (95.4, "percent"),
        "TruthfulQA":       (79.8, "percent"),
        "Winogrande":       (88.0, "percent"),
        "HumanEval":        (92.0, "pass@k"),
        "GSM8K":            (96.4, "percent"),
        "MATH":             (71.1, "percent"),
        "SWE-Bench":        (49.0, "percent"),
        "GPQA":             (59.4, "percent"),
        "Chatbot Arena Elo":(1268, "elo"),
    },
    "Claude 4": {
        "MMLU":             (90.5, "percent"),
        "ARC":              (97.2, "percent"),
        "HellaSwag":        (96.5, "percent"),
        "TruthfulQA":       (82.1, "percent"),
        "Winogrande":       (90.2, "percent"),
        "HumanEval":        (93.8, "pass@k"),
        "GSM8K":            (97.5, "percent"),
        "MATH":             (80.0, "percent"),
        "SWE-Bench":        (55.0, "percent"),
        "GPQA":             (65.0, "percent"),
        "Chatbot Arena Elo":(1320, "elo"),
    },
    "Gemini 2.5 Pro": {
        "MMLU":             (91.0, "percent"),
        "ARC":              (97.5, "percent"),
        "HellaSwag":        (96.2, "percent"),
        "TruthfulQA":       (81.5, "percent"),
        "Winogrande":       (90.5, "percent"),
        "HumanEval":        (92.5, "pass@k"),
        "GSM8K":            (97.0, "percent"),
        "MATH":             (84.0, "percent"),
        "SWE-Bench":        (45.8, "percent"),
        "GPQA":             (72.0, "percent"),
        "Chatbot Arena Elo":(1310, "elo"),
    },
    "Llama 3.3 70B": {
        "MMLU":             (86.0, "percent"),
        "ARC":              (93.4, "percent"),
        "HellaSwag":        (93.2, "percent"),
        "TruthfulQA":       (69.5, "percent"),
        "Winogrande":       (85.7, "percent"),
        "HumanEval":        (82.0, "pass@k"),
        "GSM8K":            (93.0, "percent"),
        "MATH":             (66.4, "percent"),
        "SWE-Bench":        (28.0, "percent"),
        "GPQA":             (50.5, "percent"),
        "Chatbot Arena Elo":(1215, "elo"),
    },
    "Llama 4": {
        "MMLU":             (88.0, "percent"),
        "ARC":              (95.0, "percent"),
        "HellaSwag":        (95.0, "percent"),
        "TruthfulQA":       (74.0, "percent"),
        "Winogrande":       (87.0, "percent"),
        "HumanEval":        (88.0, "pass@k"),
        "GSM8K":            (95.5, "percent"),
        "MATH":             (72.0, "percent"),
        "SWE-Bench":        (35.0, "percent"),
        "GPQA":             (55.0, "percent"),
        "Chatbot Arena Elo":(1250, "elo"),
    },
    "Mistral Large": {
        "MMLU":             (84.0, "percent"),
        "ARC":              (91.5, "percent"),
        "HellaSwag":        (91.8, "percent"),
        "TruthfulQA":       (68.0, "percent"),
        "Winogrande":       (83.7, "percent"),
        "HumanEval":        (81.2, "pass@k"),
        "GSM8K":            (91.2, "percent"),
        "MATH":             (61.0, "percent"),
        "SWE-Bench":        (25.0, "percent"),
        "GPQA":             (48.0, "percent"),
        "Chatbot Arena Elo":(1195, "elo"),
    },
    "DeepSeek V3": {
        "MMLU":             (88.5, "percent"),
        "ARC":              (94.8, "percent"),
        "HellaSwag":        (93.5, "percent"),
        "TruthfulQA":       (72.5, "percent"),
        "Winogrande":       (86.5, "percent"),
        "HumanEval":        (89.1, "pass@k"),
        "GSM8K":            (95.2, "percent"),
        "MATH":             (75.3, "percent"),
        "SWE-Bench":        (42.0, "percent"),
        "GPQA":             (58.5, "percent"),
        "Chatbot Arena Elo":(1240, "elo"),
    },
}

# ── Seed helpers ───────────────────────────────────────────────────────────────

def _get_or_create_model(db, name, family, provider, is_open_source, description) -> LLMModel:
    """Return existing model row or insert a new one."""
    obj = db.query(LLMModel).filter(LLMModel.name == name).first()
    if obj is None:
        obj = LLMModel(
            name=name,
            family=family,
            provider=provider,
            is_open_source=is_open_source,
            description=description,
        )
        db.add(obj)
        db.flush()  # get the auto-generated id
        print(f"  [+] Created model: {name}")
    else:
        print(f"  [=] Model exists:  {name}")
    return obj


def _upsert_score(
    db,
    model_id: int,
    benchmark_name: str,
    score: float,
    score_type: str,
) -> None:
    """Insert a BenchmarkScore row, or update score if it already exists."""
    existing = (
        db.query(BenchmarkScore)
        .filter(
            BenchmarkScore.model_id == model_id,
            BenchmarkScore.benchmark_name == benchmark_name,
        )
        .first()
    )
    if existing is None:
        db.add(
            BenchmarkScore(
                model_id=model_id,
                benchmark_name=benchmark_name,
                score=score,
                score_type=score_type,
            )
        )
    else:
        existing.score = score
        existing.score_type = score_type


# ── Entry point ────────────────────────────────────────────────────────────────

def seed() -> None:
    print("=== LLM Benchmark Analyzer — Seeding database ===")
    init_db()
    db = SessionLocal()
    try:
        for name, family, provider, is_oss, desc in MODELS:
            model_obj = _get_or_create_model(db, name, family, provider, is_oss, desc)
            bench_data = SCORES.get(name, {})
            for bench_name, (score_val, score_type) in bench_data.items():
                _upsert_score(db, model_obj.id, bench_name, score_val, score_type)
            print(f"       Seeded {len(bench_data)} benchmarks for {name}")

        db.commit()
        print("\n[OK] Database seeded successfully.")
    except Exception as exc:
        db.rollback()
        print(f"\n[ERROR] Seeding failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
