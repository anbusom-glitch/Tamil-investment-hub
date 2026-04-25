import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# அதிவேக மொழிபெயர்ப்பு
@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(str(text)[:1000])
    except: return str(text)

# 2. மேம்படுத்தப்பட்ட CSS (Big Font & Normal Round Style)
st.markdown("""
    <style>
    /* எழுத்து அளவை அதிகரித்துள்ளேன் */
    html, body, [class*="css"] { font-size: 15px !important; background-color: #0d1117; color: #ffffff; }
    
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 2px solid #39FF14; padding: 12px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 14px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    .header-container { text-align: center; margin: 20px 0; }
    .main-title { 
        font-size: 45px !important; 
        font-weight: 950; 
        background: linear-gradient(90deg, #39FF14, #FF3131);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 15px rgba(57, 255, 20, 0.4);
        margin-bottom: 0px;
    }
    .sub-title { font-size: 15px !important; color: #8b949e; font-style: italic; margin-top: -5px; }
    
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; }
    .m-label { color: #ffffff !important; font-size: 12px; text-transform: uppercase; opacity: 0.8; }
    .m-value { color: #ffffff !important; font-size: 18px; font-weight: bold; }
    
    /* பிழையற்ற நியூஸ் கார்டு */
    .news-card { background: #161b22; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #39FF14; }
    
    [data-testid="stHeader"] { height: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. லைவ் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#39FF14" if c >= 0 else "#FF3131"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE)", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

# 5. டேப்கள்
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Analysis", "⭐ Ratings", "🔮 Forecast", "📅 Action", "🗞️ News", "📌 Watchlist"
])

stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")
    if 'symbol' in info or 'longName' in info:
        stock_loaded = True
except:
    pass

# TAB 1: ANALYSIS
with tab1:
    if stock_loaded:
        st.markdown(f"<p style='font-size:20px; font-weight:bold;'>{info.get('longName', 'N/A')}</p>", unsafe_allow_html=True)
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">Market Cap</span><br><span class="m-value">₹{info.get("marketCap", 0)//10**7:,.0f} Cr</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">ROE</span><br><span class="m-value">{info.get("returnOnEquity", 0)*100:.2f}%</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=450, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

# TAB 2: RATINGS (Normal Round Chart)
with tab2:
    if stock_loaded:
        st.markdown("### Shareholding Pattern (Normal Round)")
        promo = info.get('heldPercentInsiders', 0) * 100
        inst = info.get('heldPercentInstitutions', 0) * 100
        public = 100 - (promo + inst)
        
        labels = ['Promoters', 'Institutions', 'Public']
        values = [promo, inst, max(0, public)]
        
        # 3D நீக்கப்பட்டு சாதாரண ரவுண்ட் வடிவம்
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5)]) 
        fig_pie.update_layout(height=400, template="plotly_dark", showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)

# TAB 5: NEWS (KeyError Fix)
with tab5:
    if stock_loaded:
        try:
            news_list = stock_obj.news
            if news_list:
                for n in news_list[:5]:
                    title = n.get('title', 'No Title Available')
                    link = n.get('link', '#')
                    pub = n.get('publisher', 'Market News')
                    st.markdown(f"""
                        <div class="news-card">
                            <a href="{link}" target="_blank" style="color:#39FF14; font-weight:bold; font-size:17px; text-decoration:none;">{title}</a><br>
                            <small style="color:#8b949e;">{pub}</small>
                        </div>
                    """, unsafe_allow_html=True)
            else: st.write("செய்திகள் இல்லை.")
        except: st.error("செய்திகளைப் பெறுவதில் பிழை.")

# TAB 6: WATCHLIST
with tab6:
    st.markdown("### My Watchlist")
    if st.button(f"➕ Add {u_input}"):
        if u_input not in st.session_state['watchlist']:
            st.session_state['watchlist'].append(u_input)
            st.rerun()
    
    st.divider()
    for item in st.session_state['watchlist']:
        cw1, cw2 = st.columns([5, 1])
        cw1.write(f"**📌 {item}**")
        if cw2.button("Remove", key=f"del_{item}"):
            st.session_state['watchlist'].remove(item)
            st.rerun()

st.markdown("<div style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</div>", unsafe_allow_html=True)
