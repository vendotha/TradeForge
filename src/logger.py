import logging
import os


def setup_logger():
    # Ensure log file exists in root directory
    log_file = os.path.join(os.getcwd(), 'bot.log')

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger("BinanceBot")


logger = setup_logger()