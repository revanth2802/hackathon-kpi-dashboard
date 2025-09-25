import streamlit as st
import pandas as pd
import numpy as np
import time
import io
import os
import sqlite3
import ssl
import smtplib
from email.message import EmailMessage
import urllib.request
import json
import plotly.express as px

st.set_page_config(page_title="CGCian Hackathon MVP", page_icon="🚀", layout="wide")

# Sidebar navigation
st.sidebar.title("CGCian Hackathon MVP")
page = st.sidebar.radio("Go to", [
    "Overview",
    "Process Automation",
    "Customer Experience",
    "Data Insights",
])

# Mock data helpers
@st.cache_data
def load_mock_kpis():
    rng = np.random.default_rng(42)
    days = pd.date_range(end=pd.Timestamp.today().normalize(), periods=30)
    df = pd.DataFrame({
        "date": days,
        "tickets": rng.integers(80, 150, size=len(days)),
        "avg_handle_min": rng.normal(12, 2.5, size=len(days)).round(1),
        "csat": rng.normal(4.3, 0.2, size=len(days)).round(2)
    })
    df["anomaly"] = (df["avg_handle_min"] > df["avg_handle_min"].mean() + 2*df["avg_handle_min"].std())
    return df

# Pages
if page == "Overview":
    st.title("🚀 CGCian Hackathon MVP Starter")
    st.write("""
    Use this app as a starting point. Replace mock flows with your real logic or APIs.
    - Process Automation: Intake form + workflow simulation
    - Customer Experience: Simple Q&A with canned responses
    - Data Insights: KPI dashboard with anomaly highlight
    """)
    st.info("Tip: Start with one end-to-end hero flow. You can demo using mock data.")

elif page == "Process Automation":
    st.header("⚙️ Process Automation – Intake to Action")
    with st.form("intake"):
        name = st.text_input("Requester Name")
        dept = st.selectbox("Department", ["Operations", "Sales", "Support", "IT"]) 
        need = st.text_area("Describe the request")
        priority = st.select_slider("Priority", ["Low", "Medium", "High"]) 
        submitted = st.form_submit_button("Submit & Trigger Workflow")
    if submitted:
        with st.spinner("Submitting and triggering workflow…"):
            time.sleep(1.2)
        st.success(f"Ticket created for {name} in {dept}. Notifications sent. Priority: {priority}.")
        st.caption("In production: replace with API calls (e.g., Jira/ServiceNow/Slack/Email)")

elif page == "Customer Experience":
    st.header("💬 Customer Experience – FAQ Assistant")
    st.write("Ask a question about our mock knowledge base.")
    q = st.text_input("Your question")
    if st.button("Get Answer"):
        # Placeholder retrieval logic
        answers = {
            "pricing": "You can find pricing in the internal catalog. For enterprise quotes, contact Sales.",
            "sla": "Our standard SLA is 99.9% uptime with 4-hour response for P1 incidents.",
            "onboarding": "Onboarding takes ~5 business days. Use the onboarding portal to track status.",
        }
        key = None
        for k in answers:
            if k in q.lower():
                key = k
                break
        reply = answers.get(key, "No exact match found. We’ll connect you with a specialist.")
        st.info(reply)
        st.caption("In production: add retrieval over Confluence/SharePoint/Docs via search/embeddings.")

