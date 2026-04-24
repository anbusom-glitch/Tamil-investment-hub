import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from translate import Translator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# லோகோ வசதி
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# மொழிபெயர்ப்பு (Tamil fallback)
def translate_to_tamil(text):
    try:
        translator = Translator(to_lang="ta")
        return translator.translate(text[:500])
    except:
        return text

# 2. லைவ் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS"]
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

# 3. CSS வடிவமைப்பு
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 5px 0; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 8px; margin-bottom: 6px; display: flex; justify-content: space-between; }
    .m-label { color: #8b949e; font-size: 10px; }
    .m-value { color: #ffd700; font-size: 13px; font-weight: bold; }
    .news-box { background: #1c2128; border-radius: 8px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# மேலடுக்கு டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 4. தரவு சேகரிப்பு (Data Fetching - NameError வராமல் இருக்க வெளியே வைக்கப்பட்டுள்ளது)
u_input = st.text_input("பங்கின் பெயர் (eg: SBI, TCS)", value="COALINDIA").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input

# குளோபல் வேரியபிள்ஸ் (Global variables)
stock_data_loaded = False
info = {}
stock = None

try:
    stock = yf.Ticker(ticker)
    info = stock.info
    if 'longName' in info:
        stock_data_loaded = True
except:
    st.error("தரவுகளைப் பெற முடியவில்லை. சரியான குறியீட்டை உள்ளிடவும்.")

# 5. TABS (நீங்கள் கேட்ட புதிய வரிசை)
if stock_data_loaded:
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Analysis", "📝 Overview", "🗞️ News", "🤝 Holders", "📅 Actions", "🔮 Forecast"])

    with tab1:
        st.markdown(f"### {info.get('longName', ticker)}")
        price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">LTP</span><br><span class="m-value">₹{price:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        pd_sel = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        hist = stock.history(period=pd_sel, interval="1m" if pd_sel=="1d" else "1d")
        
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=2))])
        fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📝 Overview")
        about_en = info.get('longBusinessSummary', 'No data.')
        if sel_lang == "Tamil":
            st.write(translate_to_tamil(about_en))
        else:
            st.write(about_en)

    with tab3:
        st.markdown("### 🗞️ News Feed")
        try:
            for n in stock.news[:10]:
                st.markdown(f"""
                    <div class="news-box">
                        <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">{n['title']}</a><br>
                        <small style="color:#8b949e;">{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b')}</small>
                    </div>
                """, unsafe_allow_html=True)
        except: st.write("செய்திகள் இல்லை.")

    with tab4:
        st.markdown("### 🤝 Shareholding Pattern")
        p = info.get('heldPercentInsiders', 0.5) * 100
        inst = info.get('heldPercentInstitutions', 0.3) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, inst, 100-(p+inst)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
        fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab5:
        st.markdown("### 📅 Corporate Actions")
        acts = stock.actions.tail(10).sort_index(ascending=False)
        for date, row in acts.iterrows():
            if row['Dividends'] > 0: st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{row['Dividends']}")
            if row['Stock Splits'] > 0: st.success(f"📅 {date.strftime('%d %b %Y')} - Bonus/Split: {row['Stock Splits']}")

    with tab6:
        st.markdown("### 🔮 Forecast")
        roe = info.get('returnOnEquity', 0)
        if roe > 0.15: st.success("Strong Fundamental Strength 🚀")
        else: st.warning("Neutral Growth ⚖️")
        st.write(f"ROE: {roe*100:.2f}%")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
