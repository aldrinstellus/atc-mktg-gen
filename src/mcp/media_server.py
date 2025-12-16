"""
Media MCP Server - Image generation and processing following MCP protocol.

Provides standardized tool interface for:
- Analyzing reference images (style extraction)
- Generating marketing images
- Resizing images for different platforms
"""
from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import base64
import io
from PIL import Image

import google.generativeai as genai


@dataclass
class MCPToolResult:
    """Standard MCP tool result."""
    success: bool
    data: Any
    error: Optional[str] = None


class MediaMCPServer:
    """
    MCP Server for media operations (image generation and processing).

    Following the MCP pattern from YouTube "Agent Factory" reference.
    Uses Gemini for reasoning and Imagen for image generation.
    """

    def __init__(self, api_key: str):
        """
        Initialize Media MCP Server.

        Args:
            api_key: Google AI API key
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)

        # Models
        self.vision_model = genai.GenerativeModel("gemini-2.0-flash-exp")
        self.text_model = genai.GenerativeModel("gemini-2.0-flash-exp")

    # ==================== MCP TOOLS ====================

    def get_tools(self) -> List[Dict]:
        """
        Return list of available tools (MCP discovery).

        Returns:
            List of tool definitions with name, description, parameters
        """
        return [
            {
                "name": "analyze_reference_image",
                "description": "Analyze a reference image to extract visual style information",
                "parameters": {
                    "image_data": {"type": "bytes", "required": True}
                }
            },
            {
                "name": "process_brief",
                "description": "Process a campaign brief and extract structured information",
                "parameters": {
                    "brief": {"type": "string", "required": True},
                    "client_name": {"type": "string", "required": True}
                }
            },
            {
                "name": "generate_image_prompt",
                "description": "Generate an optimized prompt for image generation",
                "parameters": {
                    "brief_data": {"type": "object", "required": True},
                    "brand_data": {"type": "object", "required": True},
                    "style_data": {"type": "object", "required": False},
                    "platform": {"type": "string", "required": False}
                }
            },
            {
                "name": "generate_image",
                "description": "Generate a marketing image using AI",
                "parameters": {
                    "prompt": {"type": "string", "required": True},
                    "width": {"type": "integer", "required": False},
                    "height": {"type": "integer", "required": False}
                }
            },
            {
                "name": "resize_image",
                "description": "Resize an image for a specific platform",
                "parameters": {
                    "image_data": {"type": "bytes", "required": True},
                    "width": {"type": "integer", "required": True},
                    "height": {"type": "integer", "required": True}
                }
            }
        ]

    async def call_tool(self, tool_name: str, **kwargs) -> MCPToolResult:
        """
        Call a tool by name (MCP standard interface).

        Args:
            tool_name: Name of the tool to call
            **kwargs: Tool parameters

        Returns:
            MCPToolResult with success status and data
        """
        tool_map = {
            "analyze_reference_image": self.analyze_reference_image,
            "process_brief": self.process_brief,
            "generate_image_prompt": self.generate_image_prompt,
            "generate_image": self.generate_image,
            "resize_image": self.resize_image
        }

        if tool_name not in tool_map:
            return MCPToolResult(
                success=False,
                data=None,
                error=f"Unknown tool: {tool_name}"
            )

        try:
            result = await tool_map[tool_name](**kwargs)
            return MCPToolResult(success=True, data=result)
        except Exception as e:
            return MCPToolResult(success=False, data=None, error=str(e))

    # ==================== TOOL IMPLEMENTATIONS ====================

    async def analyze_reference_image(self, image_data: bytes) -> Dict:
        """
        Analyze a reference image to extract visual style.

        Args:
            image_data: Raw image bytes

        Returns:
            Style information dictionary
        """
        prompt = """
        Analyze this reference image and extract its visual style for use in generating similar marketing content.

        Return a JSON object with:
        {
            "color_palette": ["list of dominant colors as hex codes"],
            "lighting": "description of lighting style",
            "composition": "composition style description",
            "mood": "overall mood/atmosphere",
            "texture": "texture quality description",
            "style_keywords": ["keyword1", "keyword2", "keyword3"],
            "style_description": "2-3 sentence description of the visual style that can be used in image generation"
        }

        Return ONLY valid JSON, no markdown code blocks or explanation.
        """

        # Create image part for multimodal input
        image_part = {
            "mime_type": "image/jpeg",
            "data": base64.b64encode(image_data).decode("utf-8")
        }

        response = await self.vision_model.generate_content_async([prompt, image_part])
        text = response.text.strip()

        # Clean up response if wrapped in markdown
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])
        if text.startswith("json"):
            text = text[4:].strip()

        import json
        return json.loads(text)

    async def process_brief(self, brief: str, client_name: str) -> Dict:
        """
        Process a campaign brief and extract structured information.

        Args:
            brief: Campaign brief text
            client_name: Name of the client

        Returns:
            Structured brief data
        """
        prompt = f"""
        Analyze this marketing campaign brief for {client_name} and extract structured information.

        Brief: {brief}

        Return a JSON object with:
        {{
            "theme": "main theme (e.g., Christmas, Summer Sale, Product Launch)",
            "mood": "overall mood (e.g., festive, warm, energetic, professional)",
            "key_elements": ["list", "of", "visual", "elements", "to include"],
            "colors_suggested": ["color suggestions based on theme"],
            "headline": "catchy headline text to display prominently on the image (ALWAYS provide one based on campaign)",
            "subheadline": "secondary text like tagline or offer details (can be null)",
            "text_overlay": "combined marketing text for the image",
            "style_keywords": ["keywords", "for", "image", "generation"],
            "target_audience": "who this is for",
            "call_to_action": "what action should viewers take (e.g., Order Now, Shop Today)"
        }}

        IMPORTANT: Always generate compelling marketing text (headline + call_to_action) based on the campaign description.
        For food/restaurant campaigns, suggest appetizing headlines like "Taste the Fusion" or "Fresh & Flavorful".

        Return ONLY valid JSON, no markdown code blocks or explanation.
        """

        response = await self.text_model.generate_content_async(prompt)
        text = response.text.strip()

        # Clean up response
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1])
        if text.startswith("json"):
            text = text[4:].strip()

        import json
        return json.loads(text)

    async def generate_image_prompt(
        self,
        brief_data: Dict,
        brand_data: Dict,
        style_data: Optional[Dict] = None,
        platform: str = "instagram_post"
    ) -> str:
        """
        Generate an optimized prompt for image generation.

        Args:
            brief_data: Processed brief information
            brand_data: Brand guidelines
            style_data: Optional style from reference image
            platform: Target platform

        Returns:
            Optimized image generation prompt
        """
        prompt_parts = []

        # Core description
        prompt_parts.append(f"Professional marketing image for {brand_data.get('name', 'brand')}")

        # Theme and mood
        if brief_data.get("theme"):
            prompt_parts.append(f"Theme: {brief_data['theme']}")
        if brief_data.get("mood"):
            prompt_parts.append(f"Mood: {brief_data['mood']}")

        # Key visual elements
        if brief_data.get("key_elements"):
            elements = ", ".join(brief_data["key_elements"][:5])  # Limit to 5
            prompt_parts.append(f"Include: {elements}")

        # Brand colors (important for consistency)
        if brand_data.get("colors"):
            colors = ", ".join(brand_data["colors"][:3])  # Top 3 colors
            prompt_parts.append(f"Brand colors: {colors}")

        # Brand style guidelines
        if brand_data.get("style"):
            prompt_parts.append(f"Brand style: {brand_data['style']}")

        # Reference style (if provided)
        if style_data:
            if style_data.get("lighting"):
                prompt_parts.append(f"Lighting: {style_data['lighting']}")
            if style_data.get("style_description"):
                prompt_parts.append(f"Visual style: {style_data['style_description']}")

        # Marketing text (IMPORTANT for ads)
        text_elements = []
        if brief_data.get("headline"):
            text_elements.append(f"Headline: '{brief_data['headline']}'")
        if brief_data.get("subheadline"):
            text_elements.append(f"Subheadline: '{brief_data['subheadline']}'")
        if brief_data.get("call_to_action"):
            text_elements.append(f"Call-to-action: '{brief_data['call_to_action']}'")

        if text_elements:
            prompt_parts.append("MUST include bold, readable text overlay with: " + ", ".join(text_elements))
        elif brief_data.get("text_overlay"):
            prompt_parts.append(f"MUST include text overlay: '{brief_data['text_overlay']}'")

        # Quality modifiers
        prompt_parts.append("High quality, professional photography, marketing-ready")
        prompt_parts.append("Clean composition, visually appealing")
        prompt_parts.append("Text should be large, clear, and easy to read against the background")

        return ". ".join(prompt_parts)

    async def generate_image(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1080
    ) -> Optional[bytes]:
        """
        Generate a marketing image using Gemini 2.0 with native image generation.

        Args:
            prompt: Image generation prompt
            width: Target width
            height: Target height

        Returns:
            Generated image bytes or None if failed
        """
        try:
            # Use Gemini 2.0 Flash with image generation capability
            # Configure model with image output modality
            imagen_model = genai.GenerativeModel(
                model_name="gemini-2.0-flash-exp",
                generation_config={"response_modalities": ["TEXT", "IMAGE"]}
            )

            # Check if text is requested in the prompt
            include_text = "MUST include" in prompt and "text" in prompt.lower()

            # Enhanced prompt for image generation
            if include_text:
                enhanced_prompt = f"""Generate a high-quality MARKETING IMAGE with text overlay:

