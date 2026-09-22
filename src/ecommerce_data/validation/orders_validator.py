import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
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
    validation_results = validate_base_dataset_rules(
        df=df,
        required_columns=REQUIRED_COLUMNS,
        non_null_columns=NON_NULL_COLUMNS,
        unique_columns=UNIQUE_COLUMNS,
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




    validation_results["order_status"] = {
        "status": 
            get_status(
                allowed_order_statuses_result["is_valid"]
                ),
        "details": allowed_order_statuses_result,
    }
    validation_results["datetime_parseability"] = {
        "status": 
            get_status(
                datetime_parseability_result["is_valid"]
                ),
        "details": datetime_parseability_result,
    }
    validation_results["functional_dependency"] = {
        "status": 
            get_status(
                functional_dependency_valid
                ),
        "details": functional_dependency_result
    }
    validation_results["datetime_order"] = {
        "status": 
            get_status(
                temporal_rules_valid,failure_status="WARNING",
                ),
                
        "details": temporal_rules_result
    }
        
    

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
        }
