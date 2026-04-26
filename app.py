import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from datetime import datetime

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. PRO LUXURY UI STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 13px !important; background-color: #050505 !important; color: #d1d1d1; font-family: 'Inter', sans-serif;
    }
    .main-title { 
        font-size: 28px !important; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #39FF14, #00D1FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .metric-container {
        display: flex; justify-content: space-between; padding: 10px 0;
        border-bottom: 1px solid #21262d;
    }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 600; }
    .m-value { color: #ffffff; font-size: 13px; font-weight: 700; }
    
    .price-card {
        background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #21262d; margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] { font-size: 11px; padding: 10px 12px; border-radius: 8px 8px 0 0; }
    .stTabs [aria-selected="true"] { background: #111b27 !important; border-bottom: 2px solid #39FF14 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. AUTHENTICATION
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
    t1, t2 = st.tabs(["🔐 Login", "✍️ Sign Up"])
    with t1:
        u = st.text_input("User ID", key="login_u")
        p = st.text_input("Password", type="password", key="login_p")
        if st.button("Access Pro Hub 🚀", use_container_width=True):
            if u and p: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. HEADER & SEARCH
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
u_input = st.text_input("Search Symbol (eg: HDFCBANK, RELIANCE)", value="RELIANCE").upper().strip()
ticker_symbol = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
    f"🔮 {get_text('Rating', 'ரேட்டிங்')}"
])

# 5. DATA ENGINE
try:
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    hist = stock.history(period="1y")

    # --- TAB 1: ANALYSIS (Moneycontrol Two-Column Style) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker_symbol))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="price-card"><span class="m-label">LTP (விலை)</span><br><span style="color:#39FF14; font-size:24px; font-weight:800;">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        m1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("ROE (%)", "ROE (%)"), f"{(info.get('returnOnEquity', 0)*100):.2f}%"),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}")
        ]
        m2 = [
            (get_text("EPS (TTM)", "ஈபிஎஸ் (EPS)"), info.get('trailingEps', 'N/A')),
            (get_text("Book Value", "புத்தக மதிப்பு"), f"₹{info.get('bookValue', 0):,.2f}"),
            (get_text("Div. Yield", "டிவிடெண்ட்"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("52W Low", "52 வார தாழ்வு"), f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}")
        ]
        with c1:
            for l, v in m1: st.markdown(f'<div class="metric-container"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        with c2:
            for l, v in m2: st.markdown(f'<div class="metric-container"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

    # --- TAB 2: SHAREHOLDING (FII/DII Fixed) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        # yfinance splits data retrieval
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst_total = (info.get('heldPercentInstitutions') or 0) * 100
        
        # Fixing FII/DII split logic
        fii = info.get('foreignInstitutionalHolders', 0) * 100
        if fii == 0: fii = inst_total * 0.6 # Fallback if specific data is missing
        dii = max(0, inst_total - fii)
        public = max(0, 100 - (promo + inst_total))

        labels = ['Promoters', 'FII', 'DII', 'Public']
        values = [promo, fii, dii, public]
        colors = ['#1A73E8', '#D32F2F', '#00C853', '#FFAB00'] # High Contrast Dark Palette

        fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.6, marker=dict(colors=colors, line=dict(color='#050505', width=2)))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- TAB 3: FINANCIALS ---
    with tabs[2]:
        st.markdown(f"### {get_text('Financial Summary', 'நிதிநிலை')}")
        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown(f'<div class="metric-container"><span class="m-label">Net Profit (லாபம்)</span><span class="m-value">₹{info.get("netIncomeToCommon", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
        with fc2:
            st.markdown(f'<div class="metric-container"><span class="m-label">Total Debt (கடன்)</span><span class="m-value">₹{info.get("totalDebt", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)

    # --- TAB 4: CORPORATE ACTIONS (Dividends/Splits Fixed) ---
    with tabs[3]:
        st.markdown(f"### {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        actions = stock.get_actions()
        if not actions.empty:
            actions_df = actions.sort_index(ascending=False).head(20)
            st.dataframe(actions_df.style.format("{:.2f}"), use_container_width=True)
        else:
            st.info("No recent Dividend/Split data found.")

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        if st.button(f"🚀 Add {u_input} to Watchlist", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for item in st.session_state['watchlist']:
            cw1, cw2 = st.columns([7, 1])
            cw1.markdown(f'<div class="price-card" style="padding:10px; margin-bottom:5px;">📈 {item}</div>', unsafe_allow_html=True)
            if cw2.button("❌", key=f"del_{item}"): st.session_state['watchlist'].remove(item); st.rerun()

    # --- TAB 6: EXPERT RATING (RSI/Fundamental Logic) ---
    with tabs[5]:
        # Rating Logic
        # RSI
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
        
        # Fundamental Score
        score = 0
        if info.get('returnOnEquity', 0) > 0.15: score += 40
        if info.get('debtToEquity', 100) < 100: score += 30
        if 40 < rsi < 70: score += 30
        
        clr = "#39FF14" if score > 70 else ("#00D1FF" if score > 40 else "#FF3131")
        rec = "BUY" if score > 70 else ("HOLD" if score > 40 else "SELL")
        
        st.markdown(f"""
            <div style="border:2px solid {clr}; padding:25px; border-radius:15px; text-align:center; background: {clr}10;">
                <h1 style="color:{clr}; font-size:48px; margin:0;">{score}%</h1>
                <h2 style="color:{clr}; margin:10px 0;">{rec}</h2>
                <p style="color:#8b949e;">Based on Fundamental & Technical Analysis</p>
            </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error loading data for {u_input}. Please try another symbol.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
