# SAVEPOINT: ATC-MKTG-GEN Architecture Planning

**Created**: 2025-12-15 14:30
**Session**: Architecture planning and workflow verification
**Status**: In Progress (Plan Mode)

---

## Quick Resume

```bash
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN
cat reference/context-summary.md
cat savepoints/SAVEPOINT-INDEX.md
```

---

## Session Summary

### What Was Done

1. **Analyzed existing reference materials**:
   - YouTube "Agent Factory" architecture (Slides Agent)
   - Auzmor AI Agent Design Principles (14 slides)
   - Existing PRD document

2. **Mapped YouTube architecture to use case**:
   - Confirmed PERFECT FIT for marketing asset generator
   - Slides Agent → Marketing Asset Agent
   - GCS Bucket → Google Drive
   - Same: Gemini 3 Pro, Nano Banana Pro, Cloud Run, MCP

3. **User decisions confirmed**:
   | Decision | Answer |
   |----------|--------|
   | Image Generation | Nano Banana Pro (Gemini) |
   | First Client | Burgers & Curries |
   | Drive Structure | Need to set up |
   | Team Auth | Google Workspace |

4. **Created detailed architecture diagrams**:
   - Full system architecture
   - Simple 5-step workflow
   - Data flow explanation

5. **Implementation plan created** (4 phases, ~10 days)

---

## Architecture Overview (Verified)

```
SIMPLE WORKFLOW:
1. Team member opens website → logs in with Google
2. Fills form: client, brief, platform, reference image
3. AI Agent: Brief → Brand → Reference → Generate
4. User reviews images, picks favorites
5. System saves to Google Drive
```

### Key Components
- **Frontend**: Web UI on Cloud Run URL
- **Backend**: Python/FastAPI + LangGraph
- **Agent Workers**: Brief Processor, Brand Retriever, Reference Analyzer, Image Generator
- **MCP Servers**: Drive MCP + Media MCP
- **AI Models**: Gemini 3 Pro (reasoning) + Nano Banana Pro (image gen)
- **Storage**: Google Drive (organized by client/campaign/platform)

---

## Files Changed

| File | Action |
|------|--------|
| `/Users/admin/.claude/plans/sparkling-juggling-codd.md` | Created - Full implementation plan |
| `savepoints/2025-12-15-architecture-planning.md` | Created - This savepoint |

---

## Project State

```
/Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN/
├── CLAUDE.md                    # Project instructions
├── PRD.md                       # Product requirements (needs update)
├── PROJECT-THEME.md             # Organization standards
├── README.md                    # Project overview
├── reference/                   # Parsed research (6 files)
│   ├── 00-REFERENCE-INDEX.md
│   ├── auzmor-ai-agent-principles.md
│   ├── architecture-diagrams.md
│   ├── context-summary.md
│   ├── google-cloud-slides-agent-architecture.md
│   └── youtube-agent-factory.md
├── research-sources/            # Original sources
│   ├── presentations/extracted/ # 14 JPG slides
│   └── youtube/                 # Architecture screenshot
├── savepoints/                  # Session savepoints
├── docs/                        # SDLC documentation
└── src/                         # Source code (empty - not started)
```

---

## Next Steps

- [ ] **Approve architecture** - User to confirm workflow is correct
- [ ] Exit plan mode
- [ ] Phase 1: Create GCP project, enable APIs
- [ ] Phase 1: Set up Google Drive folder structure
- [ ] Phase 1: Scaffold Cloud Run service

---

## Plan File Location

Full implementation plan saved at:
`/Users/admin/.claude/plans/sparkling-juggling-codd.md`

---

## Links

| Resource | Path |
|----------|------|
| Implementation Plan | `/Users/admin/.claude/plans/sparkling-juggling-codd.md` |
| Context Summary | `../reference/context-summary.md` |
| CLAUDE.md | `../CLAUDE.md` |
| PRD | `../PRD.md` |
| Savepoint Index | `./SAVEPOINT-INDEX.md` |

---

## Key Diagrams Created

### Simple Workflow
```
1. USER → Opens website, logs in
2. USER → Selects client, enters brief, uploads reference
3. AGENT → Brief Processor → Brand Retriever → Reference Analyzer → Image Generator
4. USER → Reviews, selects favorites
5. SYSTEM → Saves to Google Drive
```

### Architecture Summary
```
Team Browser → Cloud Run (LangGraph Agent) → Vertex AI (Gemini + Nano Banana) → Google Drive
```

---

**Session Duration**: ~45 minutes
**Mode**: Plan Mode (awaiting architecture approval)
