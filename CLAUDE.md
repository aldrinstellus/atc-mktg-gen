# CLAUDE.md - ATC Marketing Content Generator

## Project Overview

**Type**: Marketing Content Generator
**Location**: `/Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN`
**Created**: 2025-12-15

---

## Quick Context Loading

```bash
# Load full context at session start (REQUIRED)
cat reference/context-summary.md

# Load specific references as needed
cat reference/auzmor-ai-agent-principles.md              # AI agent design (14 slides)
cat reference/google-cloud-slides-agent-architecture.md  # Google Cloud example
cat reference/youtube-agent-factory.md                   # YouTube technologies
cat reference/architecture-diagrams.md                   # ASCII diagrams
```

---

## Project Structure

```
ATC-MKTG-GEN/
├── README.md                    # Project overview (GitHub-ready)
├── CLAUDE.md                    # This file - Claude instructions
├── savepoints/                  # Session savepoints with history
│   ├── SAVEPOINT-INDEX.md       # Global index (check latest here)
│   └── YYYY-MM-DD-*.md          # Timestamped savepoints
├── .gitignore                   # Git exclusions
│
├── reference/                   # Parsed research (Claude-ready markdown)
│   ├── 00-REFERENCE-INDEX.md    # Navigation hub
│   ├── context-summary.md       # KEY: Load at session start (~8KB)
│   ├── auzmor-ai-agent-principles.md
│   ├── google-cloud-slides-agent-architecture.md
│   ├── youtube-agent-factory.md
│   └── architecture-diagrams.md
│
├── research-sources/            # Original source materials
│   ├── presentations/
│   │   ├── Auzmor AI Agent Design Principles.pptx
│   │   └── extracted/           # 14 JPG slide images
│   └── youtube/
│       ├── architecture-diagram.png
│       └── transcript-notes.md
│
├── docs/                        # SDLC documentation
│   ├── 00-DOCUMENTATION-INDEX.md
│   ├── architecture/            # ADRs, system design
│   └── guides/                  # How-to documentation
│
└── src/                         # Source code (future)
```

---

## Research Materials Summary

### 1. Auzmor AI Agent Design Principles (14 slides)
**Source**: Sonu Sam, Auzmor
**File**: `reference/auzmor-ai-agent-principles.md`
**Topics**:
- Context Engineering (dynamic instructions, history management)
- LangGraph (cyclic graphs for real-world tasks)
- Team of Agents (supervisor pattern)
- Model Serving (cloud vs self-hosted)
- Memory & Persistence (checkpointers, vector DBs)
- Trust & Observability (Langfuse, deep tracing)
- Middleware (lifecycle hooks, PII safety)
- Small Language Models (SLMs) - pros/cons
- Infrastructure Strategy (OSS vs LangSmith)
- Human-in-the-Loop (HITL)
- Tools & MCP Protocol
- Streaming & Rendering UX

### 2. Google Cloud Slides Agent (YouTube)
**Source**: The Agent Factory - Vlad Klesnikov & Remy Gustambski
**File**: `reference/google-cloud-slides-agent-architecture.md`
**Topics**:
- Antigravity (Firebase Studio/Project IDX)
- Gemini 3 Pro & Nano Banana Pro
- Google Cloud Agent Starter Pack
- MCP Server integration
- Slides Agent architecture

---

## Development Patterns

### AI Agent Best Practices (from research)
1. **Supervisor Pattern**: Single-purpose agents > "God Model"
2. **Configuration-Driven**: Model changes = YAML/JSON config change
3. **Just-in-Time Context**: Inject data only when needed
4. **Checkpointing**: Save state at every step for pause/resume
5. **Observability First**: Deep tracing with Langfuse/LangSmith
6. **Human-in-the-Loop**: Interrupt before sensitive actions

### Context Engineering
- **Dynamic Instructions**: Change prompts based on active node
- **History Management**: Summarize or trim old messages
- **Token Optimization**: Don't stuff prompts with everything

---

## Commands

```bash
# Navigate to project
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN

# View extracted slides
ls research-sources/presentations/extracted/

# View all references
ls reference/

# Check savepoint index
cat savepoints/SAVEPOINT-INDEX.md

# Load context
cat reference/context-summary.md
```

---

## Session Protocol

### Starting a Session
1. Navigate to project: `cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN`
2. Load context: `cat reference/context-summary.md`
3. Check savepoint index: `cat savepoints/SAVEPOINT-INDEX.md`

### During Session
- Reference specific files as needed from `reference/`
- Track progress with todos

### Ending a Session
- Create savepoint (see protocol below)

---

## Savepoint Protocol

**Triggers**: "savepoint", "save progress", "create savepoint"

**Location**: `savepoints/` folder (dedicated, with history tracking)

**Index**: `savepoints/SAVEPOINT-INDEX.md` - always check latest here

**Naming**: `savepoints/YYYY-MM-DD-description.md` (kebab-case)

### Creating a Savepoint

1. Create new file: `savepoints/YYYY-MM-DD-description.md`
2. Update `savepoints/SAVEPOINT-INDEX.md`:
   - Change "Latest Savepoint" link
   - Add row to History table
   - Update "Last Updated" date

### Savepoint Template

```markdown
# SAVEPOINT: ATC-MKTG-GEN

**Created**: [DATE TIME]
**Session**: [BRIEF DESCRIPTION]
**Status**: [In Progress / Complete]

---

## Quick Resume
```bash
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN
cat reference/context-summary.md
cat savepoints/SAVEPOINT-INDEX.md
```

## Session Summary
### What Was Done
[List of accomplishments]

### Files Changed
| File | Action |
|------|--------|
| ... | Created/Modified/Deleted |

## Project State
[Current structure overview]

## Next Steps
- [ ] Task 1
- [ ] Task 2

## Links
| Resource | Path |
|----------|------|
| Context | `../reference/context-summary.md` |
| CLAUDE.md | `../CLAUDE.md` |
| Savepoint Index | `./SAVEPOINT-INDEX.md` |
```

### Finding Savepoints
```bash
# View savepoint index (RECOMMENDED)
cat savepoints/SAVEPOINT-INDEX.md

# List all savepoints
ls -la savepoints/

# Read latest savepoint
cat savepoints/$(ls -t savepoints/*.md | grep -v INDEX | head -1)
```

---

## Key Files Reference

| File | Purpose | When to Load |
|------|---------|--------------|
| `CLAUDE.md` | Project instructions | Auto-loaded by Claude |
| `PROJECT-THEME.md` | Organization standards & audit checklist | Project audits, new project setup |
| `reference/context-summary.md` | Full AI context | Session start (REQUIRED) |
| `reference/00-REFERENCE-INDEX.md` | Reference navigation | Need specific topic |
| `savepoints/SAVEPOINT-INDEX.md` | Savepoint history & links | Resume previous work |
| `README.md` | Project overview | Sharing/GitHub |

---

## Folder Naming Convention

All folders use **kebab-case** (no spaces) for CLI compatibility:
- `research-sources/` (not `research docs/`)
- `presentations/` (not `atc presentation docs/`)
- `extracted/` (not `slides/`)

---

**Last Updated**: 2025-12-15
