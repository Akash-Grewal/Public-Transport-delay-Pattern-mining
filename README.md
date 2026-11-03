# Public Transport Delay Pattern Mining (Data Mining Mini Project)

Implementation of the design in `docs/Public_Transport_Delay_Pattern_Mining_Mini_Project_Report.docx`.

> **Important:** `data/sample_bus_trips.csv` is **synthetic** (made by `data/generate_sample_data.py`).
> Results from it demonstrate the workflow only and are **not** findings about any real transport network.
> To get real findings, run the pipeline on a documented real dataset and cite it in the report.

## Quick start
```bash
pip install -r requirements.txt
python data/generate_sample_data.py          # (optional) regenerate the synthetic sample
python main.py                               # run everything -> outputs/
python -m unittest -v                        # run tests T-01 .. T-08 (+ extras)
```
Open `outputs/dashboard.html` in a browser for the local dashboard.

Use your own data:
```bash
python main.py --input my_trips.csv --threshold 5 --min-support 0.03 --min-confidence 0.6 \
               --dataset-note "Source: <provider>, <title>, <date range>, <licence>"
```
Required CSV columns: `trip_id, route_id, stop_id, scheduled_arrival, actual_arrival`
Optional: `weather, traffic_level` (if absent, the analysis runs without inventing them).

## Structure
| Path | Purpose | Report ref |
|---|---|---|
| `main.py` | Runs the full pipeline, writes `outputs/` | 6.3, 6.7 |
| `src/config.py` | Threshold (5 min, strict `>`), thresholds, seeds | 5.2 |
| `src/preprocessing.py` | Validation, cleaning, delay + label | FR-01..03 |
| `src/features.py` | Time bands, day type (scheduled-time only) | 5.1 |
| `src/summaries.py` | Route / stop / time-band summaries | FR-04 |
| `src/association.py` | Own Apriori; rules → Delayed (support, confidence, lift) | FR-05, 5.3 |
| `src/clustering.py` | Scaled K-Means on route-segment profiles | FR-06 |
| `src/classification.py` | Decision tree vs majority baseline; chronological split; leakage guard | FR-07 |
| `src/visualize.py`, `src/dashboard.py` | Charts + static HTML dashboard | FR-08 |
| `tests/test_pipeline.py` | Automated tests mapped to Section 6.8 | 6.8 |
| `data/` | Synthetic generator + generated CSV | 6.4 |
| `outputs/` | Generated tables, JSON metrics, charts, dashboard | - |
| `docs/` | The project report (.docx) | - |

## Key design decisions
- **Delay** = actual − scheduled (minutes). **Delayed** if delay `>` 5 min; exactly 5 = On-time (T-06).
- Rows are never silently dropped: `outputs/rejected_rows.csv` lists each with a reason; `data_quality_report.json` counts them.
- Midnight crossing: if actual is >12 h *before* scheduled, one day is added; implausible |delay| > 180 min is rejected.
- Predictors use only pre-arrival info; `actual_arrival`, `delay_minutes`, `delayed` are blocked (data leakage guard).
- Train/test split is chronological (earliest 80% / latest 20%); metrics are on the test set only.
- Association rules are exploratory; an association is not proof of causation.

## Outputs
`cleaned_data.csv, rejected_rows.csv, data_quality_report.json, route_summary.csv, stop_summary.csv,
time_band_summary.csv, association_rules.csv, segment_clusters.csv, cluster_summary.csv,
model_metrics.json, charts/*.png, dashboard.html`
