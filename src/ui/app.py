"""
Streamlit Frontend - ATC Marketing Asset Generator v1.0

Simple, clean UI for team members to generate marketing assets.
"""
import streamlit as st
import requests
import base64
from io import BytesIO
from PIL import Image
import json

# Configuration
API_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="ATC Marketing Generator",
    page_icon="🎨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1rem;
        color: #6B7280;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        background-color: #D1FAE5;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
    }
    .error-box {
        padding: 1rem;
        background-color: #FEE2E2;
        border-radius: 0.5rem;
        border-left: 4px solid #EF4444;
    }
    .info-box {
        padding: 1rem;
        background-color: #DBEAFE;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
    }
    .stButton > button {
        width: 100%;
        background-color: #1E3A8A;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 0.5rem;
    }
    .stButton > button:hover {
        background-color: #1E40AF;
    }
</style>
""", unsafe_allow_html=True)


def get_api_status():
    """Check if the API is available."""
    try:
        response = requests.get(f"{API_URL}/", timeout=5)
        return response.status_code == 200
    except:
        return False


def get_clients():
    """Fetch list of clients from API."""
    try:
        response = requests.get(f"{API_URL}/api/clients", timeout=10)
        if response.status_code == 200:
            return response.json()
        return []
    except:
        # Return mock data if API is down
        return [
            {"id": "burgers-and-curries", "name": "Burgers & Curries", "description": "Fusion restaurant"},
            {"id": "tech-startup-xyz", "name": "Tech Startup XYZ", "description": "B2B SaaS"},
            {"id": "fashion-brand-abc", "name": "Fashion Brand ABC", "description": "Luxury fashion"}
        ]


def get_platforms():
    """Fetch list of platforms from API."""
    try:
        response = requests.get(f"{API_URL}/api/platforms", timeout=10)
        if response.status_code == 200:
            return response.json()
        return {}
    except:
        return {
            "instagram_post": {"width": 1080, "height": 1080, "label": "Instagram Post (1:1)"},
            "instagram_story": {"width": 1080, "height": 1920, "label": "Instagram Story (9:16)"},
            "facebook_post": {"width": 1200, "height": 630, "label": "Facebook Post"},
            "linkedin_post": {"width": 1200, "height": 627, "label": "LinkedIn Post"},
        }


def get_brand(client_id):
    """Fetch brand assets for a client."""
    try:
        response = requests.get(f"{API_URL}/api/clients/{client_id}/brand", timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None


def generate_asset(client_id, brief, platform, reference_image=None):
    """Call the generate API endpoint."""
    payload = {
        "client_id": client_id,
        "brief": brief,
        "platform": platform
    }

    if reference_image:
        payload["reference_image_base64"] = reference_image

    try:
        response = requests.post(
            f"{API_URL}/api/generate",
            json=payload,
            timeout=120  # 2 minutes timeout for generation
        )
        return response.json()
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try again."}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    """Main Streamlit app."""

    # Header
    st.markdown('<p class="main-header">🎨 ATC Marketing Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">AI-powered marketing asset generation for your brands</p>', unsafe_allow_html=True)

    # API Status
    api_status = get_api_status()
    if not api_status:
        st.warning("⚠️ API is not available. Running in demo mode with mock data.")

    # Sidebar
    with st.sidebar:
        st.header("📋 Configuration")

        # Client Selection
        clients = get_clients()
        client_options = {c["name"]: c["id"] for c in clients}
        selected_client_name = st.selectbox(
            "Select Client",
            options=list(client_options.keys()),
            help="Choose the client/brand for this campaign"
        )
        selected_client_id = client_options.get(selected_client_name, "")

        # Show brand info
        if selected_client_id:
            brand = get_brand(selected_client_id)
            if brand:
                st.markdown("---")
                st.subheader("Brand Info")
                st.write(f"**Style:** {brand.get('style', 'N/A')}")
                if brand.get("colors"):
                    st.write("**Colors:**")
                    cols = st.columns(len(brand["colors"][:4]))
                    for i, color in enumerate(brand["colors"][:4]):
                        with cols[i]:
                            st.markdown(
                                f'<div style="background-color:{color};width:30px;height:30px;border-radius:4px;"></div>',
                                unsafe_allow_html=True
                            )
                            st.caption(color)

        # Platform Selection
        st.markdown("---")
        platforms = get_platforms()
        platform_options = {v["label"]: k for k, v in platforms.items()}
        selected_platform_label = st.selectbox(
            "Target Platform",
            options=list(platform_options.keys()),
            help="Select the social media platform for sizing"
        )
        selected_platform = platform_options.get(selected_platform_label, "instagram_post")

        # Show size info
        if selected_platform and platforms.get(selected_platform):
            size = platforms[selected_platform]
            st.caption(f"Size: {size['width']}x{size['height']}px")

    # Main content area
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("📝 Campaign Brief")

        # Brief input
        brief = st.text_area(
            "Describe your campaign",
            placeholder="Example: Christmas promotion for our fusion burgers. Festive theme with warm colors, show our signature burger with holiday decorations. Target: families looking for holiday dining.",
            height=150,
            help="Be specific about the theme, mood, and key elements you want"
        )

        # Reference image upload
        st.markdown("---")
        st.subheader("🖼️ Reference Image (Optional)")
        st.caption("Upload an image with the style/aesthetic you want to match")

        reference_image_base64 = None
        uploaded_file = st.file_uploader(
            "Upload reference image",
            type=["jpg", "jpeg", "png"],
            help="The AI will analyze this image and apply similar aesthetics"
        )

        if uploaded_file:
            # Display uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Reference Image", use_container_width=True)

            # Convert to base64
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            reference_image_base64 = base64.b64encode(buffered.getvalue()).decode()

        # Generate button
        st.markdown("---")
        generate_clicked = st.button(
            "🎨 Generate Marketing Asset",
            disabled=not brief,
            help="Generate an AI-powered marketing image"
        )

    with col2:
        st.header("🖼️ Generated Asset")

        if generate_clicked and brief:
            with st.spinner("Generating your marketing asset... This may take a minute."):
                # Show progress
                progress_container = st.empty()
                progress_container.info("🔄 Processing campaign brief...")

                # Call API
                result = generate_asset(
                    client_id=selected_client_id,
                    brief=brief,
                    platform=selected_platform,
                    reference_image=reference_image_base64
                )

                # Clear progress
                progress_container.empty()

                # Display result
                if result.get("success"):
                    st.success("✅ Asset generated successfully!")

                    # Display image
                    if result.get("image_base64"):
                        image_data = base64.b64decode(result["image_base64"])
                        image = Image.open(BytesIO(image_data))
                        st.image(image, caption="Generated Marketing Asset", use_container_width=True)

                        # Download button
                        st.download_button(
                            label="⬇️ Download Image",
                            data=image_data,
                            file_name=f"{selected_client_id}_{selected_platform}.png",
                            mime="image/png"
                        )

                    # Show details
                    with st.expander("📋 Generation Details"):
                        if result.get("brief_data"):
                            st.write("**Extracted Brief Data:**")
                            st.json(result["brief_data"])
                        if result.get("prompt_used"):
                            st.write("**Image Prompt Used:**")
                            st.text(result["prompt_used"])
                        if result.get("saved_path"):
                            st.write(f"**Saved to:** {result['saved_path']}")

                    # Show messages
                    if result.get("messages"):
                        with st.expander("📝 Process Log"):
                            for msg in result["messages"]:
                                st.text(f"• {msg}")

                else:
                    st.error(f"❌ Generation failed: {result.get('error', 'Unknown error')}")

                    # Show messages even on failure
                    if result.get("messages"):
                        with st.expander("📝 Process Log"):
                            for msg in result["messages"]:
                                st.text(f"• {msg}")

        else:
            # Placeholder
            st.markdown("""
            <div style="
                border: 2px dashed #CBD5E1;
                border-radius: 8px;
                padding: 4rem 2rem;
                text-align: center;
                color: #94A3B8;
            ">
                <p style="font-size: 3rem; margin-bottom: 1rem;">🎨</p>
                <p style="font-size: 1.2rem; margin-bottom: 0.5rem;">Your generated asset will appear here</p>
                <p style="font-size: 0.9rem;">Fill in the campaign brief and click Generate</p>
            </div>
            """, unsafe_allow_html=True)

    # Footer
    st.markdown("---")
    st.caption("ATC Marketing Asset Generator v1.0 | Powered by Google Gemini & Imagen")


if __name__ == "__main__":
    main()
