# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# 100% FIXED VERSION - All Features Included
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(
    page_title="TAMIL INVEST HUB PRO",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. SESSION STATE
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 3. CSS STYLING (அனைத்து டிசைன்களும் இங்கே உள்ளன)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@400;600;800&display=swap');

html, body, [class*="css"] {
    background-color: #020509 !important;
    color: #dde6f0;
    font-family: 'Exo 2', sans-serif;
}

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 32px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #39FF14 0%, #00FFD1 50%, #00AAFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin: 0;
}

.sub-title { text-align: center; color: #5a7a9a; font-size: 11px; letter-spacing: 3px; margin-bottom: 20px; }

.section-card { 
    background: #080f18; 
    padding: 22px; 
    border-radius: 14px; 
    border: 1px solid #1a2535; 
    margin-bottom: 20px;
}

.card-header {
    color: #00D4FF;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 12px;
    border-bottom: 1px solid #111d2a;
    padding-bottom: 5px;
}

/* Metric Row Styling */
.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 13px; font-weight: 600; text-transform: uppercase; }
.m-value { color: #eaf2ff; font-family: 'Orbitron', monospace; font-size: 14px; font-weight: 700; }

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 25px; border-radius: 18px; border: 1px solid rgba(57,255,20,0.25); text-align: center; margin-bottom: 20px;
}

