from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data


CSV_PATH = Path("data/raw/olist/olist_order_payments_dataset.csv")


def main() -> None:
    """Profile the raw Olist order payments dataset and investigate key anomalies."""
    # ------------------------------------------------------------------
    # Load and profile raw data
    # ------------------------------------------------------------------
    df = read_csv(CSV_PATH)
    profile = profile_data(df)

    pd.set_option("display.max_columns", None)

    print("=== DATASET OVERVIEW ===")
    print("Shape:\n", profile["shape"])
    print("Pandas types:\n", profile["pandas_types"])
    print("Generic types:\n", profile["generic_types"])
    print("Missing values:\n", profile["quality"]["missing_values"])
    print("Duplicates:\n", profile["quality"]["duplicates"])
    print("Unique values count:\n", profile["unique_values_count"])
    print("\nHead:\n", df.head())

    print(
    "Duplicate composite keys:",
        df.duplicated(
            subset=["order_id", "payment_sequential"]
        ).sum()
    )

    print(
        df["payment_type"]
        .value_counts(dropna=False)
    )

    print(
        "Minimum installments:",
        df["payment_installments"].min()
    )

    print(
        "Maximum installments:",
        df["payment_installments"].max()
    )

    print(
        "Zero installments:",
        (df["payment_installments"] == 0).sum()
    )

    print(
        "Minimum payment value:",
        df["payment_value"].min()
    )

    print(
        "Maximum payment value:",
        df["payment_value"].max()
    )

    print(
        "Zero payment value:",
        (df["payment_value"] == 0).sum()
    )

    print(
        df.loc[
            df["payment_installments"] == 0,
            [
                "order_id",
                "payment_sequential",
                "payment_type",
                "payment_installments",
                "payment_value",
            ],
        ]
    )

if __name__ == "__main__":
    main()    