# ATC-MKTG-GEN Context Summary

**Purpose**: Comprehensive context file for Claude to load at session start
**Size**: ~8KB (comprehensive)
**Last Updated**: 2025-12-15

---

## Executive Summary

This project is a **Marketing Content Generator** built using AI agent principles from Auzmor and Google Cloud patterns. The research covers:

1. **AI Agent Architecture** - LangGraph, supervisor patterns, multi-agent systems
2. **Infrastructure** - Cloud vs self-hosted, MCP protocol, observability
3. **UX Patterns** - Streaming, HITL, context management
4. **Implementation** - Google Cloud Slides Agent as reference architecture

---

## Core Principles (10 Key Patterns)

### 1. Supervisor Pattern
```
Single-purpose agents > "God Model"

Supervisor (LLM) → delegates → Worker agents (Coder, Researcher, Reviewer)
Worker → executes → returns output → Supervisor decides next step
```

### 2. Configuration-Driven Model Serving
```yaml
# Change models without code changes
model:
  provider: anthropic  # or openai, google
  name: claude-3-opus

# NOT: client.chat.completions() hardcoded
```

### 3. Context Engineering
- **Dynamic Instructions**: Change prompts based on active node (Coder vs Reviewer)
- **History Management**: Summarize or trim old messages to stay in token limits
- **Just-in-Time**: Inject data only when agent actually needs it

### 4. Memory Architecture
| Type | Mechanism | Purpose |
|------|-----------|---------|
| Short-term | Checkpointers (Postgres/Redis) | Pause/resume, state at every step |
| Long-term | Vector DBs / Knowledge Graphs | User preferences, cross-thread facts |

### 5. Observability First
- **Langfuse** (OSS) or **LangSmith** (Cloud)
- Deep tracing: See every decision, tool call, state change
- Track token usage, costs, latency
- Understand *why* agent made specific choices

### 6. Middleware Pattern
```python
# Centralized handling (not per-node):
- Retries and fallbacks (model switching)
- PII redaction before model calls
- Logging and metrics
```

### 7. Human-in-the-Loop (HITL)
```
Agent executing → Sensitive action? → INTERRUPT → User review
                                                  ├── Approve → Continue
                                                  └── Edit → Replan
```
Sensitive actions: sending email, deploying code, financial transactions

### 8. MCP Protocol for Tools
```
Agent → MCP Server → Auto-detect tools → Database/API/Storage
        (Universal standard, eliminates boilerplate)
```

### 9. Streaming for UX
- **Token Streaming**: Character-by-character for fast "Time to First Byte"
- **Message Streaming**: Full JSON objects for structured data (charts, tables)
- **Markdown Rendering**: Use react-markdown + remark-gfm for proper display

### 10. Small Language Models (SLMs)
| Pros | Cons |
|------|------|
| Fast execution | Lower reasoning ability |
| Low cost | Needs perfect context (RAG) |
| Run on consumer hardware | Prompt-sensitive |
| Specialist tasks (classification) | Struggles with ambiguity |

---

## Reference Architecture: Google Cloud Slides Agent

```
LOCAL                           GOOGLE CLOUD
┌──────────────┐               ┌─────────────────────────────────┐
│ User Browser │               │ Cloud Run                       │
│      │       │               │ ┌─────────────────────────────┐ │
│      ▼       │    Tools      │ │ Media MCP Server            │ │
│ Slides Agent │──────────────►│ └──────────┬──────────────────┘ │
│      ▲       │               │            │ Save Image         │
│ Antigravity  │   Reasoning   │            ▼                    │
│  (IDE)       │◄──────────────│ ┌─────────────────────────────┐ │
└──────────────┘               │ │ Vertex AI                   │ │
                               │ │ - Gemini 3 Pro (reasoning)  │ │
                               │ │ - Nano Banana Pro (images)  │ │
                               │ └─────────────────────────────┘ │
                               │            │                    │
                               │            ▼                    │
                               │ ┌─────────────────────────────┐ │
                               │ │ GCS Bucket (storage)        │ │
                               │ └─────────────────────────────┘ │
                               └─────────────────────────────────┘
```

