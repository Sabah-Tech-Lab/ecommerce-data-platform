from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data
from ecommerce_data.validation.data_validator import check_functional_dependency


CSV_PATH = Path("data/raw/olist/olist_geolocation_dataset.csv")


def main() -> None:
    """Profile the raw Olist geolocation dataset and investigate key anomalies."""
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
    "Latitude min/max:",
    df["geolocation_lat"].min(),
    df["geolocation_lat"].max(),
    )

    print(
        "Longitude min/max:",
        df["geolocation_lng"].min(),
        df["geolocation_lng"].max(),
    )

    print(
        "Latitude outside valid range:",
        (
            (df["geolocation_lat"] < -90)
            | (df["geolocation_lat"] > 90)
        ).sum(),
    )

    print(
        "Longitude outside valid range:",
        (
            (df["geolocation_lng"] < -180)
            | (df["geolocation_lng"] > 180)
        ).sum(),
    )

    print(
        df["geolocation_state"]
        .value_counts(dropna=False)
        .sort_index()
    )

    print(
        check_functional_dependency(
            df,
            "geolocation_zip_code_prefix",
            "geolocation_state",
        )
    )

    print(
        check_functional_dependency(
            df,
            "geolocation_zip_code_prefix",
            "geolocation_city",
        )
    )    

if __name__ == "__main__":
    main()    
