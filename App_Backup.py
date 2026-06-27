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

st_autorefresh(
    interval=60000,
    key="refresh"
)

st.title("📈 Stock Vision")

st.caption(
    "Smart Stock Analysis. Simplified"
)

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

        col_a, col_b = st.columns(2)

        with col_a:
            st.info(f"📉 Support: ₹{support:.2f}")

        with col_b:
            st.info(f"📈 Resistance: ₹{resistance:.2f}")

        # ---------------- CHART + TABLE ----------------
        left, right = st.columns([2, 1])

        with left:

            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=data.index,
                        open=open_data,
                        high=high_data,
                        low=low_data,
                        close=close_series,
                        name=stock
                    )
                ]
            )

            fig.update_layout(
                title=f"{stock} Candlestick Chart",
                xaxis_title="Time",
                yaxis_title="Price (₹)",
                height=600
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            with right:
               st.subheader("Latest Data")
               st.dataframe(data.tail())

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

        # ---------------- MARKET MOVERS ----------------
        st.divider()
        st.subheader("🔥 Market Movers")

        watchlist = {
            "Reliance": "RELIANCE.NS",
            "TCS": "TCS.NS",
            "Infosys": "INFY.NS",
            "ITC": "ITC.NS",
            "HDFC Bank": "HDFCBANK.NS",
            "ICICI Bank": "ICICIBANK.NS",
            "SBI": "SBIN.NS",
            "Bharti Airtel": "BHARTIARTL.NS",
        }

        movers = []

        for name, symbol in watchlist.items():
            try:
                df = yf.download(
                    symbol,
                    period="2d",
                    interval="1d",
                    progress=False
                )

                if len(df) >= 2:
                    close = df["Close"]

                    if hasattr(close, "columns"):
                        close = close.iloc[:, 0]

                    change = (
                        (close.iloc[-1] - close.iloc[-2])
                        / close.iloc[-2]
                    ) * 100

                    movers.append(
                        {
                            "Stock": name,
                            "Change %": round(change, 2)
                        }
                    )

            except:
                pass

        if movers:
            movers_df = pd.DataFrame(movers)

            gainers = movers_df.sort_values(
                "Change %",
                ascending=False
            ).head(3)

            losers = movers_df.sort_values(
                "Change %",
                ascending=True
            ).head(3)

            col1, col2 = st.columns(2)

            with col1:
                st.success("📈 Top Gainers")
                st.dataframe(gainers)

            with col2:
                st.error("📉 Top Losers")
                st.dataframe(losers)

# ---------------- MARKET NEWS ----------------
                st.subheader("📰 Latest Market News")

                feed = feedparser.parse(
    "https://news.google.com/rss/search?q=Indian+Stock+Market"
)

    for article in feed.entries[:5]:
     st.markdown(
        f"• [{article.title}]({article.link})"
    )
    id="sjf24x"
    st.divider()
    st.subheader("🔥 Market Movers")

    watchlist = {
    "Reliance": "RELIANCE.NS",
    "TCS": "TCS.NS",
    "Infosys": "INFY.NS",
    "ITC": "ITC.NS",
    "HDFC Bank": "HDFCBANK.NS",
    "ICICI Bank": "ICICIBANK.NS",
    "SBI": "SBIN.NS",
    "Bharti Airtel": "BHARTIARTL.NS",
}

    movers = []

    for name, symbol in watchlist.items():
     try:
        df = yf.download(
            symbol,
            period="2d",
            interval="1d",
            progress=False
        )

        if len(df) >= 2:
            close = df["Close"]

            if hasattr(close, "columns"):
                close = close.iloc[:, 0]

            change = (
                (close.iloc[-1] - close.iloc[-2])
                / close.iloc[-2]
            ) * 100

            movers.append(
                {
                    "Stock": name,
                    "Change %": round(change, 2)
                }
            )

     except:
        pass

     if movers:
      movers_df = pd.DataFrame(movers)

    gainers = movers_df.sort_values(
        "Change %",
        ascending=False
    ).head(3)

    losers = movers_df.sort_values(
        "Change %",
        ascending=True
    ).head(3)

    col1, col2 = st.columns(2)

    with col1:
        st.success("📈 Top Gainers")
        st.dataframe(gainers)

    with col2:
        st.error("📉 Top Losers")
        st.dataframe(losers)


except Exception as e:
    st.error(f"Error: {e}")
