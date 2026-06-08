import logging
from bot.client import BinanceFuturesClient

def execute_order(symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):

    logging.info(f"Orchestrating logic block for: {order_type} {side} {quantity} {symbol}")
    
    # Initiate the Client Wrapper
    bot_client = BinanceFuturesClient()
    
    result = bot_client.place_futures_order(
        symbol=symbol,
        side=side,
        order_type=order_type,
        quantity=quantity,
        price=price,
        stop_price=stop_price
    )
    
    return result