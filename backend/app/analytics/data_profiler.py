import pandas as pd
import numpy as np
from typing import Any

def profile_dataframe(df: pd.DataFrame) -> dict:
    """Compute EDA statistics for a dataframe using pandas/numpy."""
    profile = {
        "shape": {"rows": len(df), "columns": len(df.columns)},
        "columns": {},
        "missing_values": {},
        "correlation_matrix": None,
        "sample": df.head(5).fillna("").to_dict(orient="records"),
    }

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    for col in df.columns:
        col_info = {
            "dtype": str(df[col].dtype),
            "null_count": int(df[col].isnull().sum()),
            "null_pct": round(df[col].isnull().mean() * 100, 2),
            "unique_count": int(df[col].nunique()),
        }
        if col in numeric_cols:
            col_info.update({
                "mean": round(float(df[col].mean()), 4) if not df[col].isnull().all() else None,
                "std": round(float(df[col].std()), 4) if not df[col].isnull().all() else None,
                "min": round(float(df[col].min()), 4) if not df[col].isnull().all() else None,
                "max": round(float(df[col].max()), 4) if not df[col].isnull().all() else None,
                "median": round(float(df[col].median()), 4) if not df[col].isnull().all() else None,
                "q25": round(float(df[col].quantile(0.25)), 4) if not df[col].isnull().all() else None,
                "q75": round(float(df[col].quantile(0.75)), 4) if not df[col].isnull().all() else None,
            })
        else:
            top_vals = df[col].value_counts().head(5).to_dict()
            col_info["top_values"] = {str(k): int(v) for k, v in top_vals.items()}
        profile["columns"][col] = col_info
        profile["missing_values"][col] = col_info["null_count"]

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr().round(4)
        profile["correlation_matrix"] = corr.fillna(0).to_dict()

    return profile

def get_schema_summary(df: pd.DataFrame) -> str:
    """Return a compact schema string for LLM prompts."""
    lines = [f"DataFrame with {len(df)} rows and {len(df.columns)} columns:"]
    for col in df.columns:
        dtype = str(df[col].dtype)
        nulls = int(df[col].isnull().sum())
        lines.append(f"  - {col} ({dtype}), {nulls} nulls")
    return "\n".join(lines)
