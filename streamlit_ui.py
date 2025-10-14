#!/usr/bin/env python3
# Streamlit UI for Compliance Mapping Dashboard (Optional)
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Compliance Mapping Dashboard", layout="wide")

st.title("Compliance Mapping Dashboard – NIST 800-53 & ISO 27001")
st.caption("Upload your mapping CSV to explore status, evidence and gaps.")

uploaded = st.file_uploader("Upload compliance_mapping.csv", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
    required = ["Control_ID","Framework","Control_Name","Mapped_To","Status","Evidence_File","Owner","Due_Date","Notes"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        st.error(f"Missing required columns: {missing}")
    else:
        df["Framework"] = df["Framework"].str.strip().str.upper()
        df["Status"] = df["Status"].str.strip().str.title()
        df["Evidence_Provided"] = df["Evidence_File"].apply(lambda x: "Yes" if pd.notna(x) and str(x).strip().upper() not in {"N/A", ""} else "No")

        st.subheader("Controls")
        st.dataframe(df, use_container_width=True)

        st.subheader("Status Summary")
        status_summary = df.groupby(["Framework","Status"]).size().unstack(fill_value=0)
        st.dataframe(status_summary)

        st.subheader("Evidence Summary")
        evidence_summary = df.groupby(["Framework","Evidence_Provided"]).size().unstack(fill_value=0)
        st.dataframe(evidence_summary)

        st.subheader("Gaps (Not Implemented or Missing Evidence)")
        gaps = df[(df["Status"]!="Implemented") | (df["Evidence_Provided"]=="No")]
        st.dataframe(gaps)
else:
    st.info("Upload a CSV to begin. A sample 'compliance_mapping.csv' is included in the repository.")
