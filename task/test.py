import pandas as pd

from config import get_source_engine, get_target_engine


def main() -> None:
    source_engine = get_source_engine()
    target_engine = get_target_engine()
    try:
        source = pd.read_sql(
            "SELECT * FROM breast_cancer",
            con=source_engine,
        )
        target = pd.read_sql(
            "SELECT * FROM transformed_breast_cancer",
            con=target_engine,
        )
        print("Source rows:", len(source))
        print("Target rows:", len(target))
        print("\nSource sample:")
        print(source.head(3))
        print("\nTransformed target sample:")
        print(target.head(3))
    finally:
        source_engine.dispose()
        target_engine.dispose()


if __name__ == "__main__":
    main()
