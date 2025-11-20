import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from src.config import API_KEY, SECRET_KEY, BASE_URL
from src.logger import logger


class BinanceClient:
    def __init__(self):
        self.headers = {
            'X-MBX-APIKEY': API_KEY
        }

    def _get_signature(self, params):
        query_string = urlencode(params)
        return hmac.new(
            SECRET_KEY.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def send_signed_request(self, method, endpoint, params=None):
        if params is None:
            params = {}

        # Add timestamp (mandatory for Binance)
        params['timestamp'] = int(time.time() * 1000)
        params['signature'] = self._get_signature(params)

        url = f"{BASE_URL}{endpoint}"

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers, params=params)
            else:
                response = requests.post(url, headers=self.headers, params=params)

            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            return None
        except Exception as e:
            logger.error(f"Request Failed: {str(e)}")
            return None

    def place_order(self, symbol, side, order_type, quantity, price=None):
        params = {
            'symbol': symbol.upper(),
            'side': side.upper(),
            'type': order_type.upper(),
            'quantity': quantity
        }

        if price:
            params['price'] = price
            params['timeInForce'] = 'GTC'  # Good Till Cancel

        logger.info(f"Sending {order_type} order: {side} {quantity} {symbol}")
        return self.send_signed_request("POST", "/fapi/v1/order", params)