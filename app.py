import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# வாட்ச்லிஸ்ட் நினைவகம்
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
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:1000])
    except:
        return str(text)

# 2. லைவ் டிக்கர் (சிறிய எழுத்துக்கள்)
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

# 3. பிரீமியம் CSS (Font-size Small & White Labels)
st.markdown("""
    <style>
    /* முழு பக்கத்திற்கான சிறிய எழுத்து அளவு */
    html, body, [class*="css"] { font-size: 11px !important; background-color: #0d1117; color: #c9d1d9; }
    
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #f85149; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 11px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* தலைப்பு - Red/Green Shade */
    .header-container { text-align: center; margin: 10px 0; }
    .main-title { 
        font-size: 26px !important; 
        font-weight: 900; 
        background: linear-gradient(90deg, #2ea043, #f85149);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; font-style: italic; margin-top: -5px; }
    
    /* மெட்ரிக்ஸ் - White & Extra Small */
    .metric-row { 
        background: #1c2128; 
        border: 1px solid #30363d; 
        border-radius: 6px; 
        padding: 6px 10px; 
        margin-bottom: 6px; 
        display: flex; 
        justify-content: space-between; 
    }
    .m-label { color: #ffffff !important; font-size: 8.5px; text-transform: uppercase; opacity: 0.8; }
    .m-value { color: #ffffff !important; font-size: 11.5px; font-weight: bold; }
    
    /* டேப்கள் மற்றும் பட்டன்கள் சிறியதாக்க */
    .stButton>button { font-size: 10px !important; padding: 2px 10px !important; }
    [data-testid="stHeader"] { height: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 4. மேல் டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# லோகோ மற்றும் தலைப்பு
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:45px; border-radius:8px;"></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. பங்கு தேடல்
u_input = st.text_input("பங்கின் பெயர் (eg: TCS, SBI)", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if 'symbol' in info:
        stock_loaded = True
except:
    st.info("சரியான பங்குப் பெயரை உள்ளிடவும்...")

# 6. டேப்கள்
if stock_loaded:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "📝 Overview", "🤝 Shareholding", "Watchlist"])

    with tab1:
        st.markdown(f"<p style='font-size:14px; font-weight:bold; margin-bottom:5px;'>{info.get('longName', ticker)}</p>", unsafe_allow_html=True)
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        
        # மெட்ரிக்ஸ் - White & Small
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.2f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E RATIO</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">52W LOW</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">52W HIGH</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        hist = stock_obj.history(period="1mo")
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=280, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab2:
        summary = info.get('longBusinessSummary') or info.get('description') or "தகவல் இல்லை."
        with st.spinner("தமிழில் மாற்றுகிறேன்..."):
            st.write(translate_to_tamil(summary))

    with tab3:
        st.markdown("### 🤝 Shareholding")
        # சிறிய Donut Chart
        p = info.get('heldPercentInsiders', 0.5) * 100
        i = info.get('heldPercentInstitutions', 0.3) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, i, 100-(p+i)], hole=.75)])
        fig_pie.update_layout(height=220, margin=dict(l=5,r=5,t=5,b=5), showlegend=True, legend=dict(font=dict(size=9)))
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab4:
        st.markdown("### Watchlist")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        
        for item in st.session_state['watchlist']:
            c1, c2 = st.columns([5, 1])
            c1.markdown(f"<span style='font-size:11px;'>📌 {item}</span>", unsafe_allow_html=True)
            if c2.button("X", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("Loading Data...")

st.markdown("<div style='text-align:center;color:#444;font-size:8px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
