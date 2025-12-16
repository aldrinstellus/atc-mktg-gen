# Google Cloud Slides Agent Architecture

**Source**: The Agent Factory Podcast (YouTube)
**URL**: https://www.youtube.com/watch?v=XCGbDx7aSks&t=579s
**Hosts**: Vlad Klesnikov & Remy Gustambski (Google Cloud Developer Advocate)
**Image**: `../research-sources/youtube/architecture-diagram.png`
**Extracted**: 2025-12-15

---

## Architecture Overview

This is a reference implementation of a **Slides Agent** that generates presentation decks using Google Cloud infrastructure. The architecture demonstrates modern AI agent patterns with MCP integration.

---

## Visual Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              LOCAL MACHINE                                       │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                  │
│    ┌──────────────┐                                                             │
│    │     User     │                                                             │
│    │   (Browser)  │                                                             │
│    └───────┬──────┘                                                             │
│            │                                                                     │
│            │ Prompt (HTTPS)                                                     │
│            ▼                                                                     │
│    ┌───────────────────┐                                                        │
│    │   Slides Agent    │◄─────────────────┐                                     │
│    │   (Core Logic)    │                  │                                     │
│    └─────────┬─────────┘                  │                                     │
│              │                     ┌──────┴───────┐                             │
│              │ Response            │  Antigravity │                             │
│              ▼                     │  (IDE Tool)  │                             │
│    ┌──────────────┐                └──────────────┘                             │
│    │     User     │                                                             │
│    └──────────────┘                                                             │
│                                                                                  │
└──────────────────────────────────────────────────────────────────────────────────┘
                    │                              │
                    │ Tools                        │ Reasoning
                    │ (Solid blue arrow)           │ (Dashed red arrow)
                    ▼                              ▼
┌──────────────────────────────────────────────────────────────────────────────────┐
│                          GOOGLE CLOUD PROJECT                                     │
├──────────────────────────────────────────────────────────────────────────────────┤
│                                                                                   │
│   ┌─────────────────────────────────────────────────────────────────────────┐    │
│   │                           Cloud Run                                      │    │
│   │                                                                          │    │
│   │    ┌────────────────────────────┐                                       │    │
│   │    │     Media MCP Server       │──────────────────► GCS Bucket         │    │
│   │    │  (Image Gen/Storage API)   │     Save Image     (Object Storage)   │    │
│   │    └────────────────────────────┘                                       │    │
│   │                                                                          │    │
│   └─────────────────────────────────────────────────────────────────────────┘    │
│                         │                                                         │
│                         │ generate_image                                          │
│                         ▼                                                         │
│   ┌─────────────────────────────────────────────────────────────────────────┐    │
│   │                          Vertex AI                                       │    │
│   │                                                                          │    │
│   │    ┌────────────────────────┐    ┌────────────────────────────┐         │    │
│   │    │     Gemini 3 Pro       │    │     Nano Banana Pro        │         │    │
│   │    │     (Red box)          │    │     (Blue box)             │         │    │
│   │    │                        │    │                            │         │    │
│   │    │  - Reasoning           │    │  - Image Generation        │         │    │
│   │    │  - Planning            │    │  - 2K/4K resolution        │         │    │
│   │    │  - Orchestration       │    │  - Text rendering          │         │    │
│   │    │  - Decision making     │    │  - Infographics            │         │    │
│   │    └────────────────────────┘    └────────────────────────────┘         │    │
│   │                                                                          │    │
│   └─────────────────────────────────────────────────────────────────────────┘    │
│                                                                                   │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### Local Machine Components

| Component | Description | Role |
|-----------|-------------|------|
| **User (Browser)** | End user interface | Sends prompts, receives generated presentations |
| **Slides Agent** | Core application | Orchestrates the workflow, processes requests |
| **Antigravity** | Firebase Studio / Project IDX | AI-powered IDE integration for development |

### Google Cloud Components

| Component | Service | Description |
|-----------|---------|-------------|
| **Cloud Run** | Serverless compute | Hosts the Media MCP Server, auto-scaling |
| **Media MCP Server** | MCP implementation | Handles image generation requests and storage |
| **GCS Bucket** | Cloud Storage | Stores generated images for presentations |
| **Vertex AI** | AI Platform | Hosts the AI models |
| **Gemini 3 Pro** | LLM | Reasoning, planning, text generation |
| **Nano Banana Pro** | Image Model | High-quality image generation |

---

## Data Flow

### 1. User Request Flow
```
User (Browser)
      │
      │ Prompt (HTTPS)
      ▼
Slides Agent
      │
      │ Response
      ▼
User (Browser)
```

### 2. Tools Flow (Solid Blue Arrow)
```
Slides Agent ────► Cloud Run ────► Media MCP Server
                                          │
                                          │ Save Image
                                          ▼
                                    GCS Bucket
```

