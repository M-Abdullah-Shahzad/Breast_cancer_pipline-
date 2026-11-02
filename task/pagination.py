import pandas as pd
from sqlalchemy import text


def iter_source_chunks(source_engine, chunksize: int = 100):
    """Yield actual breast-cancer source rows in bounded chunks."""
    if chunksize < 1:
        raise ValueError("chunksize must be at least 1")

    query = text("SELECT * FROM breast_cancer")
    with source_engine.connect() as connection:
        for chunk in pd.read_sql(query, con=connection, chunksize=chunksize):
            yield chunk
