import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
    check_allowed_values,
    check_functional_dependency,
)

from ecommerce_data.validation.customers_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    UNIQUE_COLUMNS,
    ALLOWED_CUSTOMER_STATES,
    FUNCTIONAL_DEPENDENCIES,
)

from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_customers(df: pd.DataFrame) -> dict:
    """Validate the Olist customers dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, uniqueness, allowed
    customer states, and functional dependencies. 

    Args:
        df: Raw Olist customers DataFrame to validate.

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
    allowed_customer_states_result = check_allowed_values(
        df, 
        "customer_state", 
        ALLOWED_CUSTOMER_STATES,
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

    validation_results["customer_states"] = {
        "status": 
            get_status(
                allowed_customer_states_result["is_valid"]
                ),
        "details": allowed_customer_states_result,
    }        
    validation_results["functional_dependency"] = {
        "status": 
            get_status(
                functional_dependency_valid
                ),
        "details": functional_dependency_result
    }
    

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
        }
         