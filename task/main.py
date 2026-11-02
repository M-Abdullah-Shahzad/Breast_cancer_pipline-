from tabulate import tabulate

from config import get_source_engine


def main() -> None:
    engine = get_source_engine()
    try:
        with engine.connect() as connection:
            queries = [
                (
                    "Question 1: Aggregates for Age > 50 and Grade 3",
                    """
                    SELECT Status,
                           COUNT(*) AS total_patients,
                           ROUND(AVG(`Tumor Size`), 2) AS avg_tumor_size,
                           ROUND(AVG(`Survival Months`), 2) AS avg_survival_months
                    FROM breast_cancer
                    WHERE Age > 50 AND Grade LIKE '%3%'
                    GROUP BY Status
                    """,
                    ["Status", "Total Patients", "Avg Tumor Size", "Avg Survival Months"],
                ),
                (
                    "Question 2: Patient Categorization by Age Group",
                    """
                    SELECT CASE
                               WHEN Age < 40 THEN 'Young (<40)'
                               WHEN Age BETWEEN 40 AND 60 THEN 'Middle-Aged (40-60)'
                               ELSE 'Senior (>60)'
                           END AS age_group,
                           COUNT(*) AS total_patients,
                           ROUND(AVG(`Survival Months`), 2) AS avg_survival_months
                    FROM breast_cancer
                    GROUP BY age_group
                    """,
                    ["Age Group", "Total Patients", "Avg Survival Months"],
                ),
                (
                    "Question 3: Race vs Average Survival and Tumor Size",
                    """
                    SELECT Race,
                           ROUND(AVG(`Survival Months`), 2) AS avg_survival,
                           ROUND(AVG(`Tumor Size`), 2) AS avg_tumor_size
                    FROM breast_cancer
                    GROUP BY Race
                    ORDER BY avg_survival DESC
                    """,
                    ["Race", "Avg Survival Months", "Avg Tumor Size"],
                ),
            ]

            for title, query, headers in queries:
                print(f"\n{title}")
                result = connection.exec_driver_sql(query).fetchall()
                print(tabulate(result, headers=headers, tablefmt="grid"))
    finally:
        engine.dispose()


if __name__ == "__main__":
    main()
