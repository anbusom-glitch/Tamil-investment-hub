import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="Tamil Invest Hub", layout="wide")

# Custom CSS for Mobile Look
st.markdown("""
    <style>
    .main { background-color: #121212; color: white; }
    .stMetric { background-color: #1e1e1e; padding: 10px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# Title
st.title("📊 Tamil Invest Hub")

# Sidebar for Language & Search
with st.sidebar:
    lang = st.radio("Language / மொழி", ["English", "தமிழ்"])
    ticker = st.text_input("Enter Stock Symbol (e.g. RELIANCE.NS)", "RELIANCE.NS")

t = {
    "English": {"price": "Current Price", "chart": "Price Chart", "news": "Latest News"},
    "தமிழ்": {"price": "தற்போதைய விலை", "chart": "விலை வரைபடம்", "news": "சமீபத்திய செய்திகள்"}
}[lang]

# Fetch Data
data = yf.Ticker(ticker)
hist = data.history(period="1mo")
info = data.info

if not hist.empty:
    # 1. CHART AT THE TOP (Moneycontrol Style)
    st.subheader(f"{ticker} - {t['chart']}")
    fig = go.Figure(data=[go.Candlestick(x=hist.index,
                open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'])])
    fig.update_layout(theme_override="plotly_dark", height=400, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig, use_container_width=True)

    # 2. METRICS BELOW CHART
    col1, col2, col3 = st.columns(3)
    col1.metric(t['price'], f"₹{info.get('currentPrice', 'N/A')}")
    col2.metric("Day Change", f"{round(info.get('regularMarketChangePercent', 0), 2)}%")
    col3.metric("Dividend Yield", f"{info.get('dividendYield', 0)*100}%" if info.get('dividendYield') else "0%")

    # 3. NEWS SECTION
    st.divider()
    st.subheader(t['news'])
    for news in data.news[:5]:
        st.write(f"🔗 [{news['title']}]({news['link']})")
else:
    st.error("Invalid Ticker or No Data Found!")
