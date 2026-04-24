import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# 1. பக்கத்தின் அமைப்பு (Page Configuration)
st.set_page_config(
    page_title="Tamil Invest Hub",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. # 2. பிரீமியம் லுக் தரும் டிசைன் (Custom CSS)
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    div[data-testid="stMetricValue"] { font-size: 24px; color: #00ff00; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #2e7d32; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி மற்றும் தேடல் வசதி (Sidebar)
with st.sidebar:
    st.title("⚙️ Settings")
    lang = st.radio("Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்", ["தமிழ்", "English"])
    
    st.divider()
    ticker = st.text_input(
        "Stock Symbol (e.g. RELIANCE.NS / TATAMOTORS.NS)", 
        value="RELIANCE.NS"
    ).upper()
    
    st.info("Note: For Indian stocks, add '.NS' at the end.")

# 4. மொழி பெயர்ப்பு அகராதி (Translations)
t = {
    "தமிழ்": {
        "title": "தமிழ் இன்வெஸ்ட் ஹப்",
        "price": "தற்போதைய விலை",
        "change": "இன்றைய மாற்றம்",
        "mcap": "சந்தை மதிப்பு",
        "chart_title": "விலை வரைபடம் (கடந்த 1 மாதம்)",
        "news": "சமீபத்திய செய்திகள்",
        "error": "தவறான குறியீடு! தயவுசெய்து மீண்டும் சரிபார்க்கவும்.",
        "loading": "தரவு சேகரிக்கப்படுகிறது..."
    },
    "English": {
        "title": "Tamil Invest Hub",
        "price": "Current Price",
        "change": "Day Change",
        "mcap": "Market Cap",
        "chart_title": "Price Chart (Last 1 Month)",
        "news": "Latest News",
        "error": "Invalid Symbol! Please check again.",
        "loading": "Fetching data..."
    }
}[lang]

# 5. ஆப்பின் தலைப்பு
st.title(f"📊 {t['title']}")

# 6. தரவுகளைப் பெறுதல் (Fetching Data)
with st.spinner(t['loading']):
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        hist = stock.history(period="1mo")

        if not hist.empty:
            # அ) சார்ட் - இதுதான் முதலில் இருக்க வேண்டும் (Moneycontrol Style)
            st.subheader(f"📈 {info.get('shortName', ticker)} - {t['chart_title']}")
            
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name='Price'
            )])
            
            fig.update_layout(
                template="plotly_dark",
                xaxis_rangeslider_visible=False,
                height=450,
                margin=dict(l=10, r=10, t=10, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

            # ஆ) முக்கியமான மெட்ரிக்ஸ் (Metrics)
            st.divider()
            col1, col2, col3 = st.columns(3)
            
            curr_price = info.get('currentPrice', hist['Close'].iloc[-1])
            prev_close = info.get('previousClose', hist['Close'].iloc[-2])
            change = ((curr_price - prev_close) / prev_close) * 100
            
            col1.metric(t['price'], f"₹{curr_price:,.2f}")
            col2.metric(t['change'], f"{change:+.2f}%")
            
            mcap = info.get('marketCap', 0)
            if mcap > 10**11:
                mcap_val = f"₹{mcap/10**11:,.2f} Lakh Cr"
            else:
                mcap_val = f"₹{mcap/10**7:,.2f} Cr"
            col3.metric(t['mcap'], mcap_val)

            # இ) செய்திகள் (News)
            st.divider()
            st.subheader(f"📰 {t['news']}")
            news_list = stock.news[:5]
            if news_list:
                for item in news_list:
                    with st.expander(item['title']):
                        st.write(f"Publisher: {item['publisher']}")
                        st.link_button("Read News", item['link'])
            else:
                st.write("No recent news available.")

        else:
            st.error(t['error'])

    except Exception as e:
        st.error(f"{t['error']}")
