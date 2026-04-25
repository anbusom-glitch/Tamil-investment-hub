import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# --- 1. PAGE SETUP & CACHING ---
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# தகவல்களைத் தற்காலிகமாகச் சேமிக்க (Speed பெருக்குவதற்கு)
@st.cache_data(ttl=3600) # 1 மணிநேரம் சேமிப்பில் இருக்கும்
def fetch_stock_data(ticker):
    try:
        stock = yf.Ticker(ticker)
        return stock, stock.info
    except:
        return None, None

@st.cache_data(ttl=86400) # மொழிபெயர்ப்பை ஒரு நாள் சேமிக்க
def translate_text(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:1000])
    except:
        return text

# வாட்ச்லிஸ்ட் நினைவகம்
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# --- 2. PREMIUM CSS (White Text & Larger Font) ---
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 13px !important; 
        background-color: #0d1117; 
        color: #ffffff; /* அனைத்து எழுத்துக்களும் வெள்ளை */
    }
    .header-text { 
        background: linear-gradient(90deg, #2ea043, #f85149); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 28px !important; 
        font-weight: 800; 
        text-align: center; 
    }
    .created-by { font-size: 12px; color: #8b949e; text-align: center; margin-top: -10px; margin-bottom: 20px; }
    
    .metric-row { 
        background: #1c2128; 
        border: 1px solid #30363d; 
        border-radius: 10px; 
        padding: 15px; 
        margin-bottom: 10px; 
        display: flex; 
        justify-content: space-between; 
    }
    .m-label { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .m-value { color: #ffffff !important; font-size: 18px !important; font-weight: bold; }
    
    /* Tabs எழுத்துக்கள் */
    .stTabs [data-baseweb="tab"] { font-size: 13px !important; color: #ffffff !important; }
    </style>
    """, unsafe_allow_html=True)

# தலைப்பு
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
st.markdown('<p class="created-by">created by somasundaram</p>', unsafe_allow_html=True)

# மொழி மற்றும் தேடல்
sel_lang = st.radio("Choose Language", ["Tamil", "English"], horizontal=True)
u_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, Coal India)", value="SBI").upper()

# ஸ்மார்ட் சர்ச் மேப்பிங்
mapping = {"RELIANCE": "RELIANCE.NS", "SBI": "SBIN.NS", "SBIN": "SBIN.NS", "COAL INDIA": "COALINDIA.NS"}
ticker = mapping.get(u_input, f"{u_input}.NS" if ".NS" not in u_input else u_input)

# --- 3. DATA LOADING WITH FEEDBACK ---
with st.spinner('தரவுகள் சேகரிக்கப்படுகின்றன...'):
    stock_obj, info = fetch_stock_data(ticker)

if stock_obj and 'longName' in info:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Analysis", "📝 Overview", "🤝 Shareholding", "🔮 Forecast", 
        "📅 Action", "🗞️ News", "👀 Watchlist", "💼 Broker"
    ])

    with tab1:
        st.markdown(f"### {info.get('longName', ticker)}")
        if st.button(f"⭐ Add {u_input} to Watchlist"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()

        ltp = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{info.get('priceToBook', 'N/A')}</span></div>
                <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)
        
        hist = stock_obj.history(period="1mo")
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📝 Overview")
        desc_en = info.get('longBusinessSummary', 'தகவல் இல்லை.')
        if sel_lang == "Tamil":
            st.write(translate_text(desc_en))
        else:
            st.write(desc_en)

    with tab3:
        st.markdown("### 🤝 Shareholding")
        try:
            p_v = info.get('heldPercentInsiders', 0.5) * 100
            inst_v = info.get('heldPercentInstitutions', 0.3) * 100
            fig_p = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p_v, inst_v, 100-(p_v+inst_v)], hole=.5)])
            fig_p.update_layout(height=300, template="plotly_dark")
            st.plotly_chart(fig_p, use_container_width=True)
        except: st.write("தகவல் இல்லை.")

    with tab7:
        st.markdown("### 👀 My Watchlist")
        for item in st.session_state['watchlist']:
            c1, c2 = st.columns([4,1])
            c1.write(f"📈 {item}")
            if c2.button("Delete", key=item):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.warning("சரியான பங்குப் பெயரை உள்ளிடவும் அல்லது இணைய இணைப்பைச் சரிபார்க்கவும்.")

st.markdown("<div style='text-align:center;color:#444;font-size:11px;margin-top:50px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
