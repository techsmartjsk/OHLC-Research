import requests
import pandas as pd
import time
from datetime import datetime, timedelta

# Binance API URL
BASE_URL = "https://api.binance.com/api/v3/klines"

# Parameters
symbol = "BTCUSDT"    # Change to your required trading pair
interval = "1h"       # Hourly OHLC data
limit = 1000          # Binance allows max 1000 candles per request
years = 5             # Number of years of data required

# Calculate the start date (5 years ago)
end_time = int(time.time() * 1000)  # Current timestamp in milliseconds
start_time = int((datetime.utcnow() - timedelta(days=years * 365)).timestamp() * 1000)  # 5 years ago

# Function to fetch OHLC data
def get_binance_ohlc(symbol, interval, start_time, end_time, limit):
    url = f"{BASE_URL}?symbol={symbol}&interval={interval}&startTime={start_time}&endTime={end_time}&limit={limit}"
    response = requests.get(url).json()
    
    data = []
    for entry in response:
        data.append([
            int(entry[0]), float(entry[1]), float(entry[2]), float(entry[3]), float(entry[4]), float(entry[5])
        ])
    
    return data

# Fetch data in chunks
all_data = []
while start_time < end_time:
    print(f"Fetching data from {datetime.utcfromtimestamp(start_time / 1000)}...")

    data = get_binance_ohlc(symbol, interval, start_time, end_time, limit)
    
    if not data:
        break  # No more data available

    all_data.extend(data)
    
    # Move start time forward to avoid duplicates
    start_time = data[-1][0] + 1  # Move to the next millisecond after last received candle

    # Binance has rate limits, so avoid getting banned
    time.sleep(1)

# Convert to Pandas DataFrame
df = pd.DataFrame(all_data, columns=["Timestamp", "Open", "High", "Low", "Close", "Volume"])
df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")  # Convert timestamp to datetime

# Save to CSV
csv_filename = f"binance_{symbol}_{interval}_5years.csv"
df.to_csv(csv_filename, index=False)

print(f"✅ Data saved to {csv_filename}")
