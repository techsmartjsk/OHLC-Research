# BTCUSDT Pattern Recognition

This script analyzes historical Binance BTCUSDT 1-hour candlestick data to identify potential buy and sell patterns based on price movements.

## Features
- Extracts candlestick patterns of a specified window size (`CANDLE_WINDOW`).
- Identifies buy and sell patterns based on a predefined price move threshold (`THRESHOLD_MOVE`).
- Filters overlapping patterns using Euclidean distance.
- Saves filtered buy and sell patterns to CSV files.

## Prerequisites
Ensure you have the following dependencies installed:
```bash
pip install numpy pandas scipy
```

## Configuration
Modify the following parameters as needed:
- `CANDLE_WINDOW`: Number of candles to consider for each pattern.
- `THRESHOLD_MOVE`: Minimum price move required to classify a pattern as a buy/sell.
- `DISTANCE_THRESHOLD`: Maximum allowable similarity distance between buy and sell patterns.
- `LOOKAHEAD_CANDLES`: Number of future candles to evaluate price movement.
- `data_folder_path`: Path to the folder containing the Binance BTCUSDT dataset.
- `results_folder_path`: Path where filtered patterns will be saved.

## Usage
1. Place your `binance_BTCUSDT_1h_5years.csv` file inside the specified `data_folder_path`.
2. Run the script:
   ```bash
   python script.py
   ```
3. The filtered buy and sell patterns will be saved as:
   - `buy_patterns_filtered.csv`
   - `sell_patterns_filtered.csv`

## Output
- **Buy Patterns (`buy_patterns_filtered.csv`)**: Contains timestamps and extracted buy patterns.
- **Sell Patterns (`sell_patterns_filtered.csv`)**: Contains timestamps and extracted sell patterns.

## Functionality Breakdown
- **Pattern Extraction**: Collects OHLC (Open, High, Low, Close) values into a structured pattern.
- **Future Price Analysis**: Checks if the future closing price moves significantly to define buy/sell patterns.
- **Overlap Filtering**: Uses Euclidean distance to remove redundant or overlapping patterns.
- **CSV Export**: Saves the final buy and sell patterns for further analysis.
