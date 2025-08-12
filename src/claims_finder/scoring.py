import pandas as pd
import numpy as np
from .utils import parse_date

DEFAULT_WEIGHTS = {
    'recent_activity_bonus': 0.15,
    'near_past_producer': 0.25,
    'near_occurrence': 0.10,
    'commodity_interest': 0.20,
    'asking_price_value': 0.30
}

def compute_score(row: pd.Series, weights: dict = None, focus_commodities=None, inflation_idx: float = 1.0) -> float:
    w = weights or DEFAULT_WEIGHTS
    focus = set([c.strip().upper() for c in (focus_commodities or [])])

    years = row.get('annual_maintenance_years', 0) or 0
    activity = min(years / 5.0, 1.0)

    d_prod = row.get('km_to_producer', np.inf)
    d_occ  = row.get('km_to_occurrence', np.inf)
    near_prod = 1.0 if d_prod == 0 else np.exp(-d_prod/10) if np.isfinite(d_prod) else 0.0
    near_occ  = 1.0 if d_occ == 0 else np.exp(-d_occ/15) if np.isfinite(d_occ) else 0.0

    comm = str(row.get('commodity', '')).upper()
    commodity_match = 1.0 if (focus and any(c in comm for c in focus)) else 0.3 if not focus else 0.0

    price = row.get('asking_price', None)
    if price in (None, "") or float(price) <= 0:
        price_val = 0.5
    else:
        rel = float(price) / max(inflation_idx, 1e-6)
        price_val = 1 / (1 + np.log1p(rel))

    score = (
        w['recent_activity_bonus'] * activity +
        w['near_past_producer']   * near_prod +
        w['near_occurrence']      * near_occ +
        w['commodity_interest']   * commodity_match +
        w['asking_price_value']   * price_val
    )
    return float(round(score, 4))

def score_frame(df: pd.DataFrame, **kwargs) -> pd.DataFrame:
    out = df.copy()
    out['uv_score'] = out.apply(lambda r: compute_score(r, **kwargs), axis=1)
    return out.sort_values('uv_score', ascending=False).reset_index(drop=True)
