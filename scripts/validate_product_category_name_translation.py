from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.product_category_name_translation_validator import (
    validate_product_category_name_translation
)

CSV_PATH = Path("data/raw/olist/product_category_name_translation.csv")

def main() -> None:
    """Load the raw Olist product category name translation, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist product category name translation
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_product_category_name_translation(df)

    # ------------------------------------------------------------------
    # Print olist product category name translation validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()