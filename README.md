# claims_finder

Minimal Streamlit prototype to explore publicly available data and surface potentially undervalued mining/mineral claims in the western US.

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Data (placeholders)

- **BLM MLRS** (claims & case status) — provide CSV/GeoJSON export or an API key if applicable.
- **USGS MRDS** (occurrences/past producers).
- Optional: state registries (AZ, NV, ID, UT), infrastructure layers (roads, power), elevation.

Drop any CSVs into a `data/` folder at the project root. The app will look for:
- `data/mlrs_claims.csv` with columns: `claim_id, state, status, commodity, lat, lon, filing_date, annual_maintenance_years, asking_price`
- `data/mrds.csv` with columns: `mrds_id, commodity, past_producer, lat, lon`

## Notes

This is a research tool. It is **not** legal advice, valuation advice, nor a substitute for on-site due diligence.
