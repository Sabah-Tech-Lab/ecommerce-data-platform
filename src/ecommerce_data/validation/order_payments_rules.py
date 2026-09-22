REQUIRED_COLUMNS = {
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value",
}

NON_NULL_COLUMNS = [
    "order_id",
    "payment_sequential",
    "payment_type",
    "payment_installments",
    "payment_value",
]

COMPOSITE_KEY_COLUMNS = [
    "order_id",
    "payment_sequential",
]

ALLOWED_PAYMENT_TYPES = {
    "credit_card",
    "boleto",
    "voucher",
    "debit_card",
    "not_defined",
}

MINIMUM_VALUE_RULES = [
    ("payment_installments", 0, False),
    ("payment_value", 0, False),
]