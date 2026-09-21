"""Reusable generic data-validation helpers for pandas DataFrames."""

import pandas as pd


def is_dataframe_empty(df: pd.DataFrame) -> bool:
    """Return True when the DataFrame contains no rows."""
    return df.shape[0] == 0


def check_required_columns(df: pd.DataFrame, required_columns: set[str]) -> dict:
    """Check whether all required columns are present in the DataFrame.

    Args:
        df: DataFrame to validate.
        required_columns: Column names that must exist in the DataFrame.

    Returns:
        Validation result containing the validity flag and a sorted list of
        missing columns.
    """
    actual_columns = set(df.columns)
    missing_columns = required_columns - actual_columns

    return {
        "is_valid": not missing_columns,
        "missing_columns": sorted(missing_columns),
    }


def check_non_null_columns(df: pd.DataFrame, non_null_columns: list[str]) -> dict:
    """Check that specified columns exist and contain no null values.

    Args:
        df: DataFrame to validate.
        non_null_columns: Columns that are not allowed to contain null values.

    Returns:
        Validation result with null counts for each checked column and any
        missing columns.
    """
    column_check = check_required_columns(df, set(non_null_columns))

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "null_counts": {},
            "missing_columns": column_check["missing_columns"],
        }

    null_counts_series = df[non_null_columns].isna().sum()
    null_counts = {
        column: int(count)
        for column, count in null_counts_series.items()
    }

    return {
        "is_valid": all(count == 0 for count in null_counts.values()),
        "null_counts": null_counts,
        "missing_columns": [],
    }


def check_unique_column(df: pd.DataFrame, column_name: str) -> dict:
    """Check that a column exists and contains no duplicate values.

    Args:
        df: DataFrame to validate.
        column_name: Column whose values must be unique.

    Returns:
        Validation result with the number of duplicate occurrences and any
        missing columns.
    """
    column_check = check_required_columns(df, {column_name})

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "duplicate_values_count": 0,
            "missing_columns": column_check["missing_columns"],
        }

    duplicates_count = int(df[column_name].duplicated().sum())

    return {
        "is_valid": duplicates_count == 0,
        "duplicate_values_count": duplicates_count,
        "missing_columns": [],
    }


def check_allowed_values(
    df: pd.DataFrame,
    column_name: str,
    allowed_values: set[str],
) -> dict:
    """Check that non-null values in a column belong to an allowed set.

    Args:
        df: DataFrame to validate.
        column_name: Column whose values should be checked.
        allowed_values: Values permitted in the column.

    Returns:
        Validation result containing any unexpected values and missing columns.
        Null values are ignored and should be validated separately.
    """
    column_check = check_required_columns(df, {column_name})

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "invalid_values": [],
            "missing_columns": column_check["missing_columns"],
        }

    column_unique_values = set(df[column_name].dropna().unique())
    invalid_values = column_unique_values - allowed_values

    return {
        "is_valid": not invalid_values,
        "invalid_values": sorted(invalid_values),
        "missing_columns": [],
    }


def check_datetime_parseability(
    df: pd.DataFrame,
    datetime_columns: list[str],
) -> dict:
    """Check that non-null values in specified columns can be parsed as datetimes.

    Args:
        df: DataFrame to validate.
        datetime_columns: Columns expected to contain datetime-like values.

    Returns:
        Validation result with the number of unparseable non-null values per
        column and any missing columns.
    """
    column_check = check_required_columns(df, set(datetime_columns))

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "invalid_datetime_counts": {},
            "missing_columns": column_check["missing_columns"],
        }

    invalid_datetime_counts = {}

    for column in datetime_columns:
        non_null_values = df[column].dropna()
        parsed_values = pd.to_datetime(
            non_null_values,
            errors="coerce",
            format="mixed",
        )

        invalid_datetime_counts[column] = int(parsed_values.isna().sum())

    return {
        "is_valid": all(
            count == 0
            for count in invalid_datetime_counts.values()
        ),
        "invalid_datetime_counts": invalid_datetime_counts,
        "missing_columns": [],
    }


