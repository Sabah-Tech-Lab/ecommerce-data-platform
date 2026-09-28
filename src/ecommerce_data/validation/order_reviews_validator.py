import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
    check_composite_key,
    check_integer_like_column,
    check_value_range,
    check_datetime_parseability,
    check_datetime_order,
   
)

from ecommerce_data.validation.order_reviews_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    COMPOSITE_KEY_COLUMNS,
    INTEGER_LIKE_COLUMNS,
    VALUE_RANGE_RULES,
    DATETIME_COLUMNS,
    TEMPORAL_RULES,
)

from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_order_reviews(df: pd.DataFrame) -> dict:
    """Validate the Olist order reviews dataset against configured data-quality rules.
    The validation covers schema requirements, nullability, composite-key uniqueness,
    integer-like values, value ranges, datetime parseability, and temporal ordering. 

    Args:
        df: Raw Olist order reviews DataFrame to validate.

    Returns:
        Validation report containing an overall status and detailed results for
        each validation category.
    """

    validation_results = validate_base_dataset_rules(
        df=df,
        required_columns=REQUIRED_COLUMNS,
        non_null_columns=NON_NULL_COLUMNS,
    )

    composite_key_result = check_composite_key(
        df,
        COMPOSITE_KEY_COLUMNS,
    )
    
    datetime_parseability_result = check_datetime_parseability(
        df, 
        DATETIME_COLUMNS,
    )

    temporal_rules_result = {
        f"{earlier_column}_to_{later_column}": check_datetime_order(
            df, 
            earlier_column, 
            later_column,
        )
        for earlier_column, later_column in TEMPORAL_RULES
    }

    temporal_rules_valid = all(
        result["is_valid"]
        for result in temporal_rules_result.values()
    )

    integer_like_columns_result = {
        column_name: check_integer_like_column(
            df,
            column_name,
        )
        for column_name in INTEGER_LIKE_COLUMNS
    }

    integer_like_columns_valid = all(
        result["is_valid"]
        for result in integer_like_columns_result.values()
    )

    value_range_result = {
        column_name: check_value_range(
            df,
            column_name,
            minimum_value,
            maximum_value,
        )
        for (column_name, minimum_value, maximum_value) in VALUE_RANGE_RULES
    }

    value_range_valid = all(
        result["is_valid"]
        for result in value_range_result.values()
    )

    




    validation_results["composite_key"] = {
        "status": 
            get_status(composite_key_result["is_valid"]),
        "details": composite_key_result,
    }

    validation_results["datetime_parseability"] = {
        "status": 
            get_status(
                datetime_parseability_result["is_valid"]
            ),
        "details": datetime_parseability_result,
    }

    validation_results["datetime_order"] = {
        "status": get_status(
            temporal_rules_valid,
            failure_status="WARNING",
        ),
                
        "details": temporal_rules_result
    }    

    validation_results["integer_like_columns"] = {
        "status":
            get_status(
                integer_like_columns_valid,
            ),
        "details":
            integer_like_columns_result,    
    }

    validation_results["value_range"] = {
        "status":
            get_status(
                value_range_valid,
            ),
        "details":
            value_range_result,    
    }    
        
    

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
    }