import pandas as pd

nse_url = "https://archives.nseindia.com/content/equities/EQUITY_L.csv"

nse = pd.read_csv(nse_url)

nse_df = pd.DataFrame({
    "Company": nse["NAME OF COMPANY"],
    "Symbol": nse["SYMBOL"] + ".NS",
    "Exchange": "NSE"
})

nse_df.to_csv(
    "all_stocks.csv",
    index=False
)

print(f"NSE Stocks Saved: {len(nse_df)}")