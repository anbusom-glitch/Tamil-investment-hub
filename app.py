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

# 2. ஸ்மார்ட் சர்ச் (பெயர்களை குறியீடாக மாற்றுதல்)
def get_ticker(name):
    name = name.upper().strip()
    mapping = {
        "SBI": "SBIN.NS", "RELIANCE": "RELIANCE.NS", "COAL INDIA": "COALINDIA.NS",
        "TCS": "TCS.NS", "HDFC": "HDFCBANK.NS", "INFOSYS": "INFY.NS",
        "ICICI": "ICICIBANK.NS", "WIPRO": "WIPRO.NS", "ADANI": "ADANIENT.NS"
    }
    for key in mapping:
        if key in name: return mapping[key]
    return f"{name}.NS" if ".NS" not in name and ".BO" not in name else name

# 3. மொழித் தரவுகள்
lang_dict = {
    "English": {
        "title": "TAMIL INVEST HUB", "analysis": "🔍 Analysis", "feed": "🗞️ Market Feed",
        "search": "Search Stock (e.g. SBI, Reliance)", "ltp": "Price", "pe": "P/E", 
        "52wh": "52W High", "52wl": "52W Low", "holders": "Shareholding", 
        "about": "About Company", "news": "Live News Feed"
    },
    "Tamil": {
        "title": "தமிழ் இன்வெஸ்ட் ஹப்", "analysis": "🔍 ஆய்வு", "feed": "🗞️ சந்தை செய்திகள்",
        "search": "பங்கின் பெயர் (eg: SBI, Reliance):", "ltp": "விலை", "pe": "P/E", 
        "52wh": "52 வார உயர்வு", "52wl": "52 வாரத் தாழ்வு", "holders": "பங்குதாரர் விவரம்", 
        "about": "நிறுவனத்தைப் பற்றி", "news": "நேரலைச் செய்திகள்"
    }
}

# 4. CSS (Small Fonts for Mobile)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 10px; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 8px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# 5. மொழித் தேர்வு
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

# 6. லோகோ & தலைப்பு
logo_b64 = get_base64_logo("logo.png")
if logo_b64:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b64}" style="width:60px;border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2 = st.tabs([L["analysis"], L["feed"]])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA")
    ticker = get_ticker(u_input)
    
    try:
        # தரவுகளைப் பெறுதல்
        stock = yf.Ticker(ticker)
        info = stock.info
        
        if 'longName' in info:
            price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
            st.markdown(f"### {info.get('longName')}")
            
            # மெட்ரிக்ஸ் - விலை & 52 வாரம்
            m1, m2, m3 = st.columns(3)
            m1.metric(L["ltp"], f"₹{price:,.1f}")
            m1.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
            
            m2.metric(L["52wh"], f"₹{info.get('fiftyTwoWeekHigh', 0):,.1f}")
            m3.metric(L["52wl"], f"₹{info.get('fiftyTwoWeekLow', 0):,.1f}")

            # வரைபடம் (Price Chart)
            hist = stock.history(period="1y")
            if not hist.empty:
                fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=2))])
                fig.update_layout(height=250, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
                st.plotly_chart(fig, use_container_width=True)

            # பங்குதாரர் விவரம் (Donut Chart)
            st.markdown(f"**{L['holders']}**")
            p = info.get('heldPercentInsiders', 0.5) * 100
            fii = info.get('heldPercentInstitutions', 0.2) * 100
            fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII/DII', 'Others'], values=[p, fii, 100-(p+fii)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
            fig_pie.update_layout(height=220, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_pie, use_container_width=True)

            # நிறுவனத்தைப் பற்றி
            with st.expander(L["about"]):
                st.write(info.get('longBusinessSummary', 'N/A'))
        else:
            st.warning("Stock data not found. Please check the name.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")

with tab2:
    st.markdown(f"### {L['news']}")
    try:
        news = stock.news
        if news:
            for n in news[:8]:
                dt = datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b, %H:%M')
                st.markdown(f"""
                    <div class="news-card">
                        <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{n['title']}</a><br>
                        <span style="color:#666; font-size:10px;">{n['publisher']} • {dt}</span>
                    </div>
                """, unsafe_allow_html=True)
        else: st.info("No news available.")
    except: st.write("Unable to load news.")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
