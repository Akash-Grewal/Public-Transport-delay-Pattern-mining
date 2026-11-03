"""Run the full pipeline:  python main.py [--input data/sample_bus_trips.csv]

load -> validate/clean -> features -> summaries -> association rules ->
clustering -> classification -> charts -> dashboard
"""
import argparse
import json
import os

from src import config
from src.association import mine_rules
from src.classification import train_and_evaluate
from src.clustering import cluster_segments, cluster_summary
from src.dashboard import build_dashboard
from src.features import add_features
from src.preprocessing import clean, load_data
from src.summaries import route_summary, stop_summary, time_band_summary
from src.visualize import make_charts


def run(input_path, outdir, threshold, min_support, min_conf, dataset_note):
    os.makedirs(outdir, exist_ok=True)
    raw = load_data(input_path)
    df, rejected, report = clean(raw, threshold=threshold)
    df = add_features(df)
    df.attrs["threshold"] = threshold

    df.to_csv(os.path.join(outdir, "cleaned_data.csv"), index=False)
    rejected.to_csv(os.path.join(outdir, "rejected_rows.csv"), index=False)
    with open(os.path.join(outdir, "data_quality_report.json"), "w") as f:
        json.dump(report, f, indent=2)

    rs, ss, ts = route_summary(df), stop_summary(df), time_band_summary(df)
    rs.to_csv(os.path.join(outdir, "route_summary.csv"), index=False)
    ss.to_csv(os.path.join(outdir, "stop_summary.csv"), index=False)
    ts.to_csv(os.path.join(outdir, "time_band_summary.csv"), index=False)

    rules = mine_rules(df, min_support, min_conf)
    rules.to_csv(os.path.join(outdir, "association_rules.csv"), index=False)

    seg, cinfo = cluster_segments(df)
    seg.to_csv(os.path.join(outdir, "segment_clusters.csv"), index=False)
    clus_s = cluster_summary(seg)
    clus_s.to_csv(os.path.join(outdir, "cluster_summary.csv"), index=False)

    metrics = train_and_evaluate(df)
    with open(os.path.join(outdir, "model_metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    charts = make_charts(df, seg, metrics, os.path.join(outdir, "charts"))
    dash = build_dashboard(outdir, charts, report, rs, ts, rules, clus_s, metrics, dataset_note)

    print("Data quality:", json.dumps(report, indent=2))
    print(f"\nRules found: {len(rules)} (min_support={min_support}, min_confidence={min_conf})")
    if len(rules):
        print(rules.head(5).to_string(index=False))
    print("\nClustering:", cinfo)
    print("\nDecision tree:", json.dumps(metrics["decision_tree"]))
    print("Majority baseline:", json.dumps(metrics["majority_baseline"]))
    print(f"\nDashboard: {dash}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--input", default="data/sample_bus_trips.csv")
    ap.add_argument("--output-dir", default="outputs")
    ap.add_argument("--threshold", type=float, default=config.DELAY_THRESHOLD_MIN)
    ap.add_argument("--min-support", type=float, default=config.MIN_SUPPORT)
    ap.add_argument("--min-confidence", type=float, default=config.MIN_CONFIDENCE)
    ap.add_argument("--dataset-note", default="Results shown are from the SYNTHETIC sample dataset "
                    "(data/generate_sample_data.py). They illustrate the workflow only and are not "
                    "findings about any real transport system.")
    a = ap.parse_args()
    run(a.input, a.output_dir, a.threshold, a.min_support, a.min_confidence, a.dataset_note)
