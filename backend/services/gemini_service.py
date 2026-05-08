"""
services/gemini_service.py  —  Phase 3: Use-Case Classifier

Sends user free-text to the Gemini API and returns one of the six
supported use-case category strings.  If the API call fails for any
reason, or if Gemini returns a category we don't recognise, the
function silently returns "general_qa".

Supported categories (must match keys in benchmark_weights.json):
    coding | math_reasoning | general_qa |
    document_analysis | creative_writing | science_research

Environment variable required in backend/.env:
    GEMINI_API_KEY=<your_key>
"""

from __future__ import annotations

import json
import logging
import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────────────────

SUPPORTED_CATEGORIES: list[str] = [
    "coding",
    "math_reasoning",
    "general_qa",
    "document_analysis",
    "creative_writing",
    "science_research",
]

FALLBACK_CATEGORY: str = "general_qa"

_GEMINI_MODEL: str = "gemini-1.5-flash"   # Free-tier, fast, sufficient for classification

# ── Prompt template ────────────────────────────────────────────────────────────

_SYSTEM_PROMPT = """\
You are a task classifier for a Large Language Model recommendation system.

Given a user's description of what they need an LLM for, classify it into
EXACTLY ONE of the following categories:

  - coding            → software development, code generation, debugging, scripts
  - math_reasoning    → mathematics, calculations, proofs, numerical reasoning
  - general_qa        → general questions, factual lookups, conversation, summaries
  - document_analysis → reading, extracting, analysing or summarising documents
  - creative_writing  → stories, essays, poems, marketing copy, creative content
  - science_research  → scientific questions, research papers, technical analysis

Rules:
  1. Reply with ONLY a valid JSON object — no markdown, no extra text.
  2. The JSON must have exactly two keys: "category" and "confidence".
  3. "category" must be one of the six strings listed above.
  4. "confidence" must be a float between 0.0 and 1.0.

Example output:
{"category": "coding", "confidence": 0.95}
"""


# ── Public function ────────────────────────────────────────────────────────────

def classify_use_case(text: str) -> str:
    """
    Classify a free-text use-case description into one of the six supported
    category strings using the Gemini API.

    Parameters
    ----------
    text : str
        The user's natural-language description, e.g.
        "I need a model for writing Python unit tests."

    Returns
    -------
    str
        One of: coding | math_reasoning | general_qa |
                document_analysis | creative_writing | science_research

        Falls back silently to "general_qa" on any error.
    """
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        logger.warning(
            "classify_use_case: GEMINI_API_KEY not set. Falling back to %r.",
            FALLBACK_CATEGORY,
        )
        return FALLBACK_CATEGORY

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name=_GEMINI_MODEL,
            system_instruction=_SYSTEM_PROMPT,
        )

        response = model.generate_content(
            text,
            generation_config=genai.GenerationConfig(
                temperature=0.0,          # Deterministic classification
                max_output_tokens=64,
            ),
        )

        raw_text: str = response.text.strip()

        # Strip accidental markdown fences (```json ... ```)
        if raw_text.startswith("```"):
            raw_text = raw_text.strip("`").lstrip("json").strip()

        parsed: dict = json.loads(raw_text)
        category: str = parsed.get("category", "").strip().lower()

        if category not in SUPPORTED_CATEGORIES:
            logger.warning(
                "classify_use_case: Gemini returned unknown category %r. "
                "Falling back to %r.",
                category,
                FALLBACK_CATEGORY,
            )
            return FALLBACK_CATEGORY

        confidence: float = float(parsed.get("confidence", 0.0))
        logger.info(
            "classify_use_case: classified %r → %r (confidence=%.2f)",
            text[:80],
            category,
            confidence,
        )
        return category

    except json.JSONDecodeError as exc:
        logger.warning(
            "classify_use_case: could not parse Gemini response as JSON (%s). "
            "Falling back to %r.",
            exc,
            FALLBACK_CATEGORY,
        )
        return FALLBACK_CATEGORY

    except Exception as exc:
        logger.warning(
            "classify_use_case: Gemini API call failed (%s). "
            "Falling back to %r.",
            exc,
            FALLBACK_CATEGORY,
        )
        return FALLBACK_CATEGORY
