#!/usr/bin/env python3
"""
Compliance Mapping Dashboard – NIST 800-53 & ISO 27001
Author: Sai Deshik
Description:
  - Loads a controls mapping CSV
  - Computes status summaries per framework
  - Flags missing evidence
  - Exports Excel dashboards & gap lists
  - (Optional) Renders a quick chart using matplotlib
"""
import argparse
import sys
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

REQUIRED_COLUMNS = [
    "Control_ID","Framework","Control_Name","Mapped_To","Status",
    "Evidence_File","Owner","Due_Date","Notes"
]

def validate_columns(df: pd.DataFrame):
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

def compute_summaries(df: pd.DataFrame):
    # Standardize categorical fields
    df["Framework"] = df["Framework"].str.strip().str.upper()
    df["Status"] = df["Status"].str.strip().str.title()  # Implemented/In Progress/Not Started

    # Evidence status
    df["Evidence_Provided"] = df["Evidence_File"].apply(lambda x: "Yes" if pd.notna(x) and str(x).strip().upper() not in {"N/A", ""} else "No")

    # Summary tables
    status_summary = df.groupby(["Framework","Status"]).size().unstack(fill_value=0)
    evidence_summary = df.groupby(["Framework","Evidence_Provided"]).size().unstack(fill_value=0)

    # Compliance percentage per framework (Implemented / total)
    total_per_fw = df.groupby("Framework")["Control_ID"].count()
    implemented_per_fw = df[df["Status"]=="Implemented"].groupby("Framework")["Control_ID"].count()
    compliance_pct = (implemented_per_fw / total_per_fw * 100).fillna(0).round(1).rename("Compliance_%")

    return df, status_summary, evidence_summary, compliance_pct

def export_excels(output_dir: Path, df: pd.DataFrame, status_summary: pd.DataFrame, evidence_summary: pd.DataFrame, compliance_pct: pd.Series):
    output_dir.mkdir(parents=True, exist_ok=True)

    # Detail dashboard
    detail_path = output_dir / "Compliance_Dashboard.xlsx"
    with pd.ExcelWriter(detail_path, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="Controls", index=False)
        status_summary.to_excel(writer, sheet_name="Status_Summary")
        evidence_summary.to_excel(writer, sheet_name="Evidence_Summary")
        compliance_pct.to_frame().to_excel(writer, sheet_name="Compliance_%")
    print(f"[+] Wrote {detail_path}")

    # Gap list
    gaps = df[(df["Status"]!="Implemented") | (df["Evidence_Provided"]=="No")].copy()
    gaps.sort_values(by=["Framework","Status","Control_ID"], inplace=True)
    gaps_path = output_dir / "Compliance_Gaps.xlsx"
    gaps.to_excel(gaps_path, index=False)
    print(f"[+] Wrote {gaps_path}")

def render_chart(status_summary: pd.DataFrame, output_dir: Path):
    # Simple bar chart with matplotlib (per tool rules)
    ax = status_summary.plot(kind="bar")
    ax.set_title("Compliance Status by Framework")
    ax.set_xlabel("Framework")
    ax.set_ylabel("Number of Controls")
    fig = ax.get_figure()
    chart_path = output_dir / "status_chart.png"
    fig.savefig(chart_path, bbox_inches="tight")
    plt.close(fig)
    print(f"[+] Wrote {chart_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate compliance mapping dashboards.")
    parser.add_argument("--input", default="compliance_mapping.csv", help="Path to compliance mapping CSV")
    parser.add_argument("--outdir", default="build", help="Output directory for reports")
    parser.add_argument("--no-chart", action="store_true", help="Skip writing a status chart PNG")
    args = parser.parse_args()

    src = Path(args.input)
    if not src.exists():
        print(f"[-] Input CSV not found: {src}", file=sys.stderr)
        sys.exit(1)

    df = pd.read_csv(src)
    validate_columns(df)
    df, status_summary, evidence_summary, compliance_pct = compute_summaries(df)

    outdir = Path(args.outdir)
    export_excels(outdir, df, status_summary, evidence_summary, compliance_pct)

    if not args.no_chart:
        render_chart(status_summary, outdir)

    print("[+] Done. Open the Excel files in the output directory.")

if __name__ == "__main__":
    main()
