# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# Updated Version - Enhanced 52W Range & Buy/Sell Percentage
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# =============================================================
# 1. PAGE CONFIG
# =============================================================
st.set_page_config(
    page_title="TAMIL INVEST HUB PRO",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================
# 2. SESSION STATE
# =============================================================
defaults = {
    'is_logged_in': False,
    'language': "Tamil",
    'portfolio': [],
    'watchlist': [],
    'username': '',
    'last_symbol': '',
    'last_data': None,
}
for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# =============================================================
# 3. PREMIUM STYLING
# =============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    background-color: #020509 !important;
    color: #dde6f0;
    font-family: 'Exo 2', sans-serif;
}

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 36px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #39FF14 0%, #00FFD1 50%, #00AAFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 4px;
    margin: 0;
}

.sub-title {
    font-size: 11px !important;
    color: #5a7a9a;
    letter-spacing: 5px;
    text-transform: uppercase;
    font-family: 'Exo 2', sans-serif;
}

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 22px;
    border-radius: 18px;
    border: 1px solid rgba(57,255,20,0.2);
    text-align: center;
}

.ltp-price {
    font-family: 'Orbitron', monospace;
    font-size: 42px !important;
    color: #39FF14;
    line-height: 1;
}

.range-container {
    background: #10192a;
    border-radius: 10px;
    height: 8px;
    width: 100%;
    position: relative;
    margin: 15px 0;
}

.range-bar {
    background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14);
    height: 100%;
    border-radius: 10px;
}

.range-marker {
    position: absolute;
    top: -6px;
    width: 4px;
    height: 20px;
    background: #fff;
    box-shadow: 0 0 10px #fff;
    border-radius: 2px;
}

.section-card {
    background: #080f18;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #1a2535;
    margin-bottom: 16px;
}

.stat-card {
    background: #080f18;
    border-radius: 14px;
    border: 1px solid #1a2535;
    padding: 16px;
    text-align: center;
}

