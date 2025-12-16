# SAVEPOINT: ATC-MKTG-GEN

**Created**: 2025-12-16 09:25 PST
**Session**: Image Generation Fixed + Marketing Text Working
**Status**: Complete - Ready for GitHub/Vercel

---

## Quick Resume
```bash
cd /Users/admin/Documents/claudecode/workspaces/ATC-MKTG-GEN
source venv/bin/activate
python src/api/main.py  # API on port 8000
streamlit run src/ui/app.py  # UI on port 8501
```

## Session Summary

### What Was Done
1. **Fixed Gemini 2.0 Image Generation**
   - Root cause: Gemini returns raw PNG bytes, not base64 encoded
   - Fix: Check for PNG/JPEG/WebP magic bytes before base64 decoding
   - Location: `src/mcp/media_server.py:344-365`

2. **Enhanced Marketing Text Generation**
   - Added `headline`, `subheadline`, `call_to_action` extraction from brief
   - AI now always generates compelling marketing text
   - Location: `src/mcp/media_server.py:194-217`

3. **Improved Image Prompt Generation**
   - Added "MUST include bold, readable text overlay" when text requested
   - Text is now prominent in generated marketing images
   - Location: `src/mcp/media_server.py:283-302, 329-361`

4. **Verified Working End-to-End**
   - Campaign brief: "Weekend special promotion: 20% off all fusion burgers..."
   - Generated image includes headline, subheadline, and "ORDER NOW" CTA
   - Screenshot saved: `screenshots/generation-with-text-2025-12-16.png`

### Files Changed
| File | Action | Description |
|------|--------|-------------|
| `src/mcp/media_server.py` | Modified | Fixed image format detection, enhanced text generation |
| `screenshots/generation-working-2025-12-16.png` | Created | First working generation |
| `screenshots/generation-with-text-2025-12-16.png` | Created | Generation with marketing text |

### Technical Details
- **API**: FastAPI on port 8000
- **UI**: Streamlit on port 8501
- **Image Generation**: Gemini 2.0 Flash (`gemini-2.0-flash-exp`) with `response_modalities: ["TEXT", "IMAGE"]`
- **Image Format**: Raw PNG bytes (1024x1024), resized to target platform dimensions

### Key Code Changes

**Image Format Detection** (`media_server.py`):
```python
# Check if first bytes match known image magic bytes
if raw_data[:4] == b'\x89PNG' or raw_data[:3] == b'\xff\xd8\xff' or raw_data[:4] == b'RIFF':
    image_data = raw_data  # Already raw image bytes
```

**Marketing Text Extraction** (`media_server.py`):
```python
"headline": "catchy headline text to display prominently",
"subheadline": "secondary text like tagline or offer details",
"call_to_action": "what action should viewers take"
```

**Text-Enhanced Prompt** (`media_server.py`):
```python
if text_elements:
    prompt_parts.append("MUST include bold, readable text overlay with: " + ", ".join(text_elements))
```

## Project State

### Working Features
- Client selection (Burgers & Curries sample)
- Platform selection (Instagram, Facebook, etc.)
- Campaign brief processing via Gemini
- AI image generation with marketing text
- Image download functionality
- Generation details view

### Environment
- Python 3.9.6 with venv
- google-generativeai 0.8.5
- FastAPI + Uvicorn
- Streamlit
- Pillow for image processing

### API Key
- Location: `.env` file
- Key: `GOOGLE_API_KEY=AIzaSy...`
- Services: Gemini API enabled in Google Cloud Console

## Next Steps
- [x] Create savepoint
- [ ] Initialize git repository
- [ ] Push to GitHub
- [ ] Deploy to Vercel

## Links
| Resource | Path |
|----------|------|
| CLAUDE.md | `./CLAUDE.md` |
| Savepoint Index | `./savepoints/SAVEPOINT-INDEX.md` |
| Screenshots | `./screenshots/` |
| API Server | `http://localhost:8000` |
| Streamlit UI | `http://localhost:8501` |
