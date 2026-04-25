import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# அதிவேக மொழிபெயர்ப்பு
@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(str(text)[:1000])
    except: return str(text)

# 2. பிரீமியம் CSS (Bright Header & Professional UI)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #0d1117; color: #c9d1d9; }
    
    /* டிக்கர் */
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 2px solid #f85149; padding: 10px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 11px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* பிரகாசமான தலைப்பு (Bright Neon Gradient Title) */
    .header-container { text-align: center; margin: 15px 0; }
    .main-title { 
        font-size: 34px !important; 
        font-weight: 950; 
        margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #FF3131); /* Bright Neon Green & Red */
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(57, 255, 20, 0.4); /* Glow effect */
        letter-spacing: 1px;
    }
    .sub-title { font-size: 11px !important; color: #ffffff; font-style: italic; margin-top: -5px; opacity: 0.8; }
    
    /* மெட்ரிக்ஸ் */
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 6px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #ffffff !important; font-size: 8.5px; text-transform: uppercase; font-weight: 500; opacity: 0.9; }
    .m-value { color: #ffffff !important; font-size: 12px; font-weight: bold; }
    
    /* நியூஸ் கார்டு */
    .news-card { background: #161b22; border-radius: 6px; padding: 10px; margin-bottom: 8px; border-left: 4px solid #FF3131; }
    
    /* ரேட்டிங் பாக்ஸ் */
    .rating-box { padding: 12px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 14px; margin: 10px 0; border: 1px solid rgba(255,255,255,0.2); }
    
    [data-testid="stHeader"] { height: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. லைவ் டிக்கர்
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

# பிரகாசமான பிராண்ட் ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

# 5. டேப்கள்
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Analysis", "⭐ Ratings", "🔮 Forecast", "📅 Action", "🗞️ News", "📌 Watchlist"
])

stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")
    if 'symbol' in info:
        stock_loaded = True
except:
    pass

# TAB 1: ANALYSIS
with tab1:
    if stock_loaded:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; color:white;'>{info.get('longName')}</p>", unsafe_allow_html=True)
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">PRICE (LTP)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E RATIO</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        with col_m2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">MARKET CAP</span><br><span class="m-value">₹{info.get("marketCap", 0)//10**7:,.0f} Cr</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">ROE</span><br><span class="m-value">{info.get("returnOnEquity", 0)*100:.2f}%</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=280, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Loading Stock Data...")

# TAB 2: RATINGS
with tab2:
    if stock_loaded:
        st.markdown("### Stock Ratings & 3D Pattern")
        score = 0
        ltp = info.get('currentPrice', 0)
        ma50 = hist['Close'].rolling(50).mean().iloc[-1]
        if info.get('trailingPE', 100) < 30: score += 1
        if info.get('returnOnEquity', 0) > 0.15: score += 1
        if ltp > ma50: score += 1

        if score == 3: st.markdown('<div class="rating-box" style="background:#39FF14; color:black;">STRONG BUY 🚀</div>', unsafe_allow_html=True)
        elif score == 2: st.markdown('<div class="rating-box" style="background:#ffd700; color:black;">HOLD ⚖️</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="rating-box" style="background:#FF3131; color:white;">AVOID ⚠️</div>', unsafe_allow_html=True)
        
        p, i = info.get('heldPercentInsiders', 0)*100, info.get('heldPercentInstitutions', 0)*100
        fig_3d = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[p, i, 100-(p+i)], hole=.6, pull=[0.1, 0, 0])])
        st.plotly_chart(fig_3d, use_container_width=True)

# TAB 3: FORECAST
with tab3:
    if stock_loaded:
        target = info.get('targetMeanPrice')
        if target:
            ltp = info.get('currentPrice', 1)
            upside = ((target - ltp) / ltp) * 100
            st.metric("எதிர்பார்க்கப்படும் இலக்கு (Target)", f"₹{target:,.2f}", f"{upside:.2f}% Upside")
        else: st.info("தரவுகள் கிடைக்கவில்லை.")

# TAB 4: ACTION
with tab4:
    if stock_loaded:
        st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)

# TAB 5: NEWS
with tab5:
    if stock_loaded:
        for n in stock_obj.news[:5]:
            st.markdown(f'<div class="news-card"><a href="{n["link"]}" target="_blank" style="color:#FF3131; font-weight:bold; text-decoration:none;">{n["title"]}</a></div>', unsafe_allow_html=True)

# TAB 6: WATCHLIST
with tab6:
    st.markdown("### My Watchlist")
    if st.button(f"➕ Add {u_input} to Watchlist"):
        if u_input not in st.session_state['watchlist']:
            st.session_state['watchlist'].append(u_input)
            st.rerun()
    
    st.divider()
    if st.session_state['watchlist']:
        for item in st.session_state['watchlist']:
            cw1, cw2 = st.columns([4, 1])
            cw1.write(f"📌 {item}")
            if cw2.button("Remove", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()
    else: st.write("வாட்ச்லிஸ்ட் காலியாக உள்ளது.")

st.markdown("<div style='text-align:center;color:#444;font-size:9px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</div>", unsafe_allow_html=True)
