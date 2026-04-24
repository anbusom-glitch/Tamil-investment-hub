import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from translate import Translator # புதிய மற்றும் பாதுகாப்பான மொழிபெயர்ப்பு

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# லோகோ வசதி
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. மொழிபெயர்ப்பு வசதி (Error-Free)
def translate_to_tamil(text):
    try:
        translator = Translator(to_lang="ta")
        # பெரிய டெக்ஸ்ட் என்றால் சுருக்கி மொழிபெயர்க்கும்
        return translator.translate(text[:500]) 
    except:
        return text # பிழை வந்தால் ஆங்கிலத்திலேயே காட்டும்

# 3. லைவ் மார்க்கெட் டிக்கர்
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

# 4. CSS (Elite Mobile UI)
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

# 5. மேலடுக்கு டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# 6. மொழி & லோகோ
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 7. TABS (சரியான வரிசை)
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Analysis", "📝 Overview", "📅 Actions", "🔮 Forecast", "🗞️ News", "🤝 Holders"])

with tab1:
    u_input = st.text_input("Stock Name", value="COALINDIA").upper()
    ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        st.markdown(f"### {info.get('longName', ticker)}")

        # Compact Metrics
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

        # Chart Period Buttons
        pd = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        st_sel = st.radio("Style", ["Line", "Candle"], horizontal=True, label_visibility="collapsed")
        
        hist = stock.history(period=pd, interval="1m" if pd=="1d" else "1d")
        if not hist.empty:
            fig = go.Figure()
            if st_sel == "Line":
                fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=2)))
            else:
                fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']))
            
            fig.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except: st.info("Loading Data...")

with tab2:
    # --- OVERVIEW TAB (புதியது) ---
    st.markdown("### 📝 Overview (நிறுவனத் தகவல்)")
    about_en = info.get('longBusinessSummary', 'No data.')
    if sel_lang == "Tamil":
        with st.spinner("மொழிபெயர்க்கிறேன்..."):
            about_ta = translate_to_tamil(about_en)
            st.write(about_ta)
    else:
        st.write(about_en)
    
    col_a, col_b = st.columns(2)
    col_a.metric("Market Cap", f"₹{info.get('marketCap', 0)//10**7:,.0f} Cr")
    col_b.metric("Sector", info.get('sector', 'N/A'))

with tab3:
    st.markdown("### 📅 Actions (நிகழ்வுகள்)")
    acts = stock.actions.tail(10).sort_index(ascending=False)
    for date, row in acts.iterrows():
        if row['Dividends'] > 0: st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{row['Dividends']}")
        if row['Stock Splits'] > 0: st.success(f"📅 {date.strftime('%d %b %Y')} - Bonus/Split: {row['Stock Splits']}")

with tab4:
    # --- FORECAST TAB (புதியது) ---
    st.markdown("### 🔮 Smart Forecast (எதிர்கால கணிப்பு)")
    roe = info.get('returnOnEquity', 0)
    debt = info.get('debtToEquity', 150)
    
    if roe > 0.15 and debt < 100:
        st.success("Verdict: Strong Buy 🚀 (நல்ல எதிர்காலம் உள்ளது)")
    elif roe > 0.10:
        st.warning("Verdict: Hold/Watch ⚖️ (கவனிக்கவும்)")
    else:
        st.error("Verdict: Bearish 📉 (தவிர்ப்பது நல்லது)")
    
    st.caption("இந்தக் கணிப்பு நிறுவனத்தின் லாபம் மற்றும் கடனை அடிப்படையாகக் கொண்டது.")

with tab5:
    # --- NEWS FEED TAB (புதியது) ---
    st.markdown("### 🗞️ News Feed (சமீபத்திய செய்திகள்)")
    try:
        for n in stock.news[:10]:
            st.markdown(f"""
                <div class="news-box">
                    <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">{n['title']}</a><br>
                    <small style="color:#8b949e;">{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b')}</small>
                </div>
            """, unsafe_allow_html=True)
    except: st.write("News not available.")

with tab6:
    st.markdown("### 🤝 Holders (பங்குதாரர்கள்)")
    p = info.get('heldPercentInsiders', 0.5) * 100
    inst = info.get('heldPercentInstitutions', 0.3) * 100
    fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, inst, 100-(p+inst)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
    fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_pie, use_container_width=True)

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
