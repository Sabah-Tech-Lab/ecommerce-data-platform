"""Unit tests for reusable generic DataFrame validation helpers."""

import pandas as pd
import pytest

from ecommerce_data.validation.data_validator import (
    check_non_null_columns,
    check_required_columns,
    check_unique_column,
    is_dataframe_empty,
    check_allowed_values,
    check_datetime_parseability,
    check_datetime_order,
    check_functional_dependency,
    check_composite_key,
    check_minimum_value,
    check_integer_like_column,
)

    # ------------------------------------------------------------------
    # Fixtures for is_dataframe_columns().
    # ------------------------------------------------------------------
@pytest.fixture
def empty_dataframe():
    """Return an empty DataFrame with no rows or columns."""
    return pd.DataFrame()

@pytest.fixture
def dataframe_with_data():
    """Return a small DataFrame containing valid sample data."""
    return pd.DataFrame(
        {
            'name': ['Alice', 'Jack'],
            'age': [30,32],
        }
    )


@pytest.fixture
def dataframe_without_columns():
    """Return a DataFrame with rows but no columns."""
    return pd.DataFrame(index=[0, 1])

    # ------------------------------------------------------------------
    # Fixtures for check_required_columns().
    # ------------------------------------------------------------------

@pytest.fixture
def required_columns_all_exist():
    """Return required columns that are all present in the sample DataFrame.""" 
    return{
    "name",
    "age",
    } 

@pytest.fixture
def required_columns_all_missing():
    """Return required columns that are all absent from the sample DataFrame."""
    return {
    "eyes_color",
    "height",
    }
@pytest.fixture
def required_columns_one_missing():
    """Return required columns with one missing column."""
    return {
    "name",
    "height",
    }



    # ------------------------------------------------------------------
    # Fixtures for check_non_null_columns().
    # ------------------------------------------------------------------ 

@pytest.fixture
def dataframe_without_nulls():
    """Return a DataFrame whose checked columns contain no null values."""
    return pd.DataFrame(
        {
            "client_id": [1, 2, 3],
            "client_name": ["Alice", "Bob", "Alex"],
        }
    )


@pytest.fixture
def dataframe_with_nulls():
    """Return a DataFrame containing null values in a checked column."""
    return pd.DataFrame(
        {
            "client_id": [1, 2, 3],
            "client_name": ["Alice", None, None],
        }
    )


@pytest.fixture
def dataframe_with_missing_column():
    """Return a DataFrame missing columns used by validation tests."""
    return pd.DataFrame(
        {
            "client_id": [1, 2, 3],
        }
    )

    # ------------------------------------------------------------------
    # Fixtures for check_unique_column().
    # ------------------------------------------------------------------ 

@pytest.fixture
def df_with_unique_column():
    """Return a DataFrame with a fully unique column."""
    return pd.DataFrame(
        {
            "client_id": [1, 2, 3],
        }
    )   

@pytest.fixture
def df_with_non_unique_column():
    """Return a DataFrame containing a duplicated value."""
    return pd.DataFrame(
        {
            "name": ["Alice", "Alice", "Bob"],
        }
    )  

    # ------------------------------------------------------------------
    # Fixtues for check_allowed_values() function.
    # ------------------------------------------------------------------
@pytest.fixture
def allowed_values():
    """Return the set of values permitted by allowed-value tests."""
    return {"red", "yellow", "orange", "blue"}

@pytest.fixture
def df_with_allowed_values():
    """Return a DataFrame containing only allowed values."""
    return pd.DataFrame(
        {
            "color":["red", "yellow", "blue", "orange"],
        }
    )   

@pytest.fixture
def df_with_not_allowed_values():
    """Return a DataFrame containing disallowed values."""
    return pd.DataFrame(
        {
            "color":["purple", "yellow", "blue", "black"],
        }
    )   

@pytest.fixture
def df_with_allowed_values_and_nulls():
    """Return allowed values mixed with nulls."""
    return pd.DataFrame(
        {
            "color":["red", None, "blue", None],
        }
    ) 
# ------------------------------------------------------------------
# Fixtures for check_datetime_parseability().
# ------------------------------------------------------------------

