import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from database import engine
from models.benchmark import Base
from routes import models, benchmarks, recommend, compare, meta

# --- Setup ---
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="LLM Benchmark Analyzer API")

# --- CORS Middleware ---
cors_origins_str = os.getenv("CORS_ORIGINS", "")
origins = [origin.strip() for origin in cors_origins_str.split(",") if origin.strip()]

if not origins:
    origins = ["*"] # fallback if not set

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routers ---
app.include_router(meta.router)
app.include_router(models.router)
app.include_router(benchmarks.router)
app.include_router(recommend.router)
app.include_router(compare.router)

# --- Error Handlers ---

@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: Exception):
    # FastAPI's internal HTTPException for 404 might be handled here 
    # but normally Starlette handles HTTPExceptions automatically.
    # We will override the global 404 behavior just in case for unhandled routes.
    return JSONResponse(
        status_code=404,
        content={"detail": "Resource not found", "error_code": "NOT_FOUND"}
    )

@app.exception_handler(500)
async def custom_500_handler(request: Request, exc: Exception):
    logger.error(f"Internal Server Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error_code": "INTERNAL_ERROR"}
    )
