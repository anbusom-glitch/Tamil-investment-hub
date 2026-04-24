import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. டிக்கர் தகவல்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

# 3. பண்டமெண்டல் ஸ்கோர் கார்டு
def fundamental_analyzer(info):
    score = 0
    checks = []
    
    # ROE > 15% (திறன்)
    roe = info.get('returnOnEquity', 0)
    if roe > 0.15: 
        score += 2; checks.append("✅ ROE: முதலீட்டில் நல்ல லாபம் தருகிறது")
    else: checks.append("⚠️ ROE: லாபத்திறன் குறைவாக உள்ளது")
    
    # Debt to Equity < 1 (பாதுகாப்பு)
    debt = info.get('debtToEquity', 200)
    if debt < 100: 
        score += 3; checks.append("✅ கடன் சுமை மிகவும் குறைவு (Safe)")
    else: checks.append("⚠️ கடன் அதிகமாக உள்ளது (Risky)")
    
    # PE < 30 (விலை)
    pe = info.get('trailingPE', 100)
    if pe < 30: 
        score += 2; checks.append("✅ பங்கு நியாயமான விலையில் உள்ளது")
    else: checks.append("⚠️ பங்கின் விலை சற்று அதிகம்")

    # Current Ratio > 1.5 (நிர்வாகம்)
    cr = info.get('currentRatio', 0)
    if cr > 1.5: 
        score += 3; checks.append("✅ கையில் போதுமான பணப்புழக்கம் உள்ளது")
    
    if score >= 8: return "Strong Buy 💎", "#2ea043", checks
    elif score >= 5: return "Watchlist 👀", "#ffd700", checks
    else: return "Avoid 🚫", "#f85149", checks

# 4. CSS (Premium Quality UI)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 5px 0; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; }
    
    .f-box { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 8px; }
    .f-label { color: #8b949e; font-size: 10px; text-transform: uppercase; }
    .f-value { color: #ffd700; font-size: 14px; font-weight: bold; }
    
    .check-list { font-size: 11px; margin-top: 5px; list-style: none; padding: 0; }
    </style>
    """, unsafe_allow_html=True)

# 5. மேலடுக்கு டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# 6. லோகோ & தலைப்பு
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2, tab3 = st.tabs(["📊 Fundamental Analysis", "🤝 Shareholding", "📅 Events & Actions"])

with tab1:
    u_input = st.text_input("Search Stock", value="RELIANCE").upper()
    ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 0)
        
        st.markdown(f"### {info.get('longName', ticker)}")

        # --- SMART FUNDAMENTAL VERDICT ---
        verdict, v_color, checks = fundamental_analyzer(info)
        st.markdown(f"""
            <div style="background:{v_color}22; border:2px solid {v_color}; border-radius:10px; padding:15px; text-align:center;">
                <span style="color:{v_color}; font-size:18px; font-weight:900;">{verdict}</span>
                <div class="check-list">{"<br>".join(checks)}</div>
            </div>
        """, unsafe_allow_html=True)

        st.write("")

        # --- CORE FUNDAMENTAL METRICS ---
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="f-box"><span class="f-label">ROE (லாபத்திறன்)</span><br><span class="f-value">{info.get("returnOnEquity", 0)*100:.1f}%</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="f-box"><span class="f-label">D/E Ratio (கடன்)</span><br><span class="f-value">{info.get("debtToEquity", 0)/100:.2f}</span></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="f-box"><span class="f-label">Current Ratio (நிழப்பு)</span><br><span class="f-value">{info.get("currentRatio", 0):.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="f-box"><span class="f-label">Face Value</span><br><span class="f-value">₹{info.get("dividendYield", 0)*100:.1f}%</span></div>', unsafe_allow_html=True)

        # Interactive Chart
        pd = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        hist = stock.history(period=pd)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700'))])
        fig.update_layout(height=250, margin=dict(
