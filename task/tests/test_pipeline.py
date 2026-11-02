import pandas as pd
from sqlalchemy import create_engine, text

from pagination import iter_source_chunks
from transform import transform_chunk
from load import load_chunk


def test_iter_source_chunks_reads_actual_rows_in_chunks():
    source = create_engine("sqlite:///:memory:")
    try:
        pd.DataFrame({"id": [1, 2, 3], "Age": [35, 45, 65]}).to_sql(
            "breast_cancer", source, index=False
        )
        chunks = list(iter_source_chunks(source, chunksize=2))
        assert [len(chunk) for chunk in chunks] == [2, 1]
        assert sum(len(chunk) for chunk in chunks) == 3
    finally:
        source.dispose()


def test_transform_chunk_adds_age_group_and_risk_flag():
    source = pd.DataFrame({
        "Age": [35, 45, 65],
        "Tumor Size": [10, 25, 12],
        "Status": ["alive", "dead", "alive"],
    })
    result = transform_chunk(source)

    assert result["age_group"].tolist() == ["YOUNG", "MIDDLE", "SENIOR"]
    assert result["is_high_risk"].tolist() == [0, 1, 1]
    assert result["status"].tolist() == ["ALIVE", "DEAD", "ALIVE"]


def test_load_chunk_replaces_then_appends_in_sqlite():
    target = create_engine("sqlite:///:memory:")
    try:
        first = pd.DataFrame({"age": [35], "age_group": ["YOUNG"]})
        second = pd.DataFrame({"age": [65], "age_group": ["SENIOR"]})
        assert load_chunk(first, target, if_exists="replace") == 1
        assert load_chunk(second, target, if_exists="append") == 1

        with target.connect() as connection:
            count = connection.execute(
                text("SELECT COUNT(*) FROM transformed_breast_cancer")
            ).scalar_one()
        assert count == 2
    finally:
        target.dispose()
