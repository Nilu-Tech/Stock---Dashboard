import yfinance as yf


def get_stock_data(symbol, period="6mo"):
    """
    Fetch historical stock data from Yahoo Finance.
    """

    ticker = yf.Ticker(symbol)

    hist = ticker.history(period=period)

    return hist