@pytest.fixture
def dataframe_with_valid_datetimes():
    """Return a DataFrame containing parseable datetime strings."""
    return pd.DataFrame(
        {
            "purchase_date": [
                "2018-05-10 14:30:00",
                "2018-06-12 09:15:00",
                "2018-07-20 18:45:00",
            ],
            "delivery_date": [
                "2018-05-15 16:00:00",
                "2018-06-16 11:30:00",
                "2018-07-25 13:20:00",
            ],
        }
    )


@pytest.fixture
def dataframe_with_invalid_datetimes():
    """Return a DataFrame containing invalid datetime strings."""
    return pd.DataFrame(
        {
            "purchase_date": [
                "2018-05-10 14:30:00",
                "not-a-date",
                "2018-07-20 18:45:00",
            ],
            "delivery_date": [
                "invalid-date",
                "2018-06-16 11:30:00",
                "wrong",
            ],
        }
    )


@pytest.fixture
def dataframe_with_valid_datetimes_and_nulls():
    """Return parseable datetimes mixed with null values."""
    return pd.DataFrame(
        {
            "purchase_date": [
                "2018-05-10 14:30:00",
                None,
                "2018-07-20 18:45:00",
            ],
            "delivery_date": [
                None,
                "2018-06-16 11:30:00",
                None,
            ],
        }
    )

# ------------------------------------------------------------------
# Fixtures for check_datetime_order().
# ------------------------------------------------------------------

@pytest.fixture
def dataframe_with_valid_datetime_order():
    """Return timestamps satisfying the expected chronological order."""
    return pd.DataFrame(
        {
            "purchase_date": [
                "2018-05-10 10:00:00",
                "2018-06-12 09:00:00",
                "2018-07-20 18:00:00",
            ],
            "delivery_date": [
                "2018-05-10 12:00:00",
                "2018-06-13 09:00:00",
                "2018-07-20 18:00:00",
            ],
        }
    )


@pytest.fixture
def dataframe_with_datetime_order_violations():
    """Return timestamps containing chronological-order violations."""
    return pd.DataFrame(
        {
            "purchase_date": [
                "2018-05-10 10:00:00",
                "2018-06-14 09:00:00",
                "2018-07-22 18:00:00",
            ],
            "delivery_date": [
                "2018-05-10 12:00:00",
                "2018-06-13 09:00:00",
                "2018-07-20 18:00:00",
            ],
        }
    )


@pytest.fixture
def dataframe_with_valid_datetime_order_and_nulls():
    """Return valid datetime ordering mixed with null values."""
    return pd.DataFrame(
        {
            "purchase_date": [
                "2018-05-10 10:00:00",
                None,
                "2018-07-20 18:00:00",
            ],
            "delivery_date": [
                "2018-05-10 12:00:00",
                "2018-06-13 09:00:00",
                None,
            ],
        }
    )

# ------------------------------------------------------------------
# Fixtures for check_functional_dependency().
# ------------------------------------------------------------------

@pytest.fixture
def dataframe_with_valid_functional_dependency():
    """Return data satisfying the configured functional dependency."""
    return pd.DataFrame(
        {
            "order_id": ["A", "A", "B", "B", "C"],
            "customer_id": ["C1", "C1", "C2", "C2", "C3"],
        }
    )


@pytest.fixture
def dataframe_with_functional_dependency_violations():
    """Return data violating the configured functional dependency."""
    return pd.DataFrame(
        {
            "order_id": ["A", "A", "B", "B", "C"],
            "customer_id": ["C1", "C2", "C3", "C4", "C5"],
        }
    )

    # ------------------------------------------------------------------
    # Tests for is_dataframe_empty().
    # ------------------------------------------------------------------

def test_is_dataframe_empty_no_data(empty_dataframe):
    

    assert is_dataframe_empty(empty_dataframe) is True
   

def test_is_dataframe_empty_with_data(dataframe_with_data):

    assert is_dataframe_empty(dataframe_with_data) is False

def test_is_dataframe_empty_without_columns(dataframe_without_columns):
    assert is_dataframe_empty(dataframe_without_columns) is False   

    # ------------------------------------------------------------------
    # Tests for check_required_columns().
    # ------------------------------------------------------------------    

def test_check_required_columns_all_exist(dataframe_with_data, required_columns_all_exist):
    expected_result = {
        "is_valid": True,
        "missing_columns":[]
    } 
    result = check_required_columns(dataframe_with_data, required_columns_all_exist)
    assert result == expected_result

