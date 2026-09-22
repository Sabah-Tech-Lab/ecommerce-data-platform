import pandas as pd

from ecommerce_data.validation.base_validator import (
    validate_base_dataset_rules,
)
from ecommerce_data.validation.data_validator import (
    check_integer_like_column,
    check_minimum_value,
)
from ecommerce_data.validation.products_rules import (
    INTEGER_LIKE_COLUMNS,
    MINIMUM_VALUE_RULES,
    NON_NULL_COLUMNS,
    REQUIRED_COLUMNS,
    UNIQUE_COLUMNS,
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
    validation_results = validate_base_dataset_rules(
        df=df,
        required_columns=REQUIRED_COLUMNS,
        non_null_columns=NON_NULL_COLUMNS,
        unique_columns=UNIQUE_COLUMNS,
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

    validation_results["integer_like_columns"] = {
        "status": get_status(integer_like_columns_valid),
        "details": integer_like_columns_results,
    }

    validation_results["minimum_value_validation"] = {
        "status": get_status(
            minimum_value_rule_valid,
            failure_status="WARNING",
        ),
        "details": minimum_value_rule_result,
    }

    overall_status = get_overall_status(validation_results)

    return {
        "overall_status": overall_status,
        **validation_results,
    }





