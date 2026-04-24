import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator # நவீன மொழிபெயர்ப்பு முறை
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

# 2. ஸ்மார்ட் சர்ச் மேப்பிங் (தமிழ் மற்றும் ஆங்கிலப் பெயர்கள்)
def get_ticker_from_name(name):
    name = name.upper().strip()
    mapping = {
        "SBI": "SBIN.NS", "எஸ்பிஐ": "SBIN.NS", "STATE BANK": "SBIN.NS",
        "RELIANCE": "RELIANCE.NS", "ரிலையன்ஸ்": "RELIANCE.NS",
        "COAL INDIA": "COALINDIA.NS", "கோல் இந்தியா": "COALINDIA.NS",
        "TCS": "TCS.NS", "டிசிஎஸ்": "TCS.NS",
        "HDFC": "HDFCBANK.NS", "HDFC BANK": "HDFCBANK.NS",
        "INFOSYS": "INFY.NS", "இன்போசிஸ்": "INFY.NS",
        "TATA MOTORS": "TATAMOTORS.NS", "டாடா மோட்டார்ஸ்": "TATAMOTORS.NS"
    }
    if name in mapping:
        return mapping[name]
    elif not name.endswith(".NS") and not name.endswith(".BO"):
        # தானாகவே .NS சேர்த்து தேடுதல்
        return f"{name}.NS"
    return name

# 3. மொழித் தரவுகள்
lang_dict = {
    "English": {
        "title": "TAMIL INVEST HUB",
        "analysis": "🔍 Analysis", "broker": "💼 Broker Connect", "feed": "🗞️ Market Feed",
        "search": "Search Name (e.g. SBI, Reliance, Coal India)", "ltp": "Price", 
        "pe": "P/E", "pb": "P/B", "peg": "PEG", "chart": "Price Chart", 
        "holders": "Shareholding Pattern", "about": "About Company", 
        "actions": "Bonus & Dividends", "news": "Live Stock News"
    },
    "Tamil": {
        "title": "தமிழ் இன்வெஸ்ட் ஹப்",
        "analysis": "🔍 ஆய்வு", "broker": "💼 புரோக்கர் இணைப்பு", "feed": "🗞️ சந்தை செய்திகள்",
        "search": "பெயர் (eg: எஸ்பிஐ, ரிலையன்ஸ், கோல் இந்தியா):", "ltp": "விலை", 
        "pe": "P/E", "pb": "P/B", "peg": "PEG", "chart": "விலை வரைபடம்", 
        "holders": "பங்குதாரர் விவரம்", "about": "நிறுவனத்தைப் பற்றி", 
        "actions": "போனஸ் மற்றும் டிவிடெண்ட்", "news": "நேரலைச் செய்திகள்"
    }
}

# 4. CSS வடிவமைப்பு
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 8px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #ffd700; }
    .action-item { background: #1c2128; padding: 8px; border-radius: 5px; margin-bottom: 5px; border: 1px solid #333; font-size: 11px; }
    </style>
    """, unsafe_allow_html=True)

# 5. மொழித் தேர்வு
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 6. லோகோ மற்றும் ஹெட்ர்
logo_base = get_base64_logo("logo.png")
if logo_base:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_base}" style="width:65px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2, tab3 = st.tabs([L["analysis"], L["broker"], L["feed"]])

with tab1:
    u_input = st.text_input(L["search"], value="SBI")
    ticker = get_ticker_from_name(u_input)
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # மெட்ரிக்ஸ்
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        st.markdown(f"**{info.get('longName', ticker)}**")
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(L["ltp"], f"₹{price:,.1f}")
        m2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        m3.metric(L["pb"], f"{info.get('priceToBook', 'N/A')}")
        m4.metric(L["peg"], f"{info.get('pegRatio', 'N/A')}")

        # வரைபடம் (Chart)
        period = st.select_slider("", options=["1d", "5d", "1mo", "1y"], value="1mo")
        hist = stock.history(period=period)
        if not hist.empty:
            color = '#2ea043' if price >= info.get('regularMarketPreviousClose', 0) else '#f85149'
            fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color=color, width=2))])
            fig.update_layout(height=250, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

        # பங்குதாரர் விவரம் (Pie Chart)
        st.markdown(f"**{L['holders']}**")
        prom = info.get('heldPercentInsiders', 0.5) * 100
        inst = info.get('heldPercentInstitutions', 0.3) * 100
        others = 100 - (prom + inst)
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[prom, inst, others], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=220, margin=dict(l=0, r=0, t=20, b=0), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

        # கார்ப்பரேட் ஆக்சன்ஸ் (Dividends/Bonus)
        st.markdown(f"**{L['actions']}**")
        actions = stock.actions.tail(5).sort_index(ascending=False)
        if not actions.empty:
            for date, row in actions.iterrows():
                d_str = date.strftime('%d %b %Y')
                if row['Dividends'] > 0:
                    st.markdown(f'<div class="action-item">📅 {d_str} - <b>Dividend:</b> ₹{row["Dividends"]}</div>', unsafe_allow_html=True)
                if row['Stock Splits'] > 0:
                    st.markdown(f'<div class="action-item">📅 {d_str} - <b>Bonus/Split:</b> {row["Stock Splits"]}</div>', unsafe_allow_html=True)
        else: st.write("No recent actions.")

        # நிறுவனத்தைப் பற்றி (Auto Tamil Translation)
        with st.expander(L["about"]):
            summary = info.get('longBusinessSummary', 'N/A')
            if sel_lang == "Tamil" and summary != 'N/A':
                try:
                    summary = GoogleTranslator(source='en', target='ta').translate(summary)
                except: pass
            st.write(summary)

    except: st.info("Searching for Stock Data...")

with tab2:
    st.button("Connect Zerodha")
    st.button("Connect Angel One")

with tab3:
    st.markdown(f"### {L['news']}")
    try:
        news_list = stock.news
        if news_list:
            for n in news_list[:8]:
                ts = datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b, %H:%M')
                st.markdown(f"""
                    <div class="news-card">
                        <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n['title']}</a><br>
                        <span style="color:#666; font-size:10px;">{n['publisher']} • {ts}</span>
                    </div>
                """, unsafe_allow_html=True)
        else: st.warning("News currently unavailable.")
    except: st.error("Error fetching live news.")

st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:30px;">© 2026 TAMIL INVEST HUB</div>', unsafe_allow_html=True)