def test_check_required_columns_all_missing(dataframe_with_data, required_columns_all_missing):
    expected_result = {
        "is_valid": False,
        "missing_columns":["eyes_color", "height"]
    } 
    result = check_required_columns(dataframe_with_data, required_columns_all_missing)
    assert result == expected_result    

def test_check_required_columns_one_missing(dataframe_with_data, required_columns_one_missing):
    expected_result = {
        "is_valid": False,
        "missing_columns":["height"]
    } 
    result = check_required_columns(dataframe_with_data, required_columns_one_missing)
    assert result == expected_result

    # ------------------------------------------------------------------
    # Tests for check_non_null_columns().
    # ------------------------------------------------------------------        

def test_check_non_null_columns_without_nulls(dataframe_without_nulls):
    columns = dataframe_without_nulls.columns.tolist()

    expected_result = {
        "is_valid": True,
        "null_counts": {
            "client_id": 0,
            "client_name": 0,
        },
        "missing_columns": [],
    }

    result = check_non_null_columns(dataframe_without_nulls, columns)

    assert result == expected_result


def test_check_non_null_columns_with_nulls(dataframe_with_nulls):
    columns = dataframe_with_nulls.columns.tolist()

    expected_result = {
        "is_valid": False,
        "null_counts": {
            "client_id": 0,
            "client_name": 2,
        },
        "missing_columns": [],
    }

    result = check_non_null_columns(dataframe_with_nulls, columns)

    assert result == expected_result


def test_check_non_null_columns_with_missing_column(dataframe_with_missing_column):
    columns = ["client_name"]

    expected_result = {
        "is_valid": False,
        "null_counts": {},
        "missing_columns": ["client_name"],
    }

    result = check_non_null_columns(
        dataframe_with_missing_column,
        columns,
    )

    assert result == expected_result

    # ------------------------------------------------------------------
    # Tests for check_unique_column().
    # ------------------------------------------------------------------    

def test_check_unique_column_valid_column(df_with_unique_column):
    column = df_with_unique_column.columns[0]    

    expected_result = {
        "is_valid": True,
        "duplicate_values_count": 0,
        "missing_columns": [],
    }

    result = check_unique_column(df_with_unique_column, column)

    assert result == expected_result

def test_check_unique_column_invalid_column(df_with_non_unique_column):
    column = df_with_non_unique_column.columns[0]    

    expected_result = {
        "is_valid": False,
        "duplicate_values_count": 1,
        "missing_columns": [],
    }

    result = check_unique_column(df_with_non_unique_column, column)

    assert result == expected_result    

def test_check_unique_column_missing_column(dataframe_with_missing_column):
    column = "name"    

    expected_result = {
        "is_valid": False,
        "duplicate_values_count": 0,
        "missing_columns": ["name"],
    }

    result = check_unique_column(dataframe_with_missing_column, column)

    assert result == expected_result     

    # ------------------------------------------------------------------
    # Tests for check_allowed_values().
    # ------------------------------------------------------------------      

def test_check_allowed_values_all_valid(df_with_allowed_values, allowed_values):
    column = df_with_allowed_values.columns[0]

    expected_result = {
        "is_valid": True,
        "invalid_values": [],
        "missing_columns": [],
    }  

    result = check_allowed_values(df_with_allowed_values, column, allowed_values)  

    assert result == expected_result

def test_check_allowed_values_invalid_values(df_with_not_allowed_values, allowed_values):
    column = df_with_not_allowed_values.columns[0]

    expected_result = {
        "is_valid": False,
        "invalid_values": ["black", "purple"],
        "missing_columns": [],
    }  

    result = check_allowed_values(df_with_not_allowed_values, column, allowed_values)  

    assert result == expected_result    

def test_check_allowed_values_missing_column(dataframe_with_missing_column, allowed_values):
    column = "color"

    expected_result = {
        "is_valid": False,
        "invalid_values": [],
        "missing_columns": ["color"],
    }  

    result = check_allowed_values(dataframe_with_missing_column, column, allowed_values)  

    assert result == expected_result     

def test_check_allowed_values_valid_with_nulls(df_with_allowed_values_and_nulls, allowed_values):
    column = df_with_allowed_values_and_nulls.columns[0]

    expected_result = {
        "is_valid": True,
        "invalid_values": [],
        "missing_columns": [],
    }  

    result = check_allowed_values(df_with_allowed_values_and_nulls, column, allowed_values)  

    assert result == expected_result  

    # ------------------------------------------------------------------
    # Tests for check_datetime_parseability().
    # ------------------------------------------------------------------        

