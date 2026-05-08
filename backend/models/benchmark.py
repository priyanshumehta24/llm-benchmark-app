"""
models/benchmark.py

SQLAlchemy ORM models for the LLM Benchmark Analyzer.
Schema matches ARCHITECTURE.md exactly:
  - llm_models        → LLMModel
  - benchmark_scores  → BenchmarkScore
  - update_logs       → UpdateLog
"""

from datetime import datetime
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    Text,
    UniqueConstraint,
)
from database import Base


class LLMModel(Base):
    """Represents a single large language model entry."""

    __tablename__ = "llm_models"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False, unique=True)
    family = Column(Text, nullable=True)               # e.g. "GPT", "Claude", "Llama"
    provider = Column(Text, nullable=True)             # e.g. "OpenAI", "Anthropic"
    is_open_source = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<LLMModel id={self.id} name={self.name!r} provider={self.provider!r}>"


class BenchmarkScore(Base):
    """Stores a single benchmark result for a specific model."""

    __tablename__ = "benchmark_scores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_id = Column(Integer, ForeignKey("llm_models.id"), nullable=False)
    benchmark_name = Column(Text, nullable=False)      # e.g. "MMLU", "HumanEval"
    score = Column(Float, nullable=False)              # raw score (0–100 or Elo)
    score_type = Column(Text, default="percent")       # 'percent' | 'elo' | 'pass@k'
    source_url = Column(Text, nullable=True)
    fetched_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        UniqueConstraint("model_id", "benchmark_name", name="uq_model_benchmark"),
    )

    def __repr__(self) -> str:
        return (
            f"<BenchmarkScore model_id={self.model_id} "
            f"benchmark={self.benchmark_name!r} score={self.score}>"
        )


class UpdateLog(Base):
    """Audit log written after each scheduler run."""

    __tablename__ = "update_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    run_at = Column(DateTime, default=datetime.utcnow)
    models_updated = Column(Integer, nullable=True)
    scores_changed = Column(Integer, nullable=True)
    status = Column(Text, nullable=True)               # 'success' | 'partial' | 'failed'

    def __repr__(self) -> str:
        return f"<UpdateLog id={self.id} status={self.status!r} run_at={self.run_at}>"
