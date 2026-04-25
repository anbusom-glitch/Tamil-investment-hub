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

# 2. உலகத்தரம் வாய்ந்த UI (Sleek High-End Design)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    
    /* Header Style */
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; text-transform: lowercase; letter-spacing: 2px; opacity: 0.6; }
    
    /* Analysis Metric Cards - High Look */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .m-label { color: #8b949e !important; font-size: 11px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff !important; font-size: 18px; font-weight: 800; }
    
    /* Rating & Watchlist Cards */
    .custom-card { padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1); background: rgba(255,255,255,0.03); margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 5. டேட்டா லோடிங்
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

    # --- TAB 1: ANALYSIS (இங்கு தான் மாற்றங்கள் செய்யப்பட்டுள்ளன) ---
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        
        # மெட்ரிக்ஸ் - ஒவ்வொன்றும் தனித்தனி கார்டுகளாக (Vertical Stack for Mobile)
        metrics = [
            ("LTP (Price)", f"₹{ltp:,.2f}"),
            ("52W High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            ("52W Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}"),
            ("P/E Ratio", f"{info.get('trailingPE', 'N/A')}"),
            ("P/B Ratio", f"{info.get('priceToBook', 'N/A')}"),
            ("PEG Ratio", f"{info.get('pegRatio', 'N/A')}")
        ]
        
        for label, value in metrics:
            st.markdown(f"""
                <div class="metric-card">
                    <span class="m-label">{label}</span>
                    <span class="m-value">{value}</span>
                </div>
            """, unsafe_allow_html=True)
        
        # சார்ட்
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: SHAREHOLDING ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        pub = max(0, 100 - (promo + inst))
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, pub], hole=0.5)])
        fig_pie.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 3: RATING ---
    with tabs[2]:
        st.markdown(f"### {get_text('Rating Score', 'தர மதிப்பீடு')}")
        score = 0
        pe_val = info.get('trailingPE', 100)
        roe_val = info.get('returnOnEquity', 0)
        if 0 < pe_val < 30: score += 40
        if roe_val > 0.15: score += 40
        if ltp > (hist['Close'].rolling(50).mean().iloc[-1] if not hist.empty else 0): score += 20
        
        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        st.markdown(f'<div class="custom-card" style="text-align:center;"><h1 style="color:{color}; font-size:48px;">{score}/100</h1></div>', unsafe_allow_html=True)

    # --- TAB 4: ACTIONS ---
    with tabs[3]:
        st.markdown(f"### {get_text('Actions', 'நிகழ்வுகள்')}")
        st.dataframe(stock_obj.actions.tail(10), use_container_width=True)

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        st.markdown(f"### {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        for item in st.session_state['watchlist']:
            col_w1, col_w2 = st.columns([5, 1])
            col_w1.markdown(f'<div class="custom-card">📌 {item}</div>', unsafe_allow_html=True)
            if col_w2.button("❌", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("Loading Stock Data... (eg: RELIANCE, TCS)")

st.markdown("<p style='text-align:center;color:#444;font-size:11px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