def check_datetime_order(
    df: pd.DataFrame,
    earlier_column: str,
    later_column: str,
) -> dict:
    """Check that an earlier datetime does not occur after a later datetime.

    Args:
        df: DataFrame to validate.
        earlier_column: Column expected to contain the earlier timestamp.
        later_column: Column expected to contain the later timestamp.

    Returns:
        Validation result with the number of rows where the earlier timestamp
        is greater than the later timestamp and any missing columns.

    Notes:
        Null or unparseable values become NaT and are not counted as temporal
        violations. Validate nullability and datetime parseability separately.
    """
    column_check = check_required_columns(
        df,
        {earlier_column, later_column},
    )

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "violation_count": 0,
            "missing_columns": column_check["missing_columns"],
        }

    earlier_datetime = pd.to_datetime(
        df[earlier_column],
        errors="coerce",
        format="mixed",
    )
    later_datetime = pd.to_datetime(
        df[later_column],
        errors="coerce",
        format="mixed",
    )

    violations = earlier_datetime > later_datetime
    violation_count = int(violations.sum())

    return {
        "is_valid": violation_count == 0,
        "violation_count": violation_count,
        "missing_columns": [],
    }


def check_functional_dependency(
    df: pd.DataFrame,
    determinant_column: str,
    dependent_column: str,
) -> dict:
    """Check that each determinant value maps to at most one dependent value.

    Args:
        df: DataFrame to validate.
        determinant_column: Column whose values determine the relationship.
        dependent_column: Column expected to have one distinct value for each
            determinant value.

    Returns:
        Validation result with the number of determinant values associated with
        more than one distinct dependent value and any missing columns.

    Notes:
        Repeated identical mappings are allowed. Null handling is delegated to
        the dedicated null-validation rule.
    """
    column_check = check_required_columns(
        df,
        {determinant_column, dependent_column},
    )

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "violation_count": 0,
            "missing_columns": column_check["missing_columns"],
        }

    unique_dependent_values_count = (
        df.groupby(determinant_column)[dependent_column].nunique()
    )
    violations = unique_dependent_values_count > 1
    violation_count = int(violations.sum())

    return {
        "is_valid": violation_count == 0,
        "violation_count": violation_count,
        "missing_columns": [],
    }

def check_composite_key(df: pd.DataFrame, key_columns: list[str]) -> dict:
    column_check = check_required_columns(df, set(key_columns))

    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "violation_count": 0,
            "missing_columns": column_check["missing_columns"],
        }

    duplicate_composite_keys_count = int(
        df.duplicated(
            subset=key_columns
        ).sum()
    )

    return {
        "is_valid": duplicate_composite_keys_count== 0,
        "violation_count": duplicate_composite_keys_count,
        "missing_columns": [],
    }    

def check_minimum_value(
        df: pd.DataFrame,
        column_name: str,
        minimum_value: float,
        inclusive=True,
    ) -> dict:
    column_check = check_required_columns(df, {column_name})


    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "violation_count": 0,
            "missing_columns": column_check["missing_columns"],
        }

    if inclusive:
        violation = df[column_name] < minimum_value
    else:
        violation = df[column_name] <= minimum_value

    violation_count = int(violation.sum())

    return {
        "is_valid": violation_count == 0,
        "violation_count": violation_count,
        "missing_columns": [],
    }     

def check_integer_like_column(
        df: pd.DataFrame, 
        column_name: str,
) -> dict:
    column_check = check_required_columns(df, {column_name})


    if not column_check["is_valid"]:
        return {
            "is_valid": False,
            "violation_count": 0,
            "missing_columns": column_check["missing_columns"],
        }
    
    non_integer_values_count = int(
        df[column_name]
        .dropna()
        .mod(1)
        .ne(0)
        .sum()
        )

    return {
        "is_valid": non_integer_values_count == 0,
        "violation_count": non_integer_values_count,
        "missing_columns": [],
    }
    


     
    
     

    
       
          

