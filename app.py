import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உலகத்தரம் வாய்ந்த CSS (Modern Premium UI)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ 
        font-size: 15px !important; 
        background-color: #0d1117; 
        color: #ffffff; 
        font-family: 'Inter', sans-serif;
    }}
    
    /* பிரீமியம் டிக்கர் */
    .ticker-wrap {{ 
        width: 100%; overflow: hidden; background: rgba(22, 27, 34, 0.8); 
        border-bottom: 1px solid rgba(57, 255, 20, 0.3); 
        padding: 10px 0; position: sticky; top: 0; z-index: 999;
        backdrop-filter: blur(10px);
    }}
    .ticker-move {{ display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 13px; font-weight: 600; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    /* WORLD CLASS HEADER DESIGN */
    .header-container {{ 
        text-align: center; 
        padding: 30px 0; 
        background: radial-gradient(circle at center, rgba(57, 255, 20, 0.05) 0%, transparent 70%);
    }}
    .main-title {{ 
        font-size: 48px !important; 
        font-weight: 900; 
        margin-bottom: 0px;
        letter-spacing: -1.5px;
        background: linear-gradient(135deg, #39FF14 0%, #00D1FF 50%, #FF3131 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0px 4px 10px rgba(0, 0, 0, 0.5));
    }}
    .sub-title {{ 
        font-size: 11px !important; 
        color: #8b949e; 
        text-transform: lowercase; 
        letter-spacing: 2px;
        margin-top: 5px;
        font-weight: 400;
        opacity: 0.7;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.5);
    }}
    
    /* மார்டன் மெட்ரிக் கார்டுகள் */
    .metric-row {{ 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 12px; 
        padding: 18px; 
        margin-bottom: 12px; 
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: 0.3s ease;
    }}
    .metric-row:hover {{ transform: translateY(-2px); border-color: #39FF14; }}
    .m-label {{ color: #8b949e !important; font-size: 10px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }}
    .m-value {{ color: #ffffff !important; font-size: 18px; font-weight: 800; }}
    </style>
    """, unsafe_allow_html=True)

# 3. லைவ் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#39FF14" if c >= 0 else "#FF3131"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# 4. பிரீமியம் ஹெடர் டிஸ்ப்ளே
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச் மற்றும் டேப்கள்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# டேட்டா லோடிங்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    with tabs[0]:
        st.markdown(f"### {info.get('longName', u_input)}")
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W LOW</span><br><span class="m-value">₹{info.get("fiftyTwoWeekLow", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W HIGH</span><br><span class="m-value">₹{info.get("fiftyTwoWeekHigh", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E RATIO</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=450, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # மற்ற டேப்கள் பழைய கோடில் உள்ளது போலவே தொடரும்...
    # (சுருக்கத்திற்காக மற்ற டேப்கள் இங்கே சேர்க்கப்படவில்லை, ஆனால் அவை உங்கள் பழைய கோடில் இயங்கும்)

else:
    st.info("சரியான பங்கு குறியீட்டை உள்ளிடவும். (எ.கா: TCS, RELIANCE)")

st.markdown("<p style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
