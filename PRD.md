# AI Marketing Asset Generator - PRD

**Project**: ATC-MKTG-GEN
**Version**: 1.0
**Date**: 2025-12-15
**Status**: Discovery Phase

---

## 1. Executive Summary

Build an AI-powered marketing asset generation system that:
- Uses existing marketing assets (Google Drive, Canva) as a knowledge base
- Generates campaign-specific assets for multiple clients
- Outputs to multiple social media platforms
- Deploys on Cloud Run for team access

---

## 2. Problem Statement

### Current Pain Points
1. **Fragmented Assets**: Marketing materials scattered across Google Drive, Canva, local folders
2. **Manual Creation**: Time-consuming to create campaign assets manually
3. **Multi-Client Complexity**: Each client (e.g., "Burgers & Curries") has unique brand guidelines
4. **Platform Variations**: Different sizes/formats needed for Instagram, Facebook, etc.
5. **Reference Management**: Hard to apply aesthetics from reference images while maintaining brand

### Desired State
- Single system to generate marketing assets
- Knowledge base of existing work for brand consistency
- Reference image support for aesthetic inspiration
- Team-accessible deployment (not just local)
- Output directly to Google Drive

---

## 3. User Stories

| # | As a... | I want to... | So that... |
|---|---------|--------------|------------|
| 1 | Marketing Manager | Generate Instagram campaign for "Burgers & Curries" Christmas promo | I can quickly create branded content |
| 2 | Designer | Upload reference images from web | The AI applies those aesthetics to my brand |
| 3 | Team Member | Access the tool without technical setup | I can generate assets independently |
| 4 | Account Manager | Pull past campaign assets as reference | New campaigns maintain consistency |

---

## 4. Functional Requirements

### P0 - Must Have
| # | Requirement | Description |
|---|-------------|-------------|
| F1 | Client Selection | Select from list of clients (Burgers & Curries, etc.) |
| F2 | Campaign Brief Input | Text input for campaign details (theme, platform, etc.) |
| F3 | Asset Generation | Generate images based on brief + brand guidelines |
| F4 | Google Drive Output | Save generated assets to Google Drive folder |
| F5 | Cloud Run Deployment | Team-accessible web interface |

### P1 - Should Have
| # | Requirement | Description |
|---|-------------|-------------|
| F6 | Reference Image Upload | Upload images from web for style reference |
| F7 | Google Drive Reference | Select past campaign images as reference |
| F8 | Multi-Platform Output | Generate for Instagram, Facebook, LinkedIn, etc. |
| F9 | Brand Guidelines Enforcement | Auto-apply logos, colors, fonts |

### P2 - Nice to Have
| # | Requirement | Description |
|---|-------------|-------------|
| F10 | Canva Integration | Pull assets from Canva as knowledge base |
| F11 | Batch Generation | Generate multiple variations at once |
| F12 | Campaign History | Track past campaigns per client |

---

## 5. Technical Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                          │
│                    (Web App on Cloud Run)                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    ORCHESTRATION LAYER                      │
│              (Python/Node.js Backend on Cloud Run)          │
└─────────────────────────────────────────────────────────────┘
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│  KNOWLEDGE  │      │     AI      │      │   OUTPUT    │
│    BASE     │      │  GENERATOR  │      │   MANAGER   │
│             │      │             │      │             │
│ • Google    │      │ • Flux API  │      │ • Google    │
│   Drive API │      │ • OR DALL-E │      │   Drive API │
│ • Brand     │      │ • OR Stable │      │ • Folder    │
│   Guidelines│      │   Diffusion │      │   Structure │
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## 6. System Components

### 6.1 Knowledge Base Layer
- **Purpose**: Index and retrieve existing marketing assets
- **Source**: Google Drive folders per client
- **Data**: Logos, brand colors, past campaigns, fonts
- **Tech**: Google Drive API, vector embeddings for image search

### 6.2 AI Generation Engine
- **Purpose**: Generate marketing images
- **Options**:
  - Flux (via Replicate/FAL.ai) - High quality, fast
  - DALL-E 3 (OpenAI) - Good quality, easy API
  - Stable Diffusion (self-hosted or API)
