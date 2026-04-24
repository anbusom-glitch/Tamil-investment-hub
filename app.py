import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
import time

# மொழிபெயர்ப்பு லைப்ரரியை பாதுகாப்பாக கையாளுதல்
try:
    from googletrans import Translator
    translator = Translator()
    has_translator = True
except ImportError:
    has_translator = False

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TS INVEST PRO", page_icon="📈", layout="wide")

def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. மொழித் தரவுகள்
lang_dict = {
    "English": {
        "title": "TS INVEST PRO",
        "analysis": "🔍 Analysis", "broker": "💼 Broker Connect", "feed": "🗞️ Market Feed",
        "search": "Enter Ticker (e.g. SBIN.NS)", "ltp": "LTP", "pe": "P/E", "pb": "P/B", "peg": "PEG",
        "chart": "Price Chart", "holders": "Shareholding Pattern", "about": "About Company",
        "news": "Live News Feed", "trans_btn": "Translate to Tamil"
    },
    "Tamil": {
        "title": "TS இன்வெஸ்ட் PRO",
        "analysis": "🔍 ஆய்வு", "broker": "💼 புரோக்கர் இணைப்பு", "feed": "🗞️ சந்தை செய்திகள்",
        "search": "பங்கின் குறியீட்டை உள்ளிடவும்:", "ltp": "விலை", "pe": "P/E", "pb": "P/B", "peg": "PEG",
        "chart": "விலை வரைபடம்", "holders": "பங்குதாரர் விவரம்", "about": "நிறுவனத்தைப் பற்றி",
        "news": "நேரலைச் செய்திகள்", "trans_btn": "தமிழில் மொழிபெயர்க்க"
    }
}

# 3. மொபைல் CSS
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px !important; font-weight: 800; text-align: center; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 5px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# 4. மொழித் தேர்வு (Sidebar)
with st.sidebar:
    logo_img = get_base64("logo.png")
    if logo_img:
        st.markdown(f'<img src="data:image/png;base64,{logo_img}" style="width:70px; border-radius:10px;">', unsafe_allow_html=True)
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 5. Header
st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 6. TABS
tab1, tab2, tab3 = st.tabs([L["analysis"], L["broker"], L["feed"]])

with tab1:
    ticker = st.text_input(L["search"], value="RELIANCE.NS").upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Metrics
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        st.markdown(f"**{info.get('longName', ticker)}**")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(L["ltp"], f"₹{price:,.1f}")
        m2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        m3.metric(L["pb"], f"{info.get('priceToBook', 'N/A')}")
        m4.metric(L["peg"], f"{info.get('pegRatio', 'N/A')}")

        # வரைபடம் (Chart)
        period = st.select_slider("", options=["1mo", "3mo", "6mo", "1y"], value="1y")
        hist = stock.history(period=period)
        if not hist.empty:
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=1.5))])
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # 7. பங்குதாரர் வட்ட வரைபடம் (Shareholding Donut Chart)
        st.markdown(f"**{L['holders']}**")
        
        # தரவுகளைப் பெறுதல்
        promoter = info.get('heldPercentInsiders', 0.4) * 100
        inst = info.get('heldPercentInstitutions', 0.3) * 100
        public = 100 - (promoter + inst)
        
        labels = ['Promoters', 'Institutions (FII/DII)', 'Public/Others']
        values = [promoter, inst, public]
        
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, 
                                        marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0), 
                              legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5))
        st.plotly_chart(fig_pie, use_container_width=True)

        # 8. நிறுவனத்தைப் பற்றி (About with Translation)
        with st.expander(L["about"]):
            summary = info.get('longBusinessSummary', 'Information not available.')
            if sel_lang == "Tamil" and has_translator:
                if st.button(L["trans_btn"]):
                    with st.spinner("மொழிபெயர்க்கிறேன்..."):
                        summary = translator.translate(summary, dest='ta').text
            st.write(summary)

    except: st.info("Loading Data...")

with tab2:
    st.button("Connect Zerodha")
    st.button("Connect Angel One")

with tab3:
    st.markdown(f"### {L['news']}")
    try:
        # News fix - நேரடியாக news() மூலம் பெறுதல்
        news_items = stock.news
        if news_items:
            for n in news_items[:8]:
                st.markdown(f"""
                    <div class="news-card">
                        <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n['title']}</a><br>
                        <span style="color:#666; font-size:10px;">{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b')}</span>
                    </div>
                """, unsafe_allow_html=True)
        else: st.warning("No news available currently.")
    except: st.error("Error fetching news.")

st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:30px;">© 2026 TS INVEST</div>', unsafe_allow_html=True)
