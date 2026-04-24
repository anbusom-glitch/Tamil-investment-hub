import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# மொழிபெயர்ப்பு லைப்ரரியை பாதுகாப்பாக கையாளுதல்
try:
    from googletrans import Translator
    translator = Translator()
    has_translator = True
except Exception:
    has_translator = False

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. ஸ்மார்ட் சர்ச் மேப்பிங்
def get_ticker_from_name(name):
    name = name.upper().strip()
    mapping = {
        "SBI": "SBIN.NS", "RELIANCE": "RELIANCE.NS", "COAL INDIA": "COALINDIA.NS",
        "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS", "INFOSYS": "INFY.NS"
    }
    if name in mapping: return mapping[name]
    return f"{name}.NS" if ".NS" not in name else name

# 3. மொழித் தரவுகள்
lang_dict = {
    "English": {
        "title": "TAMIL INVEST HUB", "analysis": "🔍 Analysis", "search": "Search Stock (e.g. SBI, Reliance)",
        "ltp": "Price", "pe": "P/E", "pb": "P/B", "52wh": "52W High", "52wl": "52W Low",
        "holders": "Shareholding", "about": "About Company", "news": "News Feed"
    },
    "Tamil": {
        "title": "தமிழ் இன்வெஸ்ட் ஹப்", "analysis": "🔍 ஆய்வு", "search": "பங்கின் பெயர் (eg: SBI, Reliance):",
        "ltp": "விலை", "pe": "P/E", "pb": "P/B", "52wh": "52 வார உயர்வு", "52wl": "52 வாரத் தாழ்வு",
        "holders": "பங்குதாரர் விவரம்", "about": "நிறுவனத்தைப் பற்றி", "news": "நேரலைச் செய்திகள்"
    }
}

# 4. CSS
st.markdown("<style>html,body,[class*='css']{font-size:12px!important;background-color:#0d1117;color:#c9d1d9;}.header-text{background:linear-gradient(90deg,#ffd700,#b8860b);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:22px!important;font-weight:800;text-align:center;}[data-testid='stMetric']{background:#161b22;border:1px solid #30363d;border-radius:8px;padding:5px!important;}</style>", unsafe_allow_html=True)

# 5. மொழித் தேர்வு (Sidebar)
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 6. லோகோ & தலைப்பு
logo_b64 = get_base64_logo("logo.png")
if logo_b64:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:60px;border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2 = st.tabs([L["analysis"], L["news"]])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA")
    ticker = get_ticker_from_name(u_input)
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        st.markdown(f"**{info.get('longName', ticker)}**")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(L["ltp"], f"₹{price:,.1f}")
        m2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        m3.metric(L["pb"], f"{info.get('priceToBook', 'N/A')}")
        m4.metric("PEG", f"{info.get('pegRatio', 'N/A')}")

        h1, h2 = st.columns(2)
        h1.metric(L["52wh"], f"₹{info.get('fiftyTwoWeekHigh', 0):,.1f}")
        h2.metric(L["52wl"], f"₹{info.get('fiftyTwoWeekLow', 0):,.1f}")

        # Chart
        hist = stock.history(period="1y")
        if not hist.empty:
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700'))])
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # Shareholding
        st.markdown(f"**{L['holders']}**")
        p = info.get('heldPercentInsiders', 0.5) * 100
        fii = info.get('heldPercentInstitutions', 0.2) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, fii, 100-(p+fii)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=220, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

        # About
        with st.expander(L["about"]):
            summary = info.get('longBusinessSummary', 'N/A')
            if sel_lang == "Tamil" and has_translator:
                try:
                    summary = translator.translate(summary, dest='ta').text
                except: pass
            st.write(summary)

    except Exception: st.info("Loading Stock Data...")

with tab2:
    try:
        for n in stock.news[:8]:
            st.markdown(f'<div style="background:#161b22;padding:10px;border-radius:8px;margin-bottom:8px;border-left:3px solid #ffd700;"><a href="{n["link"]}" target="_blank" style="color:#ffd700;text-decoration:none;font-weight:600;">{n["title"]}</a></div>', unsafe_allow_html=True)
    except: st.write("News not available.")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
