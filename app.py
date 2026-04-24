import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# லோகோ வசதி
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. டிக்கர் தகவல்கள் (Nifty, Sensex & Watchlist)
def get_ticker_data(watchlist):
    tickers = ["^NSEI", "^BSESN"] + watchlist
    ticker_text = ""
    for t in tickers:
        try:
            data = yf.Ticker(t).fast_info
            price = data['last_price']
            chg = data['year_change'] * 100 if 'year_change' in data else 0
            color = "green" if chg >= 0 else "red"
            symbol = t.replace(".NS", "").replace("^", "")
            ticker_text += f" | {symbol}: <span style='color:{color};'>₹{price:,.1f} ({chg:.1f}%)</span> "
        except: continue
    return ticker_text

# 3. ஸ்மார்ட் சர்ச்
def get_symbol(name):
    mapping = {"SBI": "SBIN.NS", "RELIANCE": "RELIANCE.NS", "COAL INDIA": "COALINDIA.NS", "TCS": "TCS.NS"}
    name = name.upper().strip()
    return mapping.get(name, f"{name}.NS" if ".NS" not in name else name)

# 4. பிரீமியம் CSS (Ticker Animation சேர்த்து)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    
    /* லைவ் டிக்கர் ஸ்டைல் */
    .ticker-wrapper {
        width: 100%; overflow: hidden; background: #161b22; 
        border-bottom: 1px solid #ffd700; padding: 5px 0;
        position: sticky; top: 0; z-index: 999;
    }
    .ticker-text {
        display: inline-block; white-space: nowrap;
        animation: marquee 30s linear infinite; font-weight: bold;
    }
    @keyframes marquee {
        0% { transform: translateX(100%); }
        100% { transform: translateX(-100%); }
    }

    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. செஷன் ஸ்டேட் (Watchlist பராமரிக்க)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["RELIANCE.NS", "SBIN.NS"]

# 6. லைவ் டிக்கர் (Top Row)
ticker_content = get_ticker_data(st.session_state.watchlist)
st.markdown(f'<div class="ticker-wrapper"><div class="ticker-text">{ticker_content} {ticker_content}</div></div>', unsafe_allow_html=True)

# 7. மொழித் தேர்வு
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = {"English": {"search": "Search Stock", "52wh": "52W High", "52wl": "52W Low", "about": "About Company"},
         "Tamil": {"search": "பங்கின் பெயர்", "52wh": "52 வார உயர்வு", "52wl": "52 வாரத் தாழ்வு", "about": "நிறுவனத்தைப் பற்றி"}}[sel_lang]

# 8. லோகோ & தலைப்பு
logo_b64 = get_base64_logo("logo.png")
if logo_b64:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:50px; border-radius:8px;"></div>', unsafe_allow_html=True)
st.markdown(f'<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 9. மெயின் ஆப் (TABS)
tab1, tab2 = st.tabs(["🔍 Analysis", "🗞️ News"])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA")
    ticker = get_symbol(u_input)
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        st.markdown(f"### {info.get('longName', ticker)}")
        
        # Metrics
        m1, m2, m3 = st.columns(3)
        m1.metric("LTP", f"₹{price:,.1f}")
        m2.metric(L["52wh"], f"₹{info.get('fiftyTwoWeekHigh', 0):,.1f}")
        m3.metric(L["52wl"], f"₹{info.get('fiftyTwoWeekLow', 0):,.1f}")

        # Chart Period & Style
        p_col, s_col = st.columns(2)
        period = p_col.select_slider("Period", options=["1d", "5d", "1mo", "1y"], value="1mo")
        c_type = s_col.radio("Style", ["Line", "Candle"], horizontal=True)

        hist = stock.history(period=period)
        fig = go.Figure()
        if c_type == "Line":
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700')))
        else:
            fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']))
        
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Shareholding Pattern
        st.markdown("**Shareholding Pattern**")
        p = info.get('heldPercentInsiders', 0.5) * 100
        fii = info.get('heldPercentInstitutions', 0.2) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, fii, 100-(p+fii)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=200, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

        # 10. நிறுவனத்தைப் பற்றி (Expander with Info)
        with st.expander(L["about"]):
            st.write(info.get('longBusinessSummary', 'No info.'))
            if st.button("➕ Add to Watchlist"):
                if ticker not in st.session_state.watchlist:
                    st.session_state.watchlist.append(ticker)
                    st.success("Added to Ticker!")
                    st.rerun()

    except: st.info("Loading Data...")

with tab2:
    for n in stock.news[:8]:
        st.markdown(f'<div class="news-card"><a href="{n["link"]}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n["title"]}</a></div>', unsafe_allow_html=True)

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
