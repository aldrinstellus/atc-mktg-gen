"""
LangGraph Supervisor Agent for Marketing Asset Generation.
Implements the supervisor pattern from Auzmor AI Agent principles.
"""
from typing import TypedDict, Annotated, Sequence, Literal, Optional
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
import operator


class AgentState(TypedDict):
    """State passed between agent nodes."""
    # Input
    client_id: str
    brief: str
    platform: str
    reference_image: Optional[bytes]

    # Processed data
    brief_data: Optional[dict]
    brand_data: Optional[dict]
    style_data: Optional[dict]
    image_prompt: Optional[str]

    # Output
    generated_image: Optional[bytes]
    saved_path: Optional[str]
    error: Optional[str]

    # Workflow control
    messages: Annotated[Sequence[str], operator.add]
    next_step: str


class MarketingAssetAgent:
    """
    Supervisor agent that orchestrates the marketing asset generation workflow.

    Workflow:
    1. Brief Processor - Parse and structure the campaign brief
    2. Brand Retriever - Fetch brand assets from Google Drive
    3. Reference Analyzer - Extract style from reference image (optional)
    4. Image Generator - Create the final marketing image
    5. Output Manager - Save to Google Drive
    """

    def __init__(self, gemini_service, drive_service):
        """
        Initialize the agent with required services.

        Args:
            gemini_service: GeminiService instance
            drive_service: DriveService instance
        """
        self.gemini = gemini_service
        self.drive = drive_service
        self.graph = self._build_graph()

    def _build_graph(self) -> StateGraph:
        """Build the LangGraph workflow."""
        workflow = StateGraph(AgentState)

        # Add nodes
        workflow.add_node("brief_processor", self._process_brief)
        workflow.add_node("brand_retriever", self._retrieve_brand)
        workflow.add_node("reference_analyzer", self._analyze_reference)
        workflow.add_node("prompt_builder", self._build_prompt)
        workflow.add_node("image_generator", self._generate_image)
        workflow.add_node("output_manager", self._save_output)

        # Define edges
        workflow.set_entry_point("brief_processor")

        workflow.add_edge("brief_processor", "brand_retriever")
        workflow.add_edge("brand_retriever", "reference_analyzer")
        workflow.add_edge("reference_analyzer", "prompt_builder")
        workflow.add_edge("prompt_builder", "image_generator")
        workflow.add_edge("image_generator", "output_manager")
        workflow.add_edge("output_manager", END)

        return workflow.compile()

    async def _process_brief(self, state: AgentState) -> AgentState:
        """Process the campaign brief and extract structured data."""
        try:
            brief_data = await self.gemini.process_brief(
                state["brief"],
                state.get("client_id", "Unknown")
            )
            return {
                **state,
                "brief_data": brief_data,
                "messages": state.get("messages", []) + ["Brief processed successfully"],
                "next_step": "brand_retriever"
            }
        except Exception as e:
            return {
                **state,
                "error": f"Brief processing failed: {str(e)}",
                "messages": state.get("messages", []) + [f"Error: {str(e)}"]
            }

    async def _retrieve_brand(self, state: AgentState) -> AgentState:
        """Retrieve brand assets from Google Drive."""
        try:
            brand_data = await self.drive.get_brand_assets(state["client_id"])
            return {
                **state,
                "brand_data": brand_data,
                "messages": state.get("messages", []) + [f"Brand assets retrieved for {brand_data.get('name', state['client_id'])}"],
                "next_step": "reference_analyzer"
            }
        except Exception as e:
            return {
                **state,
                "error": f"Brand retrieval failed: {str(e)}",
                "messages": state.get("messages", []) + [f"Error: {str(e)}"]
            }

    async def _analyze_reference(self, state: AgentState) -> AgentState:
        """Analyze reference image if provided."""
        if not state.get("reference_image"):
            return {
                **state,
                "style_data": None,
                "messages": state.get("messages", []) + ["No reference image provided, skipping style analysis"],
                "next_step": "prompt_builder"
            }

        try:
            style_data = await self.gemini.analyze_reference_image(state["reference_image"])
            return {
                **state,
                "style_data": style_data,
                "messages": state.get("messages", []) + ["Reference image analyzed successfully"],
                "next_step": "prompt_builder"
            }
        except Exception as e:
            return {
                **state,
                "style_data": None,
                "messages": state.get("messages", []) + [f"Reference analysis failed (continuing without): {str(e)}"],
                "next_step": "prompt_builder"
            }

    async def _build_prompt(self, state: AgentState) -> AgentState:
        """Build the optimized image generation prompt."""
        try:
            image_prompt = await self.gemini.generate_image_prompt(
                brief_data=state.get("brief_data", {}),
                brand_data=state.get("brand_data", {}),
                style_data=state.get("style_data"),
                platform=state.get("platform", "instagram_post")
            )
            return {
                **state,
                "image_prompt": image_prompt,
                "messages": state.get("messages", []) + ["Image prompt generated"],
                "next_step": "image_generator"
            }
        except Exception as e:
            return {
                **state,
                "error": f"Prompt building failed: {str(e)}",
                "messages": state.get("messages", []) + [f"Error: {str(e)}"]
            }

    async def _generate_image(self, state: AgentState) -> AgentState:
        """Generate the marketing image."""
        from ..config import PLATFORM_SIZES

        try:
            platform = state.get("platform", "instagram_post")
            size = PLATFORM_SIZES.get(platform, PLATFORM_SIZES["instagram_post"])

            generated_image = await self.gemini.generate_image(
                state["image_prompt"],
                size
            )

            if generated_image:
                return {
                    **state,
                    "generated_image": generated_image,
                    "messages": state.get("messages", []) + ["Image generated successfully"],
                    "next_step": "output_manager"
                }
            else:
                return {
                    **state,
                    "error": "Image generation returned None",
                    "messages": state.get("messages", []) + ["Image generation failed"]
                }
        except Exception as e:
            return {
                **state,
                "error": f"Image generation failed: {str(e)}",
                "messages": state.get("messages", []) + [f"Error: {str(e)}"]
            }

    async def _save_output(self, state: AgentState) -> AgentState:
        """Save the generated image to Google Drive."""
        if not state.get("generated_image"):
            return {
                **state,
                "messages": state.get("messages", []) + ["No image to save"]
            }

        try:
            # Generate filename
            import datetime
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            theme = state.get("brief_data", {}).get("theme", "campaign")
            filename = f"{theme.lower().replace(' ', '-')}_{timestamp}.png"

            # Get campaign name from brief
            campaign_name = state.get("brief_data", {}).get("theme", "campaign").lower().replace(" ", "-")

            saved_path = await self.drive.save_generated_image(
                client_id=state["client_id"],
                campaign_name=campaign_name,
                platform=state.get("platform", "instagram_post"),
                image_data=state["generated_image"],
                filename=filename
            )

            return {
                **state,
                "saved_path": saved_path,
                "messages": state.get("messages", []) + [f"Image saved to: {saved_path}"]
            }
        except Exception as e:
            return {
                **state,
                "error": f"Save failed: {str(e)}",
                "messages": state.get("messages", []) + [f"Error: {str(e)}"]
            }

    async def run(
        self,
        client_id: str,
        brief: str,
        platform: str = "instagram_post",
        reference_image: Optional[bytes] = None
    ) -> dict:
        """
        Run the full marketing asset generation workflow.

        Args:
            client_id: Client identifier
            brief: Campaign brief text
            platform: Target platform
            reference_image: Optional reference image bytes

        Returns:
            Final state with generated image and metadata
        """
        initial_state: AgentState = {
            "client_id": client_id,
            "brief": brief,
            "platform": platform,
            "reference_image": reference_image,
            "brief_data": None,
            "brand_data": None,
            "style_data": None,
            "image_prompt": None,
            "generated_image": None,
            "saved_path": None,
            "error": None,
            "messages": ["Starting marketing asset generation workflow"],
            "next_step": "brief_processor"
        }

        # Run the graph
        final_state = await self.graph.ainvoke(initial_state)
        return final_state
