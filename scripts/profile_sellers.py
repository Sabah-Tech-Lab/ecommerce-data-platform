from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data
from ecommerce_data.validation.data_validator import check_functional_dependency


CSV_PATH = Path("data/raw/olist/olist_sellers_dataset.csv")


def main() -> None:
    """Profile the raw Olist sellers dataset and investigate key anomalies."""
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

    print(df["seller_state"].value_counts().sort_index())

    print(
        check_functional_dependency(
            df,
            "seller_zip_code_prefix",
            "seller_state",
        )
    )

    print(
        check_functional_dependency(
            df,
            "seller_zip_code_prefix",
            "seller_city",
        )
    )

if __name__ == "__main__":
    main()    