{prompt}

CRITICAL Requirements:
- This is a marketing/advertising image - TEXT IS REQUIRED
- Include all specified text (headline, call-to-action) prominently displayed
- Text must be large, bold, and highly readable
- Use contrasting colors for text visibility
- Professional marketing quality with eye-catching design
- Clean composition with text as a key visual element
- Square format (1:1 aspect ratio)

The text is the most important part of this marketing image. Make it stand out!

Create this marketing image now with the text overlay."""
            else:
                enhanced_prompt = f"""Generate a high-quality marketing image with the following specifications:

{prompt}

Requirements:
- Professional quality suitable for marketing use
- Clean composition with good visual balance
- Vibrant colors and appealing aesthetics
- Square format (1:1 aspect ratio)

Create this image now."""

            response = await imagen_model.generate_content_async(enhanced_prompt)

            # Extract image from response
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if hasattr(part, 'inline_data') and part.inline_data:
                        # Get image data from response
                        raw_data = part.inline_data.data
                        mime_type = getattr(part.inline_data, 'mime_type', 'unknown')

                        print(f"Raw data type: {type(raw_data)}, Length: {len(raw_data) if raw_data else 0}")
                        print(f"MIME type: {mime_type}")

                        # Determine if data is already raw bytes or needs base64 decoding
                        if isinstance(raw_data, str):
                            # String data is definitely base64 encoded
                            image_data = base64.b64decode(raw_data)
                        elif isinstance(raw_data, bytes):
                            # Check if first bytes match known image magic bytes
                            # PNG: \x89PNG, JPEG: \xff\xd8\xff, WebP: RIFF
                            if raw_data[:4] == b'\x89PNG' or raw_data[:3] == b'\xff\xd8\xff' or raw_data[:4] == b'RIFF':
                                # Already raw image bytes
                                image_data = raw_data
                                print("Data is already raw image bytes")
                            else:
                                # Might be base64 bytes - check if ASCII printable
                                try:
                                    # Check first 100 bytes for base64 chars
                                    test_chunk = raw_data[:100]
                                    if all(c < 128 and chr(c) in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=' for c in test_chunk):
                                        image_data = base64.b64decode(raw_data)
                                        print("Decoded base64 bytes")
                                    else:
                                        # Assume raw bytes
                                        image_data = raw_data
                                        print("Using raw bytes (not base64)")
                                except Exception as e:
                                    image_data = raw_data
                                    print(f"Base64 check failed, using raw: {e}")
                        else:
                            image_data = raw_data

                        # Debug: print first bytes
                        if image_data:
                            png_magic = b'\x89PNG'
                            jpeg_magic = b'\xff\xd8\xff'
                            print(f"First 20 bytes after processing: {image_data[:20]}")
                            print(f"Looks like PNG: {image_data[:4] == png_magic}")
                            print(f"Looks like JPEG: {image_data[:3] == jpeg_magic}")

                        # Try to open the image
                        try:
                            img = Image.open(io.BytesIO(image_data))
                            print(f"Successfully opened image: {img.format} {img.size}")
                            if img.size != (width, height):
                                img = img.resize((width, height), Image.Resampling.LANCZOS)

                            img_byte_arr = io.BytesIO()
                            img.save(img_byte_arr, format='PNG')
                            return img_byte_arr.getvalue()
                        except Exception as img_err:
                            print(f"Failed to open image: {img_err}")

                            # Save raw data for debugging
                            try:
                                with open("/tmp/gemini_raw_debug.bin", "wb") as f:
                                    f.write(raw_data if isinstance(raw_data, bytes) else raw_data.encode())
                                with open("/tmp/gemini_processed_debug.bin", "wb") as f:
                                    f.write(image_data)
                                print("Saved debug files to /tmp/gemini_*_debug.bin")
                            except Exception as save_err:
                                print(f"Could not save debug: {save_err}")
                            continue

            # If no image found, log what we got and return placeholder
            if response.candidates:
                print(f"Response parts: {[type(p).__name__ for p in response.candidates[0].content.parts]}")

            print("No valid image in response, using placeholder")
            return self._create_placeholder_image(prompt, width, height)

        except Exception as e:
            print(f"Image generation error: {e}")
            # Return a placeholder image with the prompt
            return self._create_placeholder_image(prompt, width, height)

    def _create_placeholder_image(
        self,
        prompt: str,
        width: int = 1080,
        height: int = 1080
    ) -> bytes:
        """
        Create a placeholder image when AI generation fails.

        Args:
            prompt: The prompt that was used
            width: Image width
            height: Image height

        Returns:
            PNG image bytes
        """
        from PIL import ImageDraw, ImageFont

        # Create a gradient-like background
        img = Image.new('RGB', (width, height), color='#1a1a2e')

        draw = ImageDraw.Draw(img)

        # Draw decorative elements
        # Header bar
        draw.rectangle([0, 0, width, 120], fill='#16213e')

        # Footer bar
        draw.rectangle([0, height - 80, width, height], fill='#16213e')

        # Central decorative circle
        center_x, center_y = width // 2, height // 2
        for i, radius in enumerate([200, 180, 160]):
            alpha = 30 + i * 20
            color = f'#{alpha:02x}{alpha:02x}{alpha + 30:02x}'
            draw.ellipse(
                [center_x - radius, center_y - radius,
                 center_x + radius, center_y + radius],
                outline=color, width=2
            )

        # Try to use a font, fallback to default
        try:
            title_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 48)
            text_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 24)
            small_font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 18)
        except:
            title_font = ImageFont.load_default()
            text_font = title_font
            small_font = title_font

        # Header text
        draw.text((width // 2, 60), "🎨 AI Generated Image",
                  fill='#e94560', font=title_font, anchor='mm')

        # Prompt preview (truncated)
        prompt_preview = prompt[:100] + "..." if len(prompt) > 100 else prompt
        lines = []
        words = prompt_preview.split()
        current_line = ""
        for word in words:
            if len(current_line + " " + word) < 50:
                current_line = (current_line + " " + word).strip()
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        y_offset = center_y - len(lines) * 15
        for line in lines[:4]:  # Max 4 lines
            draw.text((width // 2, y_offset), line,
                      fill='#ffffff', font=text_font, anchor='mm')
            y_offset += 35

        # Footer text
        draw.text((width // 2, height - 40),
                  "Preview • Full generation requires Imagen API",
                  fill='#888888', font=small_font, anchor='mm')

        # Save to bytes
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    async def resize_image(
        self,
        image_data: bytes,
        width: int,
        height: int
    ) -> bytes:
        """
        Resize an image to specific dimensions.

        Args:
            image_data: Original image bytes
            width: Target width
            height: Target height

        Returns:
            Resized image bytes
        """
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))

        # Resize with high quality
        img_resized = img.resize((width, height), Image.Resampling.LANCZOS)

        # Convert back to bytes
        img_byte_arr = io.BytesIO()
        img_resized.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()

    def _get_aspect_ratio(self, width: int, height: int) -> str:
        """Convert dimensions to Imagen aspect ratio string."""
        ratio = width / height

        if abs(ratio - 1) < 0.1:
            return "1:1"
        elif ratio > 1.7:
            return "16:9"
        elif ratio < 0.6:
            return "9:16"
        elif ratio > 1.2:
            return "4:3"
        elif ratio < 0.8:
            return "3:4"
        else:
            return "1:1"  # Default to square
