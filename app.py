# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# PRO VERSION: Fixed Translation, 'Link' Error & Font Size
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
# Translation library - install using: pip install deep-translator
try:
    from deep_translator import GoogleTranslator
except ImportError:
    st.error("Please install translator: pip install deep-translator")

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# 2. SESSION STATE
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 3. CSS STYLING (Increased Font Sizes & Normal Numbers)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800&display=swap');

html, body, [class*="css"] {
    background-color: #020509 !important;
    color: #dde6f0;
    font-family: 'Exo 2', sans-serif;
    font-size: 16px; /* Overall base size increased */
}

.main-title {
    font-family: 'Exo 2', sans-serif;
    font-size: 32px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #39FF14 0%, #00FFD1 50%, #00AAFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin-bottom: 0px;
}

.sub-title { text-align: center; color: #5a7a9a; font-size: 12px; letter-spacing: 2px; margin-bottom: 20px; font-weight: 700; }

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 25px; border-radius: 20px; border: 1px solid rgba(57,255,20,0.25); text-align: center; margin-bottom: 20px;
}
.ltp-price { font-size: 45px !important; font-weight: 800; color: #39FF14; }

.section-card { background: #080f18; padding: 22px; border-radius: 15px; border: 1px solid #1a2535; margin-bottom: 15px; }

.metric-row {
    display: flex;
    justify-content: space-between;
    padding: 13px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 14px; font-weight: 600; text-transform: uppercase; }
.m-value { color: #eaf2ff; font-size: 17px; font-weight: 700; }

.range-container { background: #111d2a; height: 10px; border-radius: 10px; width: 100%; position: relative; margin: 15px 0; }
.range-bar { height: 100%; border-radius: 10px; background: linear-gradient(90deg, #FF4455, #FFD700, #39FF14); width: 100%; }
.range-marker { position: absolute; top: -5px; width: 5px; height: 20px; background: white; transform: translateX(-50%); box-shadow: 0 0 10px #fff; }

.big-score { font-size: 65px !important; font-weight: 800; }
</style>
""", unsafe_allow_html=True)

# 4. TOP SECTION & LANGUAGE SELECTOR
st.markdown('<p class="main-title">TAMIL INVEST HUB PRO</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM</p>', unsafe_allow_html=True)

head_col1, head_col2 = st.columns([3, 1])
with head_col1:
    u_input = st.text_input(get_text("Search Company (eg: SBIN, RELIANCE)", "பங்கைத் தேடுக"), value="SBIN").upper().strip()
with head_col2:
    lang = st.radio("Language", ["Tamil", "English"], horizontal=True)
    st.session_state['language'] = lang

ticker = u_input if ".NS" in u_input or ".BO" in u_input else f"{u_input}.NS"

@st.cache_data(ttl=300)
def fetch_all_data(sym):
    t = yf.Ticker(sym)
    return t.info, t.history(period="1y"), t.news

# 5. EXECUTION
try:
    with st.spinner(get_text("Updating...", "தகவல்கள் சேகரிக்கப்படுகிறது...")):
        info, hist, news_list = fetch_all_data(ticker)
    
    ltp = info.get('currentPrice') or hist['Close'].iloc[-1]
    prev_close = info.get('regularMarketPreviousClose') or hist['Close'].iloc[-2]
    change = ltp - prev_close
    h52, l52 = info.get('fiftyTwoWeekHigh', ltp), info.get('fiftyTwoWeekLow', ltp)
    r_pos = ((ltp - l52) / (h52 - l52) * 100) if (h52 - l52) != 0 else 50

    # 7 PRO TABS
    tabs = st.tabs([
        get_text("Price", "விலை நிலவரம்"), 
        get_text("Technicals", "தொழில்நுட்பம்"), 
        get_text("Fundamentals", "அடிப்படை ஆய்வு"),
        get_text("Shareholding", "பங்குதாரர்கள்"),
        get_text("Financials", "நிதிநிலை"),
        get_text("About", "நிறுவனம் பற்றி"),
        get_text("News", "செய்திகள்")
    ])

    # TAB 1: OVERVIEW
    with tabs[0]:
        clr = "#39FF14" if change >= 0 else "#FF4455"
        st.markdown(f"""
        <div class="price-card">
            <div style="color:#5a7a9a; font-size:16px; font-weight:700;">{info.get('longName', ticker)}</div>
            <div class="ltp-price">Rs.{ltp:,.2f}</div>
            <div style="color:{clr}; font-weight:800; font-size:20px;">{change:+.2f} ({(change/prev_close*100):+.2f}%)</div>
            <div class="range-container"><div class="range-bar"></div><div class="range-marker" style="left:{r_pos}%;"></div></div>
            <div style="display:flex; justify-content:space-between; font-size:13px; color:#5a7a9a; font-weight:700;">
                <span>52W LOW: Rs.{l52:,.2f}</span><span>52W HIGH: Rs.{h52:,.2f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='#020509', plot_bgcolor='#080f18', height=450, margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

    # TAB 2: TECHNICALS
    with tabs[1]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        rsi_val = 72.5 # Example or calc
        t_data = [("RSI (14)", f"{rsi_val}"), ("Day High", f"Rs.{info.get('dayHigh',0):,.2f}"), ("Day Low", f"Rs.{info.get('dayLow',0):,.2f}")]
        for l, v in t_data:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 3 & 4 & 5 (Summary)
    with tabs[2]:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        f_data = [("Market Cap", f"Rs.{info.get('marketCap',0)/1e7:,.2f} Cr"), ("P/E Ratio", str(info.get('trailingPE','N/A'))), ("ROE", f"{(info.get('returnOnEquity',0)*100):.2f}%")]
        for l, v in f_data:
            st.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # TAB 6: ABOUT (WITH TRANSLATION)
    with tabs[5]:
        st.markdown(f"### {get_text('Company Description', 'நிறுவனம் பற்றிய விளக்கம்')}")
        raw_desc = info.get('longBusinessSummary', "No Summary.")
        
        if st.session_state['language'] == "Tamil":
            try:
                translated_desc = GoogleTranslator(source='auto', target='ta').translate(raw_desc)
                st.markdown(f'<div class="section-card" style="line-height:1.8; font-size:16px;">{translated_desc}</div>', unsafe_allow_html=True)
            except:
                st.markdown(f'<div class="section-card" style="line-height:1.8; font-size:16px;">{raw_desc}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="section-card" style="line-height:1.8; font-size:16px;">{raw_desc}</div>', unsafe_allow_html=True)

    # TAB 7: NEWS (FIXING 'LINK' ERROR)
    with tabs[6]:
        if news_list:
            for n in news_list:
                # SAFE ACCESS TO KEY 'link'
                n_link = n.get('link', '#')
                n_title = n.get('title', 'News')
                n_pub = n.get('publisher', 'Unknown')
                st.markdown(f"""
                <div class="section-card">
                    <div style="font-weight:800; font-size:16px;"><a href="{n_link}" target="_blank" style="color:#39FF14; text-decoration:none;">{n_title}</a></div>
                    <div style="font-size:13px; color:#5a7a9a; margin-top:5px;">Source: {n_pub}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No news available.")

except Exception as e:
    st.error(f"Error: {e}")

# FOOTER
st.markdown('<div style="text-align:center; padding:30px; border-top:1px solid #1a2535; font-size:12px; color:#5a7a9a;">2026 TAMIL INVEST HUB PRO - Created by Somasundaram</div>', unsafe_allow_html=True)
