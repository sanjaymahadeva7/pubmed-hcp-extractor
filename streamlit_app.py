import streamlit as st
import json
import subprocess
import time
import sys
import os
from datetime import date
import pandas as pd

# -----------------------------
# Secrets
# -----------------------------
API_KEY = st.secrets["NCBI_API_KEY"]
SYSTEM_EMAIL = st.secrets["NCBI_EMAIL"]

# -----------------------------
# Country List
# -----------------------------
countries = [
'US','Canada','Mexico','Brazil','Argentina','Chile','Colombia','Peru','Venezuela',
'Bolivia','Ecuador','Paraguay','Uruguay','Guyana','Suriname',
'UK','Ireland','France','Germany','Italy','Spain','Portugal','Netherlands','Belgium',
'Switzerland','Austria','Sweden','Norway','Finland','Denmark','Poland','Czech Republic',
'Slovakia','Hungary','Romania','Bulgaria','Croatia','Slovenia','Serbia',
'Bosnia and Herzegovina','Greece','Cyprus','Lithuania','Latvia','Estonia','Ukraine',
'Russia','Belarus','Moldova','Iceland','Luxembourg','Malta','Monaco','Andorra',
'Liechtenstein','San Marino','Vatican City',
'India','China','Japan','South Korea','North Korea','Taiwan','Singapore','Malaysia',
'Indonesia','Philippines','Thailand','Vietnam','Cambodia','Laos','Myanmar','Sri Lanka',
'Nepal','Bangladesh','Pakistan','Afghanistan','Iran','Iraq','Saudi Arabia','UAE',
'Qatar','Kuwait','Oman','Yemen','Israel','Palestine','Jordan','Lebanon','Syria','Turkey',
'Georgia','Armenia','Azerbaijan','Kazakhstan','Uzbekistan','Turkmenistan','Kyrgyzstan',
'Tajikistan','Mongolia',
'South Africa','Egypt','Nigeria','Kenya','Ethiopia','Ghana','Morocco','Algeria',
'Tunisia','Libya','Sudan','Uganda','Tanzania','Zambia','Zimbabwe','Botswana','Namibia',
'Mozambique','Angola','Cameroon','Ivory Coast','Senegal','Rwanda','Somalia',
'Australia','New Zealand','Fiji','Papua New Guinea','Bahrain'
]

# -----------------------------
# Page
# -----------------------------
st.set_page_config(page_title="PubMed HCP Extractor", layout="wide")
st.title("PubMed HCP Data Extraction Platform")

# -----------------------------
# Paper count state
# -----------------------------
if "paper_count" not in st.session_state:
    st.session_state.paper_count = 1000

def set_from_slider():
    st.session_state.paper_count = st.session_state.slider_val
    st.rerun()

def set_from_input():
    st.session_state.paper_count = st.session_state.input_val
    st.rerun()

# -----------------------------
# Paper selector
# -----------------------------
st.subheader("Number of Papers")
c1, c2 = st.columns([4,1])

with c1:
    st.slider(
        "Select",
        10, 10000,
        st.session_state.paper_count,
        10,
        key="slider_val",
        on_change=set_from_slider
    )

with c2:
    st.number_input(
        "Manual",
        10, 10000,
        st.session_state.paper_count,
        10,
        key="input_val",
        on_change=set_from_input
    )

max_papers = st.session_state.paper_count
st.caption(f"Selected: {max_papers} papers")

# -----------------------------
# Main Form
# -----------------------------
with st.form("config_form"):
    search_query = st.text_area("PubMed Search Query", value="cardiologist")

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date(2015,1,1))
    with col2:
        end_date = st.date_input("End Date", date(2026,12,31))

    selected_countries = st.multiselect("Target Countries", countries)

    user_email = st.text_input("Your Email (optional)")

    est = max_papers / 10 / 60
    st.info(f"Estimated time: {est:.1f} minutes")

    run_btn = st.form_submit_button("Run Extraction")

email_to_use = user_email if user_email else SYSTEM_EMAIL

# -----------------------------
# Run backend
# -----------------------------
if run_btn:

    config = {
        "search_query": search_query,
        "date_range": {
            "enabled": True,
            "start_date": start_date.strftime("%Y/%m/%d"),
            "end_date": end_date.strftime("%Y/%m/%d"),
            "date_type": "pdat"
        },
        "target_countries": selected_countries,
        "start_result": 1,
        "end_result": max_papers,
        "email_required": True,
        "output_filename": "data/raw/pubmed_contacts.xlsx",
        "log_filename": "logs/extraction_log.txt",
        "ncbi_email": email_to_use,
        "ncbi_api_key": API_KEY
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    st.subheader("Extraction Progress")
    progress_container = st.empty()
    status_container = st.empty()

    process = subprocess.Popen([sys.executable, "main.py"])

    while process.poll() is None:
        if os.path.exists("logs/progress.json"):
            with open("logs/progress.json") as f:
                p = json.load(f)

            progress_container.progress(p["percent"] / 100)
            status_container.write(f"Processed {p['current']} / {p['total']} papers ({p['percent']}%)")

        time.sleep(1)

    if process.returncode == 0:
        st.success("Extraction completed")

        df = pd.read_excel("data/raw/pubmed_contacts.xlsx")
        st.dataframe(df.head(20), use_container_width=True)

        with open("data/raw/pubmed_contacts.xlsx", "rb") as f:
            st.download_button("Download Excel", f, "pubmed_contacts.xlsx")
    else:
        st.error("Extraction failed")
