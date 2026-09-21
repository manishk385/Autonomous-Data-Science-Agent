import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="DSmith AI", page_icon="🤖", layout="wide")
API_URL = "http://127.0.0.1:8000"

st.markdown("""
<style>
.block-container {padding-top: 2rem; max-width: 1400px;}
.brand {font-size: 2rem; font-weight: 800;}
.subtitle {color:#6b7280;}
.status {padding:.35rem .75rem; border-radius:999px; background:#e8f7ee; color:#16803c; font-weight:600; display:inline-block;}
.card {padding:1.1rem; border:1px solid rgba(128,128,128,.22); border-radius:14px; min-height:100px;}
.card-title {color:#6b7280; font-size:.85rem;}
.card-value {font-size:1.25rem; font-weight:750;}
.pipeline {padding:1.2rem 1.4rem; border:1px solid rgba(128,128,128,.22); border-radius:14px;}
.pipeline-item {padding:.55rem 0; border-bottom:1px solid rgba(128,128,128,.12);}
.pipeline-item:last-child {border-bottom:none;}
.check {color:#16803c; font-weight:700; margin-right:.5rem;}
</style>
""", unsafe_allow_html=True)

if "result" not in st.session_state:
    st.session_state.result = None
if "history" not in st.session_state:
    st.session_state.history = []

with st.sidebar:
    st.markdown("## DSmith AI")
    st.caption("Autonomous Data Science Agent")
    st.divider()
    page = st.radio("Navigation", ["Dashboard", "New Analysis", "History"],
                     label_visibility="collapsed")
    st.divider()
    st.caption("Backend")
    try:
        health = requests.get(f"{API_URL}/health", timeout=3)
        st.success("System Ready" if health.ok else "Backend unavailable")
    except requests.RequestException:
        st.error("Backend offline")

left, right = st.columns([5, 1])
with left:
    st.markdown('<div class="brand">DSmith AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Autonomous Data Science Agent</div>', unsafe_allow_html=True)
with right:
    st.markdown('<div class="status">● System Ready</div>', unsafe_allow_html=True)
st.divider()

if page == "New Analysis":
    st.header("Autonomous Data Science Agent")
    st.write("Upload a CSV dataset and let DSmith handle cleaning, ML selection, training, and evaluation.")

    uploaded_file = st.file_uploader("Upload your dataset",type=["csv"],max_upload_size=200)
    target_column = None

    if uploaded_file is not None:
        try:
            preview_df = pd.read_csv(uploaded_file)
            st.subheader("Dataset Preview")
            st.dataframe(preview_df.head(10), use_container_width=True)
            target_column = st.selectbox(
                "Target Column", list(preview_df.columns),
                index=None, placeholder="Select target column"
            )
            st.caption(f"{preview_df.shape[0]:,} rows × {preview_df.shape[1]:,} columns")
        except Exception as exc:
            st.error(f"Could not read the CSV: {exc}")

    if st.button("Analyze Dataset", type="primary", use_container_width=True,
                  disabled=(uploaded_file is None or target_column is None)):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        data = {"target_column": target_column}
        with st.status("DSmith AI is analyzing your dataset...", expanded=True) as status:
            try:
                st.write("Uploading dataset...")
                response = requests.post(f"{API_URL}/analyze", files=files, data=data, timeout=1800)
                if response.ok:
                    result = response.json()
                    st.session_state.result = result
                    st.session_state.history.insert(0, {
                        "file": result.get("original_filename", uploaded_file.name),
                        "target": result.get("target_column", target_column),
                        "problem_type": result.get("problem_type"),
                        "best_model": result.get("best_model"),
                        "metrics": result.get("metrics"),
                    })
                    status.update(label="Analysis completed successfully", state="complete", expanded=False)
                    st.success("DSmith AI completed the analysis.")
                else:
                    status.update(label="Analysis failed", state="error", expanded=True)
                    try:
                        detail = response.json()
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error: {detail}")
            except requests.RequestException as exc:
                status.update(label="Could not connect to DSmith backend", state="error", expanded=True)
                st.error(f"Make sure FastAPI is running: uvicorn main:app --reload\n\n{exc}")

elif page == "Dashboard":
    st.header("Dashboard")
    result = st.session_state.result

    if not result:
        st.info("No analysis yet. Go to New Analysis to upload a dataset.")
    else:
        metrics = result.get("metrics") or {}
        c1, c2, c3, c4 = st.columns(4)
        cards = [
            ("Dataset", result.get("original_filename", "—")),
            ("Problem", result.get("problem_type", "—")),
            ("Best Model", result.get("best_model", "—")),
        ]
        for col, (title, value) in zip([c1, c2, c3], cards):
            with col:
                st.markdown(f'<div class="card"><div class="card-title">{title}</div><div class="card-value">{value}</div></div>', unsafe_allow_html=True)

        metric_value = "—"
        for key in ["accuracy", "f1", "f1_score", "r2", "r2_score"]:
            if key in metrics:
                value = metrics[key]
                metric_value = f"{value:.3f}" if isinstance(value, (int, float)) else str(value)
                break
        with c4:
            st.markdown(f'<div class="card"><div class="card-title">Performance</div><div class="card-value">{metric_value}</div></div>', unsafe_allow_html=True)

        st.subheader("AI Pipeline")
        steps = [
            "Dataset inspected", "Cleaning code generated", "Cleaning code validated",
            "Dataset cleaned and verified", "ML problem identified",
            "Training code generated and validated", "Model trained", "Results verified"
        ]
        st.markdown('<div class="pipeline">', unsafe_allow_html=True)
        for step in steps:
            st.markdown(f'<div class="pipeline-item"><span class="check">✓</span>{step}</div>', unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Analysis Details")
        if result.get("problem_reasoning"):
            st.write(result["problem_reasoning"])
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Selected Models**")
            for model in (result.get("selected_models") or []):
                st.write(f"• {model}")
        with col2:
            st.write("**Metrics**")
            st.json(metrics)

        downloads = result.get("downloads") or {}
        st.subheader("Downloads")
        d1, d2 = st.columns(2)
        with d1:
            url = downloads.get("cleaned_dataset")
            if url:
                r = requests.get(f"{API_URL}{url}", timeout=30)
                if r.ok:
                    st.download_button("Download Cleaned Dataset", r.content,
                                       "cleaned_dataset.csv", "text/csv", use_container_width=True)
        with d2:
            url = downloads.get("trained_model")
            if url:
                r = requests.get(f"{API_URL}{url}", timeout=30)
                if r.ok:
                    st.download_button("Download Trained Model", r.content,
                                       "best_model.joblib", "application/octet-stream", use_container_width=True)

else:
    st.header("Analysis History")
    if not st.session_state.history:
        st.info("No completed analyses yet.")
    else:
        for item in st.session_state.history:
            with st.expander(f"{item.get('file', 'Dataset')} — {item.get('problem_type', 'Unknown')}"):
                st.write(f"**Target:** {item.get('target', '—')}")
                st.write(f"**Best Model:** {item.get('best_model', '—')}")
                st.json(item.get("metrics") or {})