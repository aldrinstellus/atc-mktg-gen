"""
FastAPI Main Application - ATC Marketing Asset Generator v1.0

Provides REST API endpoints for:
- Client management
- Campaign asset generation
- Reference image handling
"""
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
import os
import io
import base64
from datetime import datetime

# Import our modules
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import get_settings, PLATFORM_SIZES, DEFAULT_CLIENTS
from mcp.drive_server import DriveMCPServer
from mcp.media_server import MediaMCPServer

# Initialize FastAPI app
app = FastAPI(
    title="ATC Marketing Asset Generator",
    description="AI-powered marketing asset generation with Google Drive integration",
    version="1.0.0"
)

# CORS middleware for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global services (initialized on startup)
drive_mcp: Optional[DriveMCPServer] = None
media_mcp: Optional[MediaMCPServer] = None


# ==================== MODELS ====================

class GenerateRequest(BaseModel):
    """Request model for asset generation."""
    client_id: str
    brief: str
    platform: str = "instagram_post"
    reference_image_base64: Optional[str] = None


class GenerateResponse(BaseModel):
    """Response model for asset generation."""
    success: bool
    image_base64: Optional[str] = None
    saved_path: Optional[str] = None
    brief_data: Optional[dict] = None
    prompt_used: Optional[str] = None
    messages: List[str] = []
    error: Optional[str] = None


class ClientResponse(BaseModel):
    """Response model for client info."""
    id: str
    name: str
    description: str


class BrandResponse(BaseModel):
    """Response model for brand assets."""
    name: str
    colors: List[str]
    primary_color: str
    style: str
    tagline: Optional[str] = None


# ==================== STARTUP ====================

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    global drive_mcp, media_mcp

    # Get settings
    try:
        settings = get_settings()
        api_key = settings.google_api_key
    except Exception:
        # Fallback to environment variable
        api_key = os.getenv("GOOGLE_API_KEY", "")

    # Initialize MCP servers
    drive_mcp = DriveMCPServer(mock_mode=True)  # Start in mock mode

    if api_key:
        media_mcp = MediaMCPServer(api_key=api_key)
        print("Media MCP Server initialized with API key")
    else:
        media_mcp = None
        print("Warning: No GOOGLE_API_KEY found, media generation disabled")


# ==================== ENDPOINTS ====================

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "app": "ATC Marketing Asset Generator",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/api/clients", response_model=List[ClientResponse])
async def list_clients():
    """Get list of available clients."""
    if not drive_mcp:
        raise HTTPException(status_code=500, detail="Drive service not initialized")

    result = await drive_mcp.call_tool("list_clients")
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@app.get("/api/clients/{client_id}/brand")
async def get_brand(client_id: str):
    """Get brand assets for a client."""
    if not drive_mcp:
        raise HTTPException(status_code=500, detail="Drive service not initialized")

    result = await drive_mcp.call_tool("get_brand_assets", client_id=client_id)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@app.get("/api/clients/{client_id}/campaigns")
async def get_campaigns(client_id: str):
    """Get past campaigns for a client."""
    if not drive_mcp:
        raise HTTPException(status_code=500, detail="Drive service not initialized")

    result = await drive_mcp.call_tool("get_past_campaigns", client_id=client_id)
    if not result.success:
        raise HTTPException(status_code=500, detail=result.error)

    return result.data


