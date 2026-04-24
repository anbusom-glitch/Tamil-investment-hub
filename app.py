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

# 2. லைவ் டிக்கர் தரவுகள் (Marquee)
def get_ticker_data():
    tickers = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS"]
    ticker_text = ""
    for t in tickers:
        try:
            d = yf.Ticker(t).fast_info
            p = d['last_price']
            c = d['year_change'] * 100 if 'year_change' in d else 0
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            ticker_text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return ticker_text

# 3. CSS (சிறிய எழுத்துக்கள், டிக்கர் மற்றும் வடிவமைப்பு)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    
    /* லைவ் மார்க்கெட் டிக்கர் */
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 5px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 25s linear infinite; font-weight: bold; font-size: 11px; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }

    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 20px !important; font-weight: 800; text-align: center; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 5px !important; }
    .news-card { background: #161b22; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# 4. லைவ் டிக்கர் (Top Row)
t_data = get_ticker_data()
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{t_data} {t_data}</div></div>', unsafe_allow_html=True)

# 5. மொழித் தேர்வு
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)
    L = {
        "Tamil": {"search": "பங்கின் பெயர்", "pe": "P/E விகிதம்", "52wh": "52 வார உயர்வு", "52wl": "52 வாரத் தாழ்வு", "about": "நிறுவனத்தைப் பற்றி", "news": "நேரலைச் செய்திகள்"},
        "English": {"search": "Search Stock", "pe": "P/E Ratio", "52wh": "52W High", "52wl": "52W Low", "about": "About Company", "news": "Live News Feed"}
    }[sel_lang]

# 6. லோகோ & தலைப்பு
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:50px; border-radius:8px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 7. TABS
tab1, tab2, tab3 = st.tabs(["🔍 Analysis", "🗞️ News", "💼 Broker"])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA").upper()
    ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        st.markdown(f"**{info.get('longName', ticker)}**")
        
        # Row 1: Price & PE
        c1, c2 = st.columns(2)
        c1.metric("LTP", f"₹{price:,.1f}")
        c2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        
        # Row 2: 52W Low (Left) & 52W High (Right) - நீங்கள் கேட்டபடி
        h1, h2 = st.columns(2)
        h1.metric(L["52wl"], f"₹{info.get('fiftyTwoWeekLow', 0):,.1f}")
        h2.metric(L["52wh"], f"₹{info.get('fiftyTwoWeekHigh', 0):,.1f}")
        
        # Row 3: PB & PEG
        r1, r2 = st.columns(2)
        r1.metric("P/B Ratio", f"{info.get('priceToBook', 'N/A')}")
        r2.metric("PEG Ratio", f"{info.get('pegRatio', 'N/A')}")

        st.divider()

        # சார்ட் கண்ட்ரோல்ஸ்
        p_col, s_col = st.columns(2)
        pd_sel = p_col.select_slider("Period", options=["1d", "5d", "1mo", "1y"], value="1mo")
        st_sel = s_col.radio("Style", ["Line", "Candle"], horizontal=True)

        hist = stock.history(period=pd_sel)
        fig = go.Figure()
        if st_sel == "Line":
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700')))
        else:
            fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']))
        
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # பங்குதாரர் விவரம்
        st.markdown("**Shareholding Pattern**")
        p = info.get('heldPercentInsiders', 0.5) * 100
        fii = info.get('heldPercentInstitutions', 0.3) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, fii, 100-(p+fii)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=200, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.2))
        st.plotly_chart(fig_pie, use_container_width=True)

        # About Stock
        with st.expander(L["about"]):
            st.write(info.get('longBusinessSummary', 'N/A'))

    except: st.info("Loading Stock Data...")

with tab2:
    st.markdown(f"### {L['news']}")
    try:
        # KeyError வராமல் இருக்க .get() பயன்படுத்தப்பட்டுள்ளது
        news_data = stock.news
        if news_data:
            for n in news_data[:10]:
                title = n.get('title', 'No Title')
                link = n.get('link', '#')
                pub = n.get('publisher', 'Unknown')
                ptime = n.get('providerPublishTime', 0)
                date_str = datetime.fromtimestamp(ptime).strftime('%d %b') if ptime else ""
                
                st.markdown(f"""
                    <div class="news-card">
                        <a href="{link}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600;">{title}</a><br>
                        <span style="color:#666; font-size:10px;">{pub} • {date_str}</span>
                    </div>
                """, unsafe_allow_html=True)
        else: st.warning("செய்திகள் எதுவும் இல்லை.")
    except Exception as e: st.write("Error loading news.")

with tab3:
    st.markdown("### Broker Connect")
    st.button("Zerodha Kite")
    st.button("Angel One")
    st.button("Upstox")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
