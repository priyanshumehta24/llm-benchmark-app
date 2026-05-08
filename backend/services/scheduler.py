"""
scheduler.py — Phase 5 implementation.
Uses APScheduler to run the scraper job every SCHEDULER_INTERVAL_HOURS hours.
On each run: fetch new scores, compare with DB, update if changed, log to UpdateLog.

Stub for Phase 1. Full implementation in Phase 5.
"""


def start_scheduler():
    """Initialize and start APScheduler background job."""
    raise NotImplementedError("Implemented in Phase 5")


def run_update_job():
    """The scheduled job: calls scraper, compares with DB, writes UpdateLog."""
    raise NotImplementedError("Implemented in Phase 5")