- **Input**: Campaign brief + brand context + reference style

### 6.3 Reference Image Processor
- **Purpose**: Extract aesthetics from reference images
- **Flow**:
  1. User uploads/selects reference image
  2. System extracts style (colors, composition, mood)
  3. Style applied to generation while maintaining brand

### 6.4 Output Manager
- **Purpose**: Save generated assets to Google Drive
- **Structure**: `/{Client}/{Campaign}/{Platform}/`
- **Formats**: PNG, JPG (platform-optimized sizes)

### 6.5 Deployment (Cloud Run)
- **Why Cloud Run**:
  - Team members get a URL to access
  - No local setup needed
  - Scales to zero when not in use (cost-effective)
  - Handles authentication via Google

---

## 7. Data Flow

```
1. User selects client → "Burgers & Curries"
2. User enters brief → "Christmas campaign, Instagram, festive food theme"
3. User optionally uploads reference images
4. System retrieves brand assets from Google Drive
5. AI generates images with brand + reference style
6. User reviews/selects favorites
7. System saves to Google Drive: /Burgers & Curries/Christmas 2025/Instagram/
```

---

## 8. Integration Points

| Service | Purpose | API |
|---------|---------|-----|
| Google Drive | Knowledge base + Output | Google Drive API v3 |
| Image Generation | Create assets | Flux/DALL-E/SD API |
| Cloud Run | Deployment | GCP Cloud Run |
| (Optional) Canva | Additional knowledge base | Canva Connect API |

---

## 9. User Interface Requirements

### Simple Web Interface
- Client dropdown selector
- Campaign brief text area
- Platform checkboxes (Instagram, Facebook, etc.)
- Reference image upload zone
- "Select from Google Drive" button for references
- Generate button
- Preview gallery
- "Save to Drive" button

---

## 10. Deployment Strategy

### For Team Access (Cloud Run)

```bash
# Build and deploy
gcloud run deploy atc-mktg-gen \
  --source . \
  --region us-central1 \
  --allow-unauthenticated  # OR use IAM for team-only access
```

### Team Members Get:
- URL: `https://atc-mktg-gen-xxxxx.run.app`
- Google login (if authenticated)
- No installation needed

---

## 11. Success Metrics

| Metric | Target |
|--------|--------|
| Asset generation time | < 2 minutes per image |
| Brand consistency score | > 90% (manual review) |
| Team adoption | 100% of marketing team using |
| Cost per asset | < $0.50 per generated image |

---

## 12. Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| AI hallucinating brand elements | High | Use strict brand guidelines as input |
| Reference style overriding brand | Medium | Weighted style transfer (brand > reference) |
| Google Drive API limits | Low | Implement caching, batch operations |
| Image generation costs | Medium | Use efficient models, cache common elements |

---

## 13. Implementation Phases

### Phase 1: Foundation (Week 1-2)
- [ ] Set up Cloud Run project
- [ ] Google Drive API integration
- [ ] Basic web interface
- [ ] Single client support

### Phase 2: Core Generation (Week 3-4)
- [ ] AI image generation integration
- [ ] Brand guidelines enforcement
- [ ] Output to Google Drive

### Phase 3: Reference Support (Week 5-6)
- [ ] Reference image upload
- [ ] Google Drive reference selection
- [ ] Style extraction and application

### Phase 4: Polish & Deploy (Week 7-8)
- [ ] Multi-client support
- [ ] Multi-platform output sizes
- [ ] Team deployment and training

---

## 14. Open Questions

1. **Which clients to support first?** (List needed)
2. **Where are brand guidelines stored?** (Google Drive folder structure?)
3. **Preferred image generation service?** (Flux vs DALL-E vs other)
4. **Budget for API costs?** (Image generation has per-image cost)
5. **Authentication model?** (Open URL vs Google login required?)
6. **Canva integration priority?** (P1 or P2?)

---

## 15. Next Steps

1. Answer open questions above
2. Set up GCP project and enable APIs
3. Create proof-of-concept with single client
4. Test image generation quality
5. Iterate based on feedback

---

**Document Owner**: Product Manager 📋
**Last Updated**: 2025-12-15
