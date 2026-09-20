from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.order_items_validator import validate_order_items

CSV_PATH = Path("data/raw/olist/olist_order_items_dataset.csv")

def main() -> None:
    """Load the raw Olist order items dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist order items
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_order_items(df)

    # ------------------------------------------------------------------
    # Print olist order items validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()