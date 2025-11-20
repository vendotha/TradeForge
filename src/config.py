import os
from dotenv import load_dotenv
from src.logger import logger

load_dotenv()

API_KEY = os.getenv("BINANCE_API_KEY")
SECRET_KEY = os.getenv("BINANCE_SECRET_KEY")
BASE_URL = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

if not API_KEY or not SECRET_KEY:
    logger.error("API Keys not found in .env file!")
    exit(1)