import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from googletrans import Translator
import base64
import time

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# லோகோ வசதி
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

translator = Translator()

# 2. ஸ்மார்ட் சர்ச் மேப்பிங்
def get_ticker_from_name(name):
    name = name.upper().strip()
    mapping = {
        "SBI": "SBIN.NS", "STATE BANK": "SBIN.NS",
        "RELIANCE": "RELIANCE.NS", "RELIANCE INDUSTRIES": "RELIANCE.NS",
        "COAL INDIA": "COALINDIA.NS", "COALINDIA": "COALINDIA.NS",
        "TCS": "TCS.NS", "TATA CONSULTANCY": "TCS.NS",
        "HDFC": "HDFCBANK.NS", "HDFC BANK": "HDFCBANK.NS",
        "INFOSYS": "INFY.NS", "INFY": "INFY.NS",
        "ICICI": "ICICIBANK.NS", "WIPRO": "WIPRO.NS",
        "ADANI": "ADANIENT.NS", "TATA MOTORS": "TATAMOTORS.NS"
    }
    if name in mapping:
        return mapping[name]
    elif not name.endswith(".NS") and not name.endswith(".BO"):
        return f"{name}.NS"
    return name

# 3. மொழித் தரவுகள்
lang_dict = {
    "English": {
        "title": "TAMIL INVEST HUB",
        "analysis": "🔍 Analysis", "broker": "💼 Broker Connect", "feed": "🗞️ Market Feed",
        "search": "Search Stock Name or Symbol (e.g. SBI, Reliance)", "ltp": "LTP", 
        "pe": "P/E", "pb": "P/B", "peg": "PEG", "52wh": "52W High", "52wl": "52W Low",
        "chart": "Price Chart", "holders": "Shareholding Pattern", "about": "About Company", 
        "actions": "Corporate Actions", "news": "Live News Feed"
    },
    "Tamil": {
        "title": "தமிழ் இன்வெஸ்ட் ஹப்",
        "analysis": "🔍 ஆய்வு", "broker": "💼 புரோக்கர் இணைப்பு", "feed": "🗞️ சந்தை செய்திகள்",
        "search": "பங்கின் பெயர் அல்லது குறியீடு (eg: SBI, Reliance):", "ltp": "விலை", 
        "pe": "P/E", "pb": "P/B", "peg": "PEG", "52wh": "52 வார உயர்வு", "52wl": "52 வாரத் தாழ்வு",
        "chart": "விலை வரைபடம்", "holders": "பங்குதாரர் விவரம்", "about": "நிறுவனத்தைப் பற்றி", 
        "actions": "நிறுவன நிகழ்வுகள்", "news": "நேரலைச் செய்திகள்"
    }
}

# 4. மொபைல் CSS
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 10px; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 6px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #ffd700; }
    .stTabs [data-baseweb="tab"] { font-size: 11px !important; padding: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 5. மொழித் தேர்வு
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 6. லோகோ மற்றும் தலைப்பு
logo_base64 = get_base64_logo("logo.png")
if logo_base64:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_base64}" style="width:65px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2, tab3 = st.tabs([L["analysis"], L["broker"], L["feed"]])

with tab1:
    user_input = st.text_input(L["search"], value="COALINDIA")
    ticker = get_ticker_from_name(user_input)
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # 8. முதன்மைத் தகவல்கள் (Metrics)
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        st.markdown(f"**{info.get('longName', ticker)}**")
        
        # முதல் வரிசை மெட்ரிக்ஸ்
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(L["ltp"], f"₹{price:,.1f}")
        m2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        m3.metric(L["pb"], f"{info.get('priceToBook', 'N/A')}")
        m4.metric(L["peg"], f"{info.get('pegRatio', 'N/ раз')}")

        # இரண்டாவது வரிசை: 52 வாரத் தகவல்கள்
        h1, h2, h3 = st.columns([1, 1, 2])
        high_52 = info.get('fiftyTwoWeekHigh', 0)
        low_52 = info.get('fiftyTwoWeekLow', 0)
        h1.metric(L["52wh"], f"₹{high_52:,.1f}")
        h2.metric(L["52wl"], f"₹{low_52:,.1f}")
        
        st.divider()

        # 9. வரைபடம் (Dynamic Chart)
        period = st.select_slider("", options=["1d", "5d", "1mo", "1y"], value="1y")
        hist = stock.history(period=period)
        if not hist.empty:
            is_up = price >= info.get('regularMarketPreviousClose', 0)
            color = '#2ea043' if is_up else '#f85149'
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color=color, width=2))])
            fig.update_layout(height=260, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # 10. பங்குதாரர் விவரம் (Donut Chart)
        st.markdown(f"**{L['holders']}**")
        promoter = info.get('heldPercentInsiders', 0.5) * 100
        inst = info.get('heldPercentInstitutions', 0.3) * 100
        others = 100 - (promoter + inst)
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[promoter, inst, others], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=220, margin=dict(l=0, r=0, t=20, b=0), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

        # 11. நிறுவனத்தைப் பற்றி (Auto Tamil)
        with st.expander(L["about"]):
            summary_en = info.get('longBusinessSummary', 'N/A')
            if sel_lang == "Tamil":
                try:
                    summary_ta = translator.translate(summary_en, dest='ta').text
                    st.write(summary_ta)
                except: st.write(summary_en)
            else: st.write(summary_en)

    except: st.info("Loading Stock Details...")

with tab2:
    st.markdown("### Broker Portfolio Connect")
    st.button("Connect Zerodha Kite")
    st.button("Connect Angel One")

with tab3:
    st.markdown(f"### {L['news']}")
    try:
        news_list = stock.news
        if news_list:
            for n in news_list[:10]:
                dt = datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b, %H:%M')
                st.markdown(f"""
                    <div class="news-card">
                        <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n['title']}</a><br>
                        <span style="color:#666; font-size:10px;">{n['publisher']} • {dt}</span>
                    </div>
                """, unsafe_allow_html=True)
        else: st.warning("சமீபத்திய செய்திகள் எதுவும் இல்லை.")
    except: st.error("Error fetching news.")

st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:30px;">© 2026 TAMIL INVEST HUB</div>', unsafe_allow_html=True)
