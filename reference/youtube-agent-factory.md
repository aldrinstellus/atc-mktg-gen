# YouTube Reference: The Agent Factory

**Source**: The Agent Factory Podcast
**Hosts**: Vlad Klesnikov & Remy Gustambski (Google Cloud Developer Advocate)
**URL**: https://www.youtube.com/watch?v=XCGbDx7aSks&t=579s
**Extracted**: 2025-12-15

---

## Overview

This episode demonstrates building a **Slides Agent** that generates presentation decks using Google Cloud infrastructure and AI tools.

---

## Key Technologies

### 1. Antigravity (Firebase Studio / Project IDX)

**What it is**: AI-powered IDE with asynchronous agents that do planning and coding in the background

**Key Features**:
- Creates implementation plans you can review and comment on before execution
- Has a browser extension for automated UI testing
- Three review policies:
  - `request review` (default) - Human reviews before agent proceeds
  - `agent decides` - Agent determines if review needed
  - `always proceed` (sandbox only) - Full autonomy

**Underlying Model**: Gemini 3 Pro

### 2. Nano Banana Pro (Gemini 3 Pro Image Generation)

**Capabilities**:
- Reasoning capabilities built-in
- Can use Google Search to find information for image generation
- Generates 2K/4K resolution images natively
- Excellent text rendering in images (major improvement over previous models)
- Can create infographics from blog posts by understanding and extracting key information

### 3. Google Cloud Agent Starter Pack

**Purpose**: Provides boilerplate + Terraform for deployment

**Benefits**:
- Reduces setup time
- Production-ready infrastructure
- Scalable architecture out of the box

### 4. ADK (Agent Development Kit)

**Role**: Framework for building the agent logic and orchestration

---

## What They Built: Slides Agent

A presentation generator that:
1. Takes user prompts
2. Generates slide content with AI
3. Creates images for slides using Nano Banana Pro
4. Stores images in GCS (Google Cloud Storage)
5. Returns complete presentation

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LOCAL MACHINE                                    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   User (Browser)                                                        │
│        │                                                                 │
│        │ Prompt (HTTPS)                                                 │
│        ▼                                                                 │
│   ┌─────────────┐                                                       │
│   │ Slides Agent│◄────── Antigravity                                    │
│   └──────┬──────┘        (IDE Integration)                              │
│          │                                                               │
└──────────┼───────────────────────────────────────────────────────────────┘
           │
           │ Tools / Reasoning
           ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      GOOGLE CLOUD PROJECT                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│   ┌────────────────────────────┐                                        │
│   │       Cloud Run            │                                        │
│   │  ┌──────────────────────┐  │                                        │
│   │  │  Media MCP Server    │──┼──────► GCS Bucket                      │
│   │  └──────────────────────┘  │        (Save Image)                    │
│   └────────────────────────────┘                                        │
│                                                                          │
│   ┌────────────────────────────┐                                        │
│   │       Vertex AI            │                                        │
│   │  ┌──────────────┐ ┌──────────────────┐                              │
│   │  │ Gemini 3 Pro │ │ Nano Banana Pro  │                              │
│   │  │  (Reasoning) │ │(Image Generation)│                              │
│   │  └──────────────┘ └──────────────────┘                              │
│   └────────────────────────────┘                                        │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

**Image Reference**: `../research-sources/youtube/architecture-diagram.png`

---

## Data Flow

1. **User Input**: Browser sends prompt via HTTPS to Slides Agent
2. **Agent Processing**: Slides Agent uses Antigravity for IDE-level features
3. **Reasoning**: Agent sends reasoning requests to Gemini 3 Pro (Vertex AI)
4. **Image Generation**: Agent requests images from Nano Banana Pro
5. **Storage**: Media MCP Server saves images to GCS Bucket
6. **Response**: Complete presentation returned to user

---

## Workflow Insights

### Planning Mode
- Used planning mode to iterate on the implementation plan before coding
- Could comment on the plan like a collaborative document
- Review and refine approach before execution

### Automated Testing
- Antigravity automatically tested the agent using its browser extension
- Caught issues like missing image links
- Agent self-corrected and wanted to investigate/fix problems

### MCP Integration
- MCP server handles image generation and storage
- Eliminates boilerplate for cloud service connections
- Standardized interface for tool access

---

## Key Takeaways

1. **Planning First**: Use planning mode to iterate before coding
2. **Visual Quality**: Nano Banana Pro provides excellent image generation with text
3. **Serverless**: Cloud Run for scalable, managed deployment
4. **MCP Standard**: Use MCP for clean tool integrations
5. **Self-Testing**: Browser extensions enable automated UI testing
6. **Human Review**: Configurable review policies for safety

---

## Relevant Links

- YouTube Video: https://www.youtube.com/watch?v=XCGbDx7aSks&t=579s
- Google Cloud Agent Starter Pack: (search for latest)
- Firebase Studio / Project IDX: https://idx.google.com

---

## Cross-References

- For design principles: See `auzmor-ai-agent-principles.md`
- For architecture details: See `architecture-diagrams.md`
- For consolidated context: See `context-summary.md`
