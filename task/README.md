# Breast Cancer ETL Package

This directory contains the ETL modules and SQL analysis scripts.

Run from the repository root:

- `python task/etl_pipeline.py` — run the chunked MySQL-to-PostgreSQL ETL.
- `python task/main.py` — run the descriptive MySQL SQL queries.
- `python task/test.py` — compare source and target row counts and samples.

Configure SOURCE_DATABASE_URL and TARGET_DATABASE_URL in the root .env file. Never commit real credentials.

Install with `pip install -e task`. See the root README for full setup and methodology.
