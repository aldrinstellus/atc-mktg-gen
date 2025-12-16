# Architecture Diagrams

**Extracted**: 2025-12-15
**Sources**: YouTube screenshot, Auzmor presentation slides

---

## 1. Google Cloud Slides Agent Architecture

**Source**: `../research-sources/youtube/architecture-diagram.png`

### Visual Representation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            LOCAL MACHINE                                     │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│    ┌─────────────┐                                                          │
│    │    User     │                                                          │
│    │  (Browser)  │                                                          │
│    └──────┬──────┘                                                          │
│           │                                                                  │
│           │ Prompt (HTTPS)                                                  │
│           │                                                                  │
│           ▼                                                                  │
│    ┌─────────────────┐         ┌─────────────────┐                          │
│    │  Slides Agent   │◄────────│   Antigravity   │                          │
│    │                 │         │  (IDE Helper)   │                          │
│    └────────┬────────┘         └─────────────────┘                          │
│             │                                                                │
│             │ Response                                                       │
│             ▼                                                                │
│    ┌─────────────┐                                                          │
│    │    User     │                                                          │
│    └─────────────┘                                                          │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
              │
              │ Tools (API Calls)
              │
              │ Reasoning (Dashed line = async)
              ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         GOOGLE CLOUD PROJECT                                 │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         Cloud Run                                    │    │
│  │   ┌────────────────────────────────┐                                │    │
│  │   │      Media MCP Server          │────────► GCS Bucket            │    │
│  │   │   (Image Gen/Storage API)      │          (Save Image)          │    │
│  │   └────────────────────────────────┘                                │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                           │                                                  │
│                           │ generate_image                                   │
│                           ▼                                                  │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │                         Vertex AI                                    │    │
│  │                                                                      │    │
│  │   ┌────────────────────┐    ┌────────────────────────┐              │    │
│  │   │   Gemini 3 Pro     │    │   Nano Banana Pro      │              │    │
│  │   │   (Reasoning)      │    │   (Image Generation)   │              │    │
│  │   │                    │    │   - 2K/4K images       │              │    │
│  │   │   - Planning       │    │   - Text rendering     │              │    │
│  │   │   - Orchestration  │    │   - Infographics       │              │    │
│  │   └────────────────────┘    └────────────────────────┘              │    │
│  └─────────────────────────────────────────────────────────────────────┘    │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Component Breakdown

| Component | Type | Purpose |
|-----------|------|---------|
| User (Browser) | Client | Sends prompts, receives presentations |
| Slides Agent | Application | Core agent logic, orchestration |
| Antigravity | IDE Tool | Firebase Studio integration, testing |
| Media MCP Server | Cloud Run Service | Handles image generation requests |
| GCS Bucket | Storage | Stores generated images |
| Gemini 3 Pro | LLM | Reasoning, planning, text generation |
| Nano Banana Pro | Image Model | High-quality image generation |

---

## 2. Supervisor Pattern (Agent Team)

**Source**: Slide 3 - Team of Agents (`slide-03-team-of-agents.jpg`)

```
                    ┌─────────────────────┐
                    │   Supervisor Node   │
                    │       (LLM)         │
                    │  Router / Manager   │
                    └──────────┬──────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │   Coder     │     │ Researcher  │     │  Reviewer   │
    │   Worker    │     │   Worker    │     │   Worker    │
    └─────────────┘     └─────────────┘     └─────────────┘
```

### Flow

```
1. Supervisor delegates task
          │
          ▼
2. Worker executes
          │
          ▼
3. Worker returns output to Supervisor
          │
          ▼
4. Supervisor decides next step or finishes
```

---

## 3. Memory Architecture

**Source**: Slide 5 - Memory & Persistence (`slide-05-memory-persistence.jpg`)

```
┌─────────────────────────────────────────────────────────────────────┐
│                        AGENT MEMORY SYSTEM                           │
├─────────────────────────────────┬───────────────────────────────────┤
│       SHORT-TERM MEMORY         │       LONG-TERM MEMORY            │
├─────────────────────────────────┼───────────────────────────────────┤
│                                 │                                    │
│   ┌─────────────────────────┐   │   ┌─────────────────────────┐     │
│   │     Checkpointers       │   │   │    Vector Databases     │     │
│   │  - PostgresSaver        │   │   │    Knowledge Graphs     │     │
│   │  - RedisSaver           │   │   │                         │     │
│   └─────────────────────────┘   │   └─────────────────────────┘     │
│                                 │                                    │
│   Function:                     │   Function:                        │
│   - Save state at every step    │   - Store user preferences        │
│   - Pause/resume workflows      │   - Store facts across threads    │
│   - Debug & replay              │   - Long-term knowledge           │
│                                 │                                    │
└─────────────────────────────────┴───────────────────────────────────┘
```

