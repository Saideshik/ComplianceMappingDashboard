# Compliance Mapping Dashboard – NIST 800-53 & ISO 27001

A lightweight Python tool to **map, track, and visualize** security controls across **NIST 800-53** and **ISO 27001**.

## ✨ Features
- Loads a CSV of controls mapped between frameworks
- Computes implemented / in-progress / not-started counts per framework
- Flags **missing evidence** automatically
- Exports **Excel dashboards** and a **gap report**
- (Optional) **Matplotlib** PNG chart
- (Optional) **Streamlit UI** for quick exploration

## 📁 Project Structure
```
ComplianceMappingDashboard/
├── compliance_mapping.csv          # sample dataset (edit or replace)
├── compliance_dashboard.py         # CLI script
├── streamlit_ui.py                 # optional Streamlit app
├── requirements.txt
└── README.md
```

## 🚀 Quick Start

```bash
# 1) Create and activate a virtual environment (recommended)
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# 2) Install dependencies
pip install -r requirements.txt

# 3) Run the generator (writes Excel files to ./build)
python compliance_dashboard.py --input compliance_mapping.csv --outdir build

# Optional: Skip chart
python compliance_dashboard.py --input compliance_mapping.csv --outdir build --no-chart

# 4) Open the outputs
# - build/Compliance_Dashboard.xlsx
# - build/Compliance_Gaps.xlsx
# - build/status_chart.png
```

## 🖥 Optional Streamlit UI
```bash
streamlit run streamlit_ui.py
```
Then upload your own `compliance_mapping.csv`.

## 🧱 CSV Schema
Required columns:
```
Control_ID, Framework, Control_Name, Mapped_To, Status, Evidence_File, Owner, Due_Date, Notes
```
Allowed `Status` values (recommended): `Implemented`, `In Progress`, `Not Started`.

## 🧪 Sample Mapping
The included CSV contains sample mappings between **NIST 800-53** and **ISO 27001 Annex A** controls to help you get started.

## 📄 License
MIT