.ltp-price { font-family: 'Orbitron', monospace; font-size: 42px !important; color: #39FF14; line-height: 1.2; }

/* 52W Range Bar Styling */
.range-container { background: #111d2a; height: 10px; border-radius: 10px; width: 100%; position: relative; margin: 15px 0; border: 1px solid #1a2535; }
.range-bar { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14); width: 100%; }
.range-marker { position: absolute; top: -5px; width: 4px; height: 20px; background: white; border-radius: 2px; box-shadow: 0 0 10px #fff; transform: translateX(-50%); }

.big-score { font-family: 'Orbitron', monospace; font-size: 55px !important; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# 4. LOGIN SYSTEM
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
    col = st.columns([1, 1.5, 1])[1]
    with col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        u = st.text_input("User ID")
        p = st.text_input("Password", type="password")
        if st.button("LOGIN", use_container_width=True):
            if u and p:
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = u
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 5. DATA FETCHING
@st.cache_data(ttl=300)
def fetch_data(sym):
    t = yf.Ticker(sym)
    return t.info, t.history(period="1y")

def fmt_cr(v): return f"Rs.{v/1e7:,.2f} Cr" if v and not np.isnan(v) else "N/A"
def fmt_pct(v): return f"{v*100:.2f}%" if v and not np.isnan(v) else "N/A"

# 6. HEADER
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM</p>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f"**Welcome, {st.session_state['username']}**")
    st.session_state['language'] = st.radio("Language", ["Tamil", "English"], horizontal=True)
    if st.button("Logout"):
        st.session_state['is_logged_in'] = False
        st.rerun()

# 7. SEARCH & ANALYSIS
u_input = st.text_input(get_text("Enter Stock Symbol", "பங்குப் பெயரைத் தேடுக"), value="SBIN").upper().strip()
ticker = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

try:
    info, hist = fetch_data(ticker)
    
    # Overview metrics
    ltp = info.get('currentPrice') or hist['Close'].iloc[-1]
    prev_close = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
    change = ltp - prev_close
    pct_chg = (change / prev_close) * 100
    h52, l52 = info.get('fiftyTwoWeekHigh', ltp), info.get('fiftyTwoWeekLow', ltp)
    r_pos = ((ltp - l52) / (h52 - l52) * 100) if (h52 - l52) != 0 else 50

    tabs = st.tabs([get_text("Overview", "விலை விவரம்"), get_text("Fundamentals", "அடிப்படை ஆய்வு"), get_text("Rating", "மதிப்பீடு")])

    with tabs[0]:
        # Price Card
        clr = "#39FF14" if change >= 0 else "#FF4455"
        st.markdown(f"""
        <div class="price-card">
            <div style="color:#5a7a9a; font-size:14px; margin-bottom:5px;">{info.get('longName', ticker)}</div>
            <div class="ltp-price">Rs.{ltp:,.2f}</div>
            <div style="color:{clr}; font-weight:800; font-size:18px;">{change:+.2f} ({pct_chg:+.2f}%)</div>
            <div class="range-container"><div class="range-bar"></div><div class="range-marker" style="left:{r_pos}%;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#5a7a9a; font-weight:700;">
                <span>52W LOW: Rs.{l52:,.2f}</span><span>52W HIGH: Rs.{h52:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='#020509', plot_bgcolor='#080f18', height=400, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown(f"### {get_text('Fundamental Analysis', 'அடிப்படை ஆய்வு விவரங்கள்')}")
        col1, col2 = st.columns(2)
        
        with col1:
            # Valuation Section
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Valuation", "மதிப்பீடு")}</div>', unsafe_allow_html=True)
            v_metrics = [
                (get_text("Market Cap", "சந்தை மதிப்பு"), fmt_cr(info.get('marketCap'))),
                (get_text("P/E Ratio", "P/E விகிதம்"), str(info.get('trailingPE', 'N/A'))),
                (get_text("Price to Book", "P/B விகிதம்"), str(info.get('priceToBook', 'N/A'))),
                (get_text("Dividend Yield", "ஈவுத்தொகை %"), f"{info.get('dividendYield', 0)*100:.2f}%")
            ]
            for l, v in v_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Health Section
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Financial Health", "நிதி நிலை")}</div>', unsafe_allow_html=True)
            h_metrics = [
                (get_text("Debt to Equity", "கடன்/பங்கு விகிதம்"), str(info.get('debtToEquity', 'N/A'))),
                (get_text("Total Debt", "மொத்த கடன்"), fmt_cr(info.get('totalDebt'))),
                (get_text("Current Ratio", "நடப்பு விகிதம்"), str(info.get('currentRatio', 'N/A')))
            ]
            for l, v in h_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Profitability Section
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Profitability", "லாபத்தன்மை")}</div>', unsafe_allow_html=True)
            p_metrics = [
                (get_text("ROE", "பங்கு மீதான லாபம்"), fmt_pct(info.get('returnOnEquity'))),
                (get_text("Profit Margin", "லாப சதவீதம்"), fmt_pct(info.get('profitMargins'))),
                (get_text("Revenue Growth", "வருமான வளர்ச்சி"), fmt_pct(info.get('revenueGrowth')))
            ]
            for l, v in p_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Shareholding Section
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Shareholding", "பங்குதாரர்கள்")}</div>', unsafe_allow_html=True)
            promo = (info.get('heldPercentInsiders') or 0) * 100
            inst = (info.get('heldPercentInstitutions') or 0) * 100
            sh_metrics = [
                (get_text("Promoters", "புரோமோட்டர்கள்"), f"{promo:.2f}%"),
                (get_text("Institutions", "நிறுவனங்கள்"), f"{inst:.2f}%")
            ]
            for l, v in sh_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        # Buying Strength Percentage Logic
        roe_val = (info.get('returnOnEquity') or 0) * 100
        pe_val = info.get('trailingPE', 50)
        
        score = 0
        if roe_val > 15: score += 40
        elif roe_val > 8: score += 20
        
        if pe_val < 25: score += 30
        elif pe_val < 45: score += 15
        
        score += 30 if info.get('dividendYield', 0) > 0.01 else 10
        
        res_clr = "#39FF14" if score >= 60 else ("#FFD700" if score >= 40 else "#FF4455")
        st.markdown(f"""
        <div class="section-card" style="text-align:center; border: 2px solid {res_clr}44;">
            <div style="color:#5a7a9a; font-size:14px; font-weight:700;">BUYING STRENGTH</div>
            <div class="big-score" style="color:{res_clr};">{score}%</div>
            <div style="font-size:22px; font-weight:800; color:{res_clr}; margin-top:10px;">
                {get_text("INVESTMENT SIGNAL", "முதலீடு சிக்னல்")}
            </div>
        </div>
        """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")

# 8. FOOTER
st.markdown('<div style="text-align:center; padding:30px; border-top:1px solid #1a2535; font-size:10px; color:#5a7a9a; font-family:Orbitron;">2026 TAMIL INVEST HUB PRO - Created by Somasundaram</div>', unsafe_allow_html=True)
