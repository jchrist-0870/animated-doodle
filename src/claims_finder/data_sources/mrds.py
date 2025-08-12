import pandas as pd

def load_mrds_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ['lat','lon']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    return df
