import pandas as pd
import pytest

from ecommerce_data.validation.product_category_name_translation_validator import (
    validate_product_category_name_translation,
)


# ------------------------------------------------------------------
# Fixtures for validate_product_category_name_translation().
# ------------------------------------------------------------------

@pytest.fixture
def valid_product_category_name_translation_dataframe():
    return pd.DataFrame(
        {
            "product_category_name": [
                "beleza_saude",
                "informatica_acessorios",
                "automotivo",
            ],
            "product_category_name_english": [
                "health_beauty",
                "computers_accessories",
                "auto",
            ],
        }
    )


@pytest.fixture
def product_category_name_translation_dataframe_with_duplicate_category():
    return pd.DataFrame(
        {
            "product_category_name": [
                "beleza_saude",
                "beleza_saude",
            ],
            "product_category_name_english": [
                "health_beauty",
                "health_beauty_duplicate",
            ],
        }
    )


@pytest.fixture
def product_category_name_translation_dataframe_with_null_value():
    return pd.DataFrame(
        {
            "product_category_name": [
                "beleza_saude",
                "automotivo",
            ],
            "product_category_name_english": [
                "health_beauty",
                None,
            ],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_product_category_name_translation().
# ------------------------------------------------------------------


def test_validate_product_category_name_translation_with_valid_data(
    valid_product_category_name_translation_dataframe,
):
    result = validate_product_category_name_translation(
        valid_product_category_name_translation_dataframe
    )

    assert result["overall_status"] == "PASS"
    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["unique_columns"]["status"] == "PASS"


def test_validate_product_category_name_translation_with_duplicate_category(
    product_category_name_translation_dataframe_with_duplicate_category,
):
    result = validate_product_category_name_translation(
        product_category_name_translation_dataframe_with_duplicate_category
    )

    assert result["overall_status"] == "FAIL"
    assert result["unique_columns"]["status"] == "FAIL"

    assert (
        result["unique_columns"]["details"]["product_category_name"][
            "is_valid"
        ]
        is False
    )

    assert (
        result["unique_columns"]["details"]["product_category_name"][
            "duplicate_values_count"
        ]
        == 1
    )


def test_validate_product_category_name_translation_with_null_value(
    product_category_name_translation_dataframe_with_null_value,
):
    result = validate_product_category_name_translation(
        product_category_name_translation_dataframe_with_null_value
    )

    assert result["overall_status"] == "FAIL"
    assert result["non_null_columns"]["status"] == "FAIL"

    assert (
        result["non_null_columns"]["details"]["null_counts"][
            "product_category_name_english"
        ]
        == 1
    )