import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உயர் ரக நவீன UI (Sleek High-End Design)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: 14px !important; background-color: #0d1117; color: #ffffff; }}
    
    /* Sleek Header */
    .header-container {{ text-align: center; padding: 15px 0; }}
    .main-title {{ 
        font-size: 30px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }}
    .sub-title {{ font-size: 10px !important; color: #8b949e; text-transform: lowercase; letter-spacing: 2px; opacity: 0.6; }}
    
    /* Modern Watchlist Card */
    .watchlist-card {{
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 12px 20px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: 0.3s;
    }}
    .watchlist-card:hover {{
        background: rgba(57, 255, 20, 0.05);
        border-color: #39FF14;
    }}
    .stock-name {{ font-size: 16px; font-weight: 700; color: #ffffff; }}
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

# 5. வாட்ச்லிஸ்ட் பகுதி (சரிசெய்யப்பட்டது)
with tabs[4]:
    st.markdown(f"### {get_text('My Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
    
    # ஸ்டாக் சேர்க்கும் பட்டன்
    if st.button(f"➕ {get_text('Add', 'சேர்')} {u_input}", use_container_width=True):
        if u_input not in st.session_state['watchlist']:
            st.session_state['watchlist'].append(u_input)
            st.rerun()

    st.markdown("---")

    # வாட்ச்லிஸ்ட் கார்டுகள்
    if st.session_state['watchlist']:
        for stock in st.session_state['watchlist']:
            # பிரீமியம் கார்டு அமைப்பு
            col_name, col_btn = st.columns([4, 1])
            
            with col_name:
                st.markdown(f"""
                    <div class="watchlist-card">
                        <span class="stock-name">📌 {stock}</span>
                    </div>
                """, unsafe_allow_html=True)
            
            with col_btn:
                # நீக்கும் வசதி
                if st.button(f"❌", key=f"remove_{stock}"):
                    st.session_state['watchlist'].remove(stock)
                    st.rerun()
    else:
        st.info(get_text("Your watchlist is empty.", "உங்கள் வாட்ச்லிஸ்ட் காலியாக உள்ளது."))

# டேட்டா லோடிங் (மற்ற டேப்கள் வேலை செய்ய)
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and 'symbol' in info:
        hist = stock_obj.history(period="1y")
        
        with tabs[0]:
            st.markdown(f"#### {info.get('longName', u_input)}")
            st.line_chart(hist['Close'])
except:
    pass

st.markdown("<p style='text-align:center;color:#444;font-size:11px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
