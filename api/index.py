"""
Vercel serverless function wrapper for FastAPI app.
"""
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.api.main import app

# Vercel expects 'app' or 'handler' to be exposed
handler = app
