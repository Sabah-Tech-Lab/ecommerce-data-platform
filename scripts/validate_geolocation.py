from pathlib import Path
import json

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.validation.geolocation_validator import validate_geolocation

CSV_PATH = Path("data/raw/olist/olist_geolocation_dataset.csv")

def main() -> None:
    """Load the raw Olist geolocation dataset, validate it, and print the report."""

    # ------------------------------------------------------------------
    # Load and validate raw olist geolocation
    # ------------------------------------------------------------------

    df = read_csv(CSV_PATH)
    validation_report = validate_geolocation(df)

    # ------------------------------------------------------------------
    # Print olist geolocation validation report
    # ------------------------------------------------------------------ 
    
    print(
        json.dumps(
            validation_report, 
            indent=4,
            )
    )     
        

if __name__ == "__main__":
    main()