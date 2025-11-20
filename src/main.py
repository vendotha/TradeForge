import argparse
import sys
import os

# Ensure src is in path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.market_orders import execute_market_order
from src.limit_orders import execute_limit_order
from src.advanced.twap import execute_twap_order
from src.logger import logger

def main():
    parser = argparse.ArgumentParser(description="Binance Futures CLI Bot")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Market Order Command
    # Usage: python src/main.py market BTCUSDT BUY 0.001
    market_parser = subparsers.add_parser("market", help="Place Market Order")
    market_parser.add_argument("symbol", type=str, help="Trading Pair (e.g., BTCUSDT)")
    market_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Side")
    market_parser.add_argument("quantity", type=float, help="Quantity")

    # Limit Order Command
    # Usage: python src/main.py limit BTCUSDT BUY 0.001 50000
    limit_parser = subparsers.add_parser("limit", help="Place Limit Order")
    limit_parser.add_argument("symbol", type=str, help="Trading Pair")
    limit_parser.add_argument("side", type=str, choices=["BUY", "SELL"], help="Side")
    limit_parser.add_argument("quantity", type=float, help="Quantity")
    limit_parser.add_argument("price", type=float, help="Limit Price")

    # TWAP Command (Bonus)
    # Usage: python src/main.py twap BTCUSDT BUY 0.005 1 5
    twap_parser = subparsers.add_parser("twap", help="Execute TWAP Strategy")
    twap_parser.add_argument("symbol", type=str)
    twap_parser.add_argument("side", type=str)
    twap_parser.add_argument("quantity", type=float, help="Total Quantity")
    twap_parser.add_argument("duration", type=int, help="Duration in minutes")
    twap_parser.add_argument("slices", type=int, help="Number of orders")

    args = parser.parse_args()

    if args.command == "market":
        execute_market_order(args.symbol, args.side, args.quantity)
    elif args.command == "limit":
        execute_limit_order(args.symbol, args.side, args.quantity, args.price)
    elif args.command == "twap":
        execute_twap_order(args.symbol, args.side, args.quantity, args.duration, args.slices)
    else:
        parser.print_help()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user.")