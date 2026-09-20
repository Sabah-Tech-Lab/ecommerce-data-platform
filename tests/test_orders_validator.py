import pandas as pd
import pytest

from ecommerce_data.validation.orders_validator import validate_orders

    # ------------------------------------------------------------------
    # Fixtures for validate_order().
    # ------------------------------------------------------------------

@pytest.fixture
def valid_orders_dataframe():
    """Return valid sample orders that should pass all validation rules."""
    return pd.DataFrame(
        {
            "order_id": [
                "order_1",
                "order_2",
            ],
            "customer_id": [
                "customer_1",
                "customer_2",
            ],
            "order_status": [
                "delivered",
                "shipped",
            ],
            "order_purchase_timestamp": [
                "2018-01-01 10:00:00",
                "2018-02-01 09:00:00",
            ],
            "order_approved_at": [
                "2018-01-01 11:00:00",
                "2018-02-01 10:00:00",
            ],
            "order_delivered_carrier_date": [
                "2018-01-02 08:00:00",
                "2018-02-02 08:00:00",
            ],
            "order_delivered_customer_date": [
                "2018-01-05 15:00:00",
                "2018-02-05 16:00:00",
            ],
            "order_estimated_delivery_date": [
                "2018-01-10 00:00:00",
                "2018-02-10 00:00:00",
            ],
        }
    )

@pytest.fixture
def orders_dataframe_with_invalid_status(valid_orders_dataframe):
    """Return sample orders containing an unsupported order status."""
    df = valid_orders_dataframe.copy()

    df.loc[1, "order_status"] = "unknown_status"

    return df

@pytest.fixture
def orders_dataframe_with_temporal_warning(valid_orders_dataframe):
    """Return sample orders containing a temporal-order anomaly."""
    df = valid_orders_dataframe.copy()

    df.loc[
        0,
        "order_delivered_carrier_date",
    ] = "2018-01-01 09:00:00"

    return df

    # ------------------------------------------------------------------
    # Tests for validate_orders().
    # ------------------------------------------------------------------

def test_validate_orders_all_valid(valid_orders_dataframe):
    
    expected_result = {
        "overall_status": "PASS",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {
                "is_empty": False,
            },
        },
        "required_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "missing_columns": [],
            },
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "customer_id": 0,
                    "order_status": 0,
                    "order_purchase_timestamp": 0,
                    "order_estimated_delivery_date": 0,
                },
                "missing_columns": [],
            },
        },
        "unique_columns": {
            "status": "PASS",
            "details": {
                "order_id": {
                    "is_valid": True,
                    "duplicate_values_count": 0,
                    "missing_columns": [],
                }
            },
        },
        "order_status": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_values": [],
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_datetime_counts": {
                    "order_purchase_timestamp": 0,
                    "order_approved_at": 0,
                    "order_delivered_carrier_date": 0,
                    "order_delivered_customer_date": 0,
                    "order_estimated_delivery_date": 0,
                },
                "missing_columns": [],
            },
        },
        "functional_dependency": {
            "status": "PASS",
            "details": {
                "order_id_to_customer_id": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                }
            },
        },
        "datetime_order": {
            "status": "PASS",
            "details": {
                "order_purchase_timestamp_to_order_approved_at": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "order_purchase_timestamp_to_order_delivered_carrier_date": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "order_delivered_carrier_date_to_order_delivered_customer_date": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_orders(valid_orders_dataframe) 

    assert result == expected_result

def test_validate_orders_with_invalid_status(orders_dataframe_with_invalid_status): 
    expected_result = {
        "overall_status": "FAIL",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {
                "is_empty": False,
            },
        },
        "required_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "missing_columns": [],
            },
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "customer_id": 0,
                    "order_status": 0,
                    "order_purchase_timestamp": 0,
                    "order_estimated_delivery_date": 0,
                },
                "missing_columns": [],
            },
        },
        "unique_columns": {
            "status": "PASS",
            "details": {
                "order_id": {
                    "is_valid": True,
                    "duplicate_values_count": 0,
                    "missing_columns": [],
                }
            },
        },
        "order_status": {
            "status": "FAIL",
            "details": {
                "is_valid": False,
                "invalid_values": ["unknown_status"],
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_datetime_counts": {
                    "order_purchase_timestamp": 0,
                    "order_approved_at": 0,
                    "order_delivered_carrier_date": 0,
                    "order_delivered_customer_date": 0,
                    "order_estimated_delivery_date": 0,
                },
                "missing_columns": [],
            },
        },
        "functional_dependency": {
            "status": "PASS",
            "details": {
                "order_id_to_customer_id": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                }
            },
        },
        "datetime_order": {
            "status": "PASS",
            "details": {
                "order_purchase_timestamp_to_order_approved_at": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "order_purchase_timestamp_to_order_delivered_carrier_date": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "order_delivered_carrier_date_to_order_delivered_customer_date": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_orders(orders_dataframe_with_invalid_status)

    assert result == expected_result
    
def test_validate_orders_with_temporal_warning(orders_dataframe_with_temporal_warning):
    expected_result = {
        "overall_status": "WARNING",
        "dataframe_not_empty": {
            "status": "PASS",
            "details": {
                "is_empty": False,
            },
        },
        "required_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "missing_columns": [],
            },
        },
        "non_null_columns": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "null_counts": {
                    "order_id": 0,
                    "customer_id": 0,
                    "order_status": 0,
                    "order_purchase_timestamp": 0,
                    "order_estimated_delivery_date": 0,
                },
                "missing_columns": [],
            },
        },
        "unique_columns": {
            "status": "PASS",
            "details": {
                "order_id": {
                    "is_valid": True,
                    "duplicate_values_count": 0,
                    "missing_columns": [],
                }
            },
        },
        "order_status": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_values": [],
                "missing_columns": [],
            },
        },
        "datetime_parseability": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_datetime_counts": {
                    "order_purchase_timestamp": 0,
                    "order_approved_at": 0,
                    "order_delivered_carrier_date": 0,
                    "order_delivered_customer_date": 0,
                    "order_estimated_delivery_date": 0,
                },
                "missing_columns": [],
            },
        },
        "functional_dependency": {
            "status": "PASS",
            "details": {
                "order_id_to_customer_id": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                }
            },
        },
        "datetime_order": {
            "status": "WARNING",
            "details": {
                "order_purchase_timestamp_to_order_approved_at": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
                "order_purchase_timestamp_to_order_delivered_carrier_date": {
                    "is_valid": False,
                    "violation_count": 1,
                    "missing_columns": [],
                },
                "order_delivered_carrier_date_to_order_delivered_customer_date": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }   