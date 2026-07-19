"""
Appendix C.7. Cloud/Shadow Masking in the NDVI Extraction.

Compares growing-season NDVI extracted with an explicit SummaryQA-band
cloud/shadow mask against the unfiltered baseline used throughout the main
analysis, for all 19 sample districts in four years (2000, 2012, 2019,
2024). The QA-masked comparison data (data/gee_outputs/ndvi_qa_comparison.csv)
was generated separately via Google Earth Engine -- see
gee_notebook/GEE_Before_After_Images.ipynb for the extraction approach --
since it requires querying a different (QA-masked) image collection than
the primary NDVI series in data/raw/.

Produces: output/AppendixC7_qa_ndvi_comparison.csv
"""
import pandas as pd
from _paths import GEE_DIR, OUTPUT_DIR

df = pd.read_csv(GEE_DIR / "ndvi_qa_comparison.csv")
df["diff"] = df["ndvi_raw"] - df["ndvi_qa_filtered"]

treated_lowland = ["Aghdam", "Fuzuli", "Jabrayil", "Khojavand"]
treated_mountainous = ["Kalbajar", "Lachin", "Shusha", "Gubadli", "Zangilan"]
donors = ["Tartar", "Goranboy", "Barda", "Aghjabadi", "Beylagan", "Jalilabad", "Gadabay", "Dashkasan", "Gazakh", "Tovuz"]


def classify(d):
    if d in treated_mountainous:
        return "Mountainous treated"
    if d in treated_lowland:
        return "Lowland treated"
    if d in donors:
        return "Donor"
    return "Other"


df["group"] = df["district"].apply(classify)
summary = df.groupby("group")["diff"].agg(["mean", "std", "min", "max", "count"]).round(4)
print(summary.to_string())
print(f"\nOverall correlation (raw vs QA-filtered): {df['ndvi_raw'].corr(df['ndvi_qa_filtered']):.3f}")

summary.to_csv(OUTPUT_DIR / "AppendixC7_qa_ndvi_comparison.csv")
