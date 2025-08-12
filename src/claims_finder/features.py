import pandas as pd
from .utils import haversine_km

def nearest_distance_km(points_df: pd.DataFrame, target_lat: float, target_lon: float, k: int = 1):
    if points_df.empty:
        return float('inf')
    dists = (
        points_df
        .apply(lambda r: haversine_km(target_lat, target_lon, r['lat'], r['lon']), axis=1)
        .sort_values()
    )
    return dists.iloc[:k].mean()

def enrich_with_proximity(claims_df: pd.DataFrame, mrds_df: pd.DataFrame) -> pd.DataFrame:
    producers = mrds_df[mrds_df.get('past_producer', False) == True] if 'past_producer' in mrds_df.columns else mrds_df.iloc[0:0]
    occurrences = mrds_df

    def prox(row):
        d_prod = nearest_distance_km(producers, row['lat'], row['lon']) if not producers.empty else float('inf')
        d_occ  = nearest_distance_km(occurrences, row['lat'], row['lon']) if not occurrences.empty else float('inf')
        return pd.Series({'km_to_producer': d_prod, 'km_to_occurrence': d_occ})

    prox_df = claims_df.apply(prox, axis=1)
    return pd.concat([claims_df.reset_index(drop=True), prox_df], axis=1)
