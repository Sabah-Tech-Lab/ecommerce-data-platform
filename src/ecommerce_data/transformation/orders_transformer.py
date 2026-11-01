import pandas as pd


def transform_orders(df: pd.DataFrame) -> pd.DataFrame:
    """Transform raw Olist orders data into a cleaned representation."""
    cleaned_df = df.copy()

    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    cleaned_df[datetime_columns] = cleaned_df[datetime_columns].apply(
        pd.to_datetime
    )

    return cleaned_df


    