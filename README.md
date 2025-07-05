# WNR Script Generator (Live Version)

This app generates fake news broadcast scripts for WNR using OpenAI.

## Routes:
- `/` → confirms the service is up
- `/generate` (POST) → returns a full script

### Render Deployment
- Runtime: Python 3
- Build command: `pip install -r requirements.txt`
- Start command: `python app.py`
- Env var: `OPENAI_API_KEY`
