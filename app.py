import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from translate import Translator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# லோகோ உதவியாளர்
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# உறுதியான மொழிபெயர்ப்பு
def translate_to_tamil(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        translator = Translator(to_lang="ta", from_lang="en")
        return translator.translate(text[:500])
    except:
        return text

# 2. லைவ் டிக்கர் (Top Row)
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

# 3. வடிவமைப்பு (Premium CSS)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 10px; }
    
    /* மெட்ரிக் பாக்ஸ் வடிவமைப்பு */
    .metric-row { 
        background: #1c2128; border: 1px solid #30363d; border-radius: 10px; 
        padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; 
    }
    .m-label { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .m-value { color: #ffd700; font-size: 15px; font-weight: bold; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# மேலடுக்கு டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:65px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 4. தரவு சேகரிப்பு
u_input = st.text_input("பங்கின் பெயர் (eg: SBI, TCS, Reliance)", value="TCS").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input

try:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    if 'longName' in info:
        # நீங்கள் கேட்ட சரியான வரிசை: 1. Analysis, 2. Overview, 3. Shareholding, 4. Forecast, 5. Action, 6. News
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Analysis", "📝 Overview", "🤝 Shareholding", "🔮 Forecast", "📅 Action", "🗞️ News"])

        with tab1:
            st.markdown(f"### 📊 Analysis - {info.get('longName', ticker)}")
            price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
            prev_close = info.get('regularMarketPreviousClose', price)
            
            # --- பண்டமெண்டல் மெட்ரிக்ஸ் (Missing Items Added Here) ---
            st.markdown(f"""
                <div class="metric-row">
                    <div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{price:,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
                </div>
                <div class="metric-row">
                    <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{info.get('priceToBook', 'N/A')}</span></div>
                    <div style="text-align:right;"><span class="m-label">PEG Ratio</span><br><span class="m-value">{info.get('pegRatio', 'N/A')}</span></div>
                </div>
                <div class="metric-row">
                    <div><span class="m-label">52W Low (தாழ்வு)</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">52W High (உயர்வு)</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
                </div>
            """, unsafe_allow_html=True)

            pd_sel = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
            hist = stock.history(period=pd_sel, interval="1m" if pd_sel=="1d" else "1d")
            
            if not hist.empty:
                # Candlestick Chart with Logic
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index, open=hist['Open'], high=hist['High'],
                    low=hist['Low'], close=hist['Close'],
                    increasing_line_color='#2ea043', decreasing_line_color='#f85149'
                )])
                fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown("<p style='text-align:center; font-size:10px; color:#8b949e;'>நன்றி (Thank You for using Tamil Invest Hub)</p>", unsafe_allow_html=True)

        with tab2:
            st.markdown("### 📝 Overview (
