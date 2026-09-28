import pandas as pd
import pytest

from ecommerce_data.validation.order_reviews_validator import (
    validate_order_reviews,
)


# ------------------------------------------------------------------
# Fixtures for validate_order_reviews().
# ------------------------------------------------------------------


@pytest.fixture
def valid_order_reviews_dataframe():
    return pd.DataFrame(
        {
            "review_id": [
                "review_1",
                "review_2",
                "review_3",
            ],
            "order_id": [
                "order_1",
                "order_2",
                "order_3",
            ],
            "review_score": [
                5,
                4,
                3,
            ],
            "review_comment_title": [
                "Great",
                None,
                "Good",
            ],
            "review_comment_message": [
                "Very good product",
                None,
                "Everything was fine",
            ],
            "review_creation_date": [
                "2018-01-10 00:00:00",
                "2018-01-11 00:00:00",
                "2018-01-12 00:00:00",
            ],
            "review_answer_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-12 08:00:00",
                "2018-01-13 09:00:00",
            ],
        }
    )


@pytest.fixture
def order_reviews_dataframe_with_composite_key_violation():
    return pd.DataFrame(
        {
            "review_id": [
                "review_1",
                "review_1",
            ],
            "order_id": [
                "order_1",
                "order_1",
            ],
            "review_score": [
                5,
                4,
            ],
            "review_comment_title": [
                None,
                None,
            ],
            "review_comment_message": [
                None,
                None,
            ],
            "review_creation_date": [
                "2018-01-10 00:00:00",
                "2018-01-11 00:00:00",
            ],
            "review_answer_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-11 12:00:00",
            ],
        }
    )


@pytest.fixture
def order_reviews_dataframe_with_fractional_score():
    return pd.DataFrame(
        {
            "review_id": [
                "review_1",
                "review_2",
            ],
            "order_id": [
                "order_1",
                "order_2",
            ],
            "review_score": [
                5.0,
                3.5,
            ],
            "review_comment_title": [
                None,
                None,
            ],
            "review_comment_message": [
                None,
                None,
            ],
            "review_creation_date": [
                "2018-01-10 00:00:00",
                "2018-01-11 00:00:00",
            ],
            "review_answer_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-11 12:00:00",
            ],
        }
    )


@pytest.fixture
def order_reviews_dataframe_with_out_of_range_score():
    return pd.DataFrame(
        {
            "review_id": [
                "review_1",
                "review_2",
            ],
            "order_id": [
                "order_1",
                "order_2",
            ],
            "review_score": [
                5,
                6,
            ],
            "review_comment_title": [
                None,
                None,
            ],
            "review_comment_message": [
                None,
                None,
            ],
            "review_creation_date": [
                "2018-01-10 00:00:00",
                "2018-01-11 00:00:00",
            ],
            "review_answer_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-11 12:00:00",
            ],
        }
    )


@pytest.fixture
def order_reviews_dataframe_with_invalid_datetime():
    return pd.DataFrame(
        {
            "review_id": [
                "review_1",
                "review_2",
            ],
            "order_id": [
                "order_1",
                "order_2",
            ],
            "review_score": [
                5,
                4,
            ],
            "review_comment_title": [
                None,
                None,
            ],
            "review_comment_message": [
                None,
                None,
            ],
            "review_creation_date": [
                "2018-01-10 00:00:00",
                "not-a-date",
            ],
            "review_answer_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-11 12:00:00",
            ],
        }
    )


@pytest.fixture
def order_reviews_dataframe_with_temporal_violation():
    return pd.DataFrame(
        {
            "review_id": [
                "review_1",
                "review_2",
            ],
            "order_id": [
                "order_1",
                "order_2",
            ],
            "review_score": [
                5,
                4,
            ],
            "review_comment_title": [
                None,
                None,
            ],
            "review_comment_message": [
                None,
                None,
            ],
            "review_creation_date": [
                "2018-01-10 12:00:00",
                "2018-01-11 14:00:00",
            ],
            "review_answer_timestamp": [
                "2018-01-10 10:00:00",
                "2018-01-11 15:00:00",
            ],
        }
    )


# ------------------------------------------------------------------
# Tests for validate_order_reviews().
# ------------------------------------------------------------------


def test_validate_order_reviews_with_valid_data(
    valid_order_reviews_dataframe,
):
    result = validate_order_reviews(
        valid_order_reviews_dataframe
    )

    assert result["overall_status"] == "PASS"
    assert result["dataframe_not_empty"]["status"] == "PASS"
    assert result["required_columns"]["status"] == "PASS"
    assert result["non_null_columns"]["status"] == "PASS"
    assert result["composite_key"]["status"] == "PASS"
    assert result["datetime_parseability"]["status"] == "PASS"
    assert result["datetime_order"]["status"] == "PASS"
    assert result["integer_like_columns"]["status"] == "PASS"
    assert result["value_range"]["status"] == "PASS"


def test_validate_order_reviews_with_composite_key_violation(
    order_reviews_dataframe_with_composite_key_violation,
):
    result = validate_order_reviews(
        order_reviews_dataframe_with_composite_key_violation
    )

    assert result["overall_status"] == "FAIL"
    assert result["composite_key"]["status"] == "FAIL"
    assert result["composite_key"]["details"]["is_valid"] is False
    assert result["composite_key"]["details"]["violation_count"] == 1


def test_validate_order_reviews_with_fractional_score(
    order_reviews_dataframe_with_fractional_score,
):
    result = validate_order_reviews(
        order_reviews_dataframe_with_fractional_score
    )

    assert result["overall_status"] == "FAIL"
    assert result["integer_like_columns"]["status"] == "FAIL"

    assert (
        result["integer_like_columns"]["details"]["review_score"][
            "is_valid"
        ]
        is False
    )

    assert (
        result["integer_like_columns"]["details"]["review_score"][
            "violation_count"
        ]
        == 1
    )


def test_validate_order_reviews_with_out_of_range_score(
    order_reviews_dataframe_with_out_of_range_score,
):
    result = validate_order_reviews(
        order_reviews_dataframe_with_out_of_range_score
    )

    assert result["overall_status"] == "FAIL"
    assert result["value_range"]["status"] == "FAIL"

    assert (
        result["value_range"]["details"]["review_score"]["is_valid"]
        is False
    )

    assert (
        result["value_range"]["details"]["review_score"][
            "violation_count"
        ]
        == 1
    )


def test_validate_order_reviews_with_invalid_datetime(
    order_reviews_dataframe_with_invalid_datetime,
):
    result = validate_order_reviews(
        order_reviews_dataframe_with_invalid_datetime
    )

    assert result["overall_status"] == "FAIL"
    assert result["datetime_parseability"]["status"] == "FAIL"

    assert (
        result["datetime_parseability"]["details"][
            "invalid_datetime_counts"
        ]["review_creation_date"]
        == 1
    )


def test_validate_order_reviews_with_temporal_violation(
    order_reviews_dataframe_with_temporal_violation,
):
    result = validate_order_reviews(
        order_reviews_dataframe_with_temporal_violation
    )

    assert result["overall_status"] == "WARNING"
    assert result["datetime_order"]["status"] == "WARNING"

    assert (
        result["datetime_order"]["details"][
            "review_creation_date_to_review_answer_timestamp"
        ]["is_valid"]
        is False
    )

    assert (
        result["datetime_order"]["details"][
            "review_creation_date_to_review_answer_timestamp"
        ]["violation_count"]
        == 1
    )