"""
Configuration settings for ATC Marketing Asset Generator v1.0
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Google AI (Gemini)
    google_api_key: str = Field(..., env="GOOGLE_API_KEY")

    # Google Drive
    google_service_account_json: Optional[str] = Field(None, env="GOOGLE_SERVICE_ACCOUNT_JSON")
    google_drive_root_folder_id: Optional[str] = Field(None, env="GOOGLE_DRIVE_ROOT_FOLDER_ID")

    # Application
    app_env: str = Field("development", env="APP_ENV")
    app_debug: bool = Field(True, env="APP_DEBUG")
    app_port: int = Field(8000, env="APP_PORT")

    # Streamlit
    streamlit_port: int = Field(8501, env="STREAMLIT_PORT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Platform sizes for social media
PLATFORM_SIZES = {
    "instagram_post": {"width": 1080, "height": 1080, "label": "Instagram Post (1:1)"},
    "instagram_story": {"width": 1080, "height": 1920, "label": "Instagram Story (9:16)"},
    "facebook_post": {"width": 1200, "height": 630, "label": "Facebook Post"},
    "facebook_cover": {"width": 820, "height": 312, "label": "Facebook Cover"},
    "linkedin_post": {"width": 1200, "height": 627, "label": "LinkedIn Post"},
    "twitter_post": {"width": 1200, "height": 675, "label": "Twitter/X Post"},
}

# Default clients (will be populated from Google Drive)
DEFAULT_CLIENTS = [
    {
        "id": "burgers-and-curries",
        "name": "Burgers & Curries",
        "description": "Restaurant chain specializing in fusion cuisine"
    }
]


def get_settings() -> Settings:
    """Get application settings."""
    return Settings()
