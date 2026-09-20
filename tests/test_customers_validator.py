import pandas as pd
import pytest

from ecommerce_data.validation.customers_validator import (
    validate_customers,
)


# ------------------------------------------------------------------
# Fixtures for validate_customers()
# ------------------------------------------------------------------

@pytest.fixture
def valid_customers_dataframe():
    return pd.DataFrame(
        {
            "customer_id": [
                "customer_1",
                "customer_2",
            ],
            "customer_unique_id": [
                "unique_customer_1",
                "unique_customer_2",
            ],
            "customer_zip_code_prefix": [
                1000,
                2000,
            ],
            "customer_city": [
                "sao paulo",
                "rio de janeiro",
            ],
            "customer_state": [
                "SP",
                "RJ",
            ],
        }
    )


@pytest.fixture
def customers_dataframe_with_invalid_state(valid_customers_dataframe):
    df = valid_customers_dataframe.copy()

    df.loc[1, "customer_state"] = "XX"

    return df


@pytest.fixture
def customers_dataframe_with_dependency_violation(
    valid_customers_dataframe,
):
    df = valid_customers_dataframe.copy()

    df.loc[1, "customer_zip_code_prefix"] = 1000

    return df



def test_validate_customers_all_valid(valid_customers_dataframe):
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
                    "customer_id": 0,
                    "customer_unique_id": 0,
                    "customer_zip_code_prefix": 0,
                    "customer_city": 0,
                    "customer_state": 0,
                },
                "missing_columns": [],
            },
        },
        "unique_columns": {
            "status": "PASS",
            "details": {
                "customer_id": {
                    "is_valid": True,
                    "duplicate_values_count": 0,
                    "missing_columns": [],
                },
            },
        },
        "customer_states": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_values": [],
                "missing_columns": [],
            },
        },
        "functional_dependency": {
            "status": "PASS",
            "details": {
                "customer_zip_code_prefix_to_customer_state": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_customers(valid_customers_dataframe)

    assert result == expected_result


def test_validate_customers_with_invalid_state(customers_dataframe_with_invalid_state):
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
                    "customer_id": 0,
                    "customer_unique_id": 0,
                    "customer_zip_code_prefix": 0,
                    "customer_city": 0,
                    "customer_state": 0,
                },
                "missing_columns": [],
            },
        },
        "unique_columns": {
            "status": "PASS",
            "details": {
                "customer_id": {
                    "is_valid": True,
                    "duplicate_values_count": 0,
                    "missing_columns": [],
                },
            },
        },
        "customer_states": {
            "status": "FAIL",
            "details": {
                "is_valid": False,
                "invalid_values": ["XX"],
                "missing_columns": [],
            },
        },
        "functional_dependency": {
            "status": "PASS",
            "details": {
                "customer_zip_code_prefix_to_customer_state": {
                    "is_valid": True,
                    "violation_count": 0,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_customers(customers_dataframe_with_invalid_state)

    assert result == expected_result
    

def test_validate_customers_with_dependency_violation(customers_dataframe_with_dependency_violation):
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
                    "customer_id": 0,
                    "customer_unique_id": 0,
                    "customer_zip_code_prefix": 0,
                    "customer_city": 0,
                    "customer_state": 0,
                },
                "missing_columns": [],
            },
        },
        "unique_columns": {
            "status": "PASS",
            "details": {
                "customer_id": {
                    "is_valid": True,
                    "duplicate_values_count": 0,
                    "missing_columns": [],
                },
            },
        },
        "customer_states": {
            "status": "PASS",
            "details": {
                "is_valid": True,
                "invalid_values": [],
                "missing_columns": [],
            },
        },
        "functional_dependency": {
            "status": "FAIL",
            "details": {
                "customer_zip_code_prefix_to_customer_state": {
                    "is_valid": False,
                    "violation_count": 1,
                    "missing_columns": [],
                },
            },
        },
    }

    result = validate_customers(customers_dataframe_with_dependency_violation)

    assert result == expected_result    

                 