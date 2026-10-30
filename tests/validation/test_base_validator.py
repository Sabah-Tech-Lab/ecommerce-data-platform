import pandas as pd
import pytest

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)


# ------------------------------------------------------------------
# Fixtures for validate_base_dataset_rules().
# ------------------------------------------------------------------


@pytest.fixture
def valid_base_dataframe():
    return pd.DataFrame(
        {
            "id": ["id_1", "id_2", "id_3"],
            "name": ["Alice", "Bob", "Charlie"],
        }
    )


@pytest.fixture
def dataframe_with_missing_required_column():
    return pd.DataFrame(
        {
            "id": ["id_1", "id_2"],
        }
    )


@pytest.fixture
def dataframe_with_null_value():
    return pd.DataFrame(
        {
            "id": ["id_1", "id_2"],
            "name": ["Alice", None],
        }
    )


@pytest.fixture
def dataframe_with_duplicate_id():
    return pd.DataFrame(
        {
            "id": ["id_1", "id_1"],
            "name": ["Alice", "Bob"],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_base_dataset_rules().
# ------------------------------------------------------------------


def test_validate_base_dataset_rules_with_valid_data(
    valid_base_dataframe,
):
    result = validate_base_dataset_rules(
        df=valid_base_dataframe,
        required_columns={"id", "name"},
        non_null_columns=["id", "name"],
        unique_columns=["id"],
    )

    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["unique_columns"]["status"] == "PASS"


def test_validate_base_dataset_rules_with_missing_required_column(
    dataframe_with_missing_required_column,
):
    result = validate_base_dataset_rules(
        df=dataframe_with_missing_required_column,
        required_columns={"id", "name"},
        non_null_columns=["id"],
        unique_columns=["id"],
    )

    assert result["required_columns"]["status"] == "FAIL"
    assert result["required_columns"]["details"]["is_valid"] is False
    assert result["required_columns"]["details"]["missing_columns"] == [
        "name"
    ]


def test_validate_base_dataset_rules_with_null_value(
    dataframe_with_null_value,
):
    result = validate_base_dataset_rules(
        df=dataframe_with_null_value,
        required_columns={"id", "name"},
        non_null_columns=["id", "name"],
        unique_columns=["id"],
    )

    assert result["non_null_columns"]["status"] == "FAIL"

    assert (
        result["non_null_columns"]["details"]["null_counts"]["name"]
        == 1
    )


def test_validate_base_dataset_rules_with_duplicate_unique_value(
    dataframe_with_duplicate_id,
):
    result = validate_base_dataset_rules(
        df=dataframe_with_duplicate_id,
        required_columns={"id", "name"},
        non_null_columns=["id", "name"],
        unique_columns=["id"],
    )

    assert result["unique_columns"]["status"] == "FAIL"

    assert (
        result["unique_columns"]["details"]["id"][
            "duplicate_values_count"
        ]
        == 1
    )


def test_validate_base_dataset_rules_without_unique_columns(
    valid_base_dataframe,
):
    result = validate_base_dataset_rules(
        df=valid_base_dataframe,
        required_columns={"id", "name"},
        non_null_columns=["id", "name"],
    )

    assert "unique_columns" not in result