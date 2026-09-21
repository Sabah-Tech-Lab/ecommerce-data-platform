from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.products_validator import validate_products

CSV_PATH = Path("data/raw/olist/olist_products_dataset.csv")

def main() -> None:
    """Load the raw Olist products dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist products
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_products(df)

    # ------------------------------------------------------------------
    # Print olist products validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()