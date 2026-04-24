import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from googletrans import Translator # மொழிபெயர்ப்பிற்காக
import base64
import time

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TS INVEST PRO", page_icon="📈", layout="wide")

# லோகோவை Base64-ஆக மாற்றும் வசதி
def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

translator = Translator()

# 2. இருமொழி தரவுகள்
lang_dict = {
    "English": {
        "title": "TS INVEST PRO",
        "analysis": "🔍 Analysis",
        "broker": "💼 Broker Connect",
        "feed": "🗞️ Market Feed",
        "search_label": "Enter Ticker (e.g. SBIN.NS)",
        "ltp": "LTP", "pe": "P/E", "pb": "P/B", "peg": "PEG",
        "chart_title": "Price Chart",
        "shareholding_title": "Shareholding Pattern",
        "about": "About Company",
        "news_title": "Live News Feed",
        "loading_news": "Fetching news...",
        "no_news": "No news found for this stock.",
        "translate_btn": "Translate to Tamil"
    },
    "Tamil": {
        "title": "TS இன்வெஸ்ட் PRO",
        "analysis": "🔍 ஆய்வு",
        "broker": "💼 புரோக்கர் இணைப்பு",
        "feed": "🗞️ சந்தை செய்திகள்",
        "search_label": "பங்கின் குறியீட்டை உள்ளிடவும் (eg: RELIANCE.NS)",
        "ltp": "விலை", "pe": "P/E", "pb": "P/B", "peg": "PEG",
        "chart_title": "விலை வரைபடம்",
        "shareholding_title": "பங்குதாரர் விவரம்",
        "about": "நிறுவனத்தைப் பற்றி",
        "news_title": "நேரலைச் செய்திகள்",
        "loading_news": "செய்திகளைத் திரட்டுகிறேன்...",
        "no_news": "செய்திகள் எதுவும் கிடைக்கவில்லை.",
        "translate_btn": "தமிழில் மொழிபெயர்க்க"
    }
}

# 3. மொபைல் CSS (Small Fonts)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px !important; font-weight: 800; text-align: center; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 5px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ffd700; }
    .stTabs [data-baseweb="tab"] { font-size: 11px !important; padding: 8px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. மொழித் தேர்வு
with st.sidebar:
    logo_img = get_base64("logo.png")
    if logo_img:
        st.markdown(f'<img src="data:image/png;base64,{logo_img}" style="width:70px; border-radius:10px;">', unsafe_allow_html=True)
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 5. SPLASH SCREEN
if 'startup' not in st.session_state:
    p = st.empty()
    p.markdown("<div style='height:80vh; display:flex; align-items:center; justify-content:center;'><h1 style='color:#ffd700;'>TS INVEST</h1></div>", unsafe_allow_html=True)
    time.sleep(1.5)
    st.session_state.startup = True
    p.empty()

st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 6. TABS
tab1, tab2, tab3 = st.tabs([L["analysis"], L["broker"], L["feed"]])

with tab1:
    ticker = st.text_input(L["search_label"], value="RELIANCE.NS").upper()
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

        # --- Chart with Period ---
        period = st.select_slider("", options=["1mo", "3mo", "6mo", "1y"], value="1y")
        hist = stock.history(period=period)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=1.5))])
        fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

        # --- NEW: Shareholding Donut Chart ---
        st.markdown(f"**{L['shareholding_title']}**")
        holders = stock.major_holders
        if holders is not None:
            # பொதுவாக yfinance தரும் தரவுகளைப் பிரித்தல்
            labels = ['Institutions', 'Promoters', 'Public/Others']
            values = [info.get('heldPercentInstitutions', 0.2)*100, 
                      info.get('heldPercentInsiders', 0.5)*100, 
                      30.0] # மாதிரி மதிப்பு
            
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=['#58a6ff', '#ffd700', '#2ea043']))])
            fig_pie.update_layout(height=200, margin=dict(l=0, r=0, t=0, b=0), showlegend=True, legend=dict(font=dict(size=10), orientation="h"))
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- About Company with Translation ---
        with st.expander(L["about"]):
            summary = info.get('longBusinessSummary', 'N/A')
            if sel_lang == "Tamil":
                if st.button(L["translate_btn"]):
                    with st.spinner("Translating..."):
                        summary = translator.translate(summary, dest='ta').text
            st.write(summary)

    except: st.info("Loading Stock Data...")

with tab2:
    st.markdown(f"### {L['connect_title']}")
    # Broker Connect UI...
    st.button("Connect Zerodha")
    st.button("Connect Angel One")

with tab3:
    st.markdown(f"### {L['news_title']}")
    with st.spinner(L["loading_news"]):
        try:
            news_items = stock.news
            if news_items:
                for n in news_items[:8]:
                    st.markdown(f"""
                        <div class="news-card">
                            <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n['title']}</a><br>
                            <span style="color:#666; font-size:10px;">{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b')}</span>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.warning(L["no_news"])
        except:
            st.error("Could not fetch news.")

st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:20px;">© 2026 TS INVEST</div>', unsafe_allow_html=True)
