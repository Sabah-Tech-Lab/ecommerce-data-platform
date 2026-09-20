from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data


CSV_PATH = Path("data/raw/olist/olist_orders_dataset.csv")


def main() -> None:
    """Profile the raw Olist orders dataset and investigate key anomalies."""
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

    # ------------------------------------------------------------------
    # Inspect order status
    # ------------------------------------------------------------------
    print("\n=== ORDER STATUS ===")
    print(df["order_status"].value_counts())

    # ------------------------------------------------------------------
    # Inspect order -> customer relationship
    # ------------------------------------------------------------------
    print("\n=== ORDER / CUSTOMER RELATIONSHIP ===")

    customer_counts = df.groupby("order_id")["customer_id"].nunique()
    orders_with_multiple_customers = customer_counts[customer_counts > 1]

    print(
        "Orders linked to more than one customer:",
        orders_with_multiple_customers.shape[0],
    )

    # ------------------------------------------------------------------
    # Parse datetime columns for temporal investigation
    # ------------------------------------------------------------------
    purchase_timestamp = pd.to_datetime(
        df["order_purchase_timestamp"],
        format="mixed",
    )

    carrier_date = pd.to_datetime(
        df["order_delivered_carrier_date"],
        format="mixed",
    )

    customer_delivery_date = pd.to_datetime(
        df["order_delivered_customer_date"],
        format="mixed",
    )

    # ------------------------------------------------------------------
    # Temporal anomaly 1:
    # carrier date occurs before purchase timestamp
    # ------------------------------------------------------------------
    carrier_before_purchase = purchase_timestamp > carrier_date

    time_difference_carrier_before_purchase = (
        purchase_timestamp[carrier_before_purchase]
        - carrier_date[carrier_before_purchase]
    ).dt.total_seconds() / 3600

    print("\n=== CARRIER BEFORE PURCHASE ===")
    print("Violation count:", carrier_before_purchase.sum())
    print(time_difference_carrier_before_purchase)

    print(
        "Mean:",
        time_difference_carrier_before_purchase.mean(),
    )
    print(
        "Median:",
        time_difference_carrier_before_purchase.median(),
    )
    print(
        "Std:",
        time_difference_carrier_before_purchase.std(),
    )

    # ------------------------------------------------------------------
    # Temporal anomaly 2:
    # carrier date occurs after customer delivery date
    # ------------------------------------------------------------------
    carrier_after_customer_delivery = carrier_date > customer_delivery_date

    time_difference_carrier_after_delivery = (
        carrier_date[carrier_after_customer_delivery]
        - customer_delivery_date[carrier_after_customer_delivery]
    ).dt.total_seconds() / 3600

    print("\n=== CARRIER AFTER CUSTOMER DELIVERY ===")
    print("Violation count:", carrier_after_customer_delivery.sum())
    print(time_difference_carrier_after_delivery)

    print(
        "Mean:",
        time_difference_carrier_after_delivery.mean(),
    )
    print(
        "Median:",
        time_difference_carrier_after_delivery.median(),
    )
    print(
        "Std:",
        time_difference_carrier_after_delivery.std(),
    )

    # ------------------------------------------------------------------
    # Check whether both temporal anomalies affect the same orders
    # ------------------------------------------------------------------
    intersection = (
        carrier_before_purchase
        & carrier_after_customer_delivery
    )

    print("\n=== TEMPORAL ANOMALY INTERSECTION ===")
    print("Orders matching both anomalies:", intersection.sum())


if __name__ == "__main__":
    main()