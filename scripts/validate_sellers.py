from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.sellers_validator import validate_sellers

CSV_PATH = Path("data/raw/olist/olist_sellers_dataset.csv")

def main() -> None:
    """Load the raw Olist sellers dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist sellers
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_sellers(df)

    # ------------------------------------------------------------------
    # Print olist sellers validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )      

if __name__ == "__main__":
    main()