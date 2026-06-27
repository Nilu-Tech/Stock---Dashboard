import streamlit as st
from stocks import stocks


st.set_page_config(page_title="Company Insights", page_icon="🏢")

st.title("🏢 COMPANY INSIGHTS")
st.markdown("""
<style>
.info-card{
    background:#1c1f26;
    padding:25px;
    border-radius:18px;
    border:1px solid #2f333d;
    margin-bottom:20px;
    box-shadow:0 4px 12px rgba(0,0,0,0.25);
}
</style>
""", unsafe_allow_html=True)
st.caption("Understand the company beyond stock prices.")
st.divider()
if "selected_stock" not in st.session_state:
    st.warning("Please select a stock from Dashboard.")
    st.stop()

selected_stock = st.session_state["selected_stock"]

stock = stocks[selected_stock]
import yfinance as yf

ticker = yf.Ticker(stock)
news = ticker.news
info = ticker.info

st.success(f"Selected Company: {selected_stock}")
with st.expander("🏢 About Company", expanded=True):
 company_name = (
    info.get("longName")
    or info.get("shortName")
    or selected_stock
 )
 sector = info.get("sector", "N/A")
 industry = info.get("industry", "N/A")
 website = info.get("website", "N/A")
 summary = info.get("longBusinessSummary", "No description available.")

 st.subheader(company_name)

 st.write(f"**🏢 Sector:** {sector}")
 st.write(f"**🏭 Industry:** {industry}")
 st.write(f"**🌐 Website:** {website}")

 preview = summary[:450]

 st.write(preview + "...")

 with st.expander("📖 Read More"):
    st.write(summary)

with st.expander("💼 Business Segments"):

 st.subheader("🏭 Core Business")

 sector = info.get("sector", "N/A")
 industry = info.get("industry", "N/A")

 if sector == "Technology":
    st.markdown("""
 - 💻 Software Development
 - ☁️ Cloud Services
 - 🤖 Artificial Intelligence
 - 🔐 Cybersecurity
 - 📊 IT Consulting
 """)

 elif sector == "Consumer Cyclical":
    st.markdown("""
 - 🚗 Passenger Vehicles
 - 🚛 Commercial Vehicles
 - ⚡ Electric Vehicles (EV)
 - 🌍 International Business (JLR)
 - 🔧 Vehicle Services
 """)

 elif sector == "Financial Services":
    st.markdown("""
 - 💰 Loans
 - 🏦 Deposits
 - 💳 Banking Services
 - 📈 Investments
 - 🛡️ Insurance
 """)

 else:
    st.write(f"Main Industry: **{industry}**")

with st.expander("📰 Latest News"):
 if news:
    for item in news[:3]:

        content = item.get("content", {})

        title = content.get("title", "No Title")

        summary = content.get("summary", "No Summary")

        
        date = content.get("pubDate", "")
        url = content.get("canonicalUrl", {}).get("url", "")

        with st.container(border=True):
            st.subheader(title)
            st.caption(f"📰 {date[:10]}")
            st.write(summary)
            if url: 
                st.link_button("📖 Read Full News", url)

            st.markdown("---")

 else:
    st.warning("No news available.")

with st.expander("📈 News Impact"):
 if news:

    latest = news[0].get("content", {})

    summary = latest.get("summary", "").lower()

    if any(word in summary for word in [
        "growth", "profit", "expansion", "record",
        "strong", "increase", "approval", "launch"
    ]):
        st.success("🟢 Positive Impact")

    elif any(word in summary for word in [
        "loss", "decline", "fall", "weak",
        "drop", "lawsuit", "debt", "warning"
    ]):
        st.error("🔴 Negative Impact")

    else:
        st.info("🟡 Neutral Impact")
    st.subheader("💡 Why It Matters")

 if news:

    latest = news[0].get("content", {})

    summary = latest.get("summary", "").lower()

    if "profit" in summary or "growth" in summary:
        st.write("Higher profits or growth may improve future earnings and investor confidence.")

    elif "launch" in summary or "expansion" in summary:
        st.write("Expansion or new product launches can create future growth opportunities.")

    elif "loss" in summary or "decline" in summary:
        st.write("Weak financial performance may put pressure on the stock price.")

    elif "debt" in summary:
        st.write("Higher debt can increase financial risk for the company.")

    else:
        st.write("Investors should monitor how this development affects the company's future performance.")

with st.expander("⚠️ Risk Factors"):
 if sector == "Technology":
    st.markdown("""
 - ⚠️ High competition in IT industry
 - ⚠️ Dependence on global clients
 - ⚠️ Currency exchange fluctuations
 - ⚠️ Rapid technology changes
 """)

 elif sector == "Consumer Cyclical":
    st.markdown("""
 - ⚠️ Slow vehicle demand
 - ⚠️ Rising raw material costs
 - ⚠️ EV market competition
 - ⚠️ Economic slowdown
 """)

 elif sector == "Financial Services":
    st.markdown("""
 - ⚠️ Bad loans (NPAs)
 - ⚠️ RBI policy changes
 - ⚠️ Interest rate risk
 - ⚠️ Credit risk
 """)

 else:
    st.info("Risk factors will be available soon.")

with st.expander("🚀 Growth Drivers"):
 if sector == "Technology":
    st.markdown("""
 - 🚀 Artificial Intelligence
 - 🚀 Cloud Computing
 - 🚀 Digital Transformation
 - 🚀 Global IT Spending
 """)

 elif sector == "Consumer Cyclical":
    st.markdown("""
 - 🚀 Electric Vehicles
 - 🚀 Export Growth
 - 🚀 Premium Vehicle Demand
 - 🚀 Government EV Policies
 """)

 elif sector == "Financial Services":
    st.markdown("""
 - 🚀 Digital Banking
 - 🚀 Loan Growth
 - 🚀 Financial Inclusion
 - 🚀 Lower NPAs
 """)

 else:
    st.info("Growth drivers will be available soon.")