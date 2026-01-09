import streamlit as st
import json
import subprocess
import time
import sys
import os
from datetime import date
import pandas as pd

# ---------------------------------------
# API Key from Streamlit Cloud Secrets
# ---------------------------------------
API_KEY = st.secrets["NCBI_API_KEY"]

# ---------------------------------------
# Country List
# ---------------------------------------
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

# ---------------------------------------
# UI
# ---------------------------------------
st.set_page_config(page_title="PubMed HCP Extractor", layout="wide")
st.title("PubMed HCP Data Extraction Platform")

with st.form("config_form"):
    search_query = st.text_area("PubMed Search Query", value="cardiologist")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Start Date", date(2015,1,1))
    with col2:
        end_date = st.date_input("End Date", date(2026,12,31))

    selected_countries = st.multiselect("Target Countries", countries)
    max_papers = st.slider("Number of papers", 10, 10000, 1000, 10)
    ncbi_email = st.text_input("NCBI Email")

    est = max_papers / 10 / 60
    st.info(f"Estimated time: {est:.1f} minutes")

    run_btn = st.form_submit_button("Run Extraction")

if run_btn and not ncbi_email:
    st.error("NCBI Email is required")
    st.stop()

# ---------------------------------------
# Run backend
# ---------------------------------------
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
        "ncbi_email": ncbi_email,
        "ncbi_api_key": API_KEY
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    # Start backend
    process = subprocess.Popen([sys.executable, "main.py"])

    bar = st.progress(0)
    status = st.empty()

    # Live progress loop
    while process.poll() is None:
        if os.path.exists("logs/progress.json"):
            with open("logs/progress.json") as f:
                prog = json.load(f)

            percent = prog.get("percent", 0)
            current = prog.get("current", 0)
            total = prog.get("total", 0)

            bar.progress(percent / 100)
            status.write(f"Processed {current} / {total} papers ({percent}%)")

        time.sleep(1)

    if process.returncode == 0:
        st.success("Extraction completed")

        df = pd.read_excel("data/raw/pubmed_contacts.xlsx")
        st.dataframe(df.head(20), use_container_width=True)

        with open("data/raw/pubmed_contacts.xlsx", "rb") as f:
            st.download_button("Download Excel", f, "pubmed_contacts.xlsx")
    else:
        st.error("Extraction failed")
