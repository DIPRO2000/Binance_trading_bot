def validate_inputs(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):

    if not symbol or not isinstance(symbol, str):
        raise ValueError("Symbol must be a valid non-empty string (e.g., BTCUSDT).")
        
    if side.upper() not in ["BUY", "SELL"]:
        raise ValueError("Side must be exactly 'BUY' or 'SELL'.")
        
    valid_types = ["MARKET", "LIMIT", "STOP_LIMIT"]
    if order_type.upper() not in valid_types:
        raise ValueError(f"Order type must be one of the following: {valid_types}")
        
    if quantity <= 0:
        raise ValueError("Quantity must be a positive number greater than 0.")

    # Order Type Specific Validations
    if order_type.upper() == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Price is required and must be greater than 0 for LIMIT orders.")
        
    if order_type.upper() == "STOP_LIMIT":
        if price is None or price <= 0:
            raise ValueError("Execution Price (--price) is required and must be greater than 0 for STOP_LIMIT orders.")
        if stop_price is None or stop_price <= 0:
            raise ValueError("Trigger Stop Price (--stop-price) is required and must be greater than 0 for STOP_LIMIT orders.")