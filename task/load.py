import pandas as pd


def load_chunk(
    dataframe: pd.DataFrame,
    target_engine,
    if_exists: str = "append",
    chunksize: int = 500,
) -> int:
    """Load one transformed chunk inside a database transaction."""
    if dataframe.empty:
        return 0
    with target_engine.begin() as connection:
        dataframe.to_sql(
            "transformed_breast_cancer",
            con=connection,
            if_exists=if_exists,
            index=False,
            chunksize=chunksize,
            method="multi",
        )
    return len(dataframe)
