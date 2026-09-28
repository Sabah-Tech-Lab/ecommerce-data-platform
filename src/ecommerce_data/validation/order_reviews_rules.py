REQUIRED_COLUMNS = {
    "review_id",
    "order_id",
    "review_score",
    "review_comment_title",
    "review_comment_message",
    "review_creation_date",
    "review_answer_timestamp",
}

NON_NULL_COLUMNS = [
    "review_id",
    "order_id",
    "review_score",
    "review_creation_date",
    "review_answer_timestamp",
]

COMPOSITE_KEY_COLUMNS = [
    "review_id",
    "order_id",
]

INTEGER_LIKE_COLUMNS = [
    "review_score",
]

VALUE_RANGE_RULES = [
    ("review_score", 1, 5),
]

DATETIME_COLUMNS = [
    "review_creation_date",
    "review_answer_timestamp",
]

TEMPORAL_RULES = [
    (
        "review_creation_date",
        "review_answer_timestamp",
    ),
]