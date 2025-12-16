# PROJECT-THEME.md

**Purpose**: Reusable project organization standards and best practices template.
**Version**: 1.0.1
**Created**: 2025-12-15
**Last Audited**: 2025-12-15 (Final - All checks passed)

---

## Quick Audit Command

```bash
# Run this to audit any project against this theme
cd /path/to/project
cat PROJECT-THEME.md  # Review standards
# Then run verification commands below
```

---

## 1. Folder Structure Standard

### Core Structure (Mandatory)

```
project-name/                    # kebab-case, no spaces
├── CLAUDE.md                    # Claude Code instructions (auto-loaded)
├── README.md                    # GitHub/discovery overview
├── PROJECT-THEME.md             # This file - org standards
├── .gitignore                   # Git exclusions
│
├── savepoints/                  # Session state management
│   ├── SAVEPOINT-INDEX.md       # Global index with history
│   └── YYYY-MM-DD-*.md          # Timestamped savepoints
│
├── reference/                   # Parsed research (Claude-ready)
│   ├── 00-REFERENCE-INDEX.md    # Navigation hub
│   ├── context-summary.md       # KEY: Load at session start
│   └── [topic-files].md         # Topic-specific references
│
├── docs/                        # SDLC documentation
│   ├── 00-DOCUMENTATION-INDEX.md
│   ├── architecture/            # ADRs, system design
│   └── guides/                  # How-to documentation
│
├── src/                         # Source code
│
└── [project-specific]/          # Additional folders as needed
```

### Research Project Structure (Optional)

```
├── research-sources/            # Original source materials
│   ├── presentations/
│   │   ├── *.pptx               # Original files
│   │   └── extracted/           # Extracted images
│   ├── youtube/
│   │   ├── *.png                # Screenshots
│   │   └── *.md                 # Transcripts/notes
│   └── documents/
│       └── *.pdf                # PDF sources
```

### Development Project Structure (Optional)

```
├── archive/                     # Session artifacts (gitignored)
│   ├── savepoints/              # Alternative savepoint location
│   ├── screenshots/             # Test screenshots
│   ├── images/                  # Misc images
│   ├── demo-scripts/            # Presentation scripts
│   └── src-backups/             # Code experiments
│
├── __tests__/                   # Jest tests
├── e2e/                         # Playwright E2E tests
├── prisma/                      # Database schema
├── public/                      # Static assets
├── scripts/                     # Build/dev scripts
└── tokens/                      # Design tokens
```

---

## 2. Naming Conventions

### Folders (MANDATORY)

| Rule | Example | Anti-Pattern |
|------|---------|--------------|
| kebab-case | `research-sources/` | `research docs/` |
| lowercase | `presentations/` | `Presentations/` |
| no spaces | `extracted-slides/` | `extracted slides/` |
| descriptive | `architecture-diagrams/` | `misc/` |

### Files

| Type | Convention | Example |
|------|------------|---------|
| Index files | `00-*-INDEX.md` | `00-REFERENCE-INDEX.md` |
| Savepoints | `YYYY-MM-DD-description.md` | `2025-12-15-audit-complete.md` |
| Reference docs | `topic-name.md` | `context-summary.md` |
| Config files | Standard names | `CLAUDE.md`, `README.md` |

---

## 3. Required Files

### Every Project MUST Have

| File | Purpose | Template |
|------|---------|----------|
| `CLAUDE.md` | Project instructions for Claude Code | See Section 6 |
| `README.md` | GitHub/project overview | See Section 7 |
| `.gitignore` | Git exclusions | See Section 8 |

### Recommended Files

| File | Purpose | When to Include |
|------|---------|-----------------|
| `PROJECT-THEME.md` | This standards file | All projects |
| `savepoints/SAVEPOINT-INDEX.md` | Session history | Active development |
| `docs/00-DOCUMENTATION-INDEX.md` | Docs navigation | Projects with docs |
| `reference/00-REFERENCE-INDEX.md` | Reference navigation | Research projects |
| `reference/context-summary.md` | AI session context | AI-assisted projects |

---

## 4. Savepoint System

### Structure

```
savepoints/
├── SAVEPOINT-INDEX.md           # Global index (REQUIRED)
└── YYYY-MM-DD-description.md    # Timestamped savepoints
```

### SAVEPOINT-INDEX.md Template

