import os
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

class BinanceFuturesClient:
    def __init__(self):
        api_key = os.getenv("BINANCE_API_KEY")
        api_secret = os.getenv("BINANCE_API_SECRET")
        
        if not api_key or not api_secret:
            raise ValueError("API Credentials missing. Ensure BINANCE_API_KEY and BINANCE_API_SECRET are set in your .env file.")
        
        self.client = Client(api_key, api_secret, testnet=True)
        self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    def place_futures_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None, stop_price: float = None):

        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),
            "quantity": quantity
        }
        
        # Specific order type for Binance Futures
        if order_type.upper() == "MARKET":
            params["type"] = "MARKET"
            
        elif order_type.upper() == "LIMIT":
            params["type"] = "LIMIT"
            params["price"] = str(price)
            params["timeInForce"] = "GTC"  
            
        elif order_type.upper() == "STOP_LIMIT":
            params["type"] = "STOP"  
            params["price"] = str(price)
            params["stopPrice"] = str(stop_price)
            params["timeInForce"] = "GTC"

        logging.info(f"Sending API request payload: {params}")

        try:
            response = self.client.futures_create_order(**params)
            logging.info(f"API Success Response received: {response}")
            return {"success": True, "data": response}
            
        except BinanceAPIException as e:
            logging.error(f"Binance API Error: Status {e.status_code} - {e.message}")
            return {"success": False, "error": f"API Error ({e.status_code}): {e.message}"}
        except Exception as e:
            logging.error(f"System/Network exception encountered: {str(e)}")
            return {"success": False, "error": f"Network Error: {str(e)}"}