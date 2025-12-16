# API Keys - ATC Marketing Asset Generator

**IMPORTANT**: This file contains sensitive API keys. Do NOT commit to public repositories.

---

## Google AI (Gemini)

| Key | Value | Status |
|-----|-------|--------|
| `GOOGLE_API_KEY` | `[TO BE ADDED]` | Pending |

**Get key from**: https://aistudio.google.com/apikey

---

## Google Drive API

| Key | Value | Status |
|-----|-------|--------|
| `GOOGLE_SERVICE_ACCOUNT_JSON` | `[TO BE ADDED]` | Pending |
| `GOOGLE_DRIVE_ROOT_FOLDER_ID` | `[TO BE ADDED]` | Pending |

**Setup steps**:
1. Go to Google Cloud Console
2. Create Service Account
3. Enable Google Drive API
4. Download JSON key file
5. Share Drive folder with service account email

---

## Application Settings

| Key | Value | Notes |
|-----|-------|-------|
| `APP_ENV` | `development` | Change to `production` for Cloud Run |
| `APP_PORT` | `8000` | FastAPI port |
| `STREAMLIT_PORT` | `8501` | Streamlit UI port |

---

## Quick Setup

1. Copy `.env.example` to `.env`
2. Fill in the values from this file
3. Run `python -m uvicorn src.api.main:app --reload`

---

**Last Updated**: 2025-12-15
