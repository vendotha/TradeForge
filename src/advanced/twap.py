import time
from src.client import BinanceClient
from src.logger import logger


def execute_twap_order(symbol, side, total_quantity, duration_minutes, slices):
    """
    Splits a total quantity into 'slices' and executes them over 'duration_minutes'.
    """
    client = BinanceClient()

    qty_per_slice = round(float(total_quantity) / int(slices), 3)
    delay_seconds = (int(duration_minutes) * 60) / int(slices)

    logger.info(f"Starting TWAP: {total_quantity} {symbol} over {duration_minutes}m in {slices} slices.")
    print(f"TWAP Strategy: Buying {qty_per_slice} every {delay_seconds} seconds.")

    for i in range(int(slices)):
        logger.info(f"Executing TWAP Slice {i + 1}/{slices}")
        response = client.place_order(symbol, side, "MARKET", qty_per_slice)

        if response:
            print(f"Slice {i + 1} Executed: {qty_per_slice} {symbol}")

        if i < int(slices) - 1:
            time.sleep(delay_seconds)

    logger.info("TWAP Strategy Completed.")