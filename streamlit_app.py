"""Read-only Streamlit demo for the CrimeVision sample cases."""
import json
from pathlib import Path

import streamlit as st


BASE_DIR = Path(__file__).resolve().parent
CASES_DIR = BASE_DIR / "data" / "cases"
SAMPLES_DIR = BASE_DIR / "backend" / "static" / "samples"

st.set_page_config(page_title="CrimeVision AI Demo", page_icon="🔎", layout="wide")
st.title("CrimeVision AI")
st.caption("Read-only demo using the included sample case records and evidence.")

case_files = sorted(CASES_DIR.glob("*.json"))
if not case_files:
    st.error("No sample case records were found in data/cases.")
    st.stop()

cases = []
for case_file in case_files:
    with case_file.open("r", encoding="utf-8") as file:
        cases.append(json.load(file))

selected_id = st.selectbox(
    "Select a case",
    options=[case["case_id"] for case in cases],
    format_func=lambda case_id: next(
        f"{case_id} — {case['title']}" for case in cases if case["case_id"] == case_id
    ),
)
case = next(case for case in cases if case["case_id"] == selected_id)

st.subheader(case.get("title", selected_id))
summary = st.columns(4)
summary[0].metric("Incident", case.get("incident_type", "Not specified"))
summary[1].metric("Status", case.get("status", "Not specified"))
summary[2].metric("Evidence items", len(case.get("evidence", [])))
summary[3].metric("Incident date", case.get("incident_date", "Not specified"))
st.write(f"**Location:** {case.get('location', 'Not specified')}")

classification = case.get("crime_classification", {})
if classification:
    st.markdown("### Case classification")
    st.write(classification.get("primary_category", "Not specified"))
    if "confidence" in classification:
        st.metric("Classification confidence", f"{classification['confidence']:.1%}")

evidence_tab, custody_tab = st.tabs(["Evidence", "Chain of custody"])
with evidence_tab:
    for evidence in case.get("evidence", []):
        with st.expander(
            f"{evidence.get('type', 'Evidence').title()}: {evidence.get('label', 'Evidence item')}"
        ):
            st.write(f"**Timestamp:** {evidence.get('timestamp', 'Not specified')}")
            st.write(f"**SHA-256:** `{evidence.get('sha256', 'Not recorded')}`")
            filename = Path(evidence.get("file_path", "")).name
            sample_path = SAMPLES_DIR / filename
            if sample_path.is_file():
                suffix = sample_path.suffix.lower()
                if suffix in {".jpg", ".jpeg", ".png"}:
                    st.image(str(sample_path), use_container_width=True)
                elif suffix in {".wav", ".mp3", ".ogg"}:
                    st.audio(str(sample_path))

with custody_tab:
    records = case.get("chain_of_custody", [])
    if records:
        st.dataframe(records, use_container_width=True, hide_index=True)
    else:
        st.info("No chain-of-custody records are available for this case.")
