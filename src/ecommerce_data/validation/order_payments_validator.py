import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
    check_composite_key,
    check_allowed_values,
    check_minimum_value,
   
)

from ecommerce_data.validation.order_payments_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    COMPOSITE_KEY_COLUMNS,
    ALLOWED_PAYMENT_TYPES,
    MINIMUM_VALUE_RULES,
)

from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_order_payments(df: pd.DataFrame) -> dict:
    """Validate the Olist order payments dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, composite-key uniqueness,
    allowed payment types, and minimum-value constraints. 

    Args:
        df: Raw Olist order payments DataFrame to validate.

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

    allowed_payment_types_result = check_allowed_values(
        df, 
        "payment_type", 
        ALLOWED_PAYMENT_TYPES,
    )

    minimum_value_rule_result = {
        column_name: check_minimum_value(
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

    validation_results["composite_key"] = {
        "status": 
            get_status(composite_key_result["is_valid"]),
        "details": composite_key_result,
    }

    validation_results["payment_type"] = {
        "status": 
            get_status(
                allowed_payment_types_result["is_valid"]
                ),
        "details": allowed_payment_types_result,
    }

    validation_results["minimum_value_validation"] = {
        "status": 
            get_status(
                minimum_value_rule_valid,
                failure_status="WARNING",
                ),
                
        "details": minimum_value_rule_result
    }
        
    

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
        }