### 3. Reasoning Flow (Dashed Red Arrow)
```
Slides Agent ─ ─ ─► Vertex AI ────► Gemini 3 Pro
       │                                 │
       │                                 │ (Async reasoning)
       ◄─────────────────────────────────┘
```

### 4. Image Generation Flow
```
Media MCP Server
       │
       │ generate_image
       ▼
Vertex AI ────► Nano Banana Pro
                      │
                      │ Generated image
                      ▼
               GCS Bucket (stored)
```

---

## Communication Patterns

### Arrow Types in Diagram

| Arrow Type | Color | Meaning |
|------------|-------|---------|
| **Solid arrows** | Blue | Synchronous tool calls (API requests) |
| **Dashed arrows** | Red | Async reasoning/LLM calls |
| **Thin arrows** | Light blue | Data flow (save image, generate_image) |

### Protocol Details

| Connection | Protocol | Description |
|------------|----------|-------------|
| User ↔ Slides Agent | HTTPS | Secure web requests |
| Slides Agent → Cloud Run | HTTP/gRPC | Internal API calls |
| Slides Agent → Vertex AI | gRPC | Model inference requests |
| MCP Server → GCS | GCS API | Object storage operations |

---

## Technology Stack

### AI Models (Vertex AI)

**Gemini 3 Pro** (Red box in diagram)
- Primary reasoning model
- Handles planning and orchestration
- Text generation for slide content
- Decision making for workflow

**Nano Banana Pro** (Blue box in diagram)
- Specialized image generation
- 2K/4K native resolution
- Excellent text rendering in images
- Can create infographics from content
- Uses Google Search for context

### Infrastructure

**Cloud Run**
- Serverless container platform
- Auto-scaling based on demand
- Pay-per-use pricing
- Zero server management

**GCS Bucket**
- Object storage for generated images
- High availability and durability
- CDN-ready for fast delivery
- Lifecycle management

### Development Tools

**Antigravity (Firebase Studio / Project IDX)**
- AI-powered IDE
- Asynchronous planning agents
- Browser extension for UI testing
- Review policies:
  - `request review` (default)
  - `agent decides`
  - `always proceed` (sandbox)

**Google Cloud Agent Starter Pack**
- Boilerplate code
- Terraform for infrastructure
- Production-ready setup

**ADK (Agent Development Kit)**
- Framework for agent logic
- Orchestration patterns
- Tool integrations

---

## MCP Integration

The **Media MCP Server** implements the Model Context Protocol:

```
┌─────────────────────────────────────────────────────────────────┐
│                      Media MCP Server                            │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Exposed Tools:                                                 │
│  ├── generate_image(prompt, options) → image_url                │
│  ├── save_image(image_data, bucket) → storage_url               │
│  └── list_images(bucket) → image_list                           │
│                                                                  │
│  Connections:                                                    │
│  ├── Vertex AI (Nano Banana Pro) - Image generation             │
│  └── GCS Bucket - Image storage                                 │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Benefits of MCP**:
- Standardized tool interface
- Auto-discovery by agents
- Eliminates connection boilerplate
- Consistent error handling

---

## Implementation Notes

### From the Demo

1. **Planning Mode**: Used planning mode to iterate on implementation before coding
2. **Collaborative Review**: Could comment on plans like a collaborative document
3. **Auto Testing**: Antigravity browser extension automatically tested the agent
4. **Self-Correction**: Agent noticed missing image links and wanted to investigate/fix

### Key Patterns Demonstrated

1. **Separation of Concerns**: Local agent vs cloud services
2. **MCP for Tools**: Standardized tool access
3. **Dual Model Strategy**: Reasoning (Gemini) + Generation (Nano Banana Pro)
4. **Serverless**: Cloud Run for scalable hosting
5. **IDE Integration**: Antigravity for development workflow

---

## Replication Checklist

To build a similar architecture:

- [ ] Set up Google Cloud project
- [ ] Enable Vertex AI APIs
- [ ] Create Cloud Run service for MCP server
- [ ] Create GCS bucket for image storage
- [ ] Implement MCP server with image tools
- [ ] Build Slides Agent with LangGraph/ADK
- [ ] Configure Antigravity for development
- [ ] Set up Terraform for infrastructure

---

## Related Files

| File | Description |
|------|-------------|
| `youtube-agent-factory.md` | Full YouTube reference with all topics |
| `auzmor-ai-agent-principles.md` | Design principles (14 slides) |
| `architecture-diagrams.md` | All architecture diagrams |
| `context-summary.md` | Consolidated context |

---

## Original Source

- **Image**: `../research-sources/youtube/architecture-diagram.png`
- **Notes**: `../research-sources/youtube/transcript-notes.md`
- **Video**: https://www.youtube.com/watch?v=XCGbDx7aSks&t=579s
