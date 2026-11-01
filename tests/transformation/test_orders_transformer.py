import pandas as pd
import pytest

from ecommerce_data.transformation.orders_transformer import transform_orders

# ------------------------------------------------------------------
# Fixtures for transform_orders()
# ------------------------------------------------------------------

@pytest.fixture
def sample_orders_dataframe() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "order_purchase_timestamp": [
                "2026-11-01 10:30:00",
                "2026-06-15 12:00:00",
            ],
            "order_approved_at": [
                "2026-11-01 11:00:00",
                None,
            ],
            "order_delivered_carrier_date": [
                "2026-11-02 08:00:00",
                "2026-06-16 09:00:00",
            ],
            "order_delivered_customer_date": [
                "2026-11-04 15:00:00",
                "2026-06-18 17:00:00",
            ],
            "order_estimated_delivery_date": [
                "2026-11-06 00:00:00",
                "2026-06-20 00:00:00",
            ],
        }
    )

# ------------------------------------------------------------------
# Tests for transform_orders().
# ------------------------------------------------------------------  


def test_transform_orders_converts_datetime_columns(
    sample_orders_dataframe,
) -> None:
    """Verify that order timestamp columns are converted to datetime types."""

    result = transform_orders(sample_orders_dataframe)

    datetime_columns = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for column in datetime_columns:
        assert pd.api.types.is_datetime64_any_dtype(result[column])


def test_transform_orders_does_not_modify_input_dataframe(
    sample_orders_dataframe,
) -> None:
    """Verify that transform_orders does not modify the input DataFrame."""
    original_dataframe = sample_orders_dataframe.copy(deep=True)

    transform_orders(sample_orders_dataframe)

    pd.testing.assert_frame_equal(
        sample_orders_dataframe,
        original_dataframe,
    )


def test_transform_orders_preserves_missing_datetime_values(
    sample_orders_dataframe,
) -> None:
    """Verify that missing datetime values remain missing after transformation."""
    result = transform_orders(sample_orders_dataframe)

    assert result["order_approved_at"].isna().sum() == 1
        
            

