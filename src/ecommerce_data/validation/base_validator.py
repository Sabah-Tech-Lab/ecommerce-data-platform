import pandas as pd

from ecommerce_data.validation.data_validator import (
    check_non_null_columns,
    check_required_columns,
    check_unique_column,
    is_dataframe_empty,
)
from ecommerce_data.validation.reporting import get_status


def validate_base_dataset_rules(
    df: pd.DataFrame,
    required_columns: set[str],
    non_null_columns: list[str],
    unique_columns: list[str] | None = None,
) -> dict:
    """Validate shared dataset-level data-quality rules.

    The validation covers dataset emptiness, required columns,
    non-null constraints, and optional single-column uniqueness rules.

    Args:
        df: DataFrame to validate.
        required_columns: Columns that must exist in the DataFrame.
        non_null_columns: Columns that must not contain null values.
        unique_columns: Optional columns whose values must be unique.

    Returns:
        Validation results for the shared dataset-level rules.
    """
    empty_dataframe_result = is_dataframe_empty(df)

    required_columns_result = check_required_columns(
        df,
        required_columns,
    )

    non_null_columns_result = check_non_null_columns(
        df,
        non_null_columns,
    )

    validation_results = {
        "dataframe_not_empty": {
            "status": get_status(not empty_dataframe_result),
            "details": {
                "is_empty": empty_dataframe_result,
            },
        },
        "required_columns": {
            "status": get_status(
                required_columns_result["is_valid"]
            ),
            "details": required_columns_result,
        },
        "non_null_columns": {
            "status": get_status(
                non_null_columns_result["is_valid"]
            ),
            "details": non_null_columns_result,
        },
    }

    if unique_columns:
        unique_columns_result = {
            column: check_unique_column(df, column)
            for column in unique_columns
        }

        unique_columns_valid = all(
            result["is_valid"]
            for result in unique_columns_result.values()
        )

        validation_results["unique_columns"] = {
            "status": get_status(unique_columns_valid),
            "details": unique_columns_result,
        }

    return validation_results