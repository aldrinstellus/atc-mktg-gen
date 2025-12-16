"""
Google Drive Service for managing brand assets and generated content.
"""
import os
import json
from typing import Optional, List, Dict
from pathlib import Path
import io

# For local development without Google Drive
MOCK_MODE = True


class DriveService:
    """Service for interacting with Google Drive."""

    def __init__(
        self,
        service_account_json: Optional[str] = None,
        root_folder_id: Optional[str] = None
    ):
        """
        Initialize Drive service.

        Args:
            service_account_json: Path to service account JSON file
            root_folder_id: ID of the root folder in Drive
        """
        self.root_folder_id = root_folder_id
        self.service = None

        if not MOCK_MODE and service_account_json:
            self._init_drive_service(service_account_json)

    def _init_drive_service(self, service_account_json: str):
        """Initialize the Google Drive API service."""
        try:
            from google.oauth2 import service_account
            from googleapiclient.discovery import build

            credentials = service_account.Credentials.from_service_account_file(
                service_account_json,
                scopes=['https://www.googleapis.com/auth/drive']
            )
            self.service = build('drive', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Failed to initialize Drive service: {e}")
            self.service = None

    async def list_clients(self) -> List[Dict]:
        """
        List all clients from the Drive folder structure.

        Returns:
            List of client dictionaries with id, name, description
        """
        if MOCK_MODE or not self.service:
            # Return mock data for development
            return [
                {
                    "id": "burgers-and-curries",
                    "name": "Burgers & Curries",
                    "description": "Fusion restaurant chain",
                    "brand_colors": ["#FF5733", "#FFC300", "#2E4053"],
                    "logo_url": None
                },
                {
                    "id": "tech-startup-xyz",
                    "name": "Tech Startup XYZ",
                    "description": "B2B SaaS company",
                    "brand_colors": ["#3498DB", "#2ECC71", "#FFFFFF"],
                    "logo_url": None
                }
            ]

        # Real implementation would query Drive
        try:
            results = self.service.files().list(
                q=f"'{self.root_folder_id}' in parents and mimeType='application/vnd.google-apps.folder'",
                fields="files(id, name)"
            ).execute()

            clients = []
            for folder in results.get('files', []):
                clients.append({
                    "id": folder['id'],
                    "name": folder['name'],
                    "description": ""
                })
            return clients
        except Exception as e:
            print(f"Error listing clients: {e}")
            return []

    async def get_brand_assets(self, client_id: str) -> Dict:
        """
        Get brand assets for a specific client.

        Args:
            client_id: Client identifier

        Returns:
            Dictionary with brand assets (colors, logo, fonts, etc.)
        """
        if MOCK_MODE or not self.service:
            # Return mock brand data
            mock_brands = {
                "burgers-and-curries": {
                    "name": "Burgers & Curries",
                    "colors": ["#FF5733", "#FFC300", "#2E4053"],
                    "primary_color": "#FF5733",
                    "secondary_color": "#FFC300",
                    "font": "Poppins Bold",
                    "style": "Warm, inviting, fusion cuisine aesthetic",
                    "logo_url": None,
                    "tagline": "Where East Meets West"
                },
                "tech-startup-xyz": {
                    "name": "Tech Startup XYZ",
                    "colors": ["#3498DB", "#2ECC71", "#FFFFFF"],
                    "primary_color": "#3498DB",
                    "secondary_color": "#2ECC71",
                    "font": "Inter",
                    "style": "Modern, clean, professional tech aesthetic",
                    "logo_url": None,
                    "tagline": "Innovate. Scale. Succeed."
                }
            }
            return mock_brands.get(client_id, {
                "name": client_id,
                "colors": ["#333333", "#666666"],
                "style": "Professional"
            })

        # Real implementation would read from Drive
        try:
            # Find brand-assets folder
            # Read colors.json, etc.
            pass
        except Exception as e:
            print(f"Error getting brand assets: {e}")
            return {}

    async def get_past_campaigns(self, client_id: str) -> List[Dict]:
        """
        Get list of past campaigns for reference.

        Args:
            client_id: Client identifier

        Returns:
            List of past campaigns with sample images
        """
        if MOCK_MODE or not self.service:
            return [
                {
                    "id": "summer-2024",
                    "name": "Summer 2024 Campaign",
                    "date": "2024-06-01",
                    "images": []
                },
                {
                    "id": "diwali-2024",
                    "name": "Diwali 2024 Campaign",
                    "date": "2024-10-15",
                    "images": []
                }
            ]

        return []

    async def save_generated_image(
        self,
        client_id: str,
        campaign_name: str,
        platform: str,
        image_data: bytes,
        filename: str
    ) -> Optional[str]:
        """
        Save a generated image to Google Drive.

        Args:
            client_id: Client identifier
            campaign_name: Name of the campaign
            platform: Target platform (instagram, facebook, etc.)
            image_data: Image bytes to save
            filename: Name for the file

        Returns:
            URL or ID of the saved file, or None if failed
        """
        if MOCK_MODE or not self.service:
            # In mock mode, save locally
            local_path = Path(f"./generated/{client_id}/{campaign_name}/{platform}")
            local_path.mkdir(parents=True, exist_ok=True)
            file_path = local_path / filename

            with open(file_path, 'wb') as f:
                f.write(image_data)

            return str(file_path)

        # Real implementation would upload to Drive
        try:
            from googleapiclient.http import MediaIoBaseUpload

            # Create folder structure if needed
            # Upload file
            file_metadata = {
                'name': filename,
                # 'parents': [folder_id]
            }
            media = MediaIoBaseUpload(
                io.BytesIO(image_data),
                mimetype='image/png'
            )
            file = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id, webViewLink'
            ).execute()

            return file.get('webViewLink')
        except Exception as e:
            print(f"Error saving image: {e}")
            return None

    async def download_image(self, file_id: str) -> Optional[bytes]:
        """
        Download an image from Google Drive.

        Args:
            file_id: Drive file ID

        Returns:
            Image bytes or None if failed
        """
        if MOCK_MODE or not self.service:
            return None

        try:
            request = self.service.files().get_media(fileId=file_id)
            # Download logic here
            return None
        except Exception as e:
            print(f"Error downloading image: {e}")
            return None
