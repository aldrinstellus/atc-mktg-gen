# Documentation Index

**Project**: ATC-MKTG-GEN (Marketing Content Generator)
**Location**: `/Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN/docs/`
**Created**: 2025-12-15

---

## SDLC Documentation Structure

This folder follows the standard SDLC documentation structure. Files will be added as the project progresses.

---

## Planned Structure

```
docs/
├── 00-DOCUMENTATION-INDEX.md      # This file
├── 01-getting-started/            # Setup and onboarding
│   ├── README.md
│   ├── installation.md
│   └── quickstart.md
├── 02-architecture/               # System design
│   ├── README.md
│   ├── overview.md
│   └── decisions/                 # ADRs
├── 03-development/                # Development guides
│   ├── README.md
│   ├── coding-standards.md
│   └── workflows.md
├── 04-api/                        # API documentation
│   ├── README.md
│   └── endpoints.md
├── 05-testing/                    # Testing guides
│   ├── README.md
│   └── test-plan.md
├── 06-deployment/                 # Deployment guides
│   ├── README.md
│   └── environments.md
└── 07-operations/                 # Operations guides
    ├── README.md
    └── runbooks.md
```

---

## Current Status

| Section | Status | Notes |
|---------|--------|-------|
| 00-index | ✅ Created | This file |
| **COMPLETE-PROJECT-LOG.md** | ✅ **NEW** | **Full project documentation (~900 lines)** |
| 01-getting-started | ⏳ Pending | See README.md for quick start |
| 02-architecture | ✅ In Project Log | See COMPLETE-PROJECT-LOG.md Section 3 |
| 03-development | ⏳ Pending | - |
| 04-api | ✅ In Project Log | See COMPLETE-PROJECT-LOG.md Section 8 |
| 05-testing | ⏳ Pending | - |
| 06-deployment | ⏳ Pending | See Docker files |
| 07-operations | ⏳ Pending | - |

---

## Key Documentation

### COMPLETE-PROJECT-LOG.md (NEW)
**Location**: `docs/COMPLETE-PROJECT-LOG.md`
**Size**: ~900 lines
**Contents**:
1. Executive Summary
2. Session Timeline (all phases)
3. Architecture Overview (diagrams)
4. Source Code Documentation (all 7 files)
5. All Savepoints (6 total)
6. Research Materials Summary
7. Configuration Files
8. API Documentation
9. Next Steps

---

## Related Resources

### Reference Documentation (Research)
All parsed research materials are in the `reference/` folder:

| File | Description |
|------|-------------|
| `reference/context-summary.md` | Comprehensive context for Claude |
| `reference/auzmor-ai-agent-principles.md` | AI agent design principles |
| `reference/google-cloud-slides-agent-architecture.md` | Reference architecture |
| `reference/00-REFERENCE-INDEX.md` | Reference navigation |

### Project Files
| File | Description |
|------|-------------|
| `CLAUDE.md` | Project instructions for Claude |
| `reference/` | Parsed research materials |
| `research-sources/` | Original source files |
| `src/` | Source code (future) |
| `savepoints/` | Session history with index |

---

## Documentation Standards

When adding documentation:

1. **Use Markdown** - All docs in `.md` format
2. **Include TOC** - Table of contents for longer docs
3. **Code Examples** - Include runnable examples where applicable
4. **Cross-reference** - Link to related docs
5. **Keep Updated** - Update docs when code changes

---

**Last Updated**: 2025-12-15
