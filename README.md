Discord Stock Alert Bot

This project is a Stock Trading Bot that fetches and processes stock data, calculates trading signals, and sends notifications to a Discord channel. It uses various Python libraries to achieve this, including yfinance for stock data, TA-Lib for technical analysis, pandas for data manipulation, and discord.py for Discord bot functionality.
Features

  - Fetch and Process Stock Data: Retrieve historical stock data for a list of tickers.
  - Technical Indicators Calculation: Calculate MACD and RSI indicators, along with an EMA of RSI.
  - Trading Signals: Identify buy signals based on the calculated indicators.
  - Notification: Send the trading signals to a specified Discord channel.
  - Automation: Automatically check and send trading signals every 6 hours.

Requirements

  - Python 3.7 or higher
  - A Discord bot token
  - A Discord channel ID
  - .env file with the following environment variables:
    - DISCORD_TOKEN: Your Discord bot token.
    - CHANNEL_ID: The ID of the Discord channel where notifications will be sent.
