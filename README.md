# Breast Cancer Dataset ETL — MySQL to PostgreSQL

A Python ETL project that reads a breast-cancer dataset from MySQL in chunks, normalizes and enriches each chunk, and loads the transformed records into PostgreSQL. It also includes SQL analysis queries for the source table.

This repository implements data movement and descriptive SQL analysis only. It does not train a diagnostic model and must not be used for clinical decisions.

## ETL flow

```text
MySQL: breast_cancer
        |
        v
pagination.py — SELECT * in bounded chunks
        |
        v
transform.py — normalize columns and derive age_group / is_high_risk
        |
        v
load.py — transactional PostgreSQL chunk load
        |
        v
PostgreSQL: transformed_breast_cancer
```

## Requirements

- Python 3.12
- MySQL database with the source table
- PostgreSQL database with permission to create and write the target table

## Setup

From the repository root:

```bash
python -m venv .venv
# Windows PowerShell
.\.venv\Scripts\Activate.ps1
# macOS / Linux
source .venv/bin/activate

pip install -e task
```

Copy `.env.example` to `.env` and configure:

- `SOURCE_DATABASE_URL` — SQLAlchemy MySQL URL, for example using the PyMySQL driver
- `TARGET_DATABASE_URL` — SQLAlchemy PostgreSQL URL

Never commit a populated .env file or real database credentials.

## Run the ETL

```bash
python task/etl_pipeline.py
```

The pipeline reads all rows from the source table in chunks of 100, transforms each chunk, and loads the first chunk with table replacement followed by append operations. The source and target engines are disposed when the run completes.

## Run the SQL analysis

```bash
python task/main.py
```

This executes the three descriptive SQL queries against the MySQL source table.

## Verify source and target

```bash
python task/test.py
```

This prints row counts and small samples from the source and transformed target tables.

## Transformation rules

- Column names are trimmed, lowercased, and spaces are replaced with underscores.
- Numeric age, tumor size, and survival-month fields are converted safely.
- Text fields are trimmed and normalized to uppercase.
- Age groups are derived as YOUNG, MIDDLE, and SENIOR.
- The example high-risk flag is set when tumor size exceeds 20 or age exceeds 60. This is a simple project rule, not a clinical risk model.
- Duplicate rows are removed within each chunk.

## Tests

```bash
cd task
python -m pip install pytest
python -m pytest -q
```

Tests use in-memory SQLite and do not connect to real MySQL or PostgreSQL services.

## Security

Database URLs are read from environment variables. The old hardcoded MySQL and PostgreSQL credentials in previous source versions must be rotated; removing them from the current files does not remove them from Git history.
