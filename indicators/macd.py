import pandas as pd

def calculate_macd(data):
    """
    Calculate MACD, Signal Line and Histogram
    """

    close = data["Close"]

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()

    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    histogram = macd - signal

    return {
        "macd": round(macd.iloc[-1], 2),
        "signal": round(signal.iloc[-1], 2),
        "histogram": round(histogram.iloc[-1], 2)
    }