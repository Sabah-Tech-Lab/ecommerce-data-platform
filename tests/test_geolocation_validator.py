import pandas as pd
import pytest

from ecommerce_data.validation.geolocation_validator import (
    validate_geolocation,
)


# ------------------------------------------------------------------
# Fixtures for validate_geolocation().
# ------------------------------------------------------------------


@pytest.fixture
def valid_geolocation_dataframe():
    return pd.DataFrame(
        {
            "geolocation_zip_code_prefix": [
                1000,
                2000,
            ],
            "geolocation_lat": [
                -23.5,
                -22.9,
            ],
            "geolocation_lng": [
                -46.6,
                -43.2,
            ],
            "geolocation_city": [
                "sao paulo",
                "rio de janeiro",
            ],
            "geolocation_state": [
                "SP",
                "RJ",
            ],
        }
    )


@pytest.fixture
def geolocation_dataframe_with_invalid_state():
    return pd.DataFrame(
        {
            "geolocation_zip_code_prefix": [
                1000,
                2000,
            ],
            "geolocation_lat": [
                -23.5,
                -22.9,
            ],
            "geolocation_lng": [
                -46.6,
                -43.2,
            ],
            "geolocation_city": [
                "sao paulo",
                "rio de janeiro",
            ],
            "geolocation_state": [
                "SP",
                "XX",
            ],
        }
    )


@pytest.fixture
def geolocation_dataframe_with_invalid_latitude():
    return pd.DataFrame(
        {
            "geolocation_zip_code_prefix": [
                1000,
                2000,
            ],
            "geolocation_lat": [
                -23.5,
                95.0,
            ],
            "geolocation_lng": [
                -46.6,
                -43.2,
            ],
            "geolocation_city": [
                "sao paulo",
                "rio de janeiro",
            ],
            "geolocation_state": [
                "SP",
                "RJ",
            ],
        }
    )


@pytest.fixture
def geolocation_dataframe_with_invalid_longitude():
    return pd.DataFrame(
        {
            "geolocation_zip_code_prefix": [
                1000,
                2000,
            ],
            "geolocation_lat": [
                -23.5,
                -22.9,
            ],
            "geolocation_lng": [
                -46.6,
                190.0,
            ],
            "geolocation_city": [
                "sao paulo",
                "rio de janeiro",
            ],
            "geolocation_state": [
                "SP",
                "RJ",
            ],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_geolocation().
# ------------------------------------------------------------------


def test_validate_geolocation_with_valid_data(
    valid_geolocation_dataframe,
):
    result = validate_geolocation(
        valid_geolocation_dataframe
    )

    assert result["overall_status"] == "PASS"
    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["states"]["status"] == "PASS"
    assert result["value_range"]["status"] == "PASS"


def test_validate_geolocation_with_invalid_state(
    geolocation_dataframe_with_invalid_state,
):
    result = validate_geolocation(
        geolocation_dataframe_with_invalid_state
    )

    assert result["overall_status"] == "FAIL"
    assert result["states"]["status"] == "FAIL"

    assert result["states"]["details"]["is_valid"] is False
    assert result["states"]["details"]["invalid_values"] == [
        "XX"
    ]


def test_validate_geolocation_with_invalid_latitude(
    geolocation_dataframe_with_invalid_latitude,
):
    result = validate_geolocation(
        geolocation_dataframe_with_invalid_latitude
    )

    assert result["overall_status"] == "FAIL"
    assert result["value_range"]["status"] == "FAIL"

    assert (
        result["value_range"]["details"][
            "geolocation_lat"
        ]["is_valid"]
        is False
    )

    assert (
        result["value_range"]["details"][
            "geolocation_lat"
        ]["violation_count"]
        == 1
    )


def test_validate_geolocation_with_invalid_longitude(
    geolocation_dataframe_with_invalid_longitude,
):
    result = validate_geolocation(
        geolocation_dataframe_with_invalid_longitude
    )

    assert result["overall_status"] == "FAIL"
    assert result["value_range"]["status"] == "FAIL"

    assert (
        result["value_range"]["details"][
            "geolocation_lng"
        ]["is_valid"]
        is False
    )

    assert (
        result["value_range"]["details"][
            "geolocation_lng"
        ]["violation_count"]
        == 1
    )