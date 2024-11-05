import os
import glob
import requests
import pandas as pd

API_BASE_URL = "https://api.binance.us"
ORDER_BLOCK_DIR = "data/orderblocks"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    response.raise_for_status()

def fetch_current_price(symbol):
    endpoint = f"{API_BASE_URL}/api/v3/ticker/price"
    params = {"symbol": symbol}
    response = requests.get(endpoint, params=params)
    response.raise_for_status()
    data = response.json()
    return float(data["price"])

def check_order_block_prices():
    csv_files = glob.glob(os.path.join(ORDER_BLOCK_DIR, "*.csv"))
    triggered_alerts = []

    for file_path in csv_files:
        asset = os.path.basename(file_path).split("_")[0]
        df = pd.read_csv(file_path, parse_dates=["date_time"])

        try:
            current_price = fetch_current_price(asset)
            for _, row in df.iterrows():
                order_block_price = row["price"]
                order_block_type = row["type"]

                if (order_block_type == "bullish" and current_price >= order_block_price) or \
                   (order_block_type == "bearish" and current_price <= order_block_price):
                    message = f"{asset} has reached {order_block_type} order block price at {order_block_price}. Current price: {current_price}"
                    send_telegram_alert(message)
                    triggered_alerts.append(message)
        except Exception as e:
            print(f"Failed to check price for {asset}: {e}")

    if not triggered_alerts:
        print("No order block prices reached in this check.")

if __name__ == "__main__":
    check_order_block_prices()
