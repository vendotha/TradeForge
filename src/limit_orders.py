from src.client import BinanceClient
from src.logger import logger


def execute_limit_order(symbol, side, quantity, price):
    client = BinanceClient()
    response = client.place_order(symbol, side, "LIMIT", quantity, price)

    if response:
        logger.info(f"Limit Order Success: ID {response.get('orderId')} at ${price}")
        print(f"Limit Order Placed! ID: {response.get('orderId')}")
    else:
        logger.error("Limit Order Failed.")