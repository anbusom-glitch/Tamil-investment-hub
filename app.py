import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. நவீன UI (Sleek High-End Design)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: 14px !important; background-color: #0d1117; color: #ffffff; }}
    
    .header-container {{ text-align: center; padding: 15px 0; }}
    .main-title {{ 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }}
    .sub-title {{ font-size: 10px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.6; }}
    
    .metric-card {{
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }}
    .m-label {{ color: #8b949e !important; font-size: 11px; text-transform: uppercase; font-weight: 700; }}
    .m-value {{ color: #ffffff !important; font-size: 17px; font-weight: 800; }}
    
    .rating-card {{ 
        padding: 25px; border-radius: 15px; text-align: center; 
        margin: 15px 0; border: 2px solid rgba(255,255,255,0.1); 
        background: rgba(255,255,255,0.05); 
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி தேர்வு
col_lang1, col_lang2 = st.columns([8, 2])
with col_lang2:
    lang_btn = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    st.session_state['language'] = lang_btn

# 4. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. டேட்டா லோடிங்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and 'symbol' in info:
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except: stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    # Analysis Tab
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        st.markdown(f'<div class="metric-card"><span class="m-label">LTP</span><span class="m-value">₹{ltp:,.2f}</span></div>',
