import os, sys
import pandas as pd
import streamlit as st
import pydeck as pdk

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from claims_finder.data_sources.mlrs import load_mlrs_csv
from claims_finder.data_sources.mrds import load_mrds_csv
from claims_finder.features import enrich_with_proximity
from claims_finder.scoring import score_frame

st.set_page_config(page_title="Claims Finder", layout="wide")
st.title("⛏️ Claims Finder — undervaluation explorer (prototype)")

st.sidebar.header("Filters")
focus_commodities = st.sidebar.multiselect("Focus commodities", ["Gold","Silver","Copper","Lithium","Rare Earths"])
max_distance_km = st.sidebar.slider("Max km to past producer", 0, 100, 25)
state_filter = st.sidebar.multiselect("States", ["AZ","NV","ID","UT","CO","OR","WA","WY","MT","NM","CA"])

data_dir = "data"
mlrs_path = os.path.join(data_dir, "mlrs_claims.csv")
mrds_path = os.path.join(data_dir, "mrds.csv")

st.info("Drop CSVs into a `data/` folder: `mlrs_claims.csv`, `mrds.csv`. Columns are described in README.")
if not (os.path.exists(mlrs_path) and os.path.exists(mrds_path)):
    st.warning("Sample data not found. Create `data/mlrs_claims.csv` and `data/mrds.csv` to proceed.")
    st.stop()

mlrs = load_mlrs_csv(mlrs_path)
mrds = load_mrds_csv(mrds_path)

mlrs = mlrs.dropna(subset=['lat','lon'])
mrds = mrds.dropna(subset=['lat','lon'])

df = enrich_with_proximity(mlrs, mrds)
df = score_frame(df, focus_commodities=focus_commodities)

if state_filter:
    df = df[df['state'].isin(state_filter)]
df = df[df['km_to_producer'] <= max_distance_km]

st.subheader("Ranked candidates")
st.dataframe(df[['claim_id','state','status','commodity','uv_score','km_to_producer','asking_price']].head(200))

if not df.empty:
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position='[lon, lat]',
        get_radius=250,
        pickable=True,
    )
    view_state = pdk.ViewState(latitude=float(df['lat'].mean()), longitude=float(df['lon'].mean()), zoom=5)
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state, tooltip={"text": "{claim_id}\n{commodity}\nScore: {uv_score}"}))

st.caption("Research prototype. Not valuation advice; verify all facts with authoritative sources.")
