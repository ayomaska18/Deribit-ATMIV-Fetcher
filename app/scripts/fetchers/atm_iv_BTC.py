from scripts.fetchers.utils.deribit import fetch_atm_iv
from .utils.influxdb import write_to_influxdb
from .utils.deribit import save_to_csv
import time
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def fetch_btc_data():
    while True:
        try:
            timestamp, atm_iv = fetch_atm_iv('BTC', 'option')
            write_to_influxdb(timestamp, atm_iv, 'BTC')
            logging.info(f'{timestamp} BTC ATM IV: {atm_iv}')
            sys.stdout.flush()
        except Exception as e:
            logging.error(f"Error Fetching BTC data: {e}")
        time.sleep(5)