elif page == "Data Insights":
    st.header("📊 Data Insights – KPI Dashboard & Anomalies")

    # Controls
    st.subheader("Data Source")
    src = st.radio("Choose data source", ["Use sample data", "Upload CSV", "From data/ folder", "CSV from URL"], horizontal=True)
    uploaded_file = None
    df_raw = None
    selected_data_file = None
    csv_url = None
    if src == "Upload CSV":
        uploaded_file = st.file_uploader("Upload CSV with columns: date, tickets, avg_handle_min, csat", type=["csv"]) 
        if uploaded_file is not None:
            try:
                df_raw = pd.read_csv(uploaded_file)
            except Exception as e:
                st.error(f"Failed to read CSV: {e}")
    elif src == "From data/ folder":
        data_dir = os.path.join(os.getcwd(), "data")
        if not os.path.isdir(data_dir):
            st.warning(f"Data folder not found at {data_dir}")
        else:
            csv_files = [f for f in os.listdir(data_dir) if f.lower().endswith('.csv')]
            if not csv_files:
                st.info("No CSV files found in data/. Add files or use the sample/URL options.")
            else:
                selected_data_file = st.selectbox("Select a CSV in data/", csv_files)
                if selected_data_file:
                    try:
                        df_raw = pd.read_csv(os.path.join(data_dir, selected_data_file))
                    except Exception as e:
                        st.error(f"Failed to read CSV from data/: {e}")
    elif src == "CSV from URL":
        csv_url = st.text_input("Enter a direct CSV URL")
        if st.button("Load CSV from URL") and csv_url:
            try:
                df_raw = pd.read_csv(csv_url)
            except Exception as e:
                st.error(f"Failed to fetch CSV from URL: {e}")

    if src == "Use sample data" and df_raw is None:
        # Prefer a packaged sample file if present
        sample_path = os.path.join(os.getcwd(), "data", "sample_kpis.csv")
        if os.path.exists(sample_path):
            try:
                df_raw = pd.read_csv(sample_path)
            except Exception:
                df_raw = load_mock_kpis()
        else:
            df_raw = load_mock_kpis()

    # Column mapping if needed
    st.subheader("Column Mapping")
    cols = list(df_raw.columns)
    lower_cols = {c.lower(): c for c in cols}
    def auto(col_name):
        return lower_cols.get(col_name, cols[0] if cols else None)
    date_col = st.selectbox("Date column", options=cols, index=(cols.index(auto("date")) if auto("date") in cols else 0))
    tickets_col = st.selectbox("Tickets column", options=cols, index=(cols.index(auto("tickets")) if auto("tickets") in cols else 0))
    handle_col = st.selectbox("Avg handle (min) column", options=cols, index=(cols.index(auto("avg_handle_min")) if auto("avg_handle_min") in cols else 0))
    csat_col = st.selectbox("CSAT column", options=cols, index=(cols.index(auto("csat")) if auto("csat") in cols else 0))

    # Normalize
    def normalize(df):
        out = pd.DataFrame({
            "date": pd.to_datetime(df[date_col], errors="coerce"),
            "tickets": pd.to_numeric(df[tickets_col], errors="coerce"),
            "avg_handle_min": pd.to_numeric(df[handle_col], errors="coerce"),
            "csat": pd.to_numeric(df[csat_col], errors="coerce"),
        }).dropna()
        out = out.sort_values("date").reset_index(drop=True)
        return out

    df = normalize(df_raw)

    # Analytics controls
    with st.expander("Anomaly detection settings", expanded=True):
        metric = st.selectbox("Monitor metric for anomalies", ["avg_handle_min", "tickets", "csat"], index=0)
        k_std = st.slider("Std dev threshold (k)", min_value=0.5, max_value=4.0, value=2.0, step=0.1)
        window = st.slider("Rolling window (days) for baseline", min_value=5, max_value=30, value=14, step=1)

    # Compute rolling mean/std for baseline
    df[f"{metric}_roll_mean"] = df[metric].rolling(window=window, min_periods=max(3, window//2)).mean()
    df[f"{metric}_roll_std"] = df[metric].rolling(window=window, min_periods=max(3, window//2)).std()
    df["anomaly"] = df[metric] > (df[f"{metric}_roll_mean"] + k_std * df[f"{metric}_roll_std"])

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    last_row = df.iloc[-1] if len(df) else None
    col1.metric("Tickets (last day)", int(last_row["tickets"]) if last_row is not None else "–")
    col2.metric("Avg Handle (min)", float(last_row["avg_handle_min"]) if last_row is not None else "–")
    col3.metric("CSAT", float(last_row["csat"]) if last_row is not None else "–")
    col4.metric("Anomaly Days", int(df["anomaly"].sum()))

    # Charts
    c1, c2 = st.columns(2)
    with c1:
        fig1 = px.line(df, x="date", y=["tickets"], title="Tickets over time")
        st.plotly_chart(fig1, use_container_width=True)
    with c2:
        fig2 = px.line(df, x="date", y=["avg_handle_min"], title="Average Handle Time (min)")
        st.plotly_chart(fig2, use_container_width=True)

    # Highlight anomalies on chosen metric
    st.subheader("Anomaly view")
    fig3 = px.line(df, x="date", y=metric, title=f"{metric} with anomalies")
    anoms = df[df["anomaly"]]
    if not anoms.empty:
        fig3.add_scatter(x=anoms["date"], y=anoms[metric], mode="markers", name="anomaly", marker=dict(color="red", size=10))
    st.plotly_chart(fig3, use_container_width=True)

    st.dataframe(df.tail(20), use_container_width=True)

    # Downloads
    st.subheader("Downloads")
    csv_all = df.to_csv(index=False).encode("utf-8")
    st.download_button("Download processed CSV", data=csv_all, file_name="kpis_processed.csv", mime="text/csv")
    if not anoms.empty:
        csv_anoms = anoms.to_csv(index=False).encode("utf-8")
        st.download_button("Download anomalies CSV", data=csv_anoms, file_name="kpis_anomalies.csv", mime="text/csv")

    with st.expander("CSV schema & tips"):
        st.markdown(
            """
            Expected columns (you can remap in the UI):
            - `date`: parsable date (YYYY-MM-DD preferred)
            - `tickets`: integer count per day
            - `avg_handle_min`: average handling time in minutes
            - `csat`: satisfaction score (e.g., 1–5)
            """
        )
        st.caption("Not sure yet? Use the sample data option to explore the flow.")

    # --- Alerts section (Slack / Email) ---
    st.subheader("Alerts")
    if anoms.empty:
        st.info("No anomalies detected with current settings.")
    else:
        st.write(f"Detected {len(anoms)} anomaly point(s) for metric '{metric}'.")

        def get_env(name, default=None):
            # Check Streamlit secrets first, then env vars
            try:
                if name in st.secrets:
                    return st.secrets[name]
            except Exception:
                pass
            return os.getenv(name, default)

        # Slack alert
        slack_url = get_env("SLACK_WEBHOOK_URL")
        def send_slack_alert():
            if not slack_url:
                st.warning("Slack webhook not configured. Set SLACK_WEBHOOK_URL in .streamlit/secrets.toml or environment.")
                return
            text = (
                f":rotating_light: KPI Anomalies detected for '{metric}' ({len(anoms)} point(s))\n"
                f"Latest date: {anoms['date'].max()}\n"
                f"Threshold: mean+{k_std}*std (window={window})"
            )
            payload = json.dumps({"text": text}).encode("utf-8")
            req = urllib.request.Request(slack_url, data=payload, headers={"Content-Type": "application/json"})
            try:
                with urllib.request.urlopen(req, timeout=10) as resp:
                    if 200 <= resp.status < 300:
                        st.success("Slack alert sent.")
                    else:
                        st.error(f"Slack alert failed with status {resp.status}.")
            except Exception as e:
                st.error(f"Slack alert error: {e}")

        # Email alert via SMTP
        smtp_host = get_env("SMTP_HOST")
        smtp_port = int(get_env("SMTP_PORT", "587"))
        smtp_user = get_env("SMTP_USER")
        smtp_pass = get_env("SMTP_PASS")
        email_from = get_env("EMAIL_FROM")
        email_to = get_env("EMAIL_TO")  # comma-separated

        def send_email_alert():
            missing = [k for k in ["SMTP_HOST","SMTP_USER","SMTP_PASS","EMAIL_FROM","EMAIL_TO"] if not get_env(k)]
            if missing:
                st.warning(f"Email config missing: {', '.join(missing)}. Configure in secrets or env.")
                return
            recipients = [e.strip() for e in email_to.split(",") if e.strip()]
            msg = EmailMessage()
            msg["Subject"] = f"KPI Anomalies detected for {metric}"
            msg["From"] = email_from
            msg["To"] = ", ".join(recipients)
            body = (
                f"Anomalies detected for '{metric}'.\n"
                f"Count: {len(anoms)}\n"
                f"Latest date: {anoms['date'].max()}\n"
                f"Threshold: mean+{k_std}*std (window={window})\n\n"
                f"Recent anomalies:\n{anoms.tail(5).to_string(index=False)}\n"
            )
            msg.set_content(body)
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP(smtp_host, smtp_port, timeout=10) as server:
                    server.starttls(context=context)
                    server.login(smtp_user, smtp_pass)
                    server.send_message(msg)
                st.success("Email alert sent.")
            except Exception as e:
                st.error(f"Email alert error: {e}")

        c_slack, c_email = st.columns(2)
        if c_slack.button("Send Slack alert"):
            send_slack_alert()
        if c_email.button("Send Email alert"):
            send_email_alert()

    # --- Snapshots (SQLite) ---
    st.subheader("Snapshots (SQLite)")
    db_path = os.path.join(os.getcwd(), "data", "kpis.db")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    def init_db():
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS kpi_snapshots (
                    date TEXT PRIMARY KEY,
                    tickets INTEGER,
                    avg_handle_min REAL,
                    csat REAL,
                    anomaly_days INTEGER,
                    created_at TEXT
                )
                """
            )

    def save_snapshot():
        if df.empty:
            st.warning("No data to snapshot.")
            return
        init_db()
        last = df.iloc[-1]
        snapshot_date = pd.to_datetime(last["date"]).date().isoformat()
        anomaly_days = int(df["anomaly"].sum())
        with sqlite3.connect(db_path) as conn:
            conn.execute(
                """
                INSERT INTO kpi_snapshots (date, tickets, avg_handle_min, csat, anomaly_days, created_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
                ON CONFLICT(date) DO UPDATE SET
                    tickets=excluded.tickets,
                    avg_handle_min=excluded.avg_handle_min,
                    csat=excluded.csat,
                    anomaly_days=excluded.anomaly_days,
                    created_at=datetime('now')
                """,
                (snapshot_date, int(last["tickets"]), float(last["avg_handle_min"]), float(last["csat"]), anomaly_days)
            )
        st.success(f"Snapshot saved for {snapshot_date} -> anomaly_days={anomaly_days}")

    def load_snapshots():
        init_db()
        with sqlite3.connect(db_path) as conn:
            return pd.read_sql_query("SELECT * FROM kpi_snapshots ORDER BY date", conn, parse_dates=["date","created_at"]) 

    s1, s2 = st.columns(2)
    if s1.button("Save latest snapshot"):
        save_snapshot()
    if s2.button("View snapshot history"):
        try:
            hist = load_snapshots()
            if hist.empty:
                st.info("No snapshots saved yet.")
            else:
                st.dataframe(hist, use_container_width=True)
                st.plotly_chart(px.line(hist, x="date", y=["tickets","avg_handle_min","csat"], title="Snapshot trends"), use_container_width=True)
        except Exception as e:
            st.error(f"Failed to load snapshots: {e}")

    st.caption("Tip: Connect to your warehouse/API and schedule daily anomaly checks for alerts.")
