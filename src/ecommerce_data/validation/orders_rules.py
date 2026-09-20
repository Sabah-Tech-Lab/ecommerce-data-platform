"""Validation rules and configuration for the Olist orders dataset."""
    # ------------------------------------------------------------------
    #                  === Schema rules ===
    # ------------------------------------------------------------------ 

REQUIRED_COLUMNS = {
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
}

NON_NULL_COLUMNS = [
    "order_id",
    "customer_id",
    "order_status",
    "order_purchase_timestamp",
    "order_estimated_delivery_date",
]

UNIQUE_COLUMNS = [
    "order_id",
]

    # ------------------------------------------------------------------
    #                  === Value / type rules ===
    # ------------------------------------------------------------------ 

ALLOWED_ORDER_STATUSES = {
    "delivered",      
    "shipped",        
    "canceled",         
    "unavailable",     
    "invoiced",         
    "processing",     
    "created",           
    "approved",  
}

DATETIME_COLUMNS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]

    # ------------------------------------------------------------------
    #                  === Relationship rules ===
    # ------------------------------------------------------------------ 

TEMPORAL_RULES = [
    ("order_purchase_timestamp", "order_approved_at"),
    ("order_purchase_timestamp","order_delivered_carrier_date"),
    ("order_delivered_carrier_date", "order_delivered_customer_date"),
]

FUNCTIONAL_DEPENDENCIES = [
    ("order_id", "customer_id"),
]

MINIMUM_VALUE_RULES = [
    ("price", 0, False),
    ("freight_value", 0, True),
]

