from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.order_reviews_validator import validate_order_reviews

CSV_PATH = Path("data/raw/olist/olist_order_reviews_dataset.csv")

def main() -> None:
    """Load the raw Olist order reviews dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist order reviews
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_order_reviews(df)

    # ------------------------------------------------------------------
    # Print olist order reviews validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()