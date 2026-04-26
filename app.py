# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# 7-TAB PROFESSIONAL MODEL - Combined Fundamental & Technical
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# 2. SESSION STATE
if 'is_logged_in' not in st.session_state:
    st.session_state['is_logged_in'] = False
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 3. CSS STYLING (Normal Fonts for Numbers)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@300;400;600;700;800&family=Orbitron:wght@900&display=swap');

html, body, [class*="css"] {
    background-color: #020509 !important;
    color: #dde6f0;
    font-family: 'Exo 2', sans-serif;
}

.main-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 30px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #39FF14 0%, #00FFD1 50%, #00AAFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
}

.sub-title { text-align: center; color: #5a7a9a; font-size: 11px; letter-spacing: 3px; margin-bottom: 15px; }

/* Normal Numbers Styling */
.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 20px; border-radius: 18px; border: 1px solid rgba(57,255,20,0.2); text-align: center; margin-bottom: 15px;
}
.ltp-price { font-size: 40px !important; font-weight: 800; color: #39FF14; font-family: 'Exo 2', sans-serif; }

.section-card { background: #080f18; padding: 18px; border-radius: 14px; border: 1px solid #1a2535; margin-bottom: 15px; }

.metric-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 13px; font-weight: 600; text-transform: uppercase; }
/* Changed from Orbitron to Exo 2 for readability */
.m-value { color: #eaf2ff; font-family: 'Exo 2', sans-serif; font-size: 15px; font-weight: 700; }

.range-container { background: #111d2a; height: 8px; border-radius: 10px; width: 100%; position: relative; margin: 12px 0; }
.range-bar { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14); width: 100%; }
.range-marker { position: absolute; top: -6px; width: 4px; height: 18px; background: white; transform: translateX(-50%); box-shadow: 0 0 8px #fff; }

.big-score { font-size: 60px !important; font-weight: 800; font-family: 'Exo 2', sans-serif; }
</style>
""", unsafe_allow_html=True)

# 4. SEARCH & DATA FETCH
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM</p>', unsafe_allow_html=True)

with st.sidebar:
    st.session_state['language'] = st.radio("Language", ["Tamil", "English"], horizontal=True)
    if st.button("Logout"): 
        st.session_state['is_logged_in'] = False
        st.rerun()

sc1, sc2 = st.columns([3, 1])
with sc1:
    u_input = st.text_input(get_text("Search Company Name / Symbol", "பங்குப் பெயரைத் தேடுக (eg: SBIN, RELIANCE)"), value="SBIN").upper().strip()
with sc2:
    period = st.selectbox(get_text("Select Period", "காலம்"), ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

ticker = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

@st.cache_data(ttl=300)
def fetch_pro_data(sym, prd):
    t = yf.Ticker(sym)
    return t.info, t.history(period=prd), t.news[:8]

try:
    info, hist, news_list = fetch_pro_data(ticker, period)
    
    # Core calculations
    ltp = info.get('currentPrice') or hist['Close'].iloc[-1]
    prev_close = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
    change = ltp - prev_close
    h52, l52 = info.get('fiftyTwoWeekHigh', ltp), info.get('fiftyTwoWeekLow', ltp)
    r_pos = ((ltp - l52) / (h52 - l52) * 100) if (h52 - l52) != 0 else 50

    # 7 TABS SYSTEM
    t1, t2, t3, t4, t5, t6, t7 = st.tabs([
        get_text("Overview", "விலை நிலவரம்"), 
        get_text("Technicals", "தொழில்நுட்ப ஆய்வு"), 
        get_text("Fundamentals", "அடிப்படை ஆய்வு"),
        get_text("Shareholding", "பங்குதாரர்கள்"),
        get_text("Financials", "நிதிநிலை அறிக்கை"),
        get_text("About", "நிறுவனம் பற்றி"),
        get_text("News", "செய்திகள்")
    ])

    # --- TAB 1: OVERVIEW ---
    with t1:
        clr = "#39FF14" if change >= 0 else "#FF4455"
        st.markdown(f"""
        <div class="price-card">
            <div style="color:#5a7a9a; font-size:15px; margin-bottom:5px; font-weight:700;">{info.get('longName', ticker)}</div>
            <div class="ltp-price">Rs.{ltp:,.2f}</div>
            <div style="color:{clr}; font-weight:800; font-size:18px;">{change:+.2f} ({ (change/prev_close*100):+.2f}%)</div>
            <div class="range-container"><div class="range-bar"></div><div class="range-marker" style="left:{r_pos}%;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:12px; color:#5a7a9a; font-weight:700;">
                <span>52W LOW: Rs.{l52:,.2f}</span><span>52W HIGH: Rs.{h52:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='#020509', plot_bgcolor='#080f18', height=450, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: TECHNICALS ---
    with t2:
        st.markdown(f"### {get_text('Technical Indicators', 'தொழில்நுட்ப குறியீடுகள்')}")
        tc1, tc2 = st.columns(2)
        with tc1:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            # RSI Calculation
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + gain/loss))
            
            tech_data = [
                ("RSI (14)", f"{rsi.iloc[-1]:.2f}"),
                ("EMA (50)", f"Rs.{hist['Close'].ewm(span=50).mean().iloc[-1]:,.2f}"),
                ("EMA (200)", f"Rs.{hist['Close'].ewm(span=200).mean().iloc[-1]:,.2f}"),
                ("Day High", f"Rs.{info.get('dayHigh', 0):,.2f}"),
                ("Day Low", f"Rs.{info.get('dayLow', 0):,.2f}")
            ]
            for l, v in tech_data:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 3: FUNDAMENTALS ---
    with t3:
        st.markdown(f"### {get_text('Fundamental Metrics', 'அடிப்படை ஆய்வு')}")
        f1, f2 = st.columns(2)
        with f1:
            st.markdown('<div class="section-card"><div style="color:#00D4FF; font-weight:800; margin-bottom:10px;">VALUATION</div>', unsafe_allow_html=True)
            v_data = [
                ("Market Cap", f"Rs.{info.get('marketCap', 0)/1e7:,.2f} Cr"),
                ("P/E Ratio", str(info.get('trailingPE', 'N/A'))),
                ("P/B Ratio", str(info.get('priceToBook', 'N/A'))),
                ("EV/EBITDA", str(info.get('enterpriseToEbitda', 'N/A')))
            ]
            for l, v in v_data:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with f2:
            st.markdown('<div class="section-card"><div style="color:#00D4FF; font-weight:800; margin-bottom:10px;">EFFICIENCY</div>', unsafe_allow_html=True)
            e_data = [
                ("ROE", f"{(info.get('returnOnEquity', 0)*100):.2f}%"),
                ("ROA", f"{(info.get('returnOnAssets', 0)*100):.2f}%"),
                ("Debt to Equity", str(info.get('debtToEquity', 'N/A'))),
                ("Current Ratio", str(info.get('currentRatio', 'N/A')))
            ]
            for l, v in e_data:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 4: SHAREHOLDING ---
    with t4:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விவரம்')}")
        promo = (info.get('heldPercentInsiders', 0)) * 100
        inst = (info.get('heldPercentInstitutions', 0)) * 100
        retail = 100 - (promo + inst)
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Retail'], values=[promo, inst, retail], hole=.4)])
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='#020509', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        sh_rows = [("Promoters", f"{promo:.2f}%"), ("Institutions", f"{inst:.2f}%"), ("Retail / Public", f"{retail:.2f}%")]
        for l, v in sh_rows:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 5: FINANCIALS ---
    with t5:
        st.markdown(f"### {get_text('Income & Growth', 'நிதிநிலை அறிக்கை')}")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fin_data = [
            ("Total Revenue", f"Rs.{info.get('totalRevenue', 0)/1e7:,.2f} Cr"),
            ("Net Income", f"Rs.{info.get('netIncomeToCommon', 0)/1e7:,.2f} Cr"),
            ("Revenue Growth", f"{(info.get('revenueGrowth', 0)*100):.2f}%"),
            ("Earnings Growth", f"{(info.get('earningsGrowth', 0)*100):.2f}%"),
            ("Dividend Yield", f"{(info.get('dividendYield', 0)*100):.2f}%"),
            ("EPS (TTM)", f"Rs.{info.get('trailingEps', 0):.2f}")
        ]
        for l, v in fin_data:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 6: ABOUT ---
    with t6:
        st.markdown(f"### {get_text('Company Profile', 'நிறுவனம் பற்றி')}")
        st.markdown(f'<div class="section-card" style="line-height:1.6;">{info.get("longBusinessSummary", "No Summary Available.")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        details = [
            ("Sector", info.get('sector', 'N/A')),
            ("Industry", info.get('industry', 'N/A')),
            ("Full Time Employees", str(info.get('fullTimeEmployees', 'N/A'))),
            ("Website", info.get('website', 'N/A'))
        ]
        for l, v in details:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 7: NEWS ---
    with t7:
        st.markdown(f"### {get_text('Latest News', 'சமீபத்திய செய்திகள்')}")
        for n in news_list:
            st.markdown(f"""
            <div class="section-card">
                <div style="font-weight:800; font-size:15px;"><a href="{n['link']}" target="_blank" style="color:#39FF14; text-decoration:none;">{n['title']}</a></div>
                <div style="font-size:12px; color:#5a7a9a; margin-top:5px;">Source: {n['publisher']}</div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error: {e}")

# FOOTER
st.markdown('<div style="text-align:center; padding:30px; border-top:1px solid #1a2535; font-size:11px; color:#5a7a9a; font-family:Exo 2;">2026 TAMIL INVEST HUB PRO - CREATED BY SOMASUNDARAM</div>', unsafe_allow_html=True)
