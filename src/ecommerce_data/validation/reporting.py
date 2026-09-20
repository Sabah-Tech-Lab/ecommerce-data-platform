
def get_status(
    is_valid: bool,
    failure_status: str = "FAIL",
) -> str:
    """Convert a validation result into a report status.

    Args:
        is_valid: Whether the validation rule passed.
        failure_status: Status to return when validation fails.

    Returns:
        "PASS" when the rule is valid; otherwise the configured failure status.
    """
    return "PASS" if is_valid else failure_status

def get_overall_status(validation_results: dict) -> str:
    """Determine the overall status of a customers validation report.

    Args:
        validation_results: Individual validation sections containing status values.

    Returns:
        "FAIL" if any rule fails, otherwise "WARNING" if any warning exists,
        otherwise "PASS".
    """
    statuses = [
        result["status"]
        for result in validation_results.values()
    ]

    if "FAIL" in statuses:
        return "FAIL"

    if "WARNING" in statuses:
        return "WARNING"

    return "PASS"