import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
import pandas_ta as ta

# 1. பக்க அமைப்பு (Page Configuration)
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# Session State மேலாண்மை
if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = ["RELIANCE", "TCS", "HDFCBANK"]
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. LUXURY DARK UI STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        background-color: #050505 !important; 
        color: #e0e0e0; 
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Live Ticker Styling */
    .ticker-wrapper {
        background: #0d1117; color: #39FF14; padding: 12px 0;
        overflow: hidden; white-space: nowrap; border-bottom: 1px solid #21262d;
    }
    .ticker-content {
        display: inline-block; animation: ticker 40s linear infinite; font-weight: bold; font-size: 14px;
    }
    @keyframes ticker {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }
    .ticker-item { margin-right: 50px; display: inline-block; }

    /* Main Title */
    .main-title { 
        font-size: 42px !important; font-weight: 900; text-align: center; margin-top: 20px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 10px; color: #555; text-align: center; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 30px; }

    /* Metric & Watchlist Cards */
    .custom-card { 
        background: #0d1117; border: 1px solid #21262d; border-radius: 16px; 
        padding: 20px; margin-bottom: 12px; transition: 0.3s;
    }
    .custom-card:hover { border-color: #39FF14; background: #111; }
    
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 18px; font-weight: 800; display: block; }
    
    /* Input Fields */
    .stTextInput input { background-color: #0d1117 !important; border: 1px solid #21262d !important; color: white !important; border-radius: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. LIVE TICKER (Top Bar)
def render_ticker():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS", "SBI.NS"]
    ticker_html = '<div class="ticker-wrapper"><div class="ticker-content">'
    for s in indices:
        try:
            t = yf.Ticker(s)
            price = t.info.get('currentPrice') or t.info.get('regularMarketPrice')
            change = t.info.get('regularMarketChangePercent', 0)
            color = "#39FF14" if change >= 0 else "#FF3131"
            symbol_name = s.replace(".NS", "").replace("^", "")
            ticker_html += f'<span class="ticker-item">{symbol_name}: <span style="color:{color}">₹{price:,.2f} ({change:.2f}%)</span></span>'
        except: continue
    ticker_html += '</div></div>'
    st.markdown(ticker_html, unsafe_allow_html=True)

# 4. லாகின் சிஸ்டம்
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="max-width: 400px; margin: auto;">', unsafe_allow_html=True)
        l_user = st.text_input("User ID", placeholder="Enter your ID")
        l_pass = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Access Dashboard 🚀", use_container_width=True):
            if l_user and l_pass: 
                st.session_state['is_logged_in'] = True
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 5. மெயின் ஆப் (Main Interface)
render_ticker()
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Ultimate Stock Intelligence Engine</p>', unsafe_allow_html=True)

# Sidebar Controls
st.sidebar.title("Settings")
st.session_state['language'] = st.sidebar.radio("மொழி / Language", ["Tamil", "English"])
if st.sidebar.button("Logout 🚪"): 
    st.session_state['is_logged_in'] = False
    st.rerun()

# Search Bar
u_input = st.text_input("Search Symbol (eg: RELIANCE, TCS, SBIN)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist_year = stock.history(period="1y")

    # Tabs
    tabs = st.tabs([
        f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
        f"📈 {get_text('Charts', 'வரைபடம்')}", 
        f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
        f"🛠️ {get_text('Technical', 'தொழில்நுட்பம்')}"
    ])

    # --- TAB 1: Analysis ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        col1, col2, col3, col4 = st.columns(4)
        
        main_metrics = [
            ("LTP (விலை)", f"₹{info.get('currentPrice', 0):,.2f}"),
            ("Market Cap", f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            ("P/E Ratio", info.get('trailingPE', 'N/A')),
            ("Dividend Yield", f"{(info.get('dividendYield', 0)*100):.2f}%")
        ]
        
        cols = [col1, col2, col3, col4]
        for i, (l, v) in enumerate(main_metrics):
            cols[i].markdown(f'<div class="custom-card"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

    # --- TAB 2: Advanced Charts ---
    with tabs[1]:
        fig = go.Figure(data=[go.Candlestick(x=hist_year.index[-60:], open=hist_year['Open'][-60:], high=hist_year['High'][-60:], low=hist_year['Low'][-60:], close=hist_year['Close'][-60:])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=500, margin=dict(l=0,r=0,b=0,t=0))
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 3: Modern Watchlist ---
    with tabs[2]:
        st.markdown("### My Watchlist")
        if st.button(f"Add {u_input} to Watchlist", use_container_width=True):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.success(f"{u_input} Added!")

        for symbol in st.session_state['watchlist']:
            try:
                w_ticker = f"{symbol}.NS" if ".NS" not in symbol else symbol
                w_info = yf.Ticker(w_ticker).info
                w_price = w_info.get('currentPrice', 0)
                w_change = w_info.get('regularMarketChangePercent', 0)
                w_color = "#39FF14" if w_change >= 0 else "#FF3131"
                
                # Modern Watchlist Card
                st.markdown(f"""
                    <div style="background: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 15px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <span style="color: #8b949e; font-size: 11px; font-weight: bold;">{symbol}</span><br>
                            <span style="color: white; font-size: 16px; font-weight: 800;">₹{w_price:,.2f}</span>
                        </div>
                        <div style="text-align: right;">
                            <span style="color: {w_color}; font-size: 14px; font-weight: bold;">{'+' if w_change > 0 else ''}{w_change:.2f}%</span>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                if st.button(f"Remove {symbol}", key=f"del_{symbol}"):
                    st.session_state['watchlist'].remove(symbol)
                    st.rerun()
            except: continue

    # --- TAB 4: Technical Tools ---
    with tabs[3]:
        hist_year['RSI'] = ta.rsi(hist_year['Close'], length=14)
        current_rsi = hist_year['RSI'].iloc[-1]
        
        st.markdown("#### Technical Indicators")
        tc1, tc2 = st.columns(2)
        
        rsi_status = "Oversold (வாங்கலாம்)" if current_rsi < 30 else "Overbought (தவிர்க்கலாம்)" if current_rsi > 70 else "Neutral (நடுநிலை)"
        tc1.markdown(f'<div class="custom-card"><span class="m-label">RSI (14 Days)</span><span class="m-value">{current_rsi:.2f}</span><p style="font-size:11px; color:#8b949e;">{rsi_status}</p></div>', unsafe_allow_html=True)
        
        vol_ratio = info.get('regularMarketVolume', 1) / info.get('averageVolume', 1)
        tc2.markdown(f'<div class="custom-card"><span class="m-label">Volume Ratio</span><span class="m-value">{vol_ratio:.2f}x</span><p style="font-size:11px; color:#8b949e;">Trading Activity</p></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"சரியான பங்கு குறியீட்டை உள்ளிடவும். (Error: {e})")

st.markdown("<p style='text-align:center; color:#333; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
