from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.orders_validator import validate_orders

CSV_PATH = Path("data/raw/olist/olist_orders_dataset.csv")

def main() -> None:
    """Load the raw Olist orders dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist orders
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_orders(df)

    # ------------------------------------------------------------------
    # Print olist orders validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()




