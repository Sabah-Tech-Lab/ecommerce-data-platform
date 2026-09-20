from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data


CSV_PATH = Path("data/raw/olist/olist_customers_dataset.csv")

def main() -> None:
    """Profile the raw Olist customers dataset and investigate key anomalies."""
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

    customer_id_counts = (
        df.groupby("customer_unique_id")["customer_id"]
        .nunique()
    )

    customers_with_multiple_ids = customer_id_counts[
        customer_id_counts > 1
    ]

    state_counts = (
    df.groupby("customer_zip_code_prefix")["customer_state"]
    .nunique()
    )

    zip_codes_with_multiple_states = state_counts[
        state_counts > 1
    ]

    city_counts = (
        df.groupby("customer_zip_code_prefix")["customer_city"]
        .nunique()
    )

    zip_codes_with_multiple_cities = city_counts[
        city_counts > 1
    ]

    print(
        "Number of unique customers with multiple customer_ids:\n",
        customers_with_multiple_ids.shape[0],
    )

    print(
        "Maximum number of customer_ids for one customer:\n",
        customers_with_multiple_ids.max(),
    )

    print("\n=== CUSTOMER STATES ===")
    print("Unique states:", df["customer_state"].nunique())
    print("States:", sorted(df["customer_state"].unique()))
    print(df["customer_state"].value_counts())

    print(
        "Zip code prefixes linked to multiple states:",
        zip_codes_with_multiple_states.shape[0],
    )

    print(
        "Zip code prefixes linked to multiple cities:",
        zip_codes_with_multiple_cities.shape[0],
    )

    print(
        "Maximum cities linked to one zip code prefix:",
        city_counts.max(),
    )


if __name__ == "__main__":
    main()    

