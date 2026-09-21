from pathlib import Path

import pandas as pd

from ecommerce_data.ingestion.csv_reader import read_csv
from ecommerce_data.profiling.data_profiler import profile_data

CSV_PATH = Path("data/raw/olist/olist_products_dataset.csv")


def main() -> None:
    """Profile the raw Olist products dataset and investigate key anomalies."""
    # ------------------------------------------------------------------
    # Load and profile raw data
    # ------------------------------------------------------------------
    df = read_csv(CSV_PATH)
    profile = profile_data(df)

    pd.set_option("display.max_columns", None)

    print("=== DATASET OVERVIEW ===")
    print("Shape:\n", profile["shape"])
    print("Pandas types:\n", profile["pandas_types"])
    print("Generic types:\n", profile["generic_types"])
    print("Missing values:\n", profile["quality"]["missing_values"])
    print("Duplicates:\n", profile["quality"]["duplicates"])
    print("Unique values count:\n", profile["unique_values_count"])
    print("\nHead:\n", df.head())

    integer_like_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
    ]

    numeric_columns = [
        "product_name_lenght",
        "product_description_lenght",
        "product_photos_qty",
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for column in numeric_columns:
            negative_values_count = (df[column] < 0).sum()
            zero_values_count = (df[column] == 0).sum()

            print(
                 f"invalid_values in {column}:\n",
                 "\nnegative values:",negative_values_count,
                 "\nzero values:",zero_values_count,"\n"
            )
    for column in integer_like_columns:
        fractional_values_count = (
            df[column]
            .dropna()
            .mod(1)
            .ne(0)
            .sum()
        )

        print(
            f"Fractional values in {column}:\n",
            fractional_values_count,
        )

    print(
        df.loc[
         df["product_weight_g"] == 0,
         [
            "product_id",
            "product_category_name",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ],
    ]
    )



if __name__ == "__main__":
    main()    