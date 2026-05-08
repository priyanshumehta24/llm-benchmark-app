"""
scheduler.py — Phase 5 implementation.
Uses APScheduler to run the scraper job every SCHEDULER_INTERVAL_HOURS hours.
On each run: fetch new scores, compare with DB, update if changed, log to UpdateLog.
"""

import os
import logging
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from dotenv import load_dotenv

from database import SessionLocal
from models.benchmark import LLMModel, BenchmarkScore, UpdateLog
from services.scraper import fetch_hf_leaderboard, fetch_papers_with_code, fetch_arena_elo

load_dotenv()
logger = logging.getLogger(__name__)

# Note: APScheduler requires a scheduler instance.
scheduler = BackgroundScheduler()

def start_scheduler():
    """Initialize and start APScheduler background job."""
    interval_hours = int(os.getenv("SCHEDULER_INTERVAL_HOURS", "24"))
    scheduler.add_job(run_update_job, 'interval', hours=interval_hours)
    # Do not start the scheduler yet as requested
    # scheduler.start()

def run_update_job():
    """The scheduled job: calls scraper, compares with DB, writes UpdateLog."""
    db = SessionLocal()
    status = "failed"
    models_updated = 0
    scores_changed = 0
    
    try:
        # Call all 3 scraper functions sequentially
        hf_scores = fetch_hf_leaderboard(db)
        pwc_scores = fetch_papers_with_code(db)
        arena_scores = fetch_arena_elo(db)
        
        all_new_scores = hf_scores + pwc_scores + arena_scores
        
        models_updated_set = set()
        
        for new_score in all_new_scores:
            model_name = new_score["model_name"]
            benchmark_name = new_score["benchmark_name"]
            score_val = new_score["score"]
            score_type = new_score["score_type"]
            source_url = new_score["source_url"]
            
            # Find or create model
            model = db.query(LLMModel).filter(LLMModel.name == model_name).first()
            if not model:
                model = LLMModel(name=model_name)
                db.add(model)
                db.commit()
                db.refresh(model)
            
            # Find existing score
            existing_score = db.query(BenchmarkScore).filter(
                BenchmarkScore.model_id == model.id,
                BenchmarkScore.benchmark_name == benchmark_name
            ).first()
            
            if existing_score:
                # Compare new score with existing DB value
                if existing_score.score != score_val:
                    existing_score.score = score_val
                    existing_score.score_type = score_type
                    existing_score.source_url = source_url
                    existing_score.fetched_at = datetime.utcnow()
                    scores_changed += 1
                    models_updated_set.add(model.id)
            else:
                # Insert new score if it doesn't exist
                new_db_score = BenchmarkScore(
                    model_id=model.id,
                    benchmark_name=benchmark_name,
                    score=score_val,
                    score_type=score_type,
                    source_url=source_url,
                    fetched_at=datetime.utcnow()
                )
                db.add(new_db_score)
                scores_changed += 1
                models_updated_set.add(model.id)
                
        db.commit()
        models_updated = len(models_updated_set)
        status = "success"
        
    except Exception as e:
        logger.error(f"Error in scheduled update job: {e}")
        db.rollback()
        status = "failed"
    finally:
        # Log to update_logs table
        log_entry = UpdateLog(
            run_at=datetime.utcnow(),
            models_updated=models_updated,
            scores_changed=scores_changed,
            status=status
        )
        db.add(log_entry)
        db.commit()
        db.close()
        
        # Write summary line to CHANGELOG.md
        changelog_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "CHANGELOG.md")
        timestamp_str = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        summary_line = f"- {timestamp_str}: Scheduler run ({status}) - Models updated: {models_updated}, Scores changed: {scores_changed}\n"
        
        try:
            with open(changelog_path, "a", encoding="utf-8") as f:
                f.write(summary_line)
        except Exception as e:
            logger.error(f"Failed to write to CHANGELOG.md: {e}")
