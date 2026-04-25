import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# செஷன் ஸ்டேட் - தரவுகளைச் சேமிக்க
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

# மொழிபெயர்ப்பு உதவியாளர்
def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. நவீன UI (Sleek High-End Design)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: 14px !important; background-color: #0d1117; color: #ffffff; }}
    
    /* Header Style */
    .header-container {{ text-align: center; padding: 15px 0; }}
    .main-title {{ 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }}
    .sub-title {{ font-size: 10px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.6; }}
    
    /* Analysis Metric Cards */
    .metric-card {{
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }}
    .m-label {{ color: #8b949e !important; font-size: 11px; text-transform: uppercase; font-weight: 700; }}
    .m-value {{ color: #ffffff !important; font-size: 17px; font-weight: 800; }}
    
    /* Rating Card */
    .rating-card {{ 
        padding: 25px; border-radius: 15px; text-align: center; 
        margin: 15px 0; border: 2px solid rgba(255,255,255,0.1); 
        background: rgba(255,255,255,0.05); 
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி தேர்வு (Top Menu)
col_lang1, col_lang2 = st.columns([8, 2])
with col_lang2:
    lang_btn = st.radio("Language", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    st.session_state['language'] = lang_btn

# 4. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE)", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

# 6. டேப்கள் (Tabs)
tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# டேட்டா லோடிங் செக்ஷன்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and 'symbol' in info:
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    # --- Analysis Tab ---
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        metrics = [
            ("LTP (Price)", f"₹{ltp:,.2f}"),
            ("52W High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            ("52W Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}"),
            ("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
        ]
        for label, value in metrics:
            st.markdown(f'<div class="metric-card"><span class="m-label">{label}</span><span class="m-value">{value}</span></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # --- Shareholding (FII/DII) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = inst - fii
        pub = max(0, 100 - (promo + inst))
        
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
        fig_pie.update_layout(height=400, template="plotly_dark")
        st.plotly
