import numpy as np
import pandas as pd


def transform_chunk(source_chunk: pd.DataFrame) -> pd.DataFrame:
    """Normalize source columns and derive age/risk fields for one chunk."""
    if source_chunk is None or source_chunk.empty:
        return pd.DataFrame()

    dataframe = source_chunk.copy()
    dataframe.columns = (
        dataframe.columns.astype(str).str.strip().str.lower().str.replace(" ", "_")
    )

    for column in ("tumor_size", "age", "survival_months"):
        if column in dataframe.columns:
            dataframe[column] = pd.to_numeric(dataframe[column], errors="coerce")

    for column in dataframe.select_dtypes(include=["object", "string"]).columns:
        dataframe[column] = (
            dataframe[column].astype("string").str.strip().str.upper()
        )

    dataframe = dataframe.replace(["NAN", "NONE", "NULL", ""], pd.NA)

    if "age" in dataframe.columns:
        dataframe["age"] = dataframe["age"].fillna(0)
        dataframe["age_group"] = np.select(
            [dataframe["age"] > 60, dataframe["age"] >= 40],
            ["SENIOR", "MIDDLE"],
            default="YOUNG",
        )

    if "tumor_size" in dataframe.columns:
        dataframe["tumor_size"] = dataframe["tumor_size"].fillna(0)

    if {"age", "tumor_size"}.issubset(dataframe.columns):
        dataframe["is_high_risk"] = (
            (dataframe["tumor_size"] > 20) | (dataframe["age"] > 60)
        ).astype(int)

    return dataframe.drop_duplicates().reset_index(drop=True)
