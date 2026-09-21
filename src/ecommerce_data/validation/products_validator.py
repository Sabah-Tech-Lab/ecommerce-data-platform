import pandas as pd

from ecommerce_data.validation.data_validator import (
    check_non_null_columns,
    check_required_columns,
    check_unique_column,
    is_dataframe_empty,
    check_minimum_value,
    check_integer_like_column,
)

from ecommerce_data.validation.products_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    UNIQUE_COLUMNS,
    INTEGER_LIKE_COLUMNS,
    MINIMUM_VALUE_RULES,
)

from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_products(df: pd.DataFrame) -> dict:
    """Validate the Olist products dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, uniqueness,
    integer-like values, and minimum-value constraints.

    Args:
        df: Raw Olist products DataFrame to validate.

    Returns:
        Validation report containing an overall status and detailed results for
        each validation category.
    """
    empty_dataframe_result = is_dataframe_empty(df)

    required_columns_result = check_required_columns(
        df,
        REQUIRED_COLUMNS,
    )

    non_null_columns_result = check_non_null_columns(
        df,
        NON_NULL_COLUMNS,
    )

    unique_columns_result = {
        column: check_unique_column(df, column)
        for column in UNIQUE_COLUMNS
    }

    unique_columns_valid = all(
        result["is_valid"]
        for result in unique_columns_result.values()
    )

    integer_like_columns_results = {
        column: check_integer_like_column(df, column)
        for column in INTEGER_LIKE_COLUMNS     
    }

    integer_like_columns_valid = all(
        result["is_valid"]
        for result in integer_like_columns_results.values()
    )

    minimum_value_rule_result = {
        f"{column_name}": check_minimum_value(
            df,
            column_name,
            minimum_value,
            inclusive,
        )
        for column_name, minimum_value, inclusive in MINIMUM_VALUE_RULES
    }

    minimum_value_rule_valid = all(
        result["is_valid"]
        for result in minimum_value_rule_result.values()
    )

    validation_results = {

        "dataframe_not_empty": {
            "status": 
                get_status(not empty_dataframe_result),
            "details": {
            "is_empty": empty_dataframe_result,
            },
        },
        "required_columns": {
            "status": 
                get_status(required_columns_result["is_valid"]),
            "details": required_columns_result,
        },
        "non_null_columns": {
            "status": 
                get_status(non_null_columns_result["is_valid"]),
            "details": non_null_columns_result,
        },
        "unique_columns": {
            "status": get_status(unique_columns_valid),
            "details": unique_columns_result,
        },
        "integer_like_columns": {
            "status": 
                get_status(integer_like_columns_valid),
            "details": integer_like_columns_results,
        },

        "minimum_value_validation": {
            "status": 
                get_status(minimum_value_rule_valid, failure_status="WARNING"),
                
            "details": minimum_value_rule_result
        },
        
    }

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
        }        







