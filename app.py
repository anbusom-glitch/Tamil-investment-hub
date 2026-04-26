# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# Optimized for Quick Navigation & Top Search
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# 2. SESSION STATE
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 3. CSS STYLING
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

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 20px; border-radius: 18px; border: 1px solid rgba(57,255,20,0.2); text-align: center; margin-bottom: 15px;
}

.ltp-price { font-family: 'Orbitron', monospace; font-size: 38px !important; color: #39FF14; }

.section-card { background: #080f18; padding: 18px; border-radius: 14px; border: 1px solid #1a2535; margin-bottom: 15px; }

.metric-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 13px; font-weight: 600; text-transform: uppercase; }
.m-value { color: #eaf2ff; font-family: 'Orbitron', monospace; font-size: 14px; font-weight: 700; }

.range-container { background: #111d2a; height: 8px; border-radius: 10px; width: 100%; position: relative; margin: 12px 0; }
.range-bar { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14); width: 100%; }
.range-marker { position: absolute; top: -6px; width: 4px; height: 18px; background: white; transform: translateX(-50%); }

.big-score { font-family: 'Orbitron', monospace; font-size: 50px !important; font-weight: 900; }
</style>
""", unsafe_allow_html=True)

# 4. DATA HELPERS
@st.cache_data(ttl=300)
def fetch_all(sym, prd):
    t = yf.Ticker(sym)
    return t.info, t.history(period=prd), t.news[:5]

def fmt_cr(v): return f"Rs.{v/1e7:,.2f} Cr" if v and not np.isnan(v) else "N/A"
def fmt_pct(v): return f"{v*100:.2f}%" if v and not np.isnan(v) else "N/A"

# 5. SEARCH SECTION (TOP POSITION)
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM</p>', unsafe_allow_html=True)

# Search Bar and Period at the very top
sc1, sc2 = st.columns([3, 1])
with sc1:
    u_input = st.text_input(get_text("Enter Stock Symbol (eg: SBIN, RELIANCE)", "பங்குப் பெயரைத் தேடுக"), value="SBIN").upper().strip()
with sc2:
    period = st.selectbox(get_text("Select Period", "காலம்"), ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

ticker = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

# 6. DATA PROCESSING & TABS
try:
    with st.spinner("Processing..."):
        info, hist, news = fetch_all(ticker, period)
    
    ltp = info.get('currentPrice') or hist['Close'].iloc[-1]
    prev_close = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
    change = ltp - prev_close
    pct_chg = (change / prev_close) * 100
    h52, l52 = info.get('fiftyTwoWeekHigh', ltp), info.get('fiftyTwoWeekLow', ltp)
    r_pos = ((ltp - l52) / (h52 - l52) * 100) if (h52 - l52) != 0 else 50

    # Tabs for minimized scrolling
    t1, t2, t3, t4 = st.tabs([
        get_text("Overview", "விலை நிலவரம்"), 
        get_text("Fundamentals", "அடிப்படை ஆய்வு"), 
        get_text("Rating", "மதிப்பீடு"), 
        get_text("News", "செய்திகள்")
    ])

    # --- TAB 1: OVERVIEW ---
    with t1:
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

    # --- TAB 2: FUNDAMENTALS ---
    with t2:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="section-card"><div style="color:#00D4FF; font-weight:800; margin-bottom:10px;">VALUATION</div>', unsafe_allow_html=True)
            v_data = [("Market Cap", fmt_cr(info.get('marketCap'))), ("P/E Ratio", str(info.get('trailingPE', 'N/A'))), ("P/B Ratio", str(info.get('priceToBook', 'N/A'))), ("Div Yield", f"{info.get('dividendYield', 0)*100:.2f}%")]
            for l, v in v_data:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with c2:
            st.markdown(f'<div class="section-card"><div style="color:#00D4FF; font-weight:800; margin-bottom:10px;">EFFICIENCY</div>', unsafe_allow_html=True)
            e_data = [("ROE", fmt_pct(info.get('returnOnEquity'))), ("Net Margin", fmt_pct(info.get('profitMargins'))), ("Debt/Equity", str(info.get('debtToEquity', 'N/A'))), ("EPS", f"Rs.{info.get('trailingEps', 0):.2f}")]
            for l, v in e_data:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 3: RATING ---
    with t3:
        roe_val = (info.get('returnOnEquity') or 0) * 100
        score = 0
        score += 40 if roe_val > 15 else (20 if roe_val > 8 else 5)
        score += 30 if info.get('trailingPE', 50) < 25 else 10
        score += 30 if info.get('dividendYield', 0) > 0.01 else 10
        
        res_clr = "#39FF14" if score >= 60 else ("#FFD700" if score >= 40 else "#FF4455")
        st.markdown(f"""
        <div class="section-card" style="text-align:center; border: 2px solid {res_clr}44;">
            <div style="color:#5a7a9a; font-size:14px; font-weight:700;">BUYING STRENGTH</div>
            <div class="big-score" style="color:{res_clr};">{score}%</div>
            <div style="font-size:22px; font-weight:800; color:{res_clr}; margin-top:10px;">
                {"GOOD TO BUY" if score > 50 else "CAUTION"}
            </div>
        </div>
        """, unsafe_allow_html=True)

    # --- TAB 4: NEWS ---
    with t4:
        for n in news:
            st.markdown(f"""
            <div class="section-card">
                <div style="font-weight:700; font-size:14px;"><a href="{n['link']}" target="_blank" style="color:#dde6f0; text-decoration:none;">{n['title']}</a></div>
                <div style="font-size:11px; color:#5a7a9a; margin-top:5px;">Source: {n['publisher']}</div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Please check the symbol: {e}")

# FOOTER
st.markdown('<div style="text-align:center; padding:20px; border-top:1px solid #1a2535; font-size:10px; color:#5a7a9a; font-family:Orbitron;">2026 TAMIL INVEST HUB PRO - CREATED BY SOMASUNDARAM</div>', unsafe_allow_html=True)
