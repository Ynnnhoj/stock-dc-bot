stock-dc-bot
=====

This is a Python script that fetches and processes stock data, applies a trading strategy, and sends buy signals to a Discord channel.

**Functionality**

1. The script fetches historical stock data for a list of tickers using the `yfinance` library.
2. It calculates various technical indicators, including MACD, RSI, and EMA, using the `talib` library.
3. The script applies a trading strategy based on the calculated indicators and generates buy signals.
4. The buy signals are exported to a CSV file.
5. The script uses a Discord bot to send the buy signals to a specified channel.

**Configuration**

1. The script uses environment variables to store the Discord token and channel ID. You need to set these variables in a `.env` file.
2. The list of tickers can be modified in the `tickers` variable.
3. The trading strategy can be modified by adjusting the calculations and conditions in the `fetch_and_process_data` function.

**Running the Script**

1. Install the required libraries by running `pip install -r requirements.txt`.
2. Install `talib`, check https://github.com/TA-Lib/ta-lib-python.git 
3. Set the environment variables in a `.env` file.
4. Run the script using `python script.py`.

**Note**

This script is for educational purposes only and should not be used for actual trading decisions without further testing and validation.
