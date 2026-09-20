from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data


CSV_PATH = Path("data/raw/olist/olist_order_items_dataset.csv")


def main() -> None:
    """Profile the raw Olist order items dataset and investigate key anomalies."""
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

    duplicate_composite_keys = df.duplicated(
        subset=["order_id", "order_item_id"]
    ).sum()

    print(
    "Duplicate (order_id, order_item_id) pairs:\n",
    duplicate_composite_keys,
    )

    negative_prices_count = (df["price"] < 0).sum()
    zero_prices_count = (df["price"] == 0).sum()

    negative_freight_count = (df["freight_value"] < 0).sum()
    zero_freight_count = (df["freight_value"] == 0).sum()

    print("Negative prices:", negative_prices_count)
    print("Zero prices:", zero_prices_count)

    print("Negative freight values:", negative_freight_count)
    print("Zero freight values:", zero_freight_count)

    parsed_shipping_limit_date = pd.to_datetime(
    df["shipping_limit_date"],
    errors="coerce",
    format="mixed",
    ) 

    invalid_shipping_limit_dates_count = (
    parsed_shipping_limit_date.isna().sum()
    )

    print(
    "Invalid shipping_limit_date values:",
    invalid_shipping_limit_dates_count,
    )

if __name__ == "__main__":
    main()    