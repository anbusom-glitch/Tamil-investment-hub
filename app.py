import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. UI STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #050505 !important; color: #d1d1d1; }
    .main-title { 
        font-size: 26px !important; font-weight: 800;
        background: linear-gradient(90deg, #39FF14, #00D1FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 10px;
    }
    .metric-container { display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #21262d; }
    .m-label { color: #8b949e; font-size: 9px; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 12px; font-weight: 700; }
    .analysis-card { background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #21262d; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
    l_u = st.text_input("User ID", key="l_u")
    l_p = st.text_input("Password", type="password", key="l_p")
    if st.button("Access Hub 🚀", use_container_width=True):
        if l_u and l_p: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. HEADER
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}", f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", f"💰 {get_text('Financials', 'நிதிநிலை')}", f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"])

# 5. DATA FETCHING & LOGIC
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1y") # Technical analysis-க்கு ஓராண்டு தரவு தேவை

    # --- TECHNICAL CALCULATION (RSI & Moving Averages) ---
    def calculate_rsi(data, window=14):
        delta = data.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    hist['SMA50'] = hist['Close'].rolling(window=50).mean()
    hist['SMA200'] = hist['Close'].rolling(window=200).mean()
    hist['RSI'] = calculate_rsi(hist['Close'])
    
    current_rsi = hist['RSI'].iloc[-1]
    current_price = info.get('currentPrice', 0)
    sma50 = hist['SMA50'].iloc[-1]
    sma200 = hist['SMA200'].iloc[-1]

    # --- TAB 1: ANALYSIS ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        st.markdown(f'<div style="background:#0d1117; padding:10px; border-radius:10px; border:1px solid #21262d;"><span style="color:#39FF14; font-size:22px; font-weight:800;">₹{current_price:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-container"><span class="m-label">52W High</span><span class="m-value">₹{info.get("fiftyTwoWeekHigh", 0):,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">52W Low</span><span class="m-value">₹{info.get("fiftyTwoWeekLow", 0):,.2f}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-container"><span class="m-label">RSI (14D)</span><span class="m-value">{current_rsi:.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">SMA 50</span><span class="m-value">₹{sma50:,.2f}</span></div>', unsafe_allow_html=True)

    # --- TAB 2: ADVANCED FORECAST (FUNDAMENTAL + TECHNICAL) ---
    with tabs[1]:
        # --- 1. Fundamental Score (Max 60) ---
        f_score = 0
        roe = info.get('returnOnEquity', 0) * 100
        debt_to_equity = info.get('debtToEquity', 100) / 100
        pe = info.get('trailingPE', 100)
        
        if roe > 15: f_score += 20
        if debt_to_equity < 1: f_score += 20
        if pe < 25: f_score += 20

        # --- 2. Technical Score (Max 40) ---
        t_score = 0
        if 40 < current_rsi < 70: t_score += 20  # Neutral to Bullish RSI
        if current_price > sma50: t_score += 10
        if current_price > sma200: t_score += 10

        total_score = f_score + t_score
        
        # Recommendation
        if total_score > 75: 
            rec, clr = get_text("STRONG BUY", "உறுதியாக வாங்கலாம்"), "#39FF14"
        elif total_score > 55: 
            rec, clr = get_text("BUY / HOLD", "வாங்கலாம் / வைத்திருக்கலாம்"), "#00D1FF"
        else: 
            rec, clr = get_text("AVOID / SELL", "தவிர்க்கவும் / விற்கவும்"), "#FF3131"

        st.markdown(f"""
            <div style="border:2px solid {clr}; padding:25px; border-radius:15px; text-align:center; background: {clr}10;">
                <p style="color: #8b949e; font-size: 14px;">Overall Investment Rating</p>
                <h1 style="color:{clr}; font-size:45px; margin:0;">{total_score}%</h1>
                <h2 style="color:{clr}; margin:10px 0;">{rec}</h2>
                <hr style="border:0.5px solid #222;">
                <div style="display:flex; justify-content: space-around; font-size:11px;">
                    <span>Fundamental: {f_score}/60</span>
                    <span>Technical: {t_score}/40</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.info("குறிப்பு: இது தரவுகளின் அடிப்படையில் கணக்கிடப்பட்ட ஒரு மதிப்பீடு மட்டுமே. முதலீடு செய்யும் முன் உங்கள் நிதி ஆலோசகரைக் கலந்தாலோசிக்கவும்.")

    # --- TAB 3: SHAREHOLDING ---
    with tabs[2]:
        p, i = (info.get('heldPercentInsiders') or 0)*100, (info.get('heldPercentInstitutions') or 0)*100
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[p, i, 100-(p+i)], hole=0.6, marker=dict(colors=['#1A73E8', '#00C853', '#FFAB00']))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=350), use_container_width=True)

except Exception as e:
    st.error("தரவுகளைப் பெறுவதில் சிக்கல். குறியீட்டைச் சரிபார்க்கவும்.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
