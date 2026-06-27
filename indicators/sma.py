import pandas as pd


def calculate_sma(data, period):
    """
    Calculate Simple Moving Average (SMA)
    """

    sma = data["Close"].rolling(window=period).mean()

    return round(sma.iloc[-1], 2)