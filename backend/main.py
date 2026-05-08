import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from database import init_db
from routes.health import router as health_router
from routes.models import router as models_router
from routes.benchmarks import router as benchmarks_router
from routes.recommend import router as recommend_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize the database (create tables) on startup."""
    init_db()
    print("[OK] Database initialized")
    yield
    print("[STOP] Application shutdown")


app = FastAPI(
    title="LLM Model Benchmark Analyzer API",
    description=(
        "Aggregate public LLM benchmark scores, compute weighted use-case scores, "
        "and recommend the best model for a given task."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# ── CORS ──────────────────────────────────────────────────────────────────────
cors_origins_raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")
cors_origins = [origin.strip() for origin in cors_origins_raw.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routes ────────────────────────────────────────────────────────────────────
app.include_router(health_router)
app.include_router(models_router)
app.include_router(benchmarks_router)
app.include_router(recommend_router)


@app.get("/")
def root():
    return {
        "message": "LLM Benchmark Analyzer API",
        "docs": "/docs",
        "health": "/api/health"
    }
