"""
Vercel serverless function wrapper for FastAPI app.
"""
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os

app = FastAPI(
    title="ATC Marketing Asset Generator",
    description="AI-powered marketing asset generation API",
    version="1.0.0"
)

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "ATC Marketing Asset Generator",
        "version": "1.0.0",
        "deployment": "vercel"
    }

@app.get("/api/health")
async def health():
    """Health check for API."""
    api_key = os.getenv("GOOGLE_API_KEY", "")
    return {
        "status": "ok",
        "api_key_configured": bool(api_key and len(api_key) > 10)
    }

# Vercel handler
handler = app
