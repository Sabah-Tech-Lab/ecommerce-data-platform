from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.order_payments_validator import validate_order_payments

CSV_PATH = Path("data/raw/olist/olist_order_payments_dataset.csv")

def main() -> None:
    """Load the raw Olist order payments dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist order payments
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_order_payments(df)

    # ------------------------------------------------------------------
    # Print olist order payments validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()