```markdown
# Savepoint Index

**Project**: [PROJECT_NAME]
**Location**: `[FULL_PATH]/savepoints/`
**Last Updated**: [DATE]

---

## Latest Savepoint

→ **[YYYY-MM-DD-name.md](./YYYY-MM-DD-name.md)** - Brief description

---

## History

| Date | Name | Status | Summary |
|------|------|--------|---------|
| YYYY-MM-DD | [name](./YYYY-MM-DD-name.md) | ✅ Complete | Brief summary |

---

## Quick Links

| Resource | Path | Purpose |
|----------|------|---------|
| **CLAUDE.md** | [`../CLAUDE.md`](../CLAUDE.md) | Project instructions |
| **Context** | [`../reference/context-summary.md`](../reference/context-summary.md) | AI context |
| **Reference Index** | [`../reference/00-REFERENCE-INDEX.md`](../reference/00-REFERENCE-INDEX.md) | Research navigation |
| **Docs Index** | [`../docs/00-DOCUMENTATION-INDEX.md`](../docs/00-DOCUMENTATION-INDEX.md) | Documentation |
| **README** | [`../README.md`](../README.md) | Project overview |

---

## Session Resume

```bash
cd [FULL_PATH]
cat reference/context-summary.md
cat savepoints/SAVEPOINT-INDEX.md
```
```

### Savepoint File Template

```markdown
# SAVEPOINT: [PROJECT_NAME]

**Created**: [DATE TIME]
**Session**: [BRIEF DESCRIPTION]
**Status**: [In Progress / Complete]

---

## Quick Resume

```bash
cd [FULL_PATH]
cat reference/context-summary.md
cat savepoints/SAVEPOINT-INDEX.md
```

---

## Session Summary

### What Was Done
- [Accomplishment 1]
- [Accomplishment 2]

### Files Changed

| File | Action |
|------|--------|
| `path/to/file` | Created/Modified/Deleted |

---

## Project State

[Current structure overview or key metrics]

---

## Next Steps

- [ ] Task 1
- [ ] Task 2

---

## Links

| Resource | Path |
|----------|------|
| Context | `../reference/context-summary.md` |
| CLAUDE.md | `../CLAUDE.md` |
| Savepoint Index | `./SAVEPOINT-INDEX.md` |
```

---

## 5. Cross-Reference Standards

### Linking Rules

| From | To | Link Format |
|------|----|-------------|
| Same folder | Sibling file | `[name](filename.md)` |
| Child to parent | Parent folder | `[name](../filename.md)` |
| Index files | All siblings | Relative links |

### Required Links

Every INDEX file MUST link to:
- All files in its folder
- Parent CLAUDE.md
- Sibling INDEX files

### Bidirectional Linking

Reference files should cross-reference related files:
```markdown
## Cross-References

- For related topic: See `related-file.md`
- For diagrams: See `architecture-diagrams.md`
- For summary: See `context-summary.md`
```

---

## 6. CLAUDE.md Template

```markdown
# CLAUDE.md - [Project Name]

## Project Overview

**Type**: [Project Type]
**Location**: `[FULL_PATH]`
**Created**: [DATE]

---

## Quick Context Loading

```bash
# Load context at session start
cat reference/context-summary.md

# Check savepoint history
cat savepoints/SAVEPOINT-INDEX.md
```

---

## Project Structure

```
[project-name]/
├── [folder structure]
```

---

## Session Protocol

### Starting a Session
1. Navigate: `cd [FULL_PATH]`
2. Load context: `cat reference/context-summary.md`
3. Check savepoints: `cat savepoints/SAVEPOINT-INDEX.md`

### Ending a Session
- Create savepoint in `savepoints/`
- Update `SAVEPOINT-INDEX.md`

---

## Key Files Reference

| File | Purpose | When to Load |
|------|---------|--------------|
| `CLAUDE.md` | Instructions | Auto-loaded |
| `reference/context-summary.md` | AI context | Session start |
| `savepoints/SAVEPOINT-INDEX.md` | History | Resume work |

---

**Last Updated**: [DATE]
```

---

## 7. README.md Template

```markdown
# [Project Name]

**[Brief description]**

## Quick Start

```bash
cd [FULL_PATH]
cat reference/context-summary.md    # For Claude sessions
```

## Project Structure

```
[project-name]/
├── [key folders and files]
```

## Documentation

| Document | Purpose |
|----------|---------|
| `CLAUDE.md` | Claude Code instructions |
| `reference/context-summary.md` | AI session context |
| `savepoints/SAVEPOINT-INDEX.md` | Session history |

---

**Created**: [DATE]
**Status**: [Development/Research/Complete]
```

---

## 8. .gitignore Template

```gitignore
# Dependencies
node_modules/
.pnpm-store/

# Build outputs
.next/
dist/
build/
out/

# Environment
.env
.env.local
.env*.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
npm-debug.log*

# Testing
coverage/
.nyc_output/

# Archive (if using archive/ pattern)
archive/screenshots/
archive/src-backups/

# Temporary
*.tmp
*.temp
```

---

## 9. Audit Checklist

### Quick Verification Commands