---

## 4. Infrastructure Strategy Comparison

**Source**: Slide 9 - Infrastructure Strategy (`slide-09-infrastructure-strategy.jpg`)

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEPLOYMENT OPTIONS                                │
├─────────────────────────────┬───────────────────────────────────────┤
│      SELF-HOSTED (OSS)      │         CLOUD (LangSmith)             │
├─────────────────────────────┼───────────────────────────────────────┤
│                             │                                        │
│   Deployment:               │   Deployment:                         │
│   Docker/K8s                │   Managed Serverless                  │
│   (Control plane required)  │   (Zero infrastructure)               │
│                             │                                        │
│   Data Privacy:             │   Data Privacy:                       │
│   Air-gapped / VPC internal │   SaaS Compliance (SOC2)              │
│                             │                                        │
│   Observability:            │   Observability:                      │
│   Custom Setup              │   Native Tracing & Evaluation         │
│   (Jaeger/Langfuse)         │   (Built-in)                          │
│                             │                                        │
│   Maintenance:              │   Maintenance:                        │
│   HIGH                      │   LOW                                 │
│   (DevOps overhead)         │   (Fully Managed)                     │
│                             │                                        │
└─────────────────────────────┴───────────────────────────────────────┘
```

---

## 5. Human-in-the-Loop (HITL) Flow

**Source**: Slide 12 - Human-in-the-Loop (`slide-12-human-in-the-loop.jpg`)

```
┌─────────────────────────────────────────────────────────────────────┐
│                      HITL WORKFLOW                                   │
└─────────────────────────────────────────────────────────────────────┘

    Agent Executing
          │
          ▼
    ┌─────────────┐
    │  Sensitive  │──── No ────► Continue Execution
    │   Action?   │
    └──────┬──────┘
           │
          Yes
           │
           ▼
    ┌─────────────┐
    │ INTERRUPT   │
    │ (Pause)     │
    └──────┬──────┘
           │
           ▼
    ┌─────────────────────────────────────────────────────────────┐
    │                    USER REVIEW                               │
    │                                                              │
    │   ┌──────────────────┐    ┌──────────────────────────────┐  │
    │   │     APPROVE      │    │       EDIT / FEEDBACK        │  │
    │   │                  │    │                              │  │
    │   │ Signal agent to  │    │ Modify state (e.g., edit    │  │
    │   │ continue         │    │ email draft) or provide     │  │
    │   │                  │    │ feedback for replanning     │  │
    │   └────────┬─────────┘    └──────────────┬───────────────┘  │
    │            │                             │                   │
    └────────────┼─────────────────────────────┼───────────────────┘
                 │                             │
                 ▼                             ▼
          Continue Execution            Replan & Execute
```

---

## 6. MCP Protocol Integration

**Source**: Slide 13 - Tools & Capabilities (`slide-13-tools-capabilities.jpg`)

```
┌─────────────────────────────────────────────────────────────────────┐
│                         MCP ARCHITECTURE                             │
└─────────────────────────────────────────────────────────────────────┘

    ┌─────────────┐
    │   Agent     │
    │   (LLM)     │
    └──────┬──────┘
           │
           │ Standardized Interface
           │
           ▼
    ┌─────────────────────────────────────────────────────────────────┐
    │                      MCP SERVER                                  │
    │                                                                  │
    │   Auto-detect and expose tools                                  │
    │   Eliminates connection boilerplate                             │
    │                                                                  │
    └──────────────────────────┬──────────────────────────────────────┘
                               │
           ┌───────────────────┼───────────────────┐
           │                   │                   │
           ▼                   ▼                   ▼
    ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
    │  Database   │     │    APIs     │     │   Storage   │
    │   Tools     │     │   Tools     │     │   Tools     │
    └─────────────┘     └─────────────┘     └─────────────┘
```

---

## Quick Reference

| Diagram | Purpose | Source File |
|---------|---------|-------------|
| Slides Agent Architecture | Full system overview | Screenshot 2025-12-15 |
| Supervisor Pattern | Agent team structure | slide-03 |
| Memory Architecture | State management | slide-05 |
| Infrastructure Comparison | Deployment options | slide-09 |
| HITL Flow | Human oversight | slide-12 |
| MCP Integration | Tool connectivity | slide-13 |

---

## Cross-References

- For detailed principles: See `auzmor-ai-agent-principles.md`
- For YouTube context: See `youtube-agent-factory.md`
- For consolidated context: See `context-summary.md`
