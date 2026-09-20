import pandas as pd

from ecommerce_data.validation.data_validator import (
    check_non_null_columns,
    check_required_columns,
    check_unique_column,
    is_dataframe_empty,
    check_allowed_values,
    check_datetime_parseability,
    check_datetime_order,
    check_functional_dependency,
)

from ecommerce_data.validation.orders_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    UNIQUE_COLUMNS,
    ALLOWED_ORDER_STATUSES,
    DATETIME_COLUMNS,
    TEMPORAL_RULES,
    FUNCTIONAL_DEPENDENCIES,
)

from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_orders(df: pd.DataFrame) -> dict:
    """Validate the Olist orders dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, uniqueness, allowed
    order statuses, datetime parseability, functional dependencies, and temporal
    relationships. Temporal-order violations are reported as warnings rather
    than hard failures.

    Args:
        df: Raw Olist orders DataFrame to validate.

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

    datetime_parseability_result = check_datetime_parseability(
        df, 
        DATETIME_COLUMNS,
        )

    allowed_order_statuses_result = check_allowed_values(
        df, 
        "order_status", 
        ALLOWED_ORDER_STATUSES,
        )
    
    functional_dependency_result = {
        f"{determinant}_to_{dependent}": check_functional_dependency(
            df,
            determinant,
            dependent,
        )
        for determinant, dependent in FUNCTIONAL_DEPENDENCIES
    }

    functional_dependency_valid = all(
        result["is_valid"]
        for result in functional_dependency_result.values()
    )

    temporal_rules_result = {
        f"{earlier_column}_to_{later_column}": check_datetime_order(
            df, 
            earlier_column, 
            later_column,)
        for earlier_column, later_column in TEMPORAL_RULES
    }

    temporal_rules_valid = all(
        result["is_valid"]
        for result in temporal_rules_result.values()
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
            "status": 
                get_status(unique_columns_valid),
            "details": unique_columns_result,
        },
        "order_status": {
            "status": 
                get_status(allowed_order_statuses_result["is_valid"]),
            "details": allowed_order_statuses_result,
        },
        "datetime_parseability": {
            "status": 
                get_status(datetime_parseability_result["is_valid"]),
            "details": datetime_parseability_result,
        },
        "functional_dependency": {
            "status": 
                get_status(functional_dependency_valid),
            "details": functional_dependency_result
        },
        "datetime_order": {
            "status": 
                get_status(temporal_rules_valid,failure_status="WARNING",),
                
            "details": temporal_rules_result
        },
        
    }

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
        }
