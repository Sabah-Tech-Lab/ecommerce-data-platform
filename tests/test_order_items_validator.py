"""Tests for the Olist order items validation orchestrator."""

import pandas as pd
import pytest

from ecommerce_data.validation.order_items_validator import validate_order_items


# ------------------------------------------------------------------
# Fixtures for validate_order_items()
# ------------------------------------------------------------------

@pytest.fixture
def valid_order_items_dataframe():
    """Return valid sample order items that should pass all validation rules."""
    return pd.DataFrame(
        {
            "order_id": ["order_1", "order_1", "order_2"],
            "order_item_id": [1, 2, 1],
            "product_id": ["product_1", "product_2", "product_3"],
            "seller_id": ["seller_1", "seller_1", "seller_2"],
            "shipping_limit_date": [
                "2018-01-05 10:00:00",
                "2018-01-05 10:00:00",
                "2018-02-10 12:00:00",
            ],
            "price": [50.0, 25.0, 100.0],
            "freight_value": [0.0, 10.0, 15.0],
        }
    )


@pytest.fixture
def order_items_dataframe_with_composite_key_violation(
    valid_order_items_dataframe,
):
    """Return sample data containing a duplicated composite key."""
    duplicate_key_row = pd.DataFrame(
        {
            "order_id": ["order_1"],
            "order_item_id": [1],
            "product_id": ["product_4"],
            "seller_id": ["seller_3"],
            "shipping_limit_date": ["2018-01-06 10:00:00"],
            "price": [75.0],
            "freight_value": [5.0],
        }
    )

    return pd.concat(
        [valid_order_items_dataframe, duplicate_key_row],
        ignore_index=True,
    )


@pytest.fixture
def order_items_dataframe_with_invalid_price(
    valid_order_items_dataframe,
):
    """Return sample data containing a price that violates the minimum rule."""
    df = valid_order_items_dataframe.copy()
    df.loc[0, "price"] = 0.0
    return df


@pytest.fixture
def order_items_dataframe_with_invalid_datetime(
    valid_order_items_dataframe,
):
    """Return sample data containing an unparseable shipping limit date."""
    df = valid_order_items_dataframe.copy()
    df.loc[1, "shipping_limit_date"] = "not-a-date"
    return df


# ------------------------------------------------------------------
# Tests for validate_order_items()
# ------------------------------------------------------------------

def test_validate_order_items_all_valid(valid_order_items_dataframe):
    expected_result = {
        "overall_status": "PASS",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {"is_empty": False},
        },
        "required_columns": {
            "status": "PASS",
            "details": {"is_valid": True, "missing_columns": []},
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "order_item_id": 0,
                    "product_id": 0,
                    "seller_id": 0,
                    "shipping_limit_date": 0,
                    "price": 0,
                    "freight_value": 0,
                },
                "missing_columns": [],
            },
        },
        "composite_key": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "duplicate_values_count": 0,
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_datetime_counts": {"shipping_limit_date": 0},
                "missing_columns": [],
            },
        },
        "minimum_value_validation": {
            "status": "PASS",
            "details": {
                "price": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "freight_value": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_order_items(valid_order_items_dataframe)

    assert result == expected_result


def test_validate_order_items_with_composite_key_violation(
    order_items_dataframe_with_composite_key_violation,
):
    expected_result = {
        "overall_status": "FAIL",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {"is_empty": False},
        },
        "required_columns": {
            "status": "PASS",
            "details": {"is_valid": True, "missing_columns": []},
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "order_item_id": 0,
                    "product_id": 0,
                    "seller_id": 0,
                    "shipping_limit_date": 0,
                    "price": 0,
                    "freight_value": 0,
                },
                "missing_columns": [],
            },
        },
        "composite_key": {
            "status": "FAIL",
            "details": {
                "is_valid": False,
                "duplicate_values_count": 1,
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_datetime_counts": {"shipping_limit_date": 0},
                "missing_columns": [],
            },
        },
        "minimum_value_validation": {
            "status": "PASS",
            "details": {
                "price": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "freight_value": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_order_items(
        order_items_dataframe_with_composite_key_violation
    )

    assert result == expected_result


def test_validate_order_items_with_invalid_price(
    order_items_dataframe_with_invalid_price,
):
    expected_result = {
        "overall_status": "FAIL",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {"is_empty": False},
        },
        "required_columns": {
            "status": "PASS",
            "details": {"is_valid": True, "missing_columns": []},
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "order_item_id": 0,
                    "product_id": 0,
                    "seller_id": 0,
                    "shipping_limit_date": 0,
                    "price": 0,
                    "freight_value": 0,
                },
                "missing_columns": [],
            },
        },
        "composite_key": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "duplicate_values_count": 0,
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_datetime_counts": {"shipping_limit_date": 0},
                "missing_columns": [],
            },
        },
        "minimum_value_validation": {
            "status": "FAIL",
            "details": {
                "price": {
                    "is_valid": False,
                    "violation_count": 1,
                    "missing_columns": [],
                },
                "freight_value": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_order_items(
        order_items_dataframe_with_invalid_price
    )

    assert result == expected_result


def test_validate_order_items_with_invalid_datetime(
    order_items_dataframe_with_invalid_datetime,
):
    expected_result = {
        "overall_status": "FAIL",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {"is_empty": False},
        },
        "required_columns": {
            "status": "PASS",
            "details": {"is_valid": True, "missing_columns": []},
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "order_item_id": 0,
                    "product_id": 0,
                    "seller_id": 0,
                    "shipping_limit_date": 0,
                    "price": 0,
                    "freight_value": 0,
                },
                "missing_columns": [],
            },
        },
        "composite_key": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "duplicate_values_count": 0,
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "FAIL",
            "details": {
                "is_valid": False,
                "invalid_datetime_counts": {"shipping_limit_date": 1},
                "missing_columns": [],
            },
        },
        "minimum_value_validation": {
            "status": "PASS",
            "details": {
                "price": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "freight_value": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_order_items(
        order_items_dataframe_with_invalid_datetime
    )

    assert result == expected_result