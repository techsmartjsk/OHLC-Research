import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist
import os

data_folder_path = "/Users/jaskiratsingh/Development/ML Researcher/Data Collection"
results_folder_path = "/Users/jaskiratsingh/Development/ML Researcher/Data Collection"
file_path = os.path.join(data_folder_path, "binance_BTCUSDT_1h_5years.csv")
df = pd.read_csv(file_path, parse_dates=["Timestamp"])

CANDLE_WINDOW = 10 
THRESHOLD_MOVE = 15
DISTANCE_THRESHOLD = 5
LOOKAHEAD_CANDLES = 2

buy_patterns = []
sell_patterns = []

for i in range(len(df) - CANDLE_WINDOW - LOOKAHEAD_CANDLES):
    pattern = df.iloc[i:i + CANDLE_WINDOW][["Open", "High", "Low", "Close"]].values.flatten()
    future_closes = df.iloc[i + CANDLE_WINDOW: i + CANDLE_WINDOW + LOOKAHEAD_CANDLES]["Close"]
    
    current_close = df.iloc[i + CANDLE_WINDOW]["Close"]
    max_future_close = future_closes.max() 
    min_future_close = future_closes.min()

    timestamp = df.iloc[i + CANDLE_WINDOW]["Timestamp"]

    if max_future_close - current_close >= THRESHOLD_MOVE:
        buy_patterns.append((timestamp, pattern))
    elif current_close - min_future_close >= THRESHOLD_MOVE:
        sell_patterns.append((timestamp, pattern))

buy_patterns = np.array(buy_patterns, dtype=object)
sell_patterns = np.array(sell_patterns, dtype=object)

def filter_overlapping_patterns(buy_matrix, sell_matrix, threshold):
    if buy_matrix.shape[0] == 0 or sell_matrix.shape[0] == 0:
        return buy_matrix, sell_matrix

    distances = cdist(np.vstack(buy_matrix[:, 1]), np.vstack(sell_matrix[:, 1]), metric="euclidean")
    
    overlapping_buy_indices = np.any(distances < threshold, axis=1)
    overlapping_sell_indices = np.any(distances < threshold, axis=0)

    buy_matrix_filtered = buy_matrix[~overlapping_buy_indices]
    sell_matrix_filtered = sell_matrix[~overlapping_sell_indices]

    return buy_matrix_filtered, sell_matrix_filtered

buy_matrix_filtered, sell_matrix_filtered = filter_overlapping_patterns(buy_patterns, sell_patterns, DISTANCE_THRESHOLD)

buy_df = pd.DataFrame(buy_matrix_filtered, columns=["Timestamp", "Pattern"])
sell_df = pd.DataFrame(sell_matrix_filtered, columns=["Timestamp", "Pattern"])

buy_file_path  = os.path.join(results_folder_path, "buy_patterns_filtered.csv")
sell_file_path  = os.path.join(results_folder_path, "sell_patterns_filtered.csv")

buy_df.to_csv(buy_file_path, index=False)
sell_df.to_csv(sell_file_path, index=False)
