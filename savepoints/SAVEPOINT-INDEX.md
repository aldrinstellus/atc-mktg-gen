# Savepoint Index

**Project**: ATC-MKTG-GEN (Marketing Content Generator)
**Location**: `/Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN/savepoints/`
**Last Updated**: 2025-12-16

---

## Latest Savepoint

→ **[2025-12-16-image-generation-fixed.md](./2025-12-16-image-generation-fixed.md)** - Image generation working with marketing text

---

## History

| Date | Name | Status | Summary |
|------|------|--------|---------|
| 2025-12-16 | [image-generation-fixed](./2025-12-16-image-generation-fixed.md) | ✅ Complete | Fixed Gemini image format, marketing text in images |
| 2025-12-15 | [v1-app-running](./2025-12-15-v1-app-running.md) | ✅ Complete | V1.0 complete, services running on localhost:8000/8501 |
| 2025-12-15 | [architecture-planning](./2025-12-15-architecture-planning.md) | ✅ Complete | Architecture design, workflow diagrams, user decisions |
| 2025-12-15 | [session-complete](./2025-12-15-session-complete.md) | ✅ Complete | Full session - setup, audits, theme creation |
| 2025-12-15 | [final-audit](./2025-12-15-final-audit.md) | ✅ Complete | Final audit + PROJECT-THEME.md (reusable standards) |
| 2025-12-15 | [audit-complete](./2025-12-15-audit-complete.md) | ✅ Complete | Full spectrum audit - all checks passed |
| 2025-12-15 | [bulletproof](./2025-12-15-bulletproof.md) | ✅ Complete | CLI-friendly restructure, all paths fixed |
| 2025-12-15 | initial-setup | ✅ Complete | Project creation, 14 slides parsed, reference docs created |

---

## Quick Links

| Resource | Path | Purpose |
|----------|------|---------|
| **CLAUDE.md** | [`../CLAUDE.md`](../CLAUDE.md) | Project instructions (auto-loaded) |
| **PROJECT-THEME.md** | [`../PROJECT-THEME.md`](../PROJECT-THEME.md) | Organization standards & audit checklist |
| **Context Summary** | [`../reference/context-summary.md`](../reference/context-summary.md) | Full AI context (~8KB) - **LOAD FIRST** |
| **Reference Index** | [`../reference/00-REFERENCE-INDEX.md`](../reference/00-REFERENCE-INDEX.md) | Research navigation hub |
| **Docs Index** | [`../docs/00-DOCUMENTATION-INDEX.md`](../docs/00-DOCUMENTATION-INDEX.md) | SDLC documentation |
| **README** | [`../README.md`](../README.md) | GitHub project overview |

---

## Reference Files

| File | Size | Content |
|------|------|---------|
| `context-summary.md` | ~8KB | Comprehensive context for Claude |
| `auzmor-ai-agent-principles.md` | ~10KB | 14 AI agent design slides |
| `google-cloud-slides-agent-architecture.md` | ~6KB | YouTube architecture reference |
| `youtube-agent-factory.md` | ~4KB | Technologies & tools |
| `architecture-diagrams.md` | ~5KB | ASCII diagrams |

---

## Session Resume Commands

```bash
# Navigate to project
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN

# Load context (REQUIRED at session start)
cat reference/context-summary.md

# Check savepoint history
cat savepoints/SAVEPOINT-INDEX.md

# Read latest savepoint details
cat savepoints/2025-12-15-bulletproof.md
```

---

## Savepoint Protocol

When creating a new savepoint:

1. **Create file**: `savepoints/YYYY-MM-DD-description.md`
2. **Update this INDEX**:
   - Change "Latest Savepoint" link
   - Add new row to History table
   - Update "Last Updated" date
3. **Include in savepoint**:
   - Quick resume commands
   - Session summary (what was done)
   - Files changed
   - Current project state
   - Next steps

---

## Project Structure

```
ATC-MKTG-GEN/
├── savepoints/                    # Session history (THIS FOLDER)
│   ├── SAVEPOINT-INDEX.md         # This file
│   └── YYYY-MM-DD-*.md            # Timestamped savepoints
├── reference/                     # Parsed research (~33KB)
├── research-sources/              # Original materials
├── docs/                          # SDLC documentation
├── src/                           # Source code (future)
├── CLAUDE.md                      # Project instructions
├── README.md                      # GitHub overview
└── .gitignore                     # Git exclusions
```

---

## Statistics

| Metric | Value |
|--------|-------|
| Total savepoints | 1 |
| Research files | 6 |
| Research content | ~33KB |
| Slides parsed | 14 |

---

**Maintained by**: Claude Code sessions
