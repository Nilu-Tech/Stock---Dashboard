import pandas as pd

stocks_df = pd.read_csv("all_stocks.csv")

stocks = dict(
    zip(
        stocks_df["Company"],
        stocks_df["Symbol"]
    )
)