.stat-label { color: #5a7a9a; font-size: 11px; font-weight: 700; text-transform: uppercase; }
.stat-value { font-family: 'Orbitron', monospace; font-size: 16px; font-weight: 700; }
.green { color: #39FF14 !important; }
.red   { color: #FF4455 !important; }
.blue  { color: #00D4FF !important; }
.gold  { color: #FFD700 !important; }

.badge {
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 800;
}
.badge-green { background: rgba(57,255,20,0.1); color: #39FF14; border: 1px solid #39FF1444; }
.badge-red   { background: rgba(255,68,85,0.1); color: #FF4455; border: 1px solid #FF445544; }

.big-pct {
    font-family: 'Orbitron', monospace;
    font-size: 48px;
    font-weight: 900;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# 4. AUTHENTICATION
# =============================================================
if not st.session_state['is_logged_in']:
    st.markdown('<div style="text-align:center; padding:60px;"><p class="main-title">TAMIL INVEST HUB PRO</p></div>', unsafe_allow_html=True)
    col = st.columns([1, 1.5, 1])[1]
    with col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        u = st.text_input("User ID")
        p = st.text_input("Password", type="password")
        if st.button("ACCESS HUB", use_container_width=True):
            if u and p:
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = u
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =============================================================
# 5. HELPER FUNCTIONS
# =============================================================
def calc_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def calc_macd(series, fast=12, slow=26, signal=9):
    ema_f = series.ewm(span=fast, adjust=False).mean()
    ema_s = series.ewm(span=slow, adjust=False).mean()
    macd  = ema_f - ema_s
    sig   = macd.ewm(span=signal, adjust=False).mean()
    return macd, sig, macd - sig

def fmt_cr(v):
    return f"Rs.{v/1e7:,.2f} Cr" if v else "N/A"

@st.cache_data(ttl=180)
def fetch_data(sym, period):
    t = yf.Ticker(sym)
    return dict(t.info), t.history(period=period), t.actions, t.news[:8]

# =============================================================
# 6. SIDEBAR
# =============================================================
with st.sidebar:
    st.markdown(f'<p style="font-family:Orbitron; color:#39FF14;">PORTFOLIO - {st.session_state["username"]}</p>', unsafe_allow_html=True)
    st.session_state['language'] = st.radio("Language", ["Tamil", "English"], horizontal=True)
    if st.button("Logout", use_container_width=True):
        st.session_state['is_logged_in'] = False
        st.rerun()

# =============================================================
# 7. MAIN APP
# =============================================================
st.markdown('<div style="text-align:center;"><p class="main-title">TAMIL INVEST HUB PRO</p><p class="sub-title">Created by Somasundaram</p></div>', unsafe_allow_html=True)

sc1, sc2 = st.columns([4, 1])
with sc1:
    u_input = st.text_input(get_text("Search Symbol (eg: SBIN, RELIANCE)", "பங்குப் பெயரைத் தேடுக"), value="RELIANCE").upper()
with sc2:
    period = st.selectbox(get_text("Period", "காலம்"), ["1mo", "3mo", "6mo", "1y", "5y"], index=3)

ticker_symbol = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

try:
    info, hist, actions, news_list = fetch_data(ticker_symbol, period)
    
    if hist.empty:
        st.error("Data not found.")
        st.stop()

    # Calculations
    ltp = info.get('currentPrice') or hist['Close'].iloc[-1]
    prev_c = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
    day_chg = ltp - prev_c
    day_pct = (day_chg / prev_c) * 100
    
    # 52W Range Logic
    h52 = info.get('fiftyTwoWeekHigh', ltp)
    l52 = info.get('fiftyTwoWeekLow', ltp)
    range_pct = ((ltp - l52) / (h52 - l52)) * 100 if (h52 - l52) != 0 else 0

    # Tabs
    tabs = st.tabs([get_text("Chart", "விலை விவரம்"), get_text("Rating", "மதிப்பீடு"), get_text("Financials", "நிதிநிலை")])

    with tabs[0]:
        # Price Display
        chg_clr = "#39FF14" if day_chg >= 0 else "#FF4455"
        st.markdown(f"""
        <div class="price-card">
            <div style="color:#5a7a9a; font-size:14px; font-weight:800;">{info.get('longName', ticker_symbol)}</div>
            <div class="ltp-price">Rs.{ltp:,.2f}</div>
            <div style="color:{chg_clr}; font-weight:800; font-size:18px;">
                {day_chg:+.2f} ({day_pct:+.2f}%)
            </div>
            
            <div style="margin-top:20px; text-align:left;">
                <div style="display:flex; justify-content:space-between; font-size:11px; color:#5a7a9a;">
                    <span>52W Low: <b>Rs.{l52:,.2f}</b></span>
                    <span>52W High: <b>Rs.{h52:,.2f}</b></span>
                </div>
                <div class="range-container">
                    <div class="range-bar"></div>
                    <div class="range-marker" style="left: {range_pct}%;"></div>
                </div>
                <div style="text-align:center; font-size:11px; color:#39FF14;">
                    Price is at {range_pct:.1f}% of its 52W Range
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Basic Stats
        s1, s2, s3 = st.columns(3)
        s1.markdown(f'<div class="stat-card"><div class="stat-label">Market Cap</div><div class="stat-value blue">{fmt_cr(info.get("marketCap"))}</div></div>', unsafe_allow_html=True)
        s2.markdown(f'<div class="stat-card"><div class="stat-label">P/E Ratio</div><div class="stat-value gold">{info.get("trailingPE", "N/A")}</div></div>', unsafe_allow_html=True)
        s3.markdown(f'<div class="stat-card"><div class="stat-label">Dividend Yield</div><div class="stat-value green">{info.get("dividendYield", 0)*100:.2f}%</div></div>', unsafe_allow_html=True)

        # Simple Chart
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='#020509', plot_bgcolor='#080f18', height=400, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown(f"### {get_text('AI Investment Rating', 'AI முதலீடு மதிப்பீடு')}")
        
        # Simple Rating Logic (Out of 100)
        rsi = calc_rsi(hist['Close']).iloc[-1]
        roe = (info.get('returnOnEquity') or 0) * 100
        margin = (info.get('profitMargins') or 0) * 100
        
        # Calculate Score
        score = 0
        score += 30 if 40 < rsi < 65 else (15 if rsi < 30 else 5)
        score += 35 if roe > 15 else (20 if roe > 5 else 5)
        score += 35 if margin > 10 else (20 if margin > 0 else 5)
        
        # Display Result
        res_txt = "STRONG BUY" if score > 75 else ("BUY" if score > 55 else ("HOLD" if score > 40 else "AVOID"))
        res_clr = "#39FF14" if score > 55 else ("#FFD700" if score > 40 else "#FF4455")
        
        st.markdown(f"""
        <div class="section-card" style="text-align:center; border: 1px solid {res_clr}44;">
            <div style="font-size:16px; color:#5a7a9a; margin-bottom:10px;">{get_text('Overall Buy/Sell Strength', 'ஒட்டுமொத்த வாங்க/விற்க பலம்')}</div>
            <div class="big-pct" style="color:{res_clr};">{score}%</div>
            <div style="font-size:24px; font-weight:800; color:{res_clr}; margin-top:10px;">{res_txt}</div>
            <div style="margin-top:20px; font-size:14px; color:#5a7a9a;">
                100-க்கு {score} புள்ளிகள் இந்த பங்கிற்கு கிடைத்துள்ளது.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Details
        c1, c2, c3 = st.columns(3)
        c1.metric("Technical Score", f"{int(rsi)}/100")
        c2.metric("Fundamental Score", f"{int(roe)}/100")
        c3.metric("Profitability Score", f"{int(margin)}/100")

    with tabs[2]:
        st.write(info.get('longBusinessSummary', 'No data available.'))

except Exception as e:
    st.error(f"Error fetching data. Check symbol. ({e})")

# =============================================================
# FOOTER
# =============================================================
st.markdown(f"""
<div style="text-align:center; margin-top:50px; padding:20px; border-top:1px solid #1a2535;">
    <p style="color:#5a7a9a; font-size:10px; font-family:Orbitron;">
        2026 TAMIL INVEST HUB PRO - CREATED BY SOMASUNDARAM - EDUCATIONAL PURPOSES ONLY
    </p>
</div>
""", unsafe_allow_html=True)
