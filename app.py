import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# செஷன் ஸ்டேட் (Session State) - தகவல்களைச் சேமிக்க
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'portfolio' not in st.session_state: st.session_state['portfolio'] = {"balance": 0.0, "stocks": []}
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

# மொழிபெயர்ப்பு ஃபங்க்ஷன்
@st.cache_data(show_spinner=False)
def get_text(en_text, ta_text):
    return ta_text if st.session_state['language'] == "Tamil" else en_text

# 2. பிரீமியம் CSS (Themes & Settings)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: 15px !important; background-color: #0d1117; color: #ffffff; }}
    
    .ticker-wrap {{ width: 100%; overflow: hidden; background: #161b22; border-bottom: 2px solid #39FF14; padding: 12px 0; position: sticky; top: 0; z-index: 999; }}
    .ticker-move {{ display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 14px; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    .main-title {{ 
        text-align: center; font-size: 45px !important; font-weight: 950; 
        background: linear-gradient(90deg, #39FF14, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(57, 255, 20, 0.4);
    }}
    
    .profile-card {{ background: #1c2128; border-radius: 15px; padding: 20px; border: 1px solid #30363d; margin-bottom: 20px; }}
    .broker-btn {{ background: #39FF14; color: black; font-weight: bold; padding: 10px; border-radius: 8px; text-align: center; cursor: pointer; margin-bottom: 10px; }}
    
    .metric-row {{ background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }}
    .m-label {{ color: #ffffff !important; font-size: 11px; text-transform: uppercase; opacity: 0.8; }}
    .m-value {{ color: #ffffff !important; font-size: 15px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# 3. சைடுபார் (Sidebar) - Profile, Settings, & Broker
with st.sidebar:
    st.markdown(f"### 👤 {get_text('User Profile', 'பயனர் விவரம்')}")
    st.markdown('<div class="profile-card"><b>Somasundaram</b><br><small>Premium Member</small></div>', unsafe_allow_html=True)
    
    st.divider()
    
    # மொழி தேர்வு (Language Option)
    st.markdown(f"### 🌐 {get_text('Language', 'மொழி')}")
    lang_choice = st.radio("Select Language", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    st.session_state['language'] = lang_choice
    
    st.divider()
    
    # புரோக்கர் இணைப்பு (Broker Connect)
    st.markdown(f"### 💼 {get_text('Connect Broker', 'புரோக்கர் இணைப்பு')}")
    if st.button("🔗 Connect Zerodha", use_container_width=True): st.success("Connected!")
    if st.button("🔗 Connect Angel One", use_container_width=True): st.success("Connected!")
    
    st.divider()
    
    # செட்டிங்ஸ் (Settings & Theme)
    st.markdown(f"### ⚙️ {get_text('Settings', 'அமைப்பு')}")
    theme = st.selectbox("Theme", ["Dark Mode", "High Contrast", "OLED Black"])
    st.toggle("Notification Alerts", value=True)

# 4. லைவ் டிக்கர் மற்றும் தலைப்பு
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#39FF14" if c >= 0 else "#FF3131"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 5. முக்கிய தேடல் மற்றும் டேப்கள்
u_input = st.text_input("Search", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"📝 {get_text('Overview', 'விளக்கம்')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Ratings', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# டேட்டா லோடிங்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")
    stock_loaded = True
except: stock_loaded = False

if stock_loaded:
    with tabs[0]:
        st.markdown(f"### {info.get('longName', u_input)}")
        ltp = info.get('currentPrice', 0)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">LTP</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get("fiftyTwoWeekLow", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W High</span><br><span class="m-value">₹{info.get("fiftyTwoWeekHigh", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown(f"### {get_text('Business Overview', 'நிறுவன விளக்கம்')}")
        summary = info.get('longBusinessSummary', 'No Summary')
        st.write(ta_text := (GoogleTranslator(source='en', target='ta').translate(summary[:1000]) if st.session_state['language']=="Tamil" else summary))

    with tabs[5]:
        st.markdown(f"### {get_text('Your Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ {get_text('Add to Watchlist', 'வாட்ச்லிஸ்டில் சேர்')}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        st.write(st.session_state['watchlist'])

else:
    st.info("Loading Stock Data...")

st.markdown("<p style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
