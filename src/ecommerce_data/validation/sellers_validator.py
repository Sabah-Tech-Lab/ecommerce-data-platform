import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
    check_allowed_values,
)
from ecommerce_data.validation.sellers_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    UNIQUE_COLUMNS,
    ALLOWED_STATES,
)
from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)
def validate_sellers(df: pd.DataFrame) -> dict:
    """Validate the Olist sellers dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, uniqueness, and allowed
    states. 

    Args:
        df: Raw Olist sellers DataFrame to validate.

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

    allowed_states_result = check_allowed_values(
        df, 
        "seller_state", 
        ALLOWED_STATES,
    ) 

    validation_results["states"] = {
        "status": 
            get_status(
                allowed_states_result["is_valid"]
            ),
        "details": allowed_states_result,
    } 

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
    }
