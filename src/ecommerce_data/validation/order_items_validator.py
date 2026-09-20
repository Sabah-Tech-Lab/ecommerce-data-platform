import pandas as pd

from ecommerce_data.validation.data_validator import (
    check_non_null_columns,
    check_required_columns,
    check_composite_key,
    is_dataframe_empty,
    check_datetime_parseability,
    check_minimum_value,
   
)

from ecommerce_data.validation.order_items_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    COMPOSITE_KEY_COLUMNS,
    DATETIME_COLUMNS,
    MINIMUM_VALUE_RULES,
)

from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_order_items(df: pd.DataFrame) -> dict:
    """Validate the Olist order items dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, composite-key uniqueness,  
    datetime parseability, and valid values. 

    Args:
        df: Raw Olist order items DataFrame to validate.

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

    composite_key_result = check_composite_key(
        df,
        COMPOSITE_KEY_COLUMNS,
    )

    datetime_parseability_result = check_datetime_parseability(
        df, 
        DATETIME_COLUMNS,
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
        "composite_key": {
            "status": 
                get_status(composite_key_result["is_valid"]),
            "details": composite_key_result,
        },

        "datetime_parseability": {
            "status": 
                get_status(datetime_parseability_result["is_valid"]),
            "details": datetime_parseability_result,
        },

        "minimum_value_validation": {
            "status": 
                get_status(minimum_value_rule_valid),
                
            "details": minimum_value_rule_result
        },
        
    }

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
        }
