import pandas as pd
import pytest

from ecommerce_data.validation.sellers_validator import (
    validate_sellers,
)


# ------------------------------------------------------------------
# Fixtures for validate_sellers().
# ------------------------------------------------------------------


@pytest.fixture
def valid_sellers_dataframe():
    return pd.DataFrame(
        {
            "seller_id": [
                "seller_1",
                "seller_2",
                "seller_3",
            ],
            "seller_zip_code_prefix": [
                13023,
                13844,
                20031,
            ],
            "seller_city": [
                "campinas",
                "mogi guacu",
                "rio de janeiro",
            ],
            "seller_state": [
                "SP",
                "SP",
                "RJ",
            ],
        }
    )


@pytest.fixture
def sellers_dataframe_with_duplicate_seller_id():
    return pd.DataFrame(
        {
            "seller_id": [
                "seller_1",
                "seller_1",
            ],
            "seller_zip_code_prefix": [
                13023,
                13844,
            ],
            "seller_city": [
                "campinas",
                "mogi guacu",
            ],
            "seller_state": [
                "SP",
                "SP",
            ],
        }
    )


@pytest.fixture
def sellers_dataframe_with_null_value():
    return pd.DataFrame(
        {
            "seller_id": [
                "seller_1",
                "seller_2",
            ],
            "seller_zip_code_prefix": [
                13023,
                13844,
            ],
            "seller_city": [
                "campinas",
                None,
            ],
            "seller_state": [
                "SP",
                "SP",
            ],
        }
    )


@pytest.fixture
def sellers_dataframe_with_invalid_state():
    return pd.DataFrame(
        {
            "seller_id": [
                "seller_1",
                "seller_2",
            ],
            "seller_zip_code_prefix": [
                13023,
                13844,
            ],
            "seller_city": [
                "campinas",
                "mogi guacu",
            ],
            "seller_state": [
                "SP",
                "XX",
            ],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_sellers().
# ------------------------------------------------------------------


def test_validate_sellers_with_valid_data(
    valid_sellers_dataframe,
):
    result = validate_sellers(valid_sellers_dataframe)

    assert result["overall_status"] == "PASS"
    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["unique_columns"]["status"] == "PASS"
    assert result["states"]["status"] == "PASS"


def test_validate_sellers_with_duplicate_seller_id(
    sellers_dataframe_with_duplicate_seller_id,
):
    result = validate_sellers(
        sellers_dataframe_with_duplicate_seller_id
    )

    assert result["overall_status"] == "FAIL"
    assert result["unique_columns"]["status"] == "FAIL"

    assert (
        result["unique_columns"]["details"]["seller_id"][
            "is_valid"
        ]
        is False
    )

    assert (
        result["unique_columns"]["details"]["seller_id"][
            "duplicate_values_count"
        ]
        == 1
    )


def test_validate_sellers_with_null_value(
    sellers_dataframe_with_null_value,
):
    result = validate_sellers(
        sellers_dataframe_with_null_value
    )

    assert result["overall_status"] == "FAIL"
    assert result["non_null_columns"]["status"] == "FAIL"

    assert (
        result["non_null_columns"]["details"]["null_counts"][
            "seller_city"
        ]
        == 1
    )


def test_validate_sellers_with_invalid_state(
    sellers_dataframe_with_invalid_state,
):
    result = validate_sellers(
        sellers_dataframe_with_invalid_state
    )

    assert result["overall_status"] == "FAIL"
    assert result["states"]["status"] == "FAIL"

    assert (
        result["states"]["details"]["is_valid"]
        is False
    )

    assert (
        result["states"]["details"]["invalid_values"]
        == ["XX"]
    )