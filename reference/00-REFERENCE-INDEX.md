# Reference Index

**Project**: ATC-MKTG-GEN (Marketing Content Generator)
**Location**: `/Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN/reference/`
**Last Updated**: 2025-12-15

---

## Quick Start

```bash
# Load comprehensive context (recommended for new sessions)
cat reference/context-summary.md
```

---

## Reference Files

| File | Size | Description |
|------|------|-------------|
| [context-summary.md](context-summary.md) | ~8KB | **START HERE** - Consolidated context for Claude |
| [auzmor-ai-agent-principles.md](auzmor-ai-agent-principles.md) | ~10KB | All 14 slides parsed with full detail |
| [google-cloud-slides-agent-architecture.md](google-cloud-slides-agent-architecture.md) | ~6KB | Detailed architecture from YouTube demo |
| [youtube-agent-factory.md](youtube-agent-factory.md) | ~4KB | YouTube reference with technologies |
| [architecture-diagrams.md](architecture-diagrams.md) | ~5KB | ASCII diagrams for all architectures |

---

## By Topic

### AI Agent Design
- **Supervisor Pattern**: `auzmor-ai-agent-principles.md` → Section 3
- **Context Engineering**: `auzmor-ai-agent-principles.md` → Section 1
- **Memory Architecture**: `auzmor-ai-agent-principles.md` → Section 5

### Infrastructure
- **Cloud vs Self-Hosted**: `auzmor-ai-agent-principles.md` → Section 9
- **Google Cloud Architecture**: `google-cloud-slides-agent-architecture.md`
- **MCP Protocol**: `auzmor-ai-agent-principles.md` → Section 13

### UX & Safety
- **Human-in-the-Loop**: `auzmor-ai-agent-principles.md` → Section 12
- **Streaming**: `auzmor-ai-agent-principles.md` → Section 14
- **Observability**: `auzmor-ai-agent-principles.md` → Section 6

### Technologies
- **LangGraph**: `auzmor-ai-agent-principles.md` → Section 2, 7
- **Gemini 3 Pro**: `google-cloud-slides-agent-architecture.md`
- **Nano Banana Pro**: `youtube-agent-factory.md`
- **Antigravity/Firebase Studio**: `youtube-agent-factory.md`

---

## Source Materials

### PowerPoint (14 slides)
```
research-sources/presentations/
├── Auzmor AI Agent Design Principles.pptx  # Original file
└── extracted/                               # Extracted JPGs
    ├── slide-01-context-engineering.jpg
    ├── slide-02-core-problem.jpg
    ├── slide-03-team-of-agents.jpg
    ├── slide-04-model-serving.jpg
    ├── slide-05-memory-persistence.jpg
    ├── slide-06-trust-observability.jpg
    ├── slide-07-langgraph-middleware.jpg
    ├── slide-08-small-language-models.jpg
    ├── slide-09-infrastructure-strategy.jpg
    ├── slide-10-building-resilient-agents.jpg
    ├── slide-11-whats-on-horizon.jpg
    ├── slide-12-human-in-the-loop.jpg
    ├── slide-13-tools-capabilities.jpg
    └── slide-14-streaming-rendering.jpg
```

### YouTube Reference
```
research-sources/youtube/
├── architecture-diagram.png    # Architecture screenshot
└── transcript-notes.md         # Transcript notes
```

---

## Loading Context

### For New Sessions
```bash
# Navigate and load context
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN
cat reference/context-summary.md

# Or load specific topics
cat reference/auzmor-ai-agent-principles.md              # All design principles
cat reference/google-cloud-slides-agent-architecture.md  # Google Cloud example
```

### For Specific Tasks
```bash
# Agent architecture planning
cat reference/architecture-diagrams.md

# Technology research
cat reference/youtube-agent-factory.md

# Implementation patterns
cat reference/auzmor-ai-agent-principles.md
```

---

## Cross-Reference Matrix

| Topic | context-summary | auzmor-principles | google-cloud | youtube | diagrams |
|-------|-----------------|-------------------|--------------|---------|----------|
| Supervisor Pattern | ✓ | ✓✓ | - | - | ✓ |
| LangGraph | ✓ | ✓✓ | - | - | - |
| MCP Protocol | ✓ | ✓✓ | ✓✓ | ✓ | ✓ |
| HITL | ✓ | ✓✓ | - | - | ✓ |
| Cloud Architecture | ✓ | ✓ | ✓✓ | ✓✓ | ✓✓ |
| Image Generation | - | - | ✓✓ | ✓✓ | - |
| Streaming UX | ✓ | ✓✓ | - | - | - |
| Observability | ✓ | ✓✓ | - | - | - |

**Legend**: ✓ = mentioned, ✓✓ = detailed coverage

---

## File Statistics

| Metric | Value |
|--------|-------|
| Total reference files | 6 |
| Total size | ~33KB |
| Slides parsed | 14 |
| Diagrams | 6 |
| Source files | 3 |

---

**Maintained by**: Claude Code sessions
**Project Type**: Marketing Content Generator
