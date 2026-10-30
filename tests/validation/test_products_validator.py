import pandas as pd
import pytest

from ecommerce_data.validation.products_validator import validate_products


# ------------------------------------------------------------------
# Fixtures for validate_products().
# ------------------------------------------------------------------


@pytest.fixture
def valid_products_dataframe():
    return pd.DataFrame(
        {
            "product_id": [
                "product_1",
                "product_2",
                "product_3",
            ],
            "product_category_name": [
                "category_a",
                "category_b",
                None,
            ],
            "product_name_lenght": [
                40.0,
                35.0,
                None,
            ],
            "product_description_lenght": [
                200.0,
                150.0,
                None,
            ],
            "product_photos_qty": [
                2.0,
                1.0,
                None,
            ],
            "product_weight_g": [
                500.0,
                750.0,
                1000.0,
            ],
            "product_length_cm": [
                20.0,
                25.0,
                30.0,
            ],
            "product_height_cm": [
                10.0,
                15.0,
                20.0,
            ],
            "product_width_cm": [
                15.0,
                20.0,
                25.0,
            ],
        }
    )


@pytest.fixture
def products_dataframe_with_duplicate_product_id():
    return pd.DataFrame(
        {
            "product_id": [
                "product_1",
                "product_1",
            ],
            "product_category_name": [
                "category_a",
                "category_b",
            ],
            "product_name_lenght": [
                40.0,
                35.0,
            ],
            "product_description_lenght": [
                200.0,
                150.0,
            ],
            "product_photos_qty": [
                2.0,
                1.0,
            ],
            "product_weight_g": [
                500.0,
                750.0,
            ],
            "product_length_cm": [
                20.0,
                25.0,
            ],
            "product_height_cm": [
                10.0,
                15.0,
            ],
            "product_width_cm": [
                15.0,
                20.0,
            ],
        }
    )


@pytest.fixture
def products_dataframe_with_fractional_integer_like_value():
    return pd.DataFrame(
        {
            "product_id": [
                "product_1",
                "product_2",
            ],
            "product_category_name": [
                "category_a",
                "category_b",
            ],
            "product_name_lenght": [
                40.0,
                35.5,
            ],
            "product_description_lenght": [
                200.0,
                150.0,
            ],
            "product_photos_qty": [
                2.0,
                1.0,
            ],
            "product_weight_g": [
                500.0,
                750.0,
            ],
            "product_length_cm": [
                20.0,
                25.0,
            ],
            "product_height_cm": [
                10.0,
                15.0,
            ],
            "product_width_cm": [
                15.0,
                20.0,
            ],
        }
    )


@pytest.fixture
def products_dataframe_with_zero_weight():
    return pd.DataFrame(
        {
            "product_id": [
                "product_1",
                "product_2",
            ],
            "product_category_name": [
                "category_a",
                "category_b",
            ],
            "product_name_lenght": [
                40.0,
                35.0,
            ],
            "product_description_lenght": [
                200.0,
                150.0,
            ],
            "product_photos_qty": [
                2.0,
                1.0,
            ],
            "product_weight_g": [
                500.0,
                0.0,
            ],
            "product_length_cm": [
                20.0,
                25.0,
            ],
            "product_height_cm": [
                10.0,
                15.0,
            ],
            "product_width_cm": [
                15.0,
                20.0,
            ],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_products().
# ------------------------------------------------------------------


def test_validate_products_with_valid_data(valid_products_dataframe):
    result = validate_products(valid_products_dataframe)

    assert result["overall_status"] == "PASS"

    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["unique_columns"]["status"] == "PASS"
    assert result["integer_like_columns"]["status"] == "PASS"
    assert result["minimum_value_validation"]["status"] == "PASS"


def test_validate_products_with_duplicate_product_id(
    products_dataframe_with_duplicate_product_id,
):
    result = validate_products(
        products_dataframe_with_duplicate_product_id
    )

    assert result["overall_status"] == "FAIL"

    assert result["unique_columns"]["status"] == "FAIL"

    assert (
        result["unique_columns"]["details"]["product_id"]["is_valid"]
        is False
    )

    assert (
        result["unique_columns"]["details"]["product_id"][
            "duplicate_values_count"
        ]
        == 1
    )


def test_validate_products_with_fractional_integer_like_value(
    products_dataframe_with_fractional_integer_like_value,
):
    result = validate_products(
        products_dataframe_with_fractional_integer_like_value
    )

    assert result["overall_status"] == "FAIL"

    assert result["integer_like_columns"]["status"] == "FAIL"

    assert (
        result["integer_like_columns"]["details"][
            "product_name_lenght"
        ]["is_valid"]
        is False
    )

    assert (
        result["integer_like_columns"]["details"][
            "product_name_lenght"
        ]["violation_count"]
        == 1
    )


def test_validate_products_with_zero_weight(
    products_dataframe_with_zero_weight,
):
    result = validate_products(
        products_dataframe_with_zero_weight
    )

    assert result["overall_status"] == "WARNING"

    assert (
        result["minimum_value_validation"]["status"]
        == "WARNING"
    )

    assert (
        result["minimum_value_validation"]["details"][
            "product_weight_g"
        ]["is_valid"]
        is False
    )

    assert (
        result["minimum_value_validation"]["details"][
            "product_weight_g"
        ]["violation_count"]
        == 1
    )