from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import os
import logging
import sys
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

INFLUXDB_URL = os.getenv("INFLUXDB_URL")
INFLUXDB_TOKEN = os.getenv("INFLUXDB_ADMIN_TOKEN")
INFLUXDB_ORG = os.getenv("INFLUXDB_ORG")                  
INFLUXDB_BUCKET = os.getenv("INFLUXDB_BUCKET")     


def write_to_influxdb(timestamp: str, atm_iv: float, currency: str):
    with InfluxDBClient(url=INFLUXDB_URL, token=INFLUXDB_TOKEN, org=INFLUXDB_ORG) as client:
        

        write_api = client.write_api(write_options=SYNCHRONOUS)
        
        point = (
            Point("atm_iv")
            .tag("currency", currency)
            .field("value", atm_iv)
            .time(timestamp)
        )
        
        write_api.write(bucket=INFLUXDB_BUCKET, org=INFLUXDB_ORG, record=point)
