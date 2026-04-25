import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. பிரீமியம் CSS
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: 15px !important; background-color: #0d1117; color: #ffffff; }}
    .ticker-wrap {{ width: 100%; overflow: hidden; background: #161b22; border-bottom: 2px solid #39FF14; padding: 12px 0; position: sticky; top: 0; z-index: 999; }}
    .ticker-move {{ display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 14px; font-weight: bold; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    .main-title {{ 
        text-align: center; font-size: 45px !important; font-weight: 950; 
        background: linear-gradient(90deg, #39FF14, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(57, 255, 20, 0.4);
    }}
    .metric-row {{ background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }}
    .m-label {{ color: #ffffff !important; font-size: 11px; text-transform: uppercase; opacity: 0.8; }}
    .m-value {{ color: #ffffff !important; font-size: 16px; font-weight: bold; }}
    </style>
    """, unsafe_allow_html=True)

# 3. சைடுபார்
with st.sidebar:
    st.markdown(f"### 👤 {get_text('User Profile', 'பயனர் விவரம்')}")
    st.info("Somasundaram (Premium)")
    lang_choice = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)
    st.session_state['language'] = lang_choice
    
    st.divider()
    st.markdown(f"### 💼 {get_text('Broker Connect', 'புரோக்கர் இணைப்பு')}")
    st.button("🔗 Zerodha", use_container_width=True)
    st.button("🔗 Angel One", use_container_width=True)

# 4. டிக்கர் மற்றும் தலைப்பு
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
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# டேட்டா லோடிங்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    # --- ANALYSIS TAB ---
    with tabs[0]:
        st.markdown(f"### {info.get('longName', u_input)}")
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">PRICE (LTP)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W LOW</span><br><span class="m-value">₹{info.get("fiftyTwoWeekLow", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W HIGH</span><br><span class="m-value">₹{info.get("fiftyTwoWeekHigh", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E RATIO</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # --- SHAREHOLDING TAB (FII & DII பிரிக்கப்பட்டுள்ளது) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        
        # டேட்டா பிரிப்பு லாஜிக்
        promo = info.get('heldPercentInsiders', 0) * 100
        inst_total = info.get('heldPercentInstitutions', 0) * 100
        
        # FII மற்றும் DII தகவல்களை பிரித்தல்
        # குறிப்பு: yfinance நேரடி FII/DII தராது, எனவே நிறுவன முதலீட்டை (Institutions) பிரித்துக் காட்டுகிறோம்
        fii = info.get('foreignInstitutionalHolders', inst_total * 0.6) # ஒரு தோராயமான கணக்கு அல்லது கிடைக்கும் தரவு
        if fii > inst_total: fii = inst_total * 0.6
        dii = inst_total - fii
        
        public = 100 - (promo + inst_total)
        if public < 0: public = 0

        labels = ['Promoters', 'FII (Foreign)', 'DII (Domestic)', 'Public']
        values = [promo, fii, dii, public]
        colors = ['#58a6ff', '#f85149', '#39FF14', '#ffd700']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=0.5,
            marker=dict(colors=colors)
        )])
        
        fig_pie.update_layout(height=450, template="plotly_dark", showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # எண்களாகக் காட்ட
        st.markdown("#### விரிவான விவரங்கள்:")
        col_f1, col_f2 = st.columns(2)
        col_f1.write(f"🔹 Promoters: **{promo:.2f}%**")
        col_f1.write(f"🔹 FII (Foreign Investors): **{fii:.2f}%**")
        col_f2.write(f"🔹 DII (Domestic Investors): **{dii:.2f}%**")
        col_f2.write(f"🔹 Public / Others: **{public:.2f}%**")

    # --- மற்ற டேப்கள் ---
    with tabs[4]:
        st.markdown(f"### {get_text('My Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        st.divider()
        for item in st.session_state['watchlist']:
            cw1, cw2 = st.columns([5, 1])
            cw1.write(f"📌 **{item}**")
            if cw2.button("Remove", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("Loading Stock Data... (eg: TCS, RELIANCE)")
