import pandas as pd
import numpy as np
import yfinance as yf
import talib
from datetime import datetime
import discord
from discord.ext import tasks

# Function to fetch and process stock data
def fetch_and_process_data(tickers):
    start_date = "2020-01-01"
    end_date = datetime.now().strftime("%Y-%m-%d")

    all_data = []
    for ticker in tickers:
        df = yf.download(ticker, start=start_date, end=end_date)
        df["Ticker"] = ticker
        all_data.append(df)

    df = pd.concat(all_data)
    df.reset_index(inplace=True)

    # Calculate MACD and RSI using TA-Lib
    macd, macd_signal, macd_hist = talib.MACD(
        df["Close"], fastperiod=12, slowperiod=26, signalperiod=9
    )
    df["MACD_line"] = macd
    df["Signal_line"] = macd_signal
    df["Histo_line"] = macd_hist

    rsi = talib.RSI(df["Close"], timeperiod=14)
    df["RSI"] = rsi

    # Calculate RSI_EMA
    rsi_ema_period = 200
    df["RSI_EMA"] = talib.EMA(rsi, timeperiod=rsi_ema_period)
    df["RSI_EMA"] = df["RSI_EMA"].shift(
        1
    )  # Shift by one to match the EMA calculation logic

    # Correct RSI_EMA calculation
    df.loc[rsi_ema_period - 1, "RSI_EMA"] = rsi.mean()  # Set the first EMA value

    alpha = 2 / (rsi_ema_period + 1)
    for i in range(rsi_ema_period, len(df)):
        df.at[df.index[i], "RSI_EMA"] = (
            alpha * df.at[df.index[i], "RSI"]
            + (1 - alpha) * df.at[df.index[i - 1], "RSI_EMA"]
        )

    # Apply offset to RSI_EMA
    offset = 2.6309955317848335
    df["RSI_EMA"] += offset

    # Strategy Logic
    df["Bullish_Run_Start"] = (df["MACD_line"] > df["Signal_line"]) & (
        df["MACD_line"].shift(1) <= df["Signal_line"].shift(1)
    )
    df["RSI_Oversold"] = (
        (df["RSI"] <= df["RSI_EMA"])
        | (df["RSI"].shift(1) <= df["RSI_EMA"].shift(1))
        | (df["RSI"].shift(2) <= df["RSI_EMA"].shift(2))
    )
    df["Buy_Signal"] = df["Bullish_Run_Start"] & df["RSI_Oversold"]

    # Initialize columns for take profit and stop loss
    df["Take_Profit_5"] = np.nan
    df["Take_Profit_10"] = np.nan
    df["Take_Profit_15"] = np.nan
    df["Take_Profit_20"] = np.nan
    df["Stop_Loss"] = np.nan

    # Plot Entry Signals and Calculate Take Profit and Stop Loss Levels
    entry_price = np.nan
    for ticker in tickers:
        for i in range(1, len(df)):
            if df["Buy_Signal"].iloc[i] and df["Ticker"].iloc[i] == ticker:
                entry_price = df["Close"].iloc[i]
                df.at[df.index[i], "Take_Profit_5"] = entry_price * 1.05
                df.at[df.index[i], "Take_Profit_10"] = entry_price * 1.10
                df.at[df.index[i], "Take_Profit_15"] = entry_price * 1.15
                df.at[df.index[i], "Take_Profit_20"] = entry_price * 1.20
                df.at[df.index[i], "Stop_Loss"] = entry_price * 0.90

    # Display a summary of buy signals
    buy_signals = df[df["Buy_Signal"]].copy()
    buy_signals_summary = buy_signals[
        [
            "Date",
            "Ticker",
            "Close",
            "Take_Profit_5",
            "Take_Profit_10",
            "Take_Profit_15",
            "Take_Profit_20",
            "Stop_Loss",
        ]
    ]

    return buy_signals_summary


# Fetch and process data to test the strategy
tickers = ["SPY", "NVDA", "CLH", "FIZZ", "MPWR", "CMG", "ASML", "TSM", "AEHR", "TFII", "GOOG",
        "GOOGL", "ANET", "AXON", "ANF", "IRMD", "SNPS", "CDRE", "SKX", "TSLA", "EXPO",
        "PODD", "INFY", "AMAT", "IBP", "NVMI", "DY", "RMBS", "RPM", "ELF", "APH", "ISRG",
        "VRTX", "CTAS", "MLM", "AAON", "CSWI", "LMB", "PRFT", "CAMT", "ODD", "QCOM", "SYK",
        "LRCX", "LOGI", "TDCX", "WNS", "RL", "TTC", "DECK"]  # Example tickers, you can add more
buy_signals_summary = fetch_and_process_data(tickers)

# Export buy signals to a CSV file
output_file = "buy_signals_summary.csv"
buy_signals_summary.to_csv(output_file, index=False)

print(f"Buy signals summary exported to {output_file}")

# Discord Bot
intents = discord.Intents.default()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}")
    await check_signals.start()


@tasks.loop(hours=1)  # Check every hour
async def check_signals():
    channel_id = 1251391850984636496  # Replace with your channel ID
    channel = client.get_channel(channel_id)
    if not channel:
        print("Channel not found!")
        return

    buy_signals_summary = fetch_and_process_data(tickers)
    for index, row in buy_signals_summary.iterrows():
        await channel.send(
            f"Date: {row['Date']}\n"
            f"Ticker: {row['Ticker']}\n"
            f"Close: {row['Close']}\n"
            f"Take Profit 5%: {row['Take_Profit_5']}\n"
            f"Take Profit 10%: {row['Take_Profit_10']}\n"
            f"Take Profit 15%: {row['Take_Profit_15']}\n"
            f"Take Profit 20%: {row['Take_Profit_20']}\n"
            f"Stop Loss: {row['Stop_Loss']}\n"
            f"----------------------"
        )

# Run the bot with your token
client.run("")
