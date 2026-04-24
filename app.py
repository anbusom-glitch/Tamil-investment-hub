import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# --- 1. பக்க அமைப்பு (Elite UI) ---
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# வாட்ச்லிஸ்ட் நினைவகம்
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# உறுதியான தமிழ் மொழிபெயர்ப்பு
def translate_to_tamil(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:800])
    except:
        return text

# --- 2. லைவ் டிக்கர் (Live Ticker) ---
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    t_text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            t_text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return t_text

# --- 3. வடிவமைப்பு (Premium CSS) ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .m-value { color: #ffd700; font-size: 15px; font-weight: bold; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700; }
    
    @media (max-width: 640px) {
        .header-text { font-size: 20px !important; }
        .stTabs [data-baseweb="tab"] { font-size: 10px !important; padding: 8px !important; }
    }
    </style>
    """, unsafe_allow_html=True)

# UI Elements
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# முகப்புப் பக்கத்திலேயே மொழித் தேர்வு
sel_lang = st.radio("Choose Language / மொழியைத் தேர்ந்தெடுக்கவும்", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:60px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# --- 4. தேடல் மற்றும் டேட்டா (பிழையில்லாமல் வரிசைப்படுத்தப்பட்டுள்ளது) ---
u_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, TCS)", value="TCS").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input

# டேட்டா லோடிங் செக்ஷன்
stock_loaded = False
info = {}
stock_obj = None

try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if 'longName' in info:
        stock_loaded = True
except:
    st.info("சரியான பங்குப் பெயரை உள்ளிடவும்...")

# 5. TABS (நீங்கள் கேட்ட சரியான 1-8 வரிசைமுறை)
if stock_loaded:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Analysis", "📝 Overview", "🤝 Shareholding", 
        "🔮 Forecast", "📅 Action", "🗞️ News", "👀 Watchlist", "💼 Broker"
    ])

    with tab1:
        st.markdown(f"### {info.get('longName', ticker)}")
        ltp = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        # P/E, P/B, PEG, 52W High/Low (அனைத்தும் சேர்க்கப்பட்டுள்ளது)
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.1f}</span></div>
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

        pd_s = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, key="main_chart")
        hist = stock_obj.history(period=pd_s, interval="1m" if pd_s=="1d" else "1d")
        
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index, open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'],
                increasing_line_color='#2ea043', decreasing_line_color='#f85149'
            )])
            fig.update_layout(height=380, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
            st.markdown("<p style='text-align:center; font-size:10px; color:#8b949e;'>TAMIL INVEST HUB - நன்றி</p>", unsafe_allow_html=True)

    with tab2:
        st.markdown("### 📝 Overview (நிறுவனத் தகவல்)")
        desc_en = info.get('longBusinessSummary', 'தகவல் இல்லை.')
        if sel_lang == "Tamil":
            with st.spinner("தமிழில் மொழிபெயர்க்கிறேன்..."):
                st.write(translate_to_tamil(desc_en))
        else:
            st.write(desc_en)

    with tab3:
        st.markdown("### 🤝 Shareholding Pattern")
        try:
            p_val = info.get('heldPercentInsiders', 0.5) * 100
            inst_val = info.get('heldPercentInstitutions', 0.3) * 100
            fig_p = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p_val, inst_val, 100-(p_val+inst_val)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
            fig_p.update_layout(height=350, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_p, use_container_width=True)
        except: st.write("தகவல் இல்லை.")

    with tab4:
        st.markdown("### 🔮 Forecast (கணிப்பு)")
        roe = info.get('returnOnEquity', 0)
        if roe > 0.15: st.success("Strong Fundamental Strength 🚀 (நல்ல எதிர்காலம் உள்ளது)")
        else: st.warning("Neutral Growth Outlook ⚖️ (கவனிக்கவும்)")
        st.write(f"ROE (லாபத்திறன்): {roe*100:.2f}%")

    with tab5:
        st.markdown("### 📅 Action (நிகழ்வுகள்)")
        try:
            acts = stock_obj.actions.tail(10).sort_index(ascending=False)
            if not acts.empty:
                for date, row in acts.iterrows():
                    d_val = row.get('Dividends', 0)
                    if d_val > 0: st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{d_val}")
                    # Stock Splits பிழை வராமல் இருக்க செக் செய்தல்
                    if 'Stock Splits' in row and row['Stock Splits'] > 0:
                        st.success(f"📅 {date.strftime('%d %b %Y')} - Split: {row['Stock Splits']}")
            else: st.write("நிகழ்வுகள் இல்லை.")
        except: st.write("நிகழ்வுகளைப் பெறுவதில் பிழை.")

    with tab6:
        st.markdown("### 🗞️ News (நேரலைச் செய்திகள்)")
        try:
            news_data = stock_obj.news
            if news_data:
                for n in news_data[:10]:
                    # KeyError வராமல் இருக்க .get() பயன்படுத்தப்பட்டுள்ளது
                    ts = n.get('providerPublishTime', 0)
                    dt = datetime.fromtimestamp(ts).strftime('%d %b, %H:%M') if ts else "சமீபத்தில்"
                    st.markdown(f"""
                        <div class="news-card">
                            <a href="{n.get('link','#')}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">{n.get('title','News')}</a><br>
                            <small style="color:#8b949e;">{n.get('publisher','Market')} • {dt}</small>
                        </div>
                    """, unsafe_allow_html=True)
            else: st.info("செய்திகள் இல்லை.")
        except: st.write("செய்திகளைப் பெறுவதில் பிழை.")

    with tab7:
        st.markdown("### 👀 My Watchlist")
        if st.button(f"➕ Add {u_input} to Watchlist"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        st.write(st.session_state['watchlist'])

    with tab8:
        st.markdown("### 💼 Broker Connect")
        st.button("🔗 Connect Zerodha", use_container_width=True)
        st.button("🔗 Connect Angel One", use_container_width=True)
        st.button("🔗 Connect Upstox", use_container_width=True)

else:
    st.info("Loading Data...")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
