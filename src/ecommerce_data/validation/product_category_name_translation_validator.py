import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.product_category_name_translation_rules import (
    REQUIRED_COLUMNS,
    NON_NULL_COLUMNS,
    UNIQUE_COLUMNS,
)
from ecommerce_data.validation.reporting import (
    get_overall_status,
)

def validate_product_category_name_translation(df: pd.DataFrame) -> dict:
    """Validate the Olist product category name translation dataset.

    The validation covers schema requirements, nullability, and uniqueness.

    Args:
        df: Raw Olist product category name translation DataFrame to validate.

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

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
    }