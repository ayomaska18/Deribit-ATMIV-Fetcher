import requests
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
import csv
from .influxdb import write_to_influxdb


base_url = 'https://deribit.com/api/v2/public'


# get current index_price of the asset
def get_index_price(index_name: str):
    if index_name == 'SOL':
        index_name = 'sol_usd'
    elif index_name == 'ETH':
        index_name = 'eth_usd'
    else:
        index_name = 'btc_usd'

    endpoint = '/get_index_price'
    url = base_url + endpoint
    params = {
        'index_name': index_name
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        index_price = response_data['result']['index_price']
        return index_price
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None
    
# get the order book of the specifized instrument
def get_order_book(instrument_name: str, depth: int):
    endpoint = '/get_order_book'
    url = base_url + endpoint
    params = {
        'instrument_name': instrument_name,
        'depth': depth

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None

# get the list of instruments
def get_instruments(currency: str, kind: str, expired: str = 'false'):
    if currency == 'SOL':
        currency = 'any'
    endpoint = '/get_instruments'
    url = base_url + endpoint
    params = {
        'currency': currency,
        'kind': kind,
        'expired': expired

    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        response_data = response.json()
        return response_data
    else:
        print(f"Failed to retrieve data: {response.status_code} {response.text}")
        return None

# get all instruments that expire tomorrow
def get_expiring_options(data: dict, currency: str):
    instruments = data['result']
    now = datetime.datetime.now(datetime.timezone.utc)
    today = datetime.datetime(now.year, now.month, now.day, tzinfo=datetime.timezone.utc)
    today_8_utc = datetime.datetime(now.year, now.month, now.day, 8, 0, tzinfo=datetime.timezone.utc)
    tomorrow = today_8_utc + datetime.timedelta(days=1)

    expiring_options = []

    if currency == 'SOL': # for SOL
        for instrument in instruments:
            expiration_timestamp = instrument['expiration_timestamp']

            # Before today's expiration (8:00 AM UTC)
            if today <= now <= today_8_utc:
                if expiration_timestamp == int(today_8_utc.timestamp() * 1000) and instrument['base_currency'] == 'SOL':  # Matches today's expiration timestamp
                    expiring_options.append(instrument)

            # After today's expiration (8:00 AM UTC)
            else:
                if expiration_timestamp == int(tomorrow.timestamp() * 1000) and instrument['base_currency'] == 'SOL':  # Matches tomorrow's expiration timestamp
                    expiring_options.append(instrument)
            expiration_timestamp = instrument['expiration_timestamp']
    else: 
        # Before today's expiration (8:00 AM UTC)
        for instrument in instruments:
            expiration_timestamp = instrument['expiration_timestamp']
            if today <= now <= today_8_utc:
                if expiration_timestamp == int(today_8_utc.timestamp() * 1000):  # Matches today's expiration timestamp
                    expiring_options.append(instrument)

            # After today's expiration (8:00 AM UTC)
            else:
                if expiration_timestamp == int(tomorrow.timestamp() * 1000):  # Matches tomorrow's expiration timestamp
                    expiring_options.append(instrument)
    
    return expiring_options


# get the atm option 
def get_atm_option_iv(instrument_list: list, current_price: int):
    atm_option = min(instrument_list, key=lambda x: abs(x['strike'] - current_price))
    return atm_option

def save_to_csv(timestamp: datetime, atm_iv: int, file_name: str):
    with open(file_name, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, atm_iv])

def fetch_atm_iv(currency: str, kind: str):
        instruments = get_instruments(currency, kind)

        data = get_expiring_options(instruments, currency)

        current_price = get_index_price(currency)
            
        atm_option = get_atm_option_iv(data, current_price)

        atm_instrument_name = atm_option['instrument_name']

        atm_order_book = get_order_book(atm_instrument_name,1)
            
        atm_iv = atm_order_book['result']['mark_iv']

        timestamp = datetime.datetime.now().isoformat()

        return timestamp, atm_iv


       

