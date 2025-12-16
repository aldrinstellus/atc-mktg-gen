# ATC-MKTG-GEN Complete Project Log

**Project**: ATC Marketing Asset Generator v1.0
**Created**: 2025-12-15
**Status**: V1.0 Complete - Running on localhost:8000 (API) / localhost:8501 (UI)

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Session Timeline](#2-session-timeline)
3. [Architecture Overview](#3-architecture-overview)
4. [Source Code Documentation](#4-source-code-documentation)
5. [All Savepoints](#5-all-savepoints)
6. [Research Materials](#6-research-materials)
7. [Configuration Files](#7-configuration-files)
8. [API Documentation](#8-api-documentation)
9. [Next Steps](#9-next-steps)

---

## 1. Executive Summary

### What Was Built
A complete AI-powered marketing asset generator with:
- **FastAPI backend** with REST endpoints
- **Streamlit frontend** for team access
- **LangGraph supervisor agent** for workflow orchestration
- **MCP server architecture** (Drive + Media servers)
- **Google Gemini + Imagen** integration for AI generation
- **Google Drive** integration for asset storage

### Quick Start
```bash
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN
source venv/bin/activate
./run.sh
# Access: http://localhost:8501 (UI) | http://localhost:8000/docs (API)
```

### File Count
| Category | Count |
|----------|-------|
| Source Python files | 7 |
| Documentation files | 20+ |
| Reference files | 6 |
| Savepoints | 6 |
| Total markdown content | 4,000+ lines |

---

## 2. Session Timeline

### Phase 1: Research & Setup (Session 1)
1. Extracted 14 slides from `Auzmor AI Agent Design Principles.pptx`
2. Parsed slides via Claude vision into structured markdown
3. Created comprehensive reference documentation (~33KB)
4. Set up initial folder structure with kebab-case naming
5. Created CLAUDE.md with project instructions

### Phase 2: Structure & Audits (Session 1 continued)
6. Renamed folders to CLI-friendly kebab-case
7. Created README.md, .gitignore
8. Created dedicated savepoints/ folder with INDEX
9. Full spectrum audit - verified all files, links, cross-references
10. Created PROJECT-THEME.md (605-line reusable template)

### Phase 3: Architecture Planning (Session 2)
11. Analyzed research materials for architecture fit
12. Confirmed YouTube "Slides Agent" architecture maps perfectly
13. User decisions: Imagen, Burgers & Curries, Google Workspace auth
14. Created implementation plan (4 phases)
15. Created architecture diagrams

### Phase 4: V1.0 Implementation (Session 2 continued)
16. Created src/config.py - Configuration settings
17. Created src/mcp/drive_server.py - Google Drive MCP server
18. Created src/mcp/media_server.py - Media generation MCP server
19. Created src/agent/supervisor.py - LangGraph supervisor agent
20. Created src/api/main.py - FastAPI backend
21. Created src/ui/app.py - Streamlit frontend
22. Created Docker and deployment files

### Phase 5: Testing & Verification (Session 3 - Current)
23. Installed Python dependencies (50+ packages)
24. Started dev servers (API + UI)
25. Verified API endpoints working
26. Verified UI rendering in Chrome
27. Created savepoint with running state

---

## 3. Architecture Overview

### System Diagram
```
┌─────────────────────────────────────────────────────────────────┐
│                    STREAMLIT UI (Frontend)                       │
│                 http://localhost:8501                           │
│   - Client selector, brief input, platform selection            │
│   - Reference image upload                                       │
│   - Generated asset preview + download                          │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FASTAPI (Backend API)                         │
│                 http://localhost:8000                           │
│   Endpoints:                                                     │
│   - GET  /                    Health check                       │
│   - GET  /api/clients         List clients                       │
│   - GET  /api/clients/{id}/brand  Get brand assets              │
│   - GET  /api/platforms       List platform sizes                │
│   - POST /api/generate        Generate marketing asset           │
│   - POST /api/analyze-reference  Analyze reference image         │
└─────────────────────────────────────────────────────────────────┘
         │                              │
         ▼                              ▼
┌─────────────────────┐      ┌─────────────────────┐
│   DRIVE MCP SERVER  │      │   MEDIA MCP SERVER  │
│   (Google Drive)    │      │   (Gemini + Imagen) │
│                     │      │                     │
│   Tools:            │      │   Tools:            │
│   - list_clients    │      │   - process_brief   │
│   - get_brand_assets│      │   - analyze_reference│
│   - get_past_campaigns│    │   - generate_prompt │
│   - save_image      │      │   - generate_image  │
│   - download_ref    │      │   - resize_image    │
└─────────────────────┘      └─────────────────────┘
```

### Workflow (5 Steps)
```
1. USER → Opens website, selects client, enters campaign brief
2. AGENT → Brief Processor parses brief into structured data
3. AGENT → Brand Retriever fetches brand assets (colors, style, guidelines)
4. AGENT → Reference Analyzer extracts style from optional reference image
5. AGENT → Image Generator creates marketing asset, saves to Drive
```

### Technology Stack
| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| Backend | FastAPI + Python 3.9 |
| Agent Framework | LangGraph |
| Text AI | Gemini 2.0 Flash |
| Image AI | Imagen 3 |
| Storage | Google Drive API |
| Deployment | Docker + Cloud Run |

---

## 4. Source Code Documentation

### 4.1 src/config.py (56 lines)
Configuration settings using Pydantic Settings:
- Environment variable loading from .env
- Platform sizes for social media (Instagram, Facebook, LinkedIn, Twitter)
- Default clients list

### 4.2 src/mcp/drive_server.py (333 lines)
Google Drive MCP Server following standardized tool interface:

**Tools:**
| Tool | Description |
|------|-------------|
| `list_clients` | List all available clients |
| `get_brand_assets` | Get brand colors, style, guidelines |
| `get_past_campaigns` | Get reference images from past campaigns |
| `save_image` | Save generated image to Drive |
| `download_reference` | Download reference image |

**Features:**
- Mock mode for development without real Drive connection
- Real Drive implementation ready for production
- MCP-compliant tool discovery via `get_tools()`

### 4.3 src/mcp/media_server.py (378 lines)
Media MCP Server for AI operations:

**Tools:**
| Tool | Description |
|------|-------------|
| `analyze_reference_image` | Extract style from reference (Gemini Vision) |
| `process_brief` | Parse campaign brief into structured data |
| `generate_image_prompt` | Build optimized prompt from brief + brand + style |
| `generate_image` | Generate image via Imagen 3 |
| `resize_image` | Resize for different platforms |

**Models Used:**
- `gemini-2.0-flash-exp` for text and vision
- `imagen-3.0-generate-002` for image generation

### 4.4 src/agent/supervisor.py (277 lines)
LangGraph Supervisor Agent implementing workflow:

**Nodes:**
1. `brief_processor` - Parse brief
2. `brand_retriever` - Fetch brand assets
3. `reference_analyzer` - Analyze reference image
4. `prompt_builder` - Build optimized prompt
5. `image_generator` - Generate image
6. `output_manager` - Save to Drive

**State:**
```python
class AgentState(TypedDict):
    client_id: str
    brief: str
    platform: str
    reference_image: Optional[bytes]
    brief_data: Optional[dict]
    brand_data: Optional[dict]
    style_data: Optional[dict]
    image_prompt: Optional[str]
    generated_image: Optional[bytes]
    saved_path: Optional[str]
    error: Optional[str]
    messages: Sequence[str]
    next_step: str
```

### 4.5 src/api/main.py (344 lines)
FastAPI backend with REST endpoints:

**Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Health check |
| GET | `/api/clients` | List clients |
| GET | `/api/clients/{id}/brand` | Get brand assets |
| GET | `/api/clients/{id}/campaigns` | Get past campaigns |
| GET | `/api/platforms` | List platform sizes |
| POST | `/api/generate` | Generate marketing asset |
| POST | `/api/analyze-reference` | Analyze reference image |

**Request/Response Models:**
- `GenerateRequest` - client_id, brief, platform, reference_image_base64
- `GenerateResponse` - success, image_base64, saved_path, brief_data, prompt_used, messages, error

### 4.6 src/ui/app.py (338 lines)
Streamlit frontend:

**Features:**
- Client selection dropdown with brand preview
- Platform selection with size info
- Campaign brief text area
- Reference image upload with preview
- Generate button with progress feedback
- Generated asset display with download button
- Process log expander for debugging

**Styling:**
- Custom CSS for professional look
- Blue theme (#1E3A8A primary)
- Success/error/info boxes
- Dashed placeholder for empty state

---

## 5. All Savepoints

### Savepoint Index
| Date | Name | Status | Summary |
|------|------|--------|---------|
| 2025-12-15 | v1-app-running | In Progress | V1.0 complete, services on localhost:8000/8501 |
| 2025-12-15 | architecture-planning | Complete | Architecture design, workflow diagrams |
| 2025-12-15 | session-complete | Complete | Full session - setup, audits, theme |
| 2025-12-15 | final-audit | Complete | Final audit + PROJECT-THEME.md |
| 2025-12-15 | audit-complete | Complete | Full spectrum audit - all checks passed |
| 2025-12-15 | bulletproof | Complete | CLI-friendly restructure |

### Latest Savepoint: v1-app-running
- FastAPI running on http://localhost:8000
- Streamlit running on http://localhost:8501
- All endpoints verified working
- UI rendered in Chrome
- Next: Add GOOGLE_API_KEY for real image generation

---

## 6. Research Materials

### 6.1 Auzmor AI Agent Design Principles (14 slides)
| Slide | Topic | Key Concepts |
|-------|-------|--------------|
| 1 | Context Engineering | Dynamic instructions, history management, JIT context |
| 2 | Core Problem | DAGs vs LangGraph cyclic graphs |
| 3 | Team of Agents | Supervisor pattern > "God Model" |
| 4 | Model Serving | Cloud vs self-hosted, config-driven |
| 5 | Memory & Persistence | Checkpointers, vector DBs |
| 6 | Trust & Observability | Langfuse, deep tracing |
| 7 | LangGraph Middleware | Lifecycle hooks, PII safety |
| 8 | Small Language Models | SLMs pros/cons, quantization |
| 9 | Infrastructure Strategy | OSS vs LangSmith |
| 10 | Building Resilient Agents | Title slide |
| 11 | What's on Horizon | Evals, CI/CD for AI, fine-tuning |
| 12 | Human-in-the-Loop | HITL patterns, interrupts |
| 13 | Tools & Capabilities | Custom tools, MCP protocol |
| 14 | Streaming & Rendering | UX patterns, markdown |

### 6.2 Google Cloud Slides Agent (YouTube)
- Source: The Agent Factory Podcast
- Architecture: Cloud Run + MCP + Vertex AI
- Perfect fit for marketing asset generation

### Reference Files Location
```
reference/
├── 00-REFERENCE-INDEX.md       (144 lines)
├── context-summary.md          (235 lines) ← Load at session start
├── auzmor-ai-agent-principles.md (351 lines)
├── google-cloud-slides-agent-architecture.md (306 lines)
├── youtube-agent-factory.md    (165 lines)
└── architecture-diagrams.md    (280 lines)
```

---

## 7. Configuration Files

### 7.1 .env
```
GOOGLE_API_KEY=                  # Required for image generation
GOOGLE_SERVICE_ACCOUNT_JSON=     # Optional for Drive
GOOGLE_DRIVE_ROOT_FOLDER_ID=     # Optional for Drive
APP_ENV=development
APP_PORT=8000
STREAMLIT_PORT=8501
```

### 7.2 requirements.txt
```
# Core
fastapi>=0.100.0
uvicorn>=0.20.0
streamlit>=1.28.0
pydantic>=2.0.0
pydantic-settings>=2.0.0

# Google AI
google-generativeai>=0.3.0
langchain-google-genai>=0.0.5

# LangGraph
langgraph>=0.0.20

# Google Drive
google-api-python-client>=2.0.0
google-auth>=2.0.0
google-auth-oauthlib>=1.0.0

# Image processing
Pillow>=10.0.0
aiofiles>=23.0.0

# Utilities
python-dotenv>=1.0.0
python-multipart>=0.0.6
requests>=2.31.0
pytest>=7.0.0
pytest-asyncio>=0.21.0
```

### 7.3 Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000 8501
CMD ["./run.sh"]
```

### 7.4 docker-compose.yml
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - GOOGLE_API_KEY=${GOOGLE_API_KEY}
    command: python -m uvicorn src.api.main:app --host 0.0.0.0 --port 8000

  ui:
    build: .
    ports:
      - "8501:8501"
    environment:
      - API_URL=http://api:8000
    command: streamlit run src/ui/app.py --server.port 8501 --server.address 0.0.0.0
    depends_on:
      - api
```

---

## 8. API Documentation

### Health Check
```bash
curl http://localhost:8000/
# Response: {"status":"healthy","app":"ATC Marketing Asset Generator","version":"1.0.0","timestamp":"..."}
```

### List Clients
```bash
curl http://localhost:8000/api/clients
# Response: [{"id":"burgers-and-curries","name":"Burgers & Curries","description":"Fusion restaurant chain"},...]
```

### Get Brand Assets
```bash
curl http://localhost:8000/api/clients/burgers-and-curries/brand
# Response: {"name":"Burgers & Curries","colors":["#FF5733","#FFC300","#2E4053"],"primary_color":"#FF5733",...}
```

### List Platforms
```bash
curl http://localhost:8000/api/platforms
# Response: {"instagram_post":{"width":1080,"height":1080,"label":"Instagram Post (1:1)"},...}
```

### Generate Asset
```bash
curl -X POST http://localhost:8000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "client_id": "burgers-and-curries",
    "brief": "Christmas promotion for fusion burgers",
    "platform": "instagram_post"
  }'
# Response: {"success":true,"image_base64":"...","saved_path":"...","messages":[...]}
```

### OpenAPI Docs
Visit http://localhost:8000/docs for interactive Swagger documentation.

---

## 9. Next Steps

### Immediate (To Enable Image Generation)
1. [ ] Get Google API Key from https://aistudio.google.com/apikey
2. [ ] Add to .env: `GOOGLE_API_KEY=your_key`
3. [ ] Add to keys.md for documentation
4. [ ] Restart services

### Short Term
5. [ ] Test full generation workflow
6. [ ] Set up Google Drive service account
7. [ ] Upload Burgers & Curries brand assets to Drive
8. [ ] Test Drive integration

### Medium Term
9. [ ] Deploy to Cloud Run for team access
10. [ ] Add authentication (Google Workspace)
11. [ ] Add more clients
12. [ ] Add batch generation

### Long Term
13. [ ] Add Canva integration
14. [ ] Add campaign history/analytics
15. [ ] Add team collaboration features

---

## Quick Reference Commands

```bash
# Start services
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN
source venv/bin/activate
./run.sh

# API only
./run.sh api

# UI only
./run.sh ui

# Docker
./run.sh docker

# Check health
curl http://localhost:8000/

# View logs
cat savepoints/SAVEPOINT-INDEX.md

# Load context
cat reference/context-summary.md
```

---

**Document Generated**: 2025-12-15 14:30 GST
**Total Lines**: ~900
**Status**: Complete project documentation
