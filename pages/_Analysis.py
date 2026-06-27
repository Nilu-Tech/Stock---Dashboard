import streamlit as st
import yfinance as yf
from stocks import stocks
from utils.data import get_stock_data
from indicators.rsi import calculate_rsi
from indicators.ema import calculate_ema
from indicators.sma import calculate_sma


st.set_page_config(
    page_title="Analysis",
    page_icon="📊",
    layout="wide"
)

st.title("📊 ANALYSIS")
st.caption("Technical analysis and trading signals.")
st.divider()

# -------------------------
# Selected Stock
# -------------------------

if "selected_stock" not in st.session_state:
    st.warning("Please select a stock from Dashboard.")
    st.stop()

selected_stock = st.session_state["selected_stock"]

stock = stocks[selected_stock]
hist = get_stock_data(stock)

rsi = calculate_rsi(hist)
ema20 = calculate_ema(hist, 20)
ema50 = calculate_ema(hist, 50)
sma50 = calculate_sma(hist, 50)
st.subheader("📊 Technical Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("RSI", rsi)

with col2:
    st.metric("EMA 20", round(ema20, 2))

with col3:
    st.metric("EMA 50", round(ema50, 2))

with col4:
    st.metric("SMA 50", round(sma50, 2))

if hist.empty:
    st.error("No data available.")
    st.stop()