import pandas as pd


def calculate_ema(data, period):
    """
    Calculate Exponential Moving Average (EMA)
    """

    ema = data["Close"].ewm(span=period, adjust=False).mean()

    return round(ema.iloc[-1], 2)