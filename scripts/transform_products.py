from pathlib import Path
from ecommerce_data.ingestion.csv_writer import write_csv
from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.transformation.products_transformer import transform_products


CSV_PATH = Path("data/raw/olist/olist_products_dataset.csv")


def main() -> None:
    """Load and transform the raw Olist products dataset."""

    # ------------------------------------------------------------------
    # Load and transform raw data
    # ------------------------------------------------------------------

    raw_df = read_csv(CSV_PATH)
    OUTPUT_PATH = Path("data/processed/products.csv")
    cleaned_df = transform_products(raw_df)

    write_csv(
        cleaned_df,
        OUTPUT_PATH,
    )
    
    raw_columns = set(raw_df.columns)
    cleaned_columns = set(cleaned_df.columns)

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
    for column in integer_columns:
        print(f"{column}: {cleaned_df[column].dtype}")

    print(
        "Number of zero product weights in raw DataFrame:",
        (raw_df["product_weight_g"] == 0).sum(),
    )    

    print(
        "Number of missing product weights in raw DataFrame:",
        raw_df["product_weight_g"].isna().sum(),
    ) 
    print(
        "Number of missing product weights in cleaned DataFrame:",
        cleaned_df["product_weight_g"].isna().sum(),
    )    

    print("Raw shape:", raw_df.shape)
    print("Cleaned shape:", cleaned_df.shape)

    print(f"Processed products saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()    