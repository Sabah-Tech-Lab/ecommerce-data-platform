from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data
from ecommerce_data.validation.data_validator import check_functional_dependency


CSV_PATH = Path("data/raw/olist/product_category_name_translation.csv")

def main() -> None:
    """Profile the raw product category name translation and investigate key anomalies."""
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
        check_functional_dependency(
            df,
            "product_category_name",
            "product_category_name_english",
        ) 
    )

    print(
        check_functional_dependency(
            df,
            "product_category_name_english",
            "product_category_name",
        )
    )

if __name__ == "__main__":
    main()    