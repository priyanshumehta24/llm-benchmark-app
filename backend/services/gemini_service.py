"""
gemini_service.py — Phase 3 implementation.
Uses Gemini API to classify free-text use-case input into a category.
Supported categories: coding, math_reasoning, general_qa,
                       document_analysis, creative_writing, science_research

Fallback: if Gemini is unavailable or returns unknown category → "general_qa"

Stub for Phase 1. Full implementation in Phase 3.
"""

SUPPORTED_CATEGORIES = [
    "coding",
    "math_reasoning",
    "general_qa",
    "document_analysis",
    "creative_writing",
    "science_research",
]

FALLBACK_CATEGORY = "general_qa"


def classify_use_case(text: str) -> dict:
    """
    Send user text to Gemini API and parse the use-case category.
    Returns: { "category": str, "confidence": float }
    Falls back to general_qa on error.
    """
    raise NotImplementedError("Implemented in Phase 3")
