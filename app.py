import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# செஷன் ஸ்டேட் (Watchlist தரவுகளைச் சேமிக்க)
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உயர் ரக நவீன UI (Sleek High-End Design)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    
    /* Sleek Header */
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; text-transform: lowercase; letter-spacing: 2px; opacity: 0.6; }
    
    /* Modern Watchlist Card */
    .watchlist-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .stock-name { font-size: 16px; font-weight: 700; color: #ffffff; }
    
    /* Rating Card */
    .rating-card { padding: 20px; border-radius: 12px; text-align: center; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.03); }
    .score-text { font-size: 42px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச் மற்றும் டேப்கள்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 5. டேட்டா லோடிங் (Safety Checks)
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    # --- TAB 1: ANALYSIS ---
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        st.metric(label="Price", value=f"₹{ltp:,.2f}")
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: SHAREHOLDING ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        pub = max(0, 100 - (promo + inst))
        
        if promo + inst > 0:
            fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, pub], hole=0.5)])
            fig_pie.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.warning("தரவுகள் கிடைக்கவில்லை (Data Not Available).")

    # --- TAB 3: RATING ---
    with tabs[2]:
        st.markdown(f"### {get_text('Quality Score', 'பங்கின் தரம்')}")
        score = 0
        pe = info.get('trailingPE', 0)
        roe = info.get('returnOnEquity', 0)
        if 0 < pe < 30: score += 40
        if roe > 0.15: score += 40
        if not hist.empty and ltp > hist['Close'].rolling(50).mean().iloc[-1]: score += 20
        
        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        st.markdown(f'<div class="rating-card"><p class="score-text" style="color:{color};">{score}/100</p></div>', unsafe_allow_html=True)

    # --- TAB 4: ACTIONS ---
    with tabs[3]:
        st.markdown(f"### {get_text('Corporate Actions', 'நிகழ்வுகள்')}")
        acts = stock_obj.actions
        if not acts.empty:
            st.dataframe(acts.tail(10).sort_index(ascending=False), use_container_width=True)
        else:
            st.info("சமீபத்திய நிகழ்வுகள் ஏதுமில்லை.")

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        st.markdown(f"### {get_text('My Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ {get_text('Add', 'சேர்')} {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        
        st.divider()
        if st.session_state['watchlist']:
            for stock in st.session_state['watchlist']:
                col_w1, col_w2 = st.columns([5, 1])
                col_w1.markdown(f'<div class="watchlist-card"><span class="stock-name">📌 {stock}</span></div>', unsafe_allow_html=True)
                if col_w2.button("❌", key=f"del_{stock}"):
                    st.session_state['watchlist'].remove(stock)
                    st.rerun()
        else:
            st.write("வாட்ச்லிஸ்ட் காலியாக உள்ளது.")

else:
    st.info("Loading Stock Data... சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center;color:#444;font-size:11px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
