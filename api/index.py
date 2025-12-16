"""
Vercel serverless function - simple HTTP handler.
"""
from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

        api_key = os.getenv("GOOGLE_API_KEY", "")

        response = {
            "status": "healthy",
            "app": "ATC Marketing Asset Generator",
            "version": "1.0.0",
            "deployment": "vercel",
            "api_key_configured": bool(api_key and len(api_key) > 10),
            "note": "Full API available at localhost:8000. Vercel deployment is for status only."
        }

        self.wfile.write(json.dumps(response).encode())
        return
