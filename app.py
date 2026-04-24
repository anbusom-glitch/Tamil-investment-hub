import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import base64

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TS INVEST PRO", page_icon="📈", layout="wide")

# லோகோவை Base64-ஆக மாற்றும் வசதி
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. இருமொழி வசதிக்கான தரவுகள் (Language Dictionary)
lang_dict = {
    "English": {
        "title": "TS INVEST PRO",
        "analysis": "🔍 Analysis",
        "broker": "💼 Broker Connect",
        "feed": "🗞️ Market Feed",
        "search_label": "Enter Ticker (e.g. SBIN.NS)",
        "ltp": "LTP",
        "pe": "P/E",
        "pb": "P/B",
        "peg": "PEG",
        "chart_title": "Price Chart",
        "about": "About Company",
        "connect_title": "Connect Your Broker",
        "portfolio": "LIVE PORTFOLIO SUMMARY",
        "news_title": "Live News Feed",
        "lang_select": "Choose Language"
    },
    "Tamil": {
        "title": "TS இன்வெஸ்ட் PRO",
        "analysis": "🔍 ஆய்வு",
        "broker": "💼 புரோக்கர் இணைப்பு",
        "feed": "🗞️ சந்தை செய்திகள்",
        "search_label": "பங்கின் பெயரை உள்ளிடவும் (எ.கா. SBIN.NS)",
        "ltp": "தற்போதைய விலை",
        "pe": "P/E விகிதம்",
        "pb": "P/B விகிதம்",
        "peg": "PEG விகிதம்",
        "chart_title": "விலை வரைபடம்",
        "about": "நிறுவனத்தைப் பற்றி",
        "connect_title": "உங்கள் புரோக்கரை இணைக்கவும்",
        "portfolio": "நேரடி போர்ட்ஃபோலியோ விவரம்",
        "news_title": "நேரலைச் செய்திகள்",
        "lang_select": "மொழியைத் தேர்ந்தெடுக்கவும்"
    }
}

# 3. பிரீமியம் மொபைல் CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; background-color: #0d1117; color: #c9d1d9;
        font-size: 12px !important; line-height: 1.3;
    }
    .header-text {
        background: linear-gradient(90deg, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 22px !important; font-weight: 800; text-align: center;
    }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 5px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ffd700; }
    .stButton>button { width: 100%; border-radius: 6px; height: 32px; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# 4. மொழித் தேர்வு (Sidebar or Top)
with st.sidebar:
    logo_img = get_base64("logo.png")
    if logo_img:
        st.markdown(f'<img src="data:image/png;base64,{logo_img}" style="width:80px; border-radius:10px; margin-bottom:10px;">', unsafe_allow_html=True)
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 5. SPLASH SCREEN
if 'startup' not in st.session_state:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown(f"<div style='height:80vh; display:flex; flex-direction:column; align-items:center; justify-content:center;'><h1 style='color:#ffd700;'>TS INVEST</h1><p>Starting...</p></div>", unsafe_allow_html=True)
        time.sleep(2)
    st.session_state.startup = True
    placeholder.empty()

# 6. HEADER
st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2, tab3 = st.tabs([L["analysis"], L["broker"], L["feed"]])

with tab1:
    search_ticker = st.text_input(L["search_label"], value="SBIN.NS").upper()
    
    try:
        stock = yf.Ticker(search_ticker)
        info = stock.info
        
        # மெட்ரிக்ஸ்
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        st.markdown(f"**{info.get('longName', search_ticker)}**")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(L["ltp"], f"₹{price:,.1f}")
        m2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        m3.metric(L["pb"], f"{info.get('priceToBook', 'N/A')}")
        m4.metric(L["peg"], f"{info.get('pegRatio', 'N/A')}")

        st.divider()

        # வரைபடம் (Chart with Period Selector)
        st.markdown(f"**{L['chart_title']}**")
        period_col, _ = st.columns([2, 1])
        with period_col:
            period = st.radio("", ["1mo", "3mo", "6mo", "1y"], horizontal=True, label_visibility="collapsed")
        
        # தரவுகளைப் பெற்று வரைபடம் வரைதல்
        hist = stock.history(period=period)
        if not hist.empty:
            fig = go.Figure()
            # Area Chart ஸ்டைல்
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist['Close'],
                fill='tozeroy', line=dict(color='#ffd700', width=2),
                name="Price"
            ))
            fig.update_layout(
                height=280, margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, color="#8b949e"),
                yaxis=dict(showgrid=True, gridcolor='#1e2329', side="right", color="#8b949e")
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        else:
            st.warning("No chart data available.")

        with st.expander(L["about"]):
            st.write(info.get('longBusinessSummary', 'N/A'))
            
    except Exception as e:
        st.info("Searching Stock...")

with tab2:
    st.markdown(f"### {L['connect_title']}")
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div style="background:#1c2128; padding:10px; border-radius:10px; text-align:center;">Zerodha<br><span style="color:#2ea043; font-size:10px;">● Ready</span></div>', unsafe_allow_html=True)
        st.button("Link Kite", key="kite")
    with b2:
        st.markdown('<div style="background:#1c2128; padding:10px; border-radius:10px; text-align:center;">Angel One<br><span style="color:#2ea043; font-size:10px;">● Ready</span></div>', unsafe_allow_html=True)
        st.button("Link Angel", key="angel")

    st.divider()
    st.markdown(f"**{L['portfolio']}**")
    p_col1, p_col2 = st.columns(2)
    p_col1.metric("Investment", "₹4.5L")
    p_col2.metric("Current", "₹5.1L", "+₹62K")

with tab3:
    st.markdown(f"### {L['news_title']}")
    try:
        news = yf.Ticker(search_ticker).news[:6]
        for n in news:
            st.markdown(f"""
                <div class="news-card">
                    <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n['title']}</a><br>
                    <span style="color:#666; font-size:10px;">{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b')}</span>
                </div>
            """, unsafe_allow_html=True)
    except:
        st.write("News not available.")

st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:20px;">© 2026 TS INVEST</div>', unsafe_allow_html=True)
