"""Validation rules and configuration for the Olist order items dataset."""
    # ------------------------------------------------------------------
    #                  === Schema rules ===
    # ------------------------------------------------------------------ 

REQUIRED_COLUMNS = {
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "shipping_limit_date",
    "price",
    "freight_value",
}

NON_NULL_COLUMNS = [
    "order_id",
    "order_item_id",
    "product_id",
    "seller_id",
    "shipping_limit_date",
    "price",
    "freight_value",
]

COMPOSITE_KEY_COLUMNS = [
    "order_id", 
    "order_item_id",
]

    # ------------------------------------------------------------------
    #                  === Value / type rules ===
    # ------------------------------------------------------------------ 

DATETIME_COLUMNS = [
    "shipping_limit_date",
]  

MINIMUM_VALUE_RULES = [
    ("price", 0, False),
    ("freight_value", 0, True),
]

