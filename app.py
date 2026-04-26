# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# FEATURE: Advanced Fundamental Analysis with Metric-Rows
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# 2. CSS STYLING (Metric-row & Professional Dark UI)
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
}

.sub-title { text-align: center; color: #5a7a9a; font-size: 11px; letter-spacing: 3px; margin-bottom: 20px; }

.section-card { 
    background: #080f18; 
    padding: 22px; 
    border-radius: 14px; 
    border: 1px solid #1a2535; 
    margin-bottom: 20px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}

.card-header {
    color: #00D4FF;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 15px;
    border-bottom: 1px solid #1a2535;
    padding-bottom: 8px;
    text-transform: uppercase;
}

/* Metric Row Setup */
.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 13px; font-weight: 600; }
.m-value { color: #eaf2ff; font-family: 'Orbitron', monospace; font-size: 14px; font-weight: 700; }

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 25px; border-radius: 18px; border: 1px solid rgba(57,255,20,0.2); text-align: center;
}
.ltp-price { font-family: 'Orbitron', monospace; font-size: 40px !important; color: #39FF14; }

.range-container { background: #111d2a; height: 8px; border-radius: 10px; width: 100%; position: relative; margin: 15px 0; }
.range-bar { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14); width: 100%; }
.range-marker { position: absolute; top: -6px; width: 4px; height: 20px; background: white; border-radius: 2px; transform: translateX(-50%); }
</style>
""", unsafe_allow_html=True)

# 3. HELPER FUNCTIONS
def get_text(en, ta):
    return ta if st.session_state.get('language', 'Tamil') == "Tamil" else en

def fmt_cr(v): return f"Rs.{v/1e7:,.2f} Cr" if v and not np.isnan(v) else "N/A"

def fmt_pct(v): return f"{v*100:.2f}%" if v and not np.isnan(v) else "N/A"

# 4. DATA FETCHING
@st.cache_data(ttl=300)
def get_full_analysis(sym):
    t = yf.Ticker(sym)
    return t.info, t.history(period="1y")

# 5. HEADER
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM - FUNDAMENTAL ANALYSIS ENGINE</p>', unsafe_allow_html=True)

with st.sidebar:
    st.session_state['language'] = st.radio("Mozhi / Language", ["Tamil", "English"], horizontal=True)
    u_input = st.text_input(get_text("Stock Symbol", "பங்குப் பெயர்"), value="RELIANCE").upper()

ticker = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

try:
    info, hist = get_full_analysis(ticker)
    
    # Overview Data
    ltp = info.get('currentPrice') or hist['Close'].iloc[-1]
    h52, l52 = info.get('fiftyTwoWeekHigh', ltp), info.get('fiftyTwoWeekLow', ltp)
    r_pos = ((ltp - l52) / (h52 - l52) * 100) if (h52 - l52) != 0 else 50

    # UI TABS
    tabs = st.tabs([get_text("Live Price", "நேரடி விலை"), get_text("Fundamentals", "அடிப்படை ஆய்வு"), get_text("Shareholding", "பங்குதாரர்கள்")])

    with tabs[0]:
        st.markdown(f"""
        <div class="price-card">
            <div style="color:#5a7a9a; font-size:14px; margin-bottom:5px;">{info.get('longName', ticker)}</div>
            <div class="ltp-price">Rs.{ltp:,.2f}</div>
            <div class="range-container"><div class="range-bar"></div><div class="range-marker" style="left:{r_pos}%;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:11px; color:#5a7a9a;">
                <span>52W LOW: Rs.{l52:,.2f}</span><span>52W HIGH: Rs.{h52:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='#020509', plot_bgcolor='#080f18', height=400, margin=dict(t=10,b=10,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown(f"### {get_text('Fundamental Analysis', 'அடிப்படை ஆய்வு விவரங்கள்')}")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Section: Valuation (மதிப்பீடு)
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Valuation", "மதிப்பீடு")}</div>', unsafe_allow_html=True)
            valuation_metrics = [
                (get_text("Market Cap", "சந்தை மதிப்பு"), fmt_cr(info.get('marketCap'))),
                (get_text("P/E Ratio", "விலை/ஈவு விகிதம்"), str(info.get('trailingPE', 'N/A'))),
                (get_text("Price to Book", "பி/பி விகிதம்"), str(info.get('priceToBook', 'N/A'))),
                (get_text("Face Value", "முக மதிப்பு"), str(info.get('faceValue', 'N/A'))),
                (get_text("Dividend Yield", "ஈவுத்தொகை %"), f"{info.get('dividendYield', 0)*100:.2f}%")
            ]
            for l, v in valuation_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Section: Health & Debt (நிதி ஆரோக்கியம்)
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Financial Health", "நிதி ஆரோக்கியம்")}</div>', unsafe_allow_html=True)
            health_metrics = [
                (get_text("Debt to Equity", "கடன்/பங்கு விகிதம்"), str(info.get('debtToEquity', 'N/A'))),
                (get_text("Current Ratio", "நடப்பு விகிதம்"), str(info.get('currentRatio', 'N/A'))),
                (get_text("Quick Ratio", "விரைவு விகிதம்"), str(info.get('quickRatio', 'N/A'))),
                (get_text("Total Cash", "கைவசம் உள்ள பணம்"), fmt_cr(info.get('totalCash'))),
                (get_text("Total Debt", "மொத்த கடன்"), fmt_cr(info.get('totalDebt')))
            ]
            for l, v in health_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        with col2:
            # Section: Profitability (லாபத்தன்மை)
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Profitability", "லாபத்தன்மை")}</div>', unsafe_allow_html=True)
            profit_metrics = [
                (get_text("Revenue (TTM)", "வருமானம்"), fmt_cr(info.get('totalRevenue'))),
                (get_text("Net Profit", "நிகர லாபம்"), fmt_cr(info.get('netIncomeToCommon'))),
                (get_text("ROE (Return on Equity)", "பங்கு மீதான லாபம்"), fmt_pct(info.get('returnOnEquity'))),
                (get_text("ROA (Return on Assets)", "சொத்து மீதான லாபம்"), fmt_pct(info.get('returnOnAssets'))),
                (get_text("Profit Margin", "லாப சதவீதம்"), fmt_pct(info.get('profitMargins')))
            ]
            for l, v in profit_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Section: Growth (வளர்ச்சி)
            st.markdown(f'<div class="section-card"><div class="card-header">{get_text("Growth Estimates", "வளர்ச்சி மதிப்பீடு")}</div>', unsafe_allow_html=True)
            growth_metrics = [
                (get_text("Revenue Growth (YoY)", "வருமான வளர்ச்சி"), fmt_pct(info.get('revenueGrowth'))),
                (get_text("Earnings Growth", "ஈவு வளர்ச்சி"), fmt_pct(info.get('earningsGrowth'))),
                (get_text("EPS (TTM)", "ஒரு பங்கின் லாபம்"), f"Rs.{info.get('trailingEps', 0):.2f}")
            ]
            for l, v in growth_metrics:
                st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விவரங்கள்')}")
        
        # Shareholding Data
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        retail = 100 - (promo + inst)
        
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Retail'], values=[promo, inst, retail], hole=.4)])
        fig_pie.update_layout(template="plotly_dark", paper_bgcolor='#020509', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        sh_rows = [
            (get_text("Promoter Holding", "புரோமோட்டர் பங்குகள்"), f"{promo:.2f}%"),
            (get_text("Institutional Holding", "நிறுவன முதலீடு"), f"{inst:.2f}%"),
            (get_text("Public/Retail", "பொதுமக்கள் பங்குகள்"), f"{retail:.2f}%")
        ]
        for l, v in sh_rows:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"Error fetching fundamental data: {e}")

# FOOTER
st.markdown('<div style="text-align:center; padding:30px; border-top:1px solid #1a2535; font-size:10px; color:#5a7a9a; font-family:Orbitron;">2026 TAMIL INVEST HUB PRO - CREATED BY SOMASUNDARAM</div>', unsafe_allow_html=True)
