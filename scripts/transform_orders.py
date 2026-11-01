from pathlib import Path

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.ingestion.csv_writer import write_csv
from ecommerce_data.transformation.orders_transformer import transform_orders

CSV_PATH = Path("data/raw/olist/olist_orders_dataset.csv")
OUTPUT_PATH = Path("data/processed/orders.csv")


def main() -> None:
    """Load and transform the raw Olist orders dataset."""

    # ------------------------------------------------------------------
    # Load and transform raw data
    # ------------------------------------------------------------------

    raw_df = read_csv(CSV_PATH)
    transformed_df = transform_orders(raw_df)

    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]
    print("\n=== DATETIME COLUMNS ===")

    for column in datetime_columns:
        print(
            f"{column}\n"
            f"  dtype: {transformed_df[column].dtype}\n"
            f"  missing: raw={raw_df[column].isna().sum()}, "
            f"transformed={transformed_df[column].isna().sum()}"
        )   

    print("\n=== DATASET SHAPE ===")
    print(f"Raw:         {raw_df.shape}")
    print(f"Transformed: {transformed_df.shape}")

    write_csv(
        transformed_df,
        OUTPUT_PATH,
    )
    print("\n=== OUTPUT ===")
    print(f"Saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()        