**Key Technologies**:
- Antigravity (Firebase Studio/Project IDX) - AI-powered IDE
- Gemini 3 Pro - Reasoning and planning
- Nano Banana Pro - 2K/4K image generation with text rendering
- MCP Server - Tool integration standard

---

## Infrastructure Decision Matrix

| Factor | Self-Hosted (OSS) | Cloud (LangSmith) |
|--------|-------------------|-------------------|
| Deployment | Docker/K8s + control plane | Managed serverless |
| Data Privacy | Air-gapped/VPC | SOC2 compliant SaaS |
| Observability | Jaeger/Langfuse setup | Native tracing |
| Maintenance | High DevOps overhead | Low (fully managed) |
| Cost | Lower at scale | Higher but predictable |

---

## Technology Stack Reference

### AI/ML
- **LangGraph**: Stateful, cyclic agent workflows
- **LangChain**: Chain orchestration (simpler DAG workflows)
- **Langfuse**: Open-source observability
- **LangSmith**: Commercial observability (LangChain)

### Models
- **Frontier**: GPT-4, Claude 3.5, Gemini Pro
- **Open-weights**: Llama 3, Mistral
- **Serving**: vLLM, Ollama, TGI

### Infrastructure
- **Orchestration**: Kubernetes, Cloud Run
- **Storage**: PostgreSQL, Redis, Vector DBs (Pinecone, Weaviate)
- **Monitoring**: Prometheus, Grafana, Jaeger

### Standards
- **MCP**: Model Context Protocol - universal tool connections
- **Pydantic**: Schema validation for tool inputs

---

## Implementation Checklist

### Agent Design
- [ ] Define clear agent roles (supervisor + workers)
- [ ] Use configuration-driven model selection
- [ ] Implement checkpointing for state persistence
- [ ] Set up observability from day 1

### Context Management
- [ ] Dynamic system prompts per agent role
- [ ] History summarization/trimming strategy
- [ ] Just-in-time context injection

### Safety & UX
- [ ] HITL interrupts for sensitive actions
- [ ] PII redaction middleware
- [ ] Token streaming for responsiveness
- [ ] Proper markdown rendering

### Infrastructure
- [ ] Choose hosting strategy (self vs cloud)
- [ ] Set up MCP server for tool integrations
- [ ] Configure monitoring and alerting

---

## Glossary

| Term | Definition |
|------|------------|
| **DAG** | Directed Acyclic Graph - linear workflow without loops |
| **LangGraph** | Library for cyclic, stateful agent workflows |
| **Supervisor Pattern** | One manager agent coordinating specialist workers |
| **Checkpointer** | Saves agent state at each step for pause/resume |
| **HITL** | Human-in-the-Loop - human oversight at critical points |
| **MCP** | Model Context Protocol - standard for AI tool connections |
| **SLM** | Small Language Model - efficient but less capable |
| **RAG** | Retrieval Augmented Generation - context injection |
| **Quantization** | Model compression for smaller hardware |

---

## Quick Commands

```bash
# Load this context
cat /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN/reference/context-summary.md

# View specific topics
cat reference/auzmor-ai-agent-principles.md   # Full 14-slide breakdown
cat reference/youtube-agent-factory.md        # Google Cloud example
cat reference/architecture-diagrams.md        # Visual references

# View original slides
ls research-sources/presentations/extracted/
```

---

## File Locations

| File | Path | Content |
|------|------|---------|
| This summary | `reference/context-summary.md` | Consolidated context |
| Agent principles | `reference/auzmor-ai-agent-principles.md` | 14 slides parsed |
| YouTube reference | `reference/youtube-agent-factory.md` | Google Cloud example |
| Architecture | `reference/architecture-diagrams.md` | ASCII diagrams |
| Slide images | `research-sources/presentations/extracted/` | 14 JPGs |
| Original PPTX | `research-sources/presentations/` | Source file |
| YouTube screenshot | `research-sources/youtube/` | Architecture PNG |

---

**Ready for**: Marketing Content Generator development using AI agent patterns
