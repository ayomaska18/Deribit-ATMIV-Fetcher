from scripts.fetchers.utils import deribit
from scripts.fetchers.atm_iv_BTC import fetch_btc_data
from scripts.fetchers.atm_iv_ETH import fetch_eth_data
from scripts.fetchers.atm_iv_SOL import fetch_sol_data
from multiprocessing import Process
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

def main():
    
    btc_fetcher = Process(target=fetch_btc_data)
    eth_fetcher = Process(target=fetch_eth_data)
    sol_fetcher = Process(target=fetch_sol_data)

    btc_fetcher.start()
    eth_fetcher.start()
    sol_fetcher.start()

    btc_fetcher.join()
    eth_fetcher.join()
    sol_fetcher.join()

    
if __name__ == "__main__":
    main()

