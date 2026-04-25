import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. பக்க அமைப்பு
st.set_page_config(page_title="Tamil Invest Hub Pro", layout="wide")

# 2. ராயல் டிசைன் (CSS)
st.markdown("""
    <style>
    html, body, [class*="css"] { background-color: #050a0f; color: #e0e0e0; }
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 24px; font-weight: 800; text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<p class="royal-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 3. ஸ்மார்ட் டிக்கர் உள்ளீடு (Smart Ticker Input)
raw_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, Sun Pharma)", value="RELIANCE")

# --- தட்டச்சு பிழைகளைச் சரிசெய்யும் மேஜிக் (Logic) ---
ticker = raw_input.strip().replace(" ", "").upper()
if ticker and not (ticker.endswith(".NS") or ticker.endswith(".BO")):
    ticker = f"{ticker}.NS" 
# -----------------------------------------------

try:
    if ticker:
        stock = yf.Ticker(ticker)
        # டேட்டா இருக்கிறதா என்று சோதிக்க ஒரு சிறிய கால்
        hist = stock.history(period="1d")
        
        if hist.empty:
            st.error(f"'{ticker}' பற்றிய தகவல்கள் இல்லை. சரியான குறியீட்டை (eg: SUNPHARMA.NS) உள்ளிடவும்.")
        else:
            info = stock.info
            st.success(f"✅ {info.get('longName', ticker)} - தரவுகள் தயார்!")
            
            # மெட்ரிக்ஸ் மற்றும் சார்ட் இங்கே வரும் (முந்தைய கோடிங்கைத் தொடரவும்)
            curr_p = info.get('currentPrice', hist['Close'].iloc[-1])
            st.metric("தற்போதைய விலை", f"₹{curr_p:,.2f}")
            
            # கேண்டில் ஸ்டிக் சார்ட்
            full_hist = stock.history(period="1mo")
            fig = go.Figure(data=[go.Candlestick(x=full_hist.index, open=full_hist['Open'], high=full_hist['High'], low=full_hist['Low'], close=full_hist['Close'])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350)
            st.plotly_chart(fig, use_container_width=True)

except Exception as e:
    st.warning("தேடப்படும் பங்கின் பெயரைச் சரியாக உள்ளிடவும் (உதாரணம்: TATASTEEL அல்லது TCS)")
