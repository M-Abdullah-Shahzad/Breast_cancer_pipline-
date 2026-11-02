import logging

from config import get_source_engine, get_target_engine
from load import load_chunk
from pagination import iter_source_chunks
from transform import transform_chunk


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_pipeline(chunksize: int = 100) -> int:
    source_engine = get_source_engine()
    target_engine = get_target_engine()
    total_rows = 0
    first_chunk = True

    try:
        for batch_number, source_chunk in enumerate(
            iter_source_chunks(source_engine, chunksize=chunksize),
            start=1,
        ):
            transformed = transform_chunk(source_chunk)
            if transformed.empty:
                continue

            mode = "replace" if first_chunk else "append"
            rows_loaded = load_chunk(transformed, target_engine, if_exists=mode)
            first_chunk = False
            total_rows += rows_loaded
            logger.info(
                "Batch %s: transformed and loaded %s rows.",
                batch_number,
                rows_loaded,
            )

        if first_chunk:
            logger.warning("No source rows were returned; target table was not changed.")
        else:
            logger.info("ETL completed. Total rows loaded: %s", total_rows)

        return total_rows
    finally:
        source_engine.dispose()
        target_engine.dispose()


if __name__ == "__main__":
    run_pipeline()
