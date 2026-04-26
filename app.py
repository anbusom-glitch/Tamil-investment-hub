# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# 7-TAB PRO MODEL - Fixed Language Switcher & Normal Fonts
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# 2. SESSION STATE & LANGUAGE SETUP
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 3. CSS STYLING (Clean Fonts for Numbers)
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
    margin: 0;
}

.sub-title { text-align: center; color: #5a7a9a; font-size: 11px; letter-spacing: 3px; margin-bottom: 15px; }

/* Price Card with Normal Fonts */
.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 20px; border-radius: 18px; border: 1px solid rgba(57,255,20,0.2); text-align: center; margin-bottom: 15px;
}
.ltp-price { font-size: 40px !important; font-weight: 800; color: #39FF14; font-family: 'Exo 2', sans-serif; }

.section-card { background: #080f18; padding: 18px; border-radius: 14px; border: 1px solid #1a2535; margin-bottom: 15px; }

.metric-row {
    display: flex;
    justify-content: space-between;
    padding: 11px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 13px; font-weight: 600; text-transform: uppercase; }
.m-value { color: #eaf2ff; font-family: 'Exo 2', sans-serif; font-size: 15px; font-weight: 700; }

.range-container { background: #111d2a; height: 8px; border-radius: 10px; width: 100%; position: relative; margin: 12px 0; }
.range-bar { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14); width: 100%; }
.range-marker { position: absolute; top: -6px; width: 4px; height: 18px; background: white; transform: translateX(-50%); box-shadow: 0 0 8px #fff; }

.big-score { font-size: 60px !important; font-weight: 800; font-family: 'Exo 2', sans-serif; }
</style>
""", unsafe_allow_html=True)

# 4. HEADER & TOP SEARCH SECTION
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM</p>', unsafe_allow_html=True)

# Main Navigation Section
head_col1, head_col2, head_col3 = st.columns([3, 1, 1])

with head_col1:
    u_input = st.text_input(get_text("Search Symbol (eg: SBIN, RELIANCE)", "பங்குப் பெயரைத் தேடுக (eg: SBIN, RELIANCE)"), value="SBIN").upper().strip()

with head_col2:
    period = st.selectbox(get_text("Period", "காலம்"), ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

with head_col3:
    # மொழி மாற்றும் வசதி இப்போது இங்கே தெளிவாகத் தெரியும்
    lang_choice = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True, key="lang_radio")
    st.session_state['language'] = lang_choice

ticker = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

# 5. DATA HELPERS
@st.cache_data(ttl=300)
def fetch_pro_data(sym, prd):
    t = yf.Ticker(sym)
    return t.info, t.history(period=prd), t.news[:8]

def fmt_cr(v): return f"Rs.{v/1e7:,.2f} Cr" if v and not np.isnan(v) else "N/A"
def fmt_pct(v): return f"{(v*100):.2f}%" if v and not np.isnan(v) else "N/A"

# 6. APP LOGIC
try:
    with st.spinner(get_text("Loading data...", "தரவுகள் சேகரிக்கப்படுகிறது...")):
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
            <div style="color:#5a7a9a; font-size:15px; font-weight:700;">{info.get('longName', ticker)}</div>
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
        st.markdown(f"### {get_text('Technical Analysis', 'தொழில்நுட்ப ஆய்வு')}")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        # Simple EMA & RSI Calculation for Tech tab
        ema50 = hist['Close'].ewm(span=50).mean().iloc[-1]
        ema200 = hist['Close'].ewm(span=200).mean().iloc[-1]
        
        tech_metrics = [
            (get_text("Day Range", "இன்றைய எல்லை"), f"Rs.{info.get('dayLow',0):,.2f} - Rs.{info.get('dayHigh',0):,.2f}"),
            (get_text("EMA 50", "இ.எம்.ஏ 50"), f"Rs.{ema50:,.2f}"),
            (get_text("EMA 200", "இ.எம்.ஏ 200"), f"Rs.{ema200:,.2f}"),
            (get_text("Average Volume", "சராசரி வர்த்தகம்"), f"{info.get('averageVolume', 0):,}")
        ]
        for l, v in tech_metrics:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 3: FUNDAMENTALS ---
    with t3:
        st.markdown(f"### {get_text('Fundamental Analysis', 'அடிப்படை ஆய்வு')}")
        f_col1, f_col2 = st.columns(2)
        with f_col1:
            st.markdown('<div class="section-card"><div class="m-label" style="color:#00D4FF;">Valuation</div>', unsafe_allow_html=True)
            v_m = [("Market Cap", fmt_cr(info.get('marketCap'))), ("P/E Ratio", str(info.get('trailingPE', 'N/A'))), ("P/B Ratio", str(info.get('priceToBook', 'N/A')))]
            for l, v in v_m:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        with f_col2:
            st.markdown('<div class="section-card"><div class="m-label" style="color:#00D4FF;">Ratios</div>', unsafe_allow_html=True)
            r_m = [("ROE", fmt_pct(info.get('returnOnEquity'))), ("Debt/Equity", str(info.get('debtToEquity', 'N/A'))), ("Dividend Yield", fmt_pct(info.get('dividendYield')))]
            for l, v in r_m:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 4: SHAREHOLDING ---
    with t4:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விவரம்')}")
        promo = (info.get('heldPercentInsiders', 0)) * 100
        inst = (info.get('heldPercentInstitutions', 0)) * 100
        retail = max(0, 100 - (promo + inst))
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Retail'], values=[promo, inst, retail], hole=.4)])
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='#020509', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 5: FINANCIALS ---
    with t5:
        st.markdown(f"### {get_text('Income Statement', 'நிதிநிலை அறிக்கை')}")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        fin_m = [
            ("Total Revenue", fmt_cr(info.get('totalRevenue'))),
            ("Net Profit", fmt_cr(info.get('netIncomeToCommon'))),
            ("Revenue Growth", fmt_pct(info.get('revenueGrowth'))),
            ("Earnings Growth", fmt_pct(info.get('earningsGrowth'))),
            ("EPS (TTM)", f"Rs.{info.get('trailingEps', 0):.2f}")
        ]
        for l, v in fin_m:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 6: ABOUT ---
    with t6:
        st.markdown(f"### {get_text('Company Description', 'நிறுவனம் பற்றி')}")
        st.markdown(f'<div class="section-card" style="line-height:1.8; font-size:14px;">{info.get("longBusinessSummary", "N/A")}</div>', unsafe_allow_html=True)
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        about_m = [("Sector", info.get('sector', 'N/A')), ("Industry", info.get('industry', 'N/A')), ("Website", info.get('website', 'N/A'))]
        for l, v in about_m:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 7: NEWS ---
    with t7:
        st.markdown(f"### {get_text('Market News', 'சமீபத்திய செய்திகள்')}")
        for n in news_list:
            st.markdown(f"""
            <div class="section-card">
                <div style="font-weight:700; font-size:15px;"><a href="{n['link']}" target="_blank" style="color:#39FF14; text-decoration:none;">{n['title']}</a></div>
                <div style="font-size:12px; color:#5a7a9a; margin-top:5px;">Source: {n['publisher']}</div>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    st.warning(get_text(f"Please enter a valid symbol (e.g., RELIANCE). Error: {e}", f"சரியான பங்கைத் தேடவும். பிழை: {e}"))

# 7. FOOTER
st.markdown('<div style="text-align:center; padding:30px; border-top:1px solid #1a2535; font-size:11px; color:#5a7a9a; font-family:Exo 2;">2026 TAMIL INVEST HUB PRO - CREATED BY SOMASUNDARAM</div>', unsafe_allow_html=True)
