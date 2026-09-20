from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.customers_validator import validate_customers

CSV_PATH = Path("data/raw/olist/olist_customers_dataset.csv")

def main() -> None:
    """Load the raw Olist customers dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist customers
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_customers(df)

    # ------------------------------------------------------------------
    # Print olist customers validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )     
        

if __name__ == "__main__":
    main()
