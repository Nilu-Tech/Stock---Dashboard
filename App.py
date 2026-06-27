import pandas as pd
import feedparser
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh
import streamlit as st
import yfinance as yf
from stocks import stocks

# ---------------- PAGE SETTINGS ----------------
st.set_page_config(
    page_title="Indian Stock Dashboard",
    layout="wide"
)

#st_autorefresh(
#    interval=300000,
#    key="refresh"
#)

from datetime import datetime

current_time = datetime.now().strftime("%I:%M %p")

left, right = st.columns([3, 1])

with left:
    st.title("📈 StockVision")
    st.caption("Smart Stock Analysis. Simplified.")

with right:
    st.success("🟢 Market Open")
    st.caption(f"🕒 {current_time}")

st.divider()

# ---------------- STOCK SELECT ----------------
selected_stock = st.selectbox(
    "Select Stock",
    list(stocks.keys())
)

stock = stocks[selected_stock]

# ---------------- DOWNLOAD DATA ----------------
try:
    data = yf.download(
        stock,
        period="5d",
        interval="15m",
        auto_adjust=True
    )

    if data.empty:
        st.error("❌ No data available.")

    else:

        # ---------------- OHLC DATA ----------------
        open_data = data["Open"]
        high_data = data["High"]
        low_data = data["Low"]
        close_data = data["Close"]

        if hasattr(open_data, "columns"):
            open_data = open_data.iloc[:, 0]
            high_data = high_data.iloc[:, 0]
            low_data = low_data.iloc[:, 0]
            close_series = close_data.iloc[:, 0]
        else:
            close_series = close_data

            close_series = close_series.astype(float)

    latest_price = float(close_series.iloc[-1])
    try:
     ticker = yf.Ticker(stock)
     info = ticker.info
    except:
     info={}
    market_cap = info.get("marketCap", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    forward_pe = info.get("forwardPE", "N/A")
    dividend_yield = info.get("dividendYield", "N/A")
    fifty_two_high = info.get("fiftyTwoWeekHigh", "N/A")
    fifty_two_low = info.get("fiftyTwoWeekLow", "N/A")
    sector = info.get("sector", "N/A")
    industry = info.get("industry", "N/A")
    beta = info.get("beta", "N/A")
    book_value = info.get("bookValue", "N/A")

    if market_cap != "N/A":
         market_cap = f"₹{market_cap/10000000:.2f} Cr"

        # ---------------- RSI ----------------
         delta = close_series.diff()

         gain = delta.where(delta > 0, 0)
         loss = -delta.where(delta < 0, 0)

         avg_gain = gain.rolling(14).mean()
         avg_loss = loss.rolling(14).mean()

         rs = avg_gain / avg_loss
         rsi = 100 - (100 / (1 + rs))

        # ---------------- EMA ----------------
         ema20 = close_series.ewm(
            span=20,
            adjust=False
         ).mean()

         ema50 = close_series.ewm(
            span=50,
            adjust=False
         ).mean()

        # ---------------- MACD ----------------
         ema12 = close_series.ewm(
            span=12,
            adjust=False
         ).mean()

         ema26 = close_series.ewm(
            span=26,
            adjust=False
         ).mean()

         macd = ema12 - ema26

         signal_line = macd.ewm(
            span=9,
            adjust=False
         ).mean()

        # ---------------- VOLUME ----------------
         volume_data = data["Volume"]

         if hasattr(volume_data, "columns"):
            volume_series = volume_data.iloc[:, 0]
         else:
            volume_series = volume_data

         avg_volume = volume_series.rolling(20).mean()
         latest_volume = float(volume_series.iloc[-1])

        # ---------------- SUPPORT / RESISTANCE ----------------
         support = float(low_data.tail(20).min())
         resistance = float(high_data.tail(20).max())

        # ---------------- SCORE SYSTEM ----------------
         signal = "HOLD"
         reasons = []
         score = 50

        # RSI
         if rsi.iloc[-1] < 30:
            score += 20
            reasons.append("RSI is Oversold")

         elif rsi.iloc[-1] > 70:
            score -= 20
            reasons.append("RSI is Overbought")

        # EMA
         if ema20.iloc[-1] > ema50.iloc[-1]:
            score += 15
            reasons.append("EMA20 above EMA50")
         else:
            score -= 15
            reasons.append("EMA20 below EMA50")

        # MACD
         if macd.iloc[-1] > signal_line.iloc[-1]:
            score += 15
            reasons.append("MACD Bullish")
         else:
            score -= 15
            reasons.append("MACD Bearish")

        # Volume
         if latest_volume > avg_volume.iloc[-1] * 1.5:
            score += 10
            reasons.append("High Volume")
         else:
            reasons.append("Normal Volume")

        # Support
         if latest_price <= support * 1.02:
            score += 10
            reasons.append("Price Near Support")

        # Resistance
         if latest_price >= resistance * 0.98:
            score -= 10
            reasons.append("Price Near Resistance")

        # Final Signal
         if score >= 75:
            signal = "STRONG BUY"

         elif score >= 60:
            signal = "BUY"

         elif score <= 25:
            signal = "STRONG SELL"

         elif score <= 40:
            signal = "SELL"

         else:
            signal = "HOLD"

        # ---------------- METRICS ----------------
         st.subheader(f"{stock} Live Data")

         c1, c2, c3 = st.columns(3)

         with c1:
            st.metric(
                "Current Price",
                f"₹{latest_price:.2f}"
            )

         with c2:
            st.metric(
                "RSI",
                f"{rsi.iloc[-1]:.2f}"
            )

         with c3:
            st.metric(
                "EMA20",
                f"₹{ema20.iloc[-1]:.2f}"
            )

         c4, c5 = st.columns(2)

         with c4:
            st.metric(
                "Score",
                f"{score}/100"
             )

         with c5:
            st.metric(
                "Volume",
                f"{latest_volume:,.0f}"
            )

        # ---------------- SIGNAL ----------------
         st.subheader("📊 Trading Signal")

         if signal in ["BUY", "STRONG BUY"]:
            st.success(f"🟢 {signal}")

         elif signal in ["SELL", "STRONG SELL"]:
            st.error(f"🔴 {signal}")

         else:
            st.warning(f"🟡 {signal}")

         st.metric(
            "Recommendation",
            signal
         )

         for reason in reasons:
            st.write(f"✅ {reason}")

            analysis = []

         if signal in ["BUY", "STRONG BUY"]:
             analysis.append(
         f"The stock looks bullish with a score of {score}/100."
    )

         elif signal in ["SELL", "STRONG SELL"]:
            analysis.append(
         f"The stock looks weak with a score of {score}/100."
    )

         else:
            analysis.append(
         f"The stock is neutral with a score of {score}/100."
    )

         if latest_price <= support * 1.02:
          analysis.append(
        "The price is trading near support which may act as a buying zone."
    )

    if latest_price >= resistance * 0.98:
     analysis.append(
        "The price is close to resistance where selling pressure may appear."
    )

    if latest_volume > avg_volume.iloc[-1] * 1.5:
     analysis.append(
        "Volume is significantly above average, confirming market participation."
    )

    for line in analysis:
     st.info(line)

    col_a, col_b = st.columns(2)

    with col_a:
            st.info(f"📉 Support: ₹{support:.2f}")

    with col_b:
            st.info(f"📈 Resistance: ₹{resistance:.2f}")

       
        # ---------------- MARKET NEWS ----------------
    st.divider()
    st.subheader("📰 Latest Market News")

    feed = feedparser.parse(
            "https://news.google.com/rss/search?q=Indian+Stock+Market"
        )

    for article in feed.entries[:5]:
            st.markdown(
                f"• [{article.title}]({article.link})"
            )

        
    # ---------------- PORTFOLIO TRACKER ----------------
    st.divider()
    st.subheader("💼 Portfolio Tracker")

    if "portfolio" not in st.session_state:
     st.session_state.portfolio = []

    portfolio_stock = st.selectbox(
    "Select Stock",
    list(stocks.keys()),
    key="portfolio_stock"
)

    quantity = st.number_input(
    "Quantity",
    min_value=1,
    value=1
)

    buy_price = st.number_input(
    "Buy Price (₹)",
    min_value=0.0,
    value=0.0,
    step=0.05
)

    if st.button("➕ Add To Portfolio"):

     st.session_state.portfolio.append(
        {
            "Stock": portfolio_stock,
            "Qty": quantity,
            "Buy Price": buy_price
        }
     )

     st.toast(f"{portfolio_stock} added.")

# ---------------- PORTFOLIO TABLE ----------------
    if st.session_state.portfolio:

     portfolio_rows = []
     total_investment = 0
     total_current = 0

     for position in st.session_state.portfolio:

        symbol = stocks[position["Stock"]]

        try:
            df = yf.download(
                symbol,
                period="1d",
                interval="1m",
                progress=False
            )

            if not df.empty:

                close = df["Close"]

                if hasattr(close, "columns"):
                    close = close.iloc[:, 0]

                current_price = float(
                    close.iloc[-1]
                )

                investment = (
                    position["Qty"]
                    * position["Buy Price"]
                )

                current_value = (
                    position["Qty"]
                    * current_price
                )

                pnl = (
                    current_value
                    - investment
                )

                total_investment += investment
                total_current += current_value

                portfolio_rows.append(
                    {
                        "Stock":
                            position["Stock"],

                        "Qty":
                            position["Qty"],

                        "Buy Price":
                            round(
                                position["Buy Price"],
                                2
                            ),

                        "Current Price":
                            round(
                                current_price,
                                2
                            ),

                        "P&L":
                            round(
                                pnl,
                                2
                            )
                    }
                )

        except:
            pass

     if portfolio_rows:

         portfolio_df = pd.DataFrame(
            portfolio_rows
        )

         st.dataframe(
            portfolio_df,
            use_container_width=True
        )

         total_pnl = (
            total_current
            - total_investment
        )

         c1, c2, c3 = st.columns(3)

         with c1:
            st.metric(
                "Investment",
                f"₹{total_investment:,.2f}"
            )

         with c2:
            st.metric(
                "Current Value",
                f"₹{total_current:,.2f}"
            )

         with c3:
            st.metric(
                "Total P&L",
                f"₹{total_pnl:,.2f}"
            )

         if total_pnl >= 0:
            st.success(
                f"🟢 Overall Profit ₹{total_pnl:,.2f}"
            )
         else:
            st.error(
                f"🔴 Overall Loss ₹{abs(total_pnl):,.2f}"
            )

         if st.button("🗑️ Clear Portfolio"):
            st.session_state.portfolio = []
            st.rerun()

except Exception as e:
    st.error(f"Error: {e}")
