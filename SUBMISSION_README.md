# CGCian KPI Anomaly Radar — Submission README

One-liner: Detect KPI anomalies early to reduce handling time and improve CSAT, with instant Slack/Email alerts and lightweight historical snapshots.

Focus area: Data-driven insights & analytics (with optional process automation and customer experience pages scaffolded).

## What’s included (MVP)
- Data Insights dashboard
  - Load data from sample CSV (`data/sample_kpis.csv`), upload, `data/` folder, or URL
  - Rolling-baseline anomaly detection (configurable metric, std-dev threshold, window)
  - Interactive charts (Plotly) and anomaly markers
  - Export processed/anomaly CSVs
- Alerts
  - One-click Slack (Incoming Webhook) and Email (SMTP) alerts when anomalies are detected
- Snapshots
  - Save daily KPI snapshots to SQLite (`data/kpis.db`) and view history/trends
- Docs & pitch support
  - Problem/Solution/Plan templates and demo/video guides under `docs/`

## How to run (macOS, zsh)
```bash
cd /Users/revanthmalladi/Documents/gcc
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```
Open the URL printed in the terminal (usually http://localhost:8501).

## Configuration (optional)
- Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml` and fill values:
  - `SLACK_WEBHOOK_URL`
  - `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASS`, `EMAIL_FROM`, `EMAIL_TO`
- Alternatively, set these as environment variables before running the app.

## Data inputs
- Recommended CSV schema (remappable in UI):
  - `date` (YYYY-MM-DD)
  - `tickets` (int)
  - `avg_handle_min` (float)
  - `csat` (float)
- Sample file: `data/sample_kpis.csv`

## Demo flow (2–3 minutes)
1) Open Data Insights → Use sample data
2) Tweak anomaly settings (metric, k-std, window) and point out highlighted anomalies
3) Click "Send Slack alert" (and/or "Send Email alert") if configured
4) Save latest snapshot → View snapshot history and chart
5) Optional: Download processed/anomaly CSVs

For a longer format and talking points, see `docs/DEMO_SCRIPT.md`.

## Requirements coverage (mapping)
- Working Prototype (MVP)
  - Streamlit app (`app.py`) with functional Data Insights dashboard and anomaly detection
- Project Documentation
  - Problem statement → fill `docs/PROBLEM_STATEMENT.md`
  - Proposed solution & benefits → fill `docs/SOLUTION_OVERVIEW.md`
  - Technologies used → `docs/TECHNOLOGIES_USED.md`
  - Implementation plan or next steps → fill `docs/IMPLEMENTATION_PLAN.md`
- Pitch Presentation
  - Use `docs/PITCH_DECK_TEMPLATE.md` (5–7 slides) or record a 3–5 minute demo video
  - A 30-second hook outline is provided in `docs/VIDEO_OUTLINE.md`
- Source Code
  - Clean repo with run instructions (`README.md`, this `SUBMISSION_README.md`), sample data, and secrets example

Status: All core requirements are covered. Templates are ready—fill Problem/Solution/Plan to finalize.

## Technologies used
- Streamlit, Python, Pandas/Numpy, Plotly, SQLite, Slack Webhooks, SMTP (Email)
See `docs/TECHNOLOGIES_USED.md` for details.

## Next steps (optional enhancements)
- Connect to a warehouse/API for real data (Snowflake/BigQuery/etc.)
- Schedule daily runs and auto-alerts (cron/launchd/GitHub Actions)
- Add basic auth/SSO for internal sharing
- Explore ML-based anomaly detection if needed

## Teamwork
Suggested roles and RACI in `docs/TEAM_ROLES.md`. One person may cover multiple roles in hackathon mode.

## Submission checklist
- [ ] MVP runs locally (`streamlit run app.py`)
- [ ] `docs/PROBLEM_STATEMENT.md` completed
- [ ] `docs/SOLUTION_OVERVIEW.md` completed
- [ ] `docs/IMPLEMENTATION_PLAN.md` completed
- [ ] Pitch deck (or 3–5 min video) prepared
- [ ] Repo clean; `.streamlit/secrets.toml` not committed; example provided
- [ ] Optional alerts tested (Slack/Email)
