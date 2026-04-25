import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# செஷன் ஸ்டேட் - தரவுகள் சேமிக்க (மிக முக்கியம்)
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

# மொழிபெயர்ப்பு உதவியாளர்
def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. பிரீமியம் CSS (UI மேம்பாடு)
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
    
    .metric-row {{ background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }}
    .m-label {{ color: #ffffff !important; font-size: 11px; text-transform: uppercase; opacity: 0.8; }}
    .m-value {{ color: #ffffff !important; font-size: 16px; font-weight: bold; }}
    
    .rating-card {{ padding: 25px; border-radius: 15px; text-align: center; margin: 15px 0; border: 2px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.05); }}
    .score-text {{ font-size: 50px; font-weight: 900; margin: 5px 0; }}
    </style>
    """, unsafe_allow_html=True)

# 3. சைடுபார் (Sidebar)
with st.sidebar:
    st.markdown(f"### 👤 {get_text('User Profile', 'பயனர் விவரம்')}")
    st.info("Somasundaram (Premium)")
    
    st.divider()
    lang_choice = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)
    st.session_state['language'] = lang_choice
    
    st.divider()
    st.markdown(f"### 💼 {get_text('Broker Connect', 'புரோக்கர் இணைப்பு')}")
    st.button("🔗 Zerodha", use_container_width=True)
    st.button("🔗 Angel One", use_container_width=True)

# 4. டிக்கர் மற்றும் தலைப்பு
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

# 5. சர்ச் மற்றும் டேப்கள்
u_input = st.text_input("Search", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# டேட்டா லோடிங் (Try-Except Error Handling)
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
    # --- ANALYSIS TAB ---
    with tabs[0]:
        st.markdown(f"### {info.get('longName', u_input)}")
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">PRICE (LTP)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W LOW</span><br><span class="m-value">₹{info.get("fiftyTwoWeekLow", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W HIGH</span><br><span class="m-value">₹{info.get("fiftyTwoWeekHigh", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E RATIO</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # --- SHAREHOLDING TAB ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = info.get('heldPercentInsiders', 0) * 100
        inst = info.get('heldPercentInstitutions', 0) * 100
        public = 100 - (promo + inst)
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, max(0, public)], hole=0.5)])
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- RATING TAB ---
    with tabs[2]:
        st.markdown(f"### {get_text('Quality Rating Score', 'தர மதிப்பீடு')}")
        score = 0
        pe = info.get('trailingPE', 100)
        roe = info.get('returnOnEquity', 0)
        if pe < 30: score += 40
        if roe > 0.15: score += 40
        if ltp > hist['Close'].rolling(50).mean().iloc[-1]: score += 20
        
        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        st.markdown(f'<div class="rating-card"><p class="score-text" style="color:{color};">{score}/100</p></div>', unsafe_allow_html=True)

    # --- CORPORATE ACTIONS TAB ---
    with tabs[3]:
        st.markdown(f"### {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        acts = stock_obj.actions.tail(10).sort_index(ascending=False)
        if not acts.empty:
            st.table(acts)
        else:
            st.info("No recent actions.")

    # --- WATCHLIST TAB ---
    with tabs[4]:
        st.markdown(f"### {get_text('My Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        
        st.divider()
        for item in st.session_state['watchlist']:
            cw1, cw2 = st.columns([5, 1])
            cw1.write(f"📌 **{item}**")
            if cw2.button("Remove", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("Loading Stock Data... Please enter a valid symbol (eg: TCS, RELIANCE).")

st.markdown("<p style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
