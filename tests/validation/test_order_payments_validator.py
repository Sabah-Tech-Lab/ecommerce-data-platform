import pandas as pd
import pytest

from ecommerce_data.validation.order_payments_validator import (
    validate_order_payments,
)


# ------------------------------------------------------------------
# Fixtures for validate_order_payments().
# ------------------------------------------------------------------


@pytest.fixture
def valid_order_payments_dataframe():
    return pd.DataFrame(
        {
            "order_id": [
                "order_1",
                "order_1",
                "order_2",
            ],
            "payment_sequential": [
                1,
                2,
                1,
            ],
            "payment_type": [
                "credit_card",
                "voucher",
                "boleto",
            ],
            "payment_installments": [
                2,
                1,
                1,
            ],
            "payment_value": [
                100.0,
                20.0,
                75.0,
            ],
        }
    )


@pytest.fixture
def order_payments_dataframe_with_composite_key_violation():
    return pd.DataFrame(
        {
            "order_id": [
                "order_1",
                "order_1",
            ],
            "payment_sequential": [
                1,
                1,
            ],
            "payment_type": [
                "credit_card",
                "voucher",
            ],
            "payment_installments": [
                2,
                1,
            ],
            "payment_value": [
                100.0,
                20.0,
            ],
        }
    )


@pytest.fixture
def order_payments_dataframe_with_invalid_payment_type():
    return pd.DataFrame(
        {
            "order_id": [
                "order_1",
                "order_2",
            ],
            "payment_sequential": [
                1,
                1,
            ],
            "payment_type": [
                "credit_card",
                "crypto",
            ],
            "payment_installments": [
                2,
                1,
            ],
            "payment_value": [
                100.0,
                75.0,
            ],
        }
    )


@pytest.fixture
def order_payments_dataframe_with_zero_installments():
    return pd.DataFrame(
        {
            "order_id": [
                "order_1",
                "order_2",
            ],
            "payment_sequential": [
                1,
                1,
            ],
            "payment_type": [
                "credit_card",
                "credit_card",
            ],
            "payment_installments": [
                2,
                0,
            ],
            "payment_value": [
                100.0,
                75.0,
            ],
        }
    )


@pytest.fixture
def order_payments_dataframe_with_zero_payment_value():
    return pd.DataFrame(
        {
            "order_id": [
                "order_1",
                "order_2",
            ],
            "payment_sequential": [
                1,
                1,
            ],
            "payment_type": [
                "credit_card",
                "voucher",
            ],
            "payment_installments": [
                2,
                1,
            ],
            "payment_value": [
                100.0,
                0.0,
            ],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_order_payments().
# ------------------------------------------------------------------


def test_validate_order_payments_with_valid_data(
    valid_order_payments_dataframe,
):
    result = validate_order_payments(
        valid_order_payments_dataframe
    )

    assert result["overall_status"] == "PASS"
    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["composite_key"]["status"] == "PASS"
    assert result["payment_type"]["status"] == "PASS"
    assert result["minimum_value_validation"]["status"] == "PASS"


def test_validate_order_payments_with_composite_key_violation(
    order_payments_dataframe_with_composite_key_violation,
):
    result = validate_order_payments(
        order_payments_dataframe_with_composite_key_violation
    )

    assert result["overall_status"] == "FAIL"
    assert result["composite_key"]["status"] == "FAIL"

    assert result["composite_key"]["details"]["is_valid"] is False
    assert result["composite_key"]["details"]["violation_count"] == 1


def test_validate_order_payments_with_invalid_payment_type(
    order_payments_dataframe_with_invalid_payment_type,
):
    result = validate_order_payments(
        order_payments_dataframe_with_invalid_payment_type
    )

    assert result["overall_status"] == "FAIL"
    assert result["payment_type"]["status"] == "FAIL"

    assert result["payment_type"]["details"]["is_valid"] is False

    assert result["payment_type"]["details"]["invalid_values"] == [
        "crypto"
    ]


def test_validate_order_payments_with_zero_installments(
    order_payments_dataframe_with_zero_installments,
):
    result = validate_order_payments(
        order_payments_dataframe_with_zero_installments
    )

    assert result["overall_status"] == "WARNING"

    assert (
        result["minimum_value_validation"]["status"]
        == "WARNING"
    )

    assert (
        result["minimum_value_validation"]["details"][
            "payment_installments"
        ]["is_valid"]
        is False
    )

    assert (
        result["minimum_value_validation"]["details"][
            "payment_installments"
        ]["violation_count"]
        == 1
    )


def test_validate_order_payments_with_zero_payment_value(
    order_payments_dataframe_with_zero_payment_value,
):
    result = validate_order_payments(
        order_payments_dataframe_with_zero_payment_value
    )

    assert result["overall_status"] == "WARNING"

    assert (
        result["minimum_value_validation"]["status"]
        == "WARNING"
    )

    assert (
        result["minimum_value_validation"]["details"][
            "payment_value"
        ]["is_valid"]
        is False
    )

    assert (
        result["minimum_value_validation"]["details"][
            "payment_value"
        ]["violation_count"]
        == 1
    )