def test_check_datetime_parseability_valid_datetimes(dataframe_with_valid_datetimes):
    columns = dataframe_with_valid_datetimes.columns.values.tolist()  

    expected_result = {
        "is_valid": True,
        "invalid_datetime_counts": {
            "purchase_date": 0,
            "delivery_date": 0,
        },
        "missing_columns": [],
    }

    result = check_datetime_parseability(dataframe_with_valid_datetimes, columns)

    assert result == expected_result

def test_check_datetime_parseability_invalid_datetimes(dataframe_with_invalid_datetimes):
    columns = dataframe_with_invalid_datetimes.columns.values.tolist()  

    expected_result = {
        "is_valid": False,
        "invalid_datetime_counts": {
            "purchase_date": 1,
            "delivery_date": 2,
        },
        "missing_columns": [],
    }

    result = check_datetime_parseability(dataframe_with_invalid_datetimes, columns)

    assert result == expected_result    

def test_check_datetime_parseability_valid_datetimes_and_nulls(dataframe_with_valid_datetimes_and_nulls):
    columns = dataframe_with_valid_datetimes_and_nulls.columns.tolist()  

    expected_result = {
        "is_valid": True,
        "invalid_datetime_counts": {
            "purchase_date": 0,
            "delivery_date": 0,
        },
        "missing_columns": [],
    }

    result = check_datetime_parseability(dataframe_with_valid_datetimes_and_nulls, columns)

    assert result == expected_result   

def test_check_datetime_parseability_missing_columns(dataframe_with_missing_column):
    columns = ["purchase_date", "delivery_date"] 

    expected_result = {
        "is_valid": False,
        "invalid_datetime_counts": {},
        "missing_columns": ["delivery_date", "purchase_date"],
    }

    result = check_datetime_parseability(dataframe_with_missing_column, columns)

    assert result == expected_result   

    # ------------------------------------------------------------------
    # Tests for check_datetime_order().
    # ------------------------------------------------------------------ 

def test_check_datetime_order_valid_datetime(dataframe_with_valid_datetime_order):
    earlier_column = "purchase_date"
    later_column = "delivery_date"

    expected_result = {
        "is_valid": True,
        "violation_count": 0,
        "missing_columns": [],
    }  

    result = check_datetime_order(dataframe_with_valid_datetime_order, earlier_column, later_column)     

    assert result == expected_result

def test_check_datetime_order_with_violations(dataframe_with_datetime_order_violations):
    earlier_column = "purchase_date"
    later_column = "delivery_date"

    expected_result = {
        "is_valid": False,
        "violation_count": 2,
        "missing_columns": [],
    }  

    result = check_datetime_order(dataframe_with_datetime_order_violations, earlier_column, later_column)     

    assert result == expected_result

def test_check_datetime_order_valid_with_nulls(dataframe_with_valid_datetime_order_and_nulls):
    earlier_column = "purchase_date"
    later_column = "delivery_date"

    expected_result = {
        "is_valid": True,
        "violation_count": 0,
        "missing_columns": [],
    }  

    result = check_datetime_order(dataframe_with_valid_datetime_order_and_nulls, earlier_column, later_column)     

    assert result == expected_result

def test_check_datetime_order_missing_column(dataframe_with_missing_column):
    earlier_column = "purchase_date"
    later_column = "delivery_date"

    expected_result = {
        "is_valid": False,
        "violation_count": 0,
        "missing_columns": ["delivery_date", "purchase_date"],
    }  

    result = check_datetime_order(dataframe_with_missing_column, earlier_column, later_column)     

    assert result == expected_result   

    # ------------------------------------------------------------------
    # Tests for check_functional_dependency().
    # ------------------------------------------------------------------      

def test_check_functional_dependency_valid(dataframe_with_valid_functional_dependency):
    determinant_column = "order_id"
    dependent_column = "customer_id"

    expected_result = {
        "is_valid": True,
        "violation_count": 0,
        "missing_columns": [],
    }

    result = check_functional_dependency(
        dataframe_with_valid_functional_dependency, 
        determinant_column, 
        dependent_column
        )

    assert result == expected_result

