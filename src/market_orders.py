from src.client import BinanceClient
from src.logger import logger


def execute_market_order(symbol, side, quantity):
    client = BinanceClient()
    response = client.place_order(symbol, side, "MARKET", quantity)

    if response:
        logger.info(f"Market Order Success: ID {response.get('orderId')}")
        print(f"Order Placed! ID: {response.get('orderId')}")
    else:
        logger.error("Market Order Failed.")