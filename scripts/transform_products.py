from pathlib import Path

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.ingestion.csv_writer import write_csv
from ecommerce_data.transformation.products_transformer import transform_products


CSV_PATH = Path("data/raw/olist/olist_products_dataset.csv")
OUTPUT_PATH = Path("data/processed/products.csv")


def main() -> None:
    """Load and transform the raw Olist products dataset."""

    # ------------------------------------------------------------------
    # Load and transform raw data
    # ------------------------------------------------------------------

    raw_df = read_csv(CSV_PATH)
    cleaned_df = transform_products(raw_df)
    
    raw_columns = set(raw_df.columns)
    cleaned_columns = set(cleaned_df.columns)

    print("\n=== MODIFICATIONS ===")
    print(
        "Removed columns:",
        sorted(raw_columns - cleaned_columns),
    )

    print(
        "Added columns:",
        sorted(cleaned_columns - raw_columns),
    )

    integer_columns = [
        "product_name_length",
        "product_description_length",
        "product_photos_qty",
    ]

    print("\n=== INTEGER COLUMNS ===")
    for column in integer_columns:
        print(f"{column}: {cleaned_df[column].dtype}")

    print("\n=== PRODUCT WEIGHT ===")
    print(
        "Zero product weights in raw:",
        (raw_df["product_weight_g"] == 0).sum(),
    )    

    print(
        "Missing product weights in raw:",
        raw_df["product_weight_g"].isna().sum(),
    ) 

    print(
        "Missing product weights in cleaned:",
        cleaned_df["product_weight_g"].isna().sum(),
    )    

    print("\n=== DATASET SHAPE ===")       
    print(f"Raw:    {raw_df.shape}")
    print(f"Cleaned:{cleaned_df.shape}")

    write_csv(
        cleaned_df,
        OUTPUT_PATH,
    )
    print("\n=== OUTPUT ===")
    print(f"saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()    