```bash
# 1. Check folder naming (should return nothing)
find . -maxdepth 3 -type d -name "* *" -not -path "./.git/*"

# 2. Check required files exist
test -f CLAUDE.md && echo "✅ CLAUDE.md" || echo "❌ CLAUDE.md"
test -f README.md && echo "✅ README.md" || echo "❌ README.md"
test -f .gitignore && echo "✅ .gitignore" || echo "❌ .gitignore"

# 3. Check savepoint system
test -f savepoints/SAVEPOINT-INDEX.md && echo "✅ Savepoint INDEX" || echo "❌ Savepoint INDEX"

# 4. List all .md files
find . -name "*.md" -not -path "./.git/*" | sort

# 5. Check for broken internal links (manual review)
grep -rh '\[.*\](.*\.md)' --include="*.md" | head -20
```

### Full Audit Checklist

| Category | Check | Command/Action |
|----------|-------|----------------|
| **Structure** | No spaces in folder names | `find . -type d -name "* *"` |
| **Structure** | All kebab-case | Visual inspection |
| **Files** | CLAUDE.md exists | `test -f CLAUDE.md` |
| **Files** | README.md exists | `test -f README.md` |
| **Files** | .gitignore exists | `test -f .gitignore` |
| **Savepoints** | INDEX exists | `test -f savepoints/SAVEPOINT-INDEX.md` |
| **Savepoints** | History table updated | Read INDEX file |
| **Links** | All .md links valid | Test each link |
| **Links** | Bidirectional linking | Cross-reference check |
| **Content** | Context summary exists | `test -f reference/context-summary.md` |
| **Content** | INDEX files have all links | Read each INDEX |

---

## 10. Project Types

### Research Project

Focus on: Reference documentation, source materials, AI context loading

```
project/
├── CLAUDE.md
├── README.md
├── PROJECT-THEME.md
├── .gitignore
├── savepoints/
├── reference/           # Heavy focus here
│   ├── 00-REFERENCE-INDEX.md
│   ├── context-summary.md
│   └── [topic-files].md
├── research-sources/    # Original materials
└── docs/
```

### Development Project

Focus on: Source code, testing, deployment, archive management

```
project/
├── CLAUDE.md
├── README.md
├── PROJECT-THEME.md
├── .gitignore
├── src/                 # Heavy focus here
├── __tests__/
├── e2e/
├── docs/
├── archive/             # Session artifacts
│   └── savepoints/
└── public/
```

### Hybrid Project

Combines research foundation with active development

```
project/
├── CLAUDE.md
├── README.md
├── PROJECT-THEME.md
├── .gitignore
├── savepoints/          # Root level for active projects
├── reference/           # Research foundation
├── research-sources/    # Original materials
├── docs/                # SDLC documentation
└── src/                 # Active development
```

---

## 11. Migration Guide

### Converting Existing Project

1. **Audit current structure**
   ```bash
   find . -type d | head -20
   find . -name "*.md" | head -20
   ```

2. **Rename folders to kebab-case**
   ```bash
   # Example: rename "research docs" to "research-sources"
   mv "research docs" research-sources
   ```

3. **Create required files**
   ```bash
   touch CLAUDE.md README.md .gitignore PROJECT-THEME.md
   mkdir -p savepoints reference docs
   ```

4. **Create INDEX files**
   ```bash
   touch savepoints/SAVEPOINT-INDEX.md
   touch reference/00-REFERENCE-INDEX.md
   touch docs/00-DOCUMENTATION-INDEX.md
   ```

5. **Add cross-references**
   - Update all INDEX files with links
   - Add cross-references to content files

6. **Run audit**
   ```bash
   # Use commands from Section 9
   ```

---

## 12. Versioning

### Theme Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.1 | 2025-12-15 | Final audit passed - all files verified |
| 1.0.0 | 2025-12-15 | Initial release - ATC-MKTG-GEN patterns |

### Updating This Theme

1. Document changes in version history
2. Update "Last Audited" date
3. Run full audit on current project
4. Copy to other projects as needed

---

## Usage Instructions

### For New Projects

1. Copy this `PROJECT-THEME.md` to new project root
2. Follow templates in Sections 4-8
3. Run audit checklist (Section 9)
4. Customize project-specific sections

### For Existing Projects

1. Copy this file to project root
2. Follow Migration Guide (Section 11)
3. Run audit checklist
4. Fix any issues found

### Regular Audits

Schedule periodic audits:
- Weekly: Quick verification commands
- Monthly: Full audit checklist
- Per milestone: Complete audit with report

---

**Theme Source**: ATC-MKTG-GEN project (2025-12-15)
**Maintained By**: Claude Code sessions
**Standards Based On**: Justice League Best Practices
