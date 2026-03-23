import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from app.routes import factcheck
from app.pipeline import extractor, nli

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown logic."""
    # Startup: Load models
    print("Loading ML models...")
    extractor.load()
    nli.load()
    print("All models loaded. Ready to serve requests.")
    yield
    # Shutdown
    print("Shutting down...")


app = FastAPI(lifespan=lifespan)

# Configure CORS
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(factcheck.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}
