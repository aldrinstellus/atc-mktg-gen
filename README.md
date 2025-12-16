# ATC Marketing Asset Generator v1.0

**AI-powered marketing asset generation** with Google Gemini, LangGraph agents, and MCP server architecture.

## Features

- **Multi-Client Support**: Generate assets for different brands with unique guidelines
- **Reference Image Styling**: Upload reference images to apply similar aesthetics
- **Platform-Specific Sizing**: Instagram, Facebook, LinkedIn, Twitter
- **Google Drive Integration**: Save directly to organized Drive folders
- **Team Deployment**: Cloud Run URL for team access

## Quick Start

### Prerequisites

- Python 3.11+
- Google Cloud account (for Gemini API)
- Google API Key from [AI Studio](https://aistudio.google.com/apikey)

### Installation

```bash
# Clone/navigate to project
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### Running Locally

```bash
# Option 1: Run both services
./run.sh

# Option 2: Run API only
./run.sh api

# Option 3: Run UI only
./run.sh ui

# Option 4: Docker Compose
./run.sh docker
```

### Access Points

| Service | URL |
|---------|-----|
| **Web UI** | http://localhost:8501 |
| **API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI (Frontend)                       │
│                 http://localhost:8501                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI (Backend API)                         │
│                 http://localhost:8000                           │
└─────────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│   DRIVE MCP SERVER  │      │   MEDIA MCP SERVER  │
│   (Google Drive)    │      │   (Gemini + Imagen) │
└─────────────────────┘      └─────────────────────┘
```

## Project Structure

```
ATC-MKTG-GEN/
├── src/
│   ├── api/              # FastAPI backend
│   │   └── main.py       # Main API endpoints
│   ├── mcp/              # MCP Servers
│   │   ├── drive_server.py   # Google Drive operations
│   │   └── media_server.py   # Image generation
│   ├── agent/            # LangGraph agent
│   │   └── supervisor.py # Supervisor pattern implementation
│   ├── ui/               # Streamlit frontend
│   │   └── app.py        # Main UI
│   └── config.py         # Configuration settings
├── reference/            # Research & documentation
├── requirements.txt      # Python dependencies
├── Dockerfile           # Cloud Run deployment
├── docker-compose.yml   # Local development
├── run.sh               # Run script
├── keys.md              # API keys (not committed)
└── .env                 # Environment variables (not committed)
```

## Usage

### 1. Select Client
Choose from available clients (Burgers & Curries, Tech Startup XYZ, etc.)

### 2. Write Campaign Brief
```
Example: Christmas promotion for our fusion burgers. Festive theme with
warm colors, show our signature burger with holiday decorations.
```

### 3. Upload Reference Image (Optional)
Upload an image with the style/aesthetic you want to match.

### 4. Select Platform
Choose target platform for proper sizing:
- Instagram Post (1080x1080)
- Instagram Story (1080x1920)
- Facebook Post (1200x630)
- LinkedIn Post (1200x627)

### 5. Generate
Click generate and wait for your AI-powered marketing asset!

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/clients` | GET | List available clients |
| `/api/clients/{id}/brand` | GET | Get brand assets |
| `/api/clients/{id}/campaigns` | GET | Get past campaigns |
| `/api/platforms` | GET | List platform sizes |
| `/api/generate` | POST | Generate marketing asset |
| `/api/analyze-reference` | POST | Analyze reference image |

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Gemini API key | Yes |
| `GOOGLE_DRIVE_ROOT_FOLDER_ID` | Drive folder ID | No |
| `GOOGLE_SERVICE_ACCOUNT_JSON` | Service account path | No |

## Technology Stack

| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | FastAPI |
| Agent Framework | LangGraph |
| Text AI | Gemini 2.0 Flash |
| Image AI | Imagen 3 |
| Storage | Google Drive |
| Deployment | Cloud Run |

## Cloud Run Deployment

```bash
# Build and deploy
gcloud run deploy atc-mktg-gen \
  --source . \
  --region us-central1 \
  --set-env-vars GOOGLE_API_KEY=$GOOGLE_API_KEY

# Team gets URL like:
# https://atc-mktg-gen-xxxxx.run.app
```

## Research Foundation

Built on patterns from:
- **Auzmor AI Agent Design Principles** (14 slides)
- **Google Cloud Slides Agent** (YouTube demo)

See `reference/` folder for detailed documentation.

---

**Version**: 1.0.0
**Created**: 2025-12-15
**Status**: MVP Ready
