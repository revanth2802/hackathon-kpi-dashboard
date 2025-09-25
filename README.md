# CGCian Dream2 Bigger Hackathon – Starter Kit

Kickstart your internal hackathon project with a ready-to-run template: a minimal Streamlit MVP, clear docs, and a submission checklist. Adapt freely.

## What this includes
- Runnable MVP app (`app.py`) using Streamlit
- Documentation templates in `docs/`
- Submission checklist and pitch deck outline
- macOS-friendly quickstart

## Repo structure
```
.
├── app.py                # Minimal MVP (Streamlit)
├── requirements.txt      # Python deps
├── docs/
│   ├── PROBLEM_STATEMENT.md
│   ├── SOLUTION_OVERVIEW.md
│   ├── IMPLEMENTATION_PLAN.md
│   ├── PITCH_DECK_TEMPLATE.md
│   └── SUBMISSION_CHECKLIST.md
└── .gitignore
```

## Quickstart (macOS, zsh)
1) Create and activate a virtual env
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

2) Install dependencies
```
pip install -r requirements.txt
```

3) Run the MVP app
```
streamlit run app.py
```

4) Open the local URL shown in the terminal (typically http://localhost:8501)

## How to use this starter
- Edit the docs in `docs/` to capture your problem, solution, and plan.
- Replace the placeholder sections in `app.py` with your actual features.
- Use the `SUBMISSION_CHECKLIST.md` to stay on track.

### Data Insights flow (enhanced)
- Choose "Data Insights" in the sidebar.
- Pick one: "Use sample data", "Upload CSV", "From data/ folder", or "CSV from URL". You can remap columns in the UI.
- Adjust anomaly detection: metric, std-dev threshold, and rolling window.
- Explore charts, review highlighted anomalies, and download processed/anomaly CSVs.

CSV expectations (you can remap columns):
- `date`: parsable date (YYYY-MM-DD)
- `tickets`: integer
- `avg_handle_min`: float (minutes)
- `csat`: float (e.g., 1–5)

### Data sources
- `Use sample data`: loads `data/sample_kpis.csv` if present, else a generated sample.
- `From data/ folder`: place CSV files under `data/` and pick one in the UI.
- `CSV from URL`: paste a direct CSV URL; the app fetches it.

### Alerts configuration
Configure via `.streamlit/secrets.toml` or environment variables:

Slack (Incoming Webhook):
```
[default]
SLACK_WEBHOOK_URL = "https://hooks.slack.com/services/XXX/YYY/ZZZ"
```

Email (SMTP):
```
[default]
SMTP_HOST = "smtp.example.com"
SMTP_PORT = 587
SMTP_USER = "username"
SMTP_PASS = "password"
EMAIL_FROM = "alerts@example.com"
EMAIL_TO = "you@example.com,team@example.com"
```

You can also export these as environment variables in your shell before running Streamlit.

### Snapshots (SQLite)
- Click "Save latest snapshot" to persist the most recent KPI row to `data/kpis.db`.
- Click "View snapshot history" to see all saved entries and trend charts.
- Useful for daily runs to build a lightweight history.

## Idea prompts (pick 1 to start)
- Process automation: Intake form that triggers workflow + Slack/Email updates.
- Customer experience: FAQ assistant that searches internal knowledge base.
- Data insights: KPI dashboard with anomaly alerts (daily/weekly).
- AI/ML tool: Smart ticket triage to route requests to the right team.
- Sustainability: Carbon footprint tracker for select operations.

Tip: Choose a narrow slice that can be demoed end-to-end with mock data first.

## Submission package
- Working prototype: demo via Streamlit app or short video
- Project docs: `docs/` filled out
- Pitch: 5–7 slides using `PITCH_DECK_TEMPLATE.md`
- Source code: clean repo with instructions
 - Use `docs/SUBMISSION_CHECKLIST.md` before you submit

## Notes
- Keep scope tight: ship one “wow” flow end-to-end.
- Prefer simple integrations and mock data to show value quickly.
- Add a short demo script in your pitch or repo description.
## Technologies used
See `docs/TECHNOLOGIES_USED.md` for the stack and purpose of each component.

## How to submit (aligns with brief)
1) Ensure the MVP runs locally: `streamlit run app.py`.
2) Complete docs in `docs/`: Problem, Solution, Implementation Plan, Technologies Used.
3) Prepare your pitch: either
	- 5–7 slide deck using `docs/PITCH_DECK_TEMPLATE.md`, or
	- 3–5 minute video (use `docs/DEMO_SCRIPT.md` + `docs/VIDEO_OUTLINE.md`).
4) Clean the repo: comments, remove secrets; include `.streamlit/secrets.toml.example`.
5) Share the repo link (and video if chosen) per hackathon instructions.


### Troubleshooting
- If `streamlit` command is not found, ensure your virtualenv is activated: `source .venv/bin/activate`.
- If ports are in use, run: `streamlit run app.py --server.port 8502`.

---
Made for rapid prototyping.