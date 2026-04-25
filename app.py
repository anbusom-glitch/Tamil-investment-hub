import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# வாட்ச்லிஸ்ட் மெமரி
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# லோகோ கையாளும் முறை
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# மொழிபெயர்ப்பு
@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:800])
    except:
        return text

# 2. லைவ் டிக்கர் தரவு
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

# 3. ஸ்டைலிங் (CSS) - Red Gradient Title & White Metrics
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; color: #c9d1d9; }
    
    /* டிக்கர் */
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #f85149; padding: 10px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* தலைப்பு - Red & Green Gradient */
    .header-container { text-align: center; margin: 15px 0; }
    .main-title { 
        font-size: 32px !important; 
        font-weight: 900; 
        margin-bottom: 0px;
        background: linear-gradient(90deg, #2ea043, #f85149);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 12px !important; color: #8b949e; font-style: italic; margin-top: -5px; }
    
    /* மெட்ரிக்ஸ் - White color & Small font */
    .metric-row { 
        background: #1c2128; 
        border: 1px solid #30363d; 
        border-radius: 8px; 
        padding: 8px 12px; 
        margin-bottom: 8px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
    }
    .m-label { color: #ffffff !important; font-size: 10px; text-transform: uppercase; font-weight: 500; }
    .m-value { color: #ffffff !important; font-size: 13px; font-weight: bold; }
    
    /* நியூஸ் கார்டு */
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #f85149; }
    </style>
    """, unsafe_allow_html=True)

# 4. மேல் டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# லோகோ மற்றும் தலைப்பு
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. பங்கு தேடல்
u_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, TCS)", value="RELIANCE").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

stock_loaded = False
info = {}
stock_obj = None

try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if 'longName' in info:
        stock_loaded = True
except:
    st.info("சரியான பங்கு குறியீட்டை உள்ளிடவும்...")

# 6. டேப்கள் (Tabs)
if stock_loaded:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📊 Analysis", "📝 Overview", "🤝 Shareholding", 
        "🔮 Forecast", "📅 Action", "🗞️ News", "Watchlist"
    ])

    with tab1:
        st.markdown(f"### {info.get('longName', ticker)}")
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{info.get('priceToBook', 'N/A')}</span></div>
                <div style="text-align:right;"><span class="m-label">Market Cap (Cr)</span><br><span class="m-value">₹{info.get('marketCap', 0)//10**7:,.0f}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        pd_s = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        hist = stock_obj.history(period=pd_s)
        
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index, open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'],
                increasing_line_color='#2ea043', decreasing_line_color='#f85149'
            )])
            fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        st.markdown("### 🤝 Shareholding Pattern")
        insider = info.get('heldPercentInsiders', 0) * 100
        inst = info.get('heldPercentInstitutions', 0) * 100
        # Chart அளவில் சிறிய மாற்றம் (Small style)
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], 
                                        values=[insider, inst, 100-(insider+inst)], 
                                        hole=.6, 
                                        marker=dict(colors=['#f85149', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=300, width=300, margin=dict(l=20,r=20,t=20,b=20), showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab6:
        st.markdown("### 🗞️ News")
        news_data = stock_obj.news
        if news_data:
            for n in news_data[:5]:
                st.markdown(f"""
                    <div class="news-card">
                        <a href="{n.get('link')}" target="_blank" style="color:#f85149; text-decoration:none; font-weight:bold; font-size:14px;">{n.get('title')}</a>
                    </div>
                """, unsafe_allow_html=True)

    with tab7:
        st.markdown("### Watchlist")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        st.divider()
        for item in st.session_state['watchlist']:
            c1, c2 = st.columns([4, 1])
            c1.write(item)
            if c2.button("Remove", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("தரவுகள் லோடு ஆகின்றன...")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:40px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
