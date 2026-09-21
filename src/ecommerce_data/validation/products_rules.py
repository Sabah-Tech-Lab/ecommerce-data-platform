REQUIRED_COLUMNS = {
    "product_id",
    "product_category_name",
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
    "product_weight_g",
    "product_length_cm",
    "product_height_cm",
    "product_width_cm",
}

NON_NULL_COLUMNS = [
    "product_id",
]

UNIQUE_COLUMNS = [
    "product_id",
]

INTEGER_LIKE_COLUMNS = [
    "product_name_lenght",
    "product_description_lenght",
    "product_photos_qty",
]

MINIMUM_VALUE_RULES = [
    ("product_name_lenght", 0, False),
    ("product_description_lenght", 0, False),
    ("product_photos_qty", 0, False),
    ("product_weight_g", 0, False),
    ("product_length_cm", 0, False),
    ("product_height_cm", 0, False),
    ("product_width_cm", 0, False),
]