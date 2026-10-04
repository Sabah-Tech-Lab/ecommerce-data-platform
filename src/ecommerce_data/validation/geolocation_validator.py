import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
    check_allowed_values,
    check_value_range,
)
from ecommerce_data.validation.geolocation_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    ALLOWED_STATES,
    VALUE_RANGE_RULES,
)
from ecommerce_data.validation.reporting import (
    get_overall_status,
    get_status,

)

def validate_geolocation(df: pd.DataFrame) -> dict:
    """Validate the Olist geolocation dataset against configured data-quality rules.

    The validation covers schema requirements, nullability, allowed states and geolocation 
    value-range constraints. 

    Args:
        df: Raw Olist geolocation DataFrame to validate.

    Returns:
        Validation report containing an overall status and detailed results for
        each validation category.
    """    

    validation_results = validate_base_dataset_rules(
        df=df,
        required_columns=REQUIRED_COLUMNS,
        non_null_columns=NON_NULL_COLUMNS,
    )   

    allowed_states_result = check_allowed_values(
        df, 
        "geolocation_state", 
        ALLOWED_STATES,
    ) 

    value_range_result = {
        column_name: check_value_range(
            df,
            column_name,
            minimum_value,
            maximum_value,
        )
        for column_name, minimum_value, maximum_value in VALUE_RANGE_RULES
    }

    value_range_valid = all(
        result["is_valid"]
        for result in value_range_result.values()
    )

    validation_results["states"] = {
        "status": get_status(allowed_states_result["is_valid"]),
        "details": allowed_states_result,
    }

    validation_results["value_range"] = {
        "status": get_status(value_range_valid),
        "details": value_range_result,
    }

    overall_status = get_overall_status(validation_results)
    
    return {
        "overall_status": overall_status,
        **validation_results,
    }    