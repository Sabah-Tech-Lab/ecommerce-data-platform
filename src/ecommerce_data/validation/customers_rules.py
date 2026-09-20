"""Validation rules and configuration for the Olist customers dataset."""
    # ------------------------------------------------------------------
    #                  === Schema rules ===
    # ------------------------------------------------------------------

REQUIRED_COLUMNS = {
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",
}   

NON_NULL_COLUMNS = [
    "customer_id",
    "customer_unique_id",
    "customer_zip_code_prefix",
    "customer_city",
    "customer_state",    
]

UNIQUE_COLUMNS = [
    "customer_id",
]

    # ------------------------------------------------------------------
    #                  === Value / type rules ===
    # ------------------------------------------------------------------ 

ALLOWED_CUSTOMER_STATES = {
    "AC", "AL", "AM", "AP", 
    "BA", "CE", "DF", "ES", 
    "GO", "MA", "MG", "MS", 
    "MT", "PA", "PB", "PE", 
    "PI", "PR", "RJ", "RN", 
    "RO", "RR", "RS", "SC", 
    "SE", "SP", "TO", 
}    

    # ------------------------------------------------------------------
    #                  === Relationship rules ===
    # ------------------------------------------------------------------ 

FUNCTIONAL_DEPENDENCIES = [
    ("customer_zip_code_prefix", "customer_state"),
]    