def test_check_functional_dependency_with_violations(dataframe_with_functional_dependency_violations):
    determinant_column = "order_id"
    dependent_column = "customer_id"

    expected_result = {
        "is_valid": False,
        "violation_count": 2,
        "missing_columns": [],
    }

    result = check_functional_dependency(
        dataframe_with_functional_dependency_violations, 
        determinant_column, 
        dependent_column
        )

    assert result == expected_result   

def test_check_functional_dependency_with_missing_columns(dataframe_with_missing_column):
    determinant_column = "order_id"
    dependent_column = "customer_id"

    expected_result = {
        "is_valid": False,
        "violation_count": 0,
        "missing_columns": ["customer_id", "order_id"],
    }

    result = check_functional_dependency(
        dataframe_with_missing_column,
        determinant_column,
        dependent_column,
        )

    assert result == expected_result     


# ------------------------------------------------------------------
# Fixtures for check_composite_key().
# ------------------------------------------------------------------


@pytest.fixture
def valid_composite_key_df():
    return pd.DataFrame(
        {
            "order_id": ["order_1", "order_1", "order_2"],
            "order_item_id": [1, 2, 1],
        }
    )


@pytest.fixture
def invalid_composite_key_df():
    return pd.DataFrame(
        {
            "order_id": ["order_1", "order_1"],
            "order_item_id": [1, 1],
        }
    )


# ------------------------------------------------------------------
# Tests for check_composite_key().
# ------------------------------------------------------------------


def test_check_composite_key_valid(valid_composite_key_df):
    result = check_composite_key(
        valid_composite_key_df,
        ["order_id", "order_item_id"],
    )

    assert result["is_valid"] is True
    assert result["violation_count"] == 0


def test_check_composite_key_invalid(invalid_composite_key_df):
    result = check_composite_key(
        invalid_composite_key_df,
        ["order_id", "order_item_id"],
    )

    assert result["is_valid"] is False
    assert result["violation_count"] == 1


# ------------------------------------------------------------------
# Fixtures for check_minimum_value().
# ------------------------------------------------------------------


@pytest.fixture
def valid_minimum_value_df():
    return pd.DataFrame(
        {
            "price": [10.0, 20.0, 5.0],
            "freight_value": [0.0, 5.0, 10.0],
        }
    )


@pytest.fixture
def invalid_minimum_value_df():
    return pd.DataFrame(
        {
            "price": [10.0, 0.0, -5.0],
        }
    )


# ------------------------------------------------------------------
# Tests for check_minimum_value().
# ------------------------------------------------------------------


def test_check_minimum_value_valid(valid_minimum_value_df):
    price_result = check_minimum_value(
        valid_minimum_value_df,
        "price",
        minimum_value=0,
        inclusive=False,
    )

    freight_result = check_minimum_value(
        valid_minimum_value_df,
        "freight_value",
        minimum_value=0,
        inclusive=True,
    )

    assert price_result["is_valid"] is True
    assert price_result["violation_count"] == 0

    assert freight_result["is_valid"] is True
    assert freight_result["violation_count"] == 0


def test_check_minimum_value_invalid(invalid_minimum_value_df):
    result = check_minimum_value(
        invalid_minimum_value_df,
        "price",
        minimum_value=0,
        inclusive=False,
    )

    assert result["is_valid"] is False
    assert result["violation_count"] == 2

# ------------------------------------------------------------------
# Fixtures for check_integer_like_column().
# ------------------------------------------------------------------


@pytest.fixture
def valid_integer_like_df():
    return pd.DataFrame(
        {
            "product_photos_qty": [
                1.0,
                2.0,
                3.0,
                None,
            ]
        }
    )


@pytest.fixture
def invalid_integer_like_df():
    return pd.DataFrame(
        {
            "product_photos_qty": [
                1.0,
                2.5,
                3.0,
                None,
            ]
        }
    )


# ------------------------------------------------------------------
# Tests for check_integer_like_column().
# ------------------------------------------------------------------


def test_check_integer_like_column_valid(valid_integer_like_df):
    result = check_integer_like_column(
        valid_integer_like_df,
        "product_photos_qty",
    )

    assert result["is_valid"] is True
    assert result["violation_count"] == 0


def test_check_integer_like_column_invalid(invalid_integer_like_df):
    result = check_integer_like_column(
        invalid_integer_like_df,
        "product_photos_qty",
    )

    assert result["is_valid"] is False
    assert result["violation_count"] == 1    

