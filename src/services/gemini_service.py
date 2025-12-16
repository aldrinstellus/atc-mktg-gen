"""
Gemini AI Service for text generation and image generation.
Uses Gemini 2.0 Flash for text and Imagen 3 for images.
"""
import google.generativeai as genai
from typing import Optional, List
import base64
import httpx
from pathlib import Path


class GeminiService:
    """Service for interacting with Google's Gemini AI."""

    def __init__(self, api_key: str):
        """Initialize Gemini service with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)

        # Text model for reasoning
        self.text_model = genai.GenerativeModel("gemini-2.0-flash-exp")

        # Vision model for analyzing reference images
        self.vision_model = genai.GenerativeModel("gemini-2.0-flash-exp")

    async def process_brief(self, brief: str, client_name: str) -> dict:
        """
        Process a campaign brief and extract structured information.

        Args:
            brief: The campaign brief text
            client_name: Name of the client

        Returns:
            Structured brief data with theme, mood, elements, etc.
        """
        prompt = f"""
        Analyze this marketing campaign brief for {client_name} and extract structured information.

        Brief: {brief}

        Return a JSON object with:
        {{
            "theme": "main theme (e.g., Christmas, Summer Sale)",
            "mood": "overall mood (e.g., festive, warm, energetic)",
            "key_elements": ["list", "of", "visual", "elements"],
            "colors_suggested": ["color suggestions based on theme"],
            "text_overlay": "suggested text for the image if any",
            "style_keywords": ["keywords", "for", "image", "generation"]
        }}

        Return ONLY valid JSON, no markdown or explanation.
        """

        response = await self.text_model.generate_content_async(prompt)
        text = response.text.strip()

        # Clean up response if wrapped in markdown
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        import json
        return json.loads(text)

    async def analyze_reference_image(self, image_data: bytes) -> dict:
        """
        Analyze a reference image to extract style information.

        Args:
            image_data: Raw image bytes

        Returns:
            Style information extracted from the image
        """
        prompt = """
        Analyze this reference image and extract its visual style for use in generating similar marketing content.

        Return a JSON object with:
        {
            "color_palette": ["list of dominant colors as hex codes or names"],
            "lighting": "description of lighting (e.g., warm golden, cool blue, soft natural)",
            "composition": "composition style (e.g., centered, rule of thirds, close-up)",
            "mood": "overall mood/atmosphere",
            "texture": "texture quality (e.g., clean, grungy, glossy)",
            "style_description": "2-3 sentence description of the visual style"
        }

        Return ONLY valid JSON, no markdown or explanation.
        """

        # Create image part for multimodal input
        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_data).decode("utf-8")
        }

        response = await self.vision_model.generate_content_async([prompt, image_part])
        text = response.text.strip()

        # Clean up response
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        import json
        return json.loads(text)

    async def generate_image_prompt(
        self,
        brief_data: dict,
        brand_data: dict,
        style_data: Optional[dict] = None,
        platform: str = "instagram_post"
    ) -> str:
        """
        Generate an optimized prompt for image generation.

        Args:
            brief_data: Processed brief information
            brand_data: Brand guidelines (colors, style, etc.)
            style_data: Optional style from reference image
            platform: Target platform

        Returns:
            Optimized prompt for image generation
        """
        prompt_parts = []

        # Base description
        prompt_parts.append(f"Professional marketing image for {brand_data.get('name', 'brand')}")
        prompt_parts.append(f"Theme: {brief_data.get('theme', 'promotional')}")
        prompt_parts.append(f"Mood: {brief_data.get('mood', 'professional')}")

        # Key elements
        if brief_data.get("key_elements"):
            elements = ", ".join(brief_data["key_elements"])
            prompt_parts.append(f"Featuring: {elements}")

        # Brand colors
        if brand_data.get("colors"):
            colors = ", ".join(brand_data["colors"])
            prompt_parts.append(f"Brand colors: {colors}")

        # Style from reference
        if style_data:
            prompt_parts.append(f"Lighting: {style_data.get('lighting', 'professional')}")
            prompt_parts.append(f"Style: {style_data.get('style_description', '')}")

        # Text overlay if any
        if brief_data.get("text_overlay"):
            prompt_parts.append(f"Include text: '{brief_data['text_overlay']}'")

        # Quality modifiers
        prompt_parts.append("High quality, professional photography")
        prompt_parts.append("Clean composition, marketing-ready")

        return ". ".join(prompt_parts)

    async def generate_image(self, prompt: str, size: dict) -> Optional[bytes]:
        """
        Generate an image using Imagen 3 via Gemini API.

        Args:
            prompt: The image generation prompt
            size: Dict with width and height

        Returns:
            Generated image bytes or None if failed
        """
        try:
            # Use Imagen 3 for image generation
            imagen_model = genai.ImageGenerationModel("imagen-3.0-generate-002")

            response = await imagen_model.generate_images_async(
                prompt=prompt,
                number_of_images=1,
                aspect_ratio=self._get_aspect_ratio(size),
                safety_filter_level="block_few",
                person_generation="allow_adult"
            )

            if response.images:
                return response.images[0]._pil_image
            return None

        except Exception as e:
            print(f"Image generation error: {e}")
            # Fallback: return placeholder or None
            return None

    def _get_aspect_ratio(self, size: dict) -> str:
        """Convert size to Imagen aspect ratio string."""
        width = size.get("width", 1080)
        height = size.get("height", 1080)

        ratio = width / height

        if ratio == 1:
            return "1:1"
        elif ratio > 1.5:
            return "16:9"
        elif ratio < 0.7:
            return "9:16"
        else:
            return "4:3"
