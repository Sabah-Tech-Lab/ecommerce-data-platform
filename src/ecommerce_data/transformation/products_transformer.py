import pandas as pd

def transform_products(df: pd.DataFrame) -> pd.DataFrame:
    """Transform the raw Olist products dataset into a cleaned representation.

    The transformation renames misspelled columns, converts integer-like
    columns to nullable integer types, and replaces invalid non-positive
    product weights with missing values.

    Args:
        df: Raw Olist products DataFrame to transform.

    Returns:
        A cleaned copy of the products DataFrame with standardized column
        names, corrected data types, and invalid product weights handled.
    """
    cleaned_df = df.copy()

    column_rename_map = {
        "product_name_lenght": "product_name_length",
        "product_description_lenght": "product_description_length",
    }

    integer_column_types = {
        "product_name_length": "Int64",
        "product_description_length": "Int64",
        "product_photos_qty": "Int64",
    }

    cleaned_df = cleaned_df.rename(columns=column_rename_map)
    cleaned_df = cleaned_df.astype(integer_column_types)

    cleaned_df.loc[
        cleaned_df["product_weight_g"] <= 0,
        "product_weight_g",
    ] = pd.NA

    return cleaned_df