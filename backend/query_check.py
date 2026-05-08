import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import SessionLocal
from models.benchmark import LLMModel, BenchmarkScore

db = SessionLocal()

# 1. Total models
model_count = db.query(LLMModel).count()
print("1. llm_models row count: {}".format(model_count))

# 2. Total benchmark scores
score_count = db.query(BenchmarkScore).count()
print("2. benchmark_scores row count: {}".format(score_count))

# 3. Claude 4 scores
print()
print("3. All benchmark scores for Claude 4:")
print("   {:<25} {:>10}  {}".format("Benchmark", "Score", "Type"))
print("   " + "-" * 45)

claude4 = db.query(LLMModel).filter(LLMModel.name == "Claude 4").first()
if claude4:
    scores = (
        db.query(BenchmarkScore)
        .filter(BenchmarkScore.model_id == claude4.id)
        .order_by(BenchmarkScore.benchmark_name)
        .all()
    )
    for s in scores:
        print("   {:<25} {:>10.1f}  {}".format(s.benchmark_name, s.score, s.score_type))
else:
    print("   [Claude 4 not found in DB]")

db.close()
