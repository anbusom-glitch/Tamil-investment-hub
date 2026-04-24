import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. லைவ் மார்க்கெட் டிக்கர்
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

# 3. ஸ்மார்ட் அனலைசர் லாஜிக் (சாதாரண மனிதர்களுக்காக)
def stock_analyzer(info):
    score = 0
    reasons = []
    
    # 1. PE Ratio Check
    pe = info.get('trailingPE', 100)
    if pe < 25: 
        score += 3
        reasons.append("✅ விலை குறைவாக (Cheap) உள்ளது")
    else: 
        reasons.append("⚠️ விலை அதிகமாக (Expensive) உள்ளது")
        
    # 2. Debt Check
    debt = info.get('debtToEquity', 200)
    if debt < 100: 
        score += 3
        reasons.append("✅ நிறுவனத்திற்கு கடன் சுமை குறைவு")
    else:
        reasons.append("⚠️ நிறுவனத்திற்கு கடன் அதிகம்")
        
    # 3. Profit Margin
    margin = info.get('profitMargins', 0)
    if margin > 0.1: 
        score += 4
        reasons.append("✅ நிறுவனம் நல்ல லாபம் ஈட்டுகிறது")
    
    # Verdict Logic
    if score >= 7: return "Strong Bullish 🚀 (சிறப்பானது)", "#2ea043", reasons
    elif score >= 4: return "Neutral ⚖️ (கவனிக்கவும்)", "#ffd700", reasons
    else: return "Bearish 📉 (தவிர்க்கவும்)", "#f85149", reasons

# 4. CSS (எழுத்துக்கள் & அனலைசர் டிசைன்)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 5px 0; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 30s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; }
    
    /* ஸ்மார்ட் அனலைசர் பாக்ஸ் */
    .analyzer-box {
        background: #1c2128; border-radius: 10px; padding: 15px; border: 2px solid #30363d; margin-top: 10px;
    }
    .verdict-text { font-size: 18px; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .metric-row { background: #161b22; border-radius: 8px; padding: 8px 12px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; border: 1px solid #333; }
    .m-label { color: #8b949e; font-size: 11px; }
    .m-value { color: #ffd700; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 5. மேலடுக்கு டிக்கர்
t_html = get_ticker_text()
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{t_html} {t_html}</div></div>', unsafe_allow_html=True)

# 6. மொழித் தேர்வு
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)
    L = {
        "Tamil": {"search": "பங்கின் பெயர்", "verdict": "பங்கின் தற்போதைய நிலை", "low": "52 வாரத் தாழ்வு", "high": "52 வார உயர்வு"},
        "English": {"search": "Search Stock", "verdict": "Stock Health Verdict", "low": "52W Low", "high": "52W High"}
    }[sel_lang]

# 7. லோகோ & தலைப்பு
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 8. TABS
tab1, tab2, tab3 = st.tabs(["📊 Analyzer", "📈 Corporate Actions", "💼 Broker"])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA").upper()
    ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        st.markdown(f"### {info.get('longName', ticker)}")

        # --- SMART ANALYZER SECTION ---
        verdict, v_color, reasons = stock_analyzer(info)
        st.markdown(f"""
            <div class="analyzer-box" style="border-color: {v_color};">
                <p style="color: #8b949e; text-align:center; font-size:10px;">SMART ANALYZER VERDICT</p>
                <div class="verdict-text" style="color: {v_color};">{verdict}</div>
                <ul style="list-style-type: none; padding: 0; font-size:11px;">
                    {"".join([f"<li>{r}</li>" for r in reasons])}
                </ul>
            </div>
        """, unsafe_allow_html=True)

        st.write("")

        # --- COMPACT METRICS ---
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">Current Price</span><br><span class="m-value">₹{price:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">{L['low']}</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">{L['high']}</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        # Chart Buttons
        pd_sel = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        hist = stock.history(period=pd_sel)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=2))])
        fig.update_layout(height=230, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    except: st.info("Searching Stock Data...")

with tab2:
    st.markdown("### Corporate Actions")
    try:
        actions = stock.actions.tail(8).sort_index(ascending=False)
        for date, row in actions.iterrows():
            d_str = date.strftime('%d %b %Y')
            if row['Dividends'] > 0: st.info(f"📅 {d_str} - Dividend: ₹{row['Dividends']}")
            if row['Stock Splits'] > 0: st.success(f"📅 {d_str} - Bonus/Split: {row['Stock Splits']}")
    except: st.write("No recent actions.")

with tab3:
    st.button("Connect Zerodha")
    st.button("Connect Angel One")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
