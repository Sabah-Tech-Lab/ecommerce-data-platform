import pandas as pd
import pytest

from ecommerce_data.transformation.products_transformer import transform_products

# ------------------------------------------------------------------
# Fixtures for transform_products()
# ------------------------------------------------------------------

@pytest.fixture
def raw_products_dataframe():
    return pd.DataFrame(
        {
            "product_name_lenght": pd.Series(
                [12.0, 13.0],
                dtype="float64",
            ),
            "product_description_lenght": pd.Series(
                [14.0, None],
                dtype="float64",
            ),
            "product_photos_qty": pd.Series(
                [15.0, 16.0],
                dtype="float64",
            ),
            "product_weight_g": [
                200.0,
                0.0,
            ]


        }
    )

# ------------------------------------------------------------------
# Tests for transform_products().
# ------------------------------------------------------------------


def test_transform_products_renames_columns(
    raw_products_dataframe,
):
    result = transform_products(raw_products_dataframe)

    assert "product_name_length" in result.columns
    assert "product_description_length" in result.columns

    assert "product_name_lenght" not in result.columns
    assert "product_description_lenght" not in result.columns

def test_transform_products_converts_integer_like_columns(
    raw_products_dataframe,
):
    result = transform_products(raw_products_dataframe)

    assert str(result["product_name_length"].dtype) == "Int64"
    assert str(result["product_description_length"].dtype) == "Int64"
    assert str(result["product_photos_qty"].dtype) == "Int64"  

def test_transform_products_converts_invalid_weight(
    raw_products_dataframe,
):
    result = transform_products(raw_products_dataframe)

    assert result.loc[0, "product_weight_g"] == 200.0
    assert pd.isna(result.loc[1, "product_weight_g"])

def test_transform_products_does_not_modify_input_dataframe(
    raw_products_dataframe,
):
    original_dataframe = raw_products_dataframe.copy(deep=True)

    transform_products(raw_products_dataframe)

    pd.testing.assert_frame_equal(
        raw_products_dataframe,
        original_dataframe,
    )


        