@app.get("/api/platforms")
async def list_platforms():
    """Get list of available platforms with sizes."""
    return PLATFORM_SIZES


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_asset(request: GenerateRequest):
    """
    Generate a marketing asset.

    This is the main endpoint that orchestrates the full workflow:
    1. Process the brief
    2. Get brand assets
    3. Analyze reference image (if provided)
    4. Generate image prompt
    5. Generate image
    6. Save to Drive
    """
    if not media_mcp:
        raise HTTPException(
            status_code=500,
            detail="Media service not initialized. Please set GOOGLE_API_KEY."
        )

    messages = []

    try:
        # Step 1: Process the brief
        messages.append("Processing campaign brief...")
        brief_result = await media_mcp.call_tool(
            "process_brief",
            brief=request.brief,
            client_name=request.client_id
        )
        if not brief_result.success:
            return GenerateResponse(
                success=False,
                error=f"Brief processing failed: {brief_result.error}",
                messages=messages
            )
        brief_data = brief_result.data
        messages.append(f"Brief processed: Theme = {brief_data.get('theme', 'N/A')}")

        # Step 2: Get brand assets
        messages.append("Retrieving brand assets...")
        brand_result = await drive_mcp.call_tool(
            "get_brand_assets",
            client_id=request.client_id
        )
        if not brand_result.success:
            return GenerateResponse(
                success=False,
                error=f"Brand retrieval failed: {brand_result.error}",
                messages=messages
            )
        brand_data = brand_result.data
        messages.append(f"Brand loaded: {brand_data.get('name', 'Unknown')}")

        # Step 3: Analyze reference image (if provided)
        style_data = None
        if request.reference_image_base64:
            messages.append("Analyzing reference image...")
            try:
                image_bytes = base64.b64decode(request.reference_image_base64)
                style_result = await media_mcp.call_tool(
                    "analyze_reference_image",
                    image_data=image_bytes
                )
                if style_result.success:
                    style_data = style_result.data
                    messages.append(f"Style extracted: {style_data.get('mood', 'N/A')}")
                else:
                    messages.append(f"Reference analysis skipped: {style_result.error}")
            except Exception as e:
                messages.append(f"Reference analysis failed: {str(e)}")

        # Step 4: Generate image prompt
        messages.append("Building image prompt...")
        prompt_result = await media_mcp.call_tool(
            "generate_image_prompt",
            brief_data=brief_data,
            brand_data=brand_data,
            style_data=style_data,
            platform=request.platform
        )
        if not prompt_result.success:
            return GenerateResponse(
                success=False,
                error=f"Prompt generation failed: {prompt_result.error}",
                messages=messages
            )
        image_prompt = prompt_result.data
        messages.append("Image prompt generated")

        # Step 5: Generate image
        messages.append("Generating image (this may take a moment)...")
        platform_size = PLATFORM_SIZES.get(request.platform, PLATFORM_SIZES["instagram_post"])
        image_result = await media_mcp.call_tool(
            "generate_image",
            prompt=image_prompt,
            width=platform_size["width"],
            height=platform_size["height"]
        )
        if not image_result.success or not image_result.data:
            return GenerateResponse(
                success=False,
                error=f"Image generation failed: {image_result.error or 'No image returned'}",
                messages=messages,
                prompt_used=image_prompt,
                brief_data=brief_data
            )
        image_bytes = image_result.data
        messages.append("Image generated successfully!")

        # Step 6: Save to Drive
        messages.append("Saving to Google Drive...")
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        theme_slug = brief_data.get("theme", "campaign").lower().replace(" ", "-")
        filename = f"{theme_slug}_{timestamp}.png"

        save_result = await drive_mcp.call_tool(
            "save_image",
            client_id=request.client_id,
            campaign_name=theme_slug,
            platform=request.platform,
            image_data=image_bytes,
            filename=filename
        )

        saved_path = None
        if save_result.success:
            saved_path = save_result.data.get("file_path") or save_result.data.get("web_link")
            messages.append(f"Saved to: {saved_path}")
        else:
            messages.append(f"Save warning: {save_result.error}")

        # Return success response
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")

        return GenerateResponse(
            success=True,
            image_base64=image_base64,
            saved_path=saved_path,
            brief_data=brief_data,
            prompt_used=image_prompt,
            messages=messages
        )

    except Exception as e:
        messages.append(f"Error: {str(e)}")
        return GenerateResponse(
            success=False,
            error=str(e),
            messages=messages
        )


@app.post("/api/analyze-reference")
async def analyze_reference(file: UploadFile = File(...)):
    """Analyze an uploaded reference image."""
    if not media_mcp:
        raise HTTPException(status_code=500, detail="Media service not initialized")

    try:
        contents = await file.read()
        result = await media_mcp.call_tool("analyze_reference_image", image_data=contents)

        if not result.success:
            raise HTTPException(status_code=500, detail=result.error)

        return result.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ==================== RUN ====================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
