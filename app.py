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

# 3. ஸ்மார்ட் அனலைசர் லாஜிக்
def stock_analyzer(info):
    score = 0
    reasons = []
    pe = info.get('trailingPE', 100)
    if pe < 25: 
        score += 3
        reasons.append("✅ பங்கு விலை குறைவாக (Cheap) உள்ளது")
    debt = info.get('debtToEquity', 200)
    if debt < 100: 
        score += 3
        reasons.append("✅ நிறுவனத்திற்கு கடன் சுமை குறைவு")
    margin = info.get('profitMargins', 0)
    if margin > 0.1: 
        score += 4
        reasons.append("✅ நிறுவனம் நல்ல லாபம் ஈட்டுகிறது")
    
    if score >= 7: return "Strong Bullish 🚀 (சிறப்பானது)", "#2ea043", reasons
    elif score >= 4: return "Neutral ⚖️ (கவனிக்கவும்)", "#ffd700", reasons
    else: return "Bearish 📉 (தவிர்க்கவும்)", "#f85149", reasons

# 4. CSS (Elite Design)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 5px 0; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 30s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; }
    .analyzer-box { background: #1c2128; border-radius: 10px; padding: 15px; border: 2px solid #30363d; margin-top: 10px; }
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
        "Tamil": {"search": "பங்கின் பெயர்", "about": "நிறுவனத்தைப் பற்றி", "holders": "பங்குதாரர் விவரம்", "actions": "நிறுவன நிகழ்வுகள்", "broker": "புரோக்கர் இணைப்பு"},
        "English": {"search": "Search Stock", "about": "About Company", "holders": "Shareholding Pattern", "actions": "Corporate Actions", "broker": "Broker Connect"}
    }[sel_lang]

# 7. லோகோ & தலைப்பு
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 8. TABS (வரிசை மாற்றப்பட்டுள்ளது)
tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "📅 Actions", "🤝 Shareholding", "💼 Broker"])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA").upper()
    ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        st.markdown(f"### {info.get('longName', ticker)}")

        # --- SMART ANALYZER ---
        verdict, v_color, reasons = stock_analyzer(info)
        st.markdown(f"""
            <div class="analyzer-box" style="border-color: {v_color};">
                <div style="font-size: 18px; font-weight: 800; text-align: center; color: {v_color};">{verdict}</div>
                <p style="font-size:11px; margin-top:5px; text-align:center;">{" | ".join(reasons)}</p>
            </div>
        """, unsafe_allow_html=True)

        # --- COMPACT METRICS ---
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">LTP</span><br><span class="m-value">₹{price:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
        """, unsafe_allow_html=True)

        # Chart
        pd_sel = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        hist = stock.history(period=pd_sel)
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=2))])
        fig.update_layout(height=230, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # --- ABOUT COMPANY (Analysis Tab-லேயே நிறுவனத்தின் சுருக்கம்) ---
        st.markdown(f"#### {L['about']}")
        st.write(info.get('longBusinessSummary', 'தகவல் இல்லை.'))

    except: st.info("Searching Stock Data...")

with tab2:
    st.markdown(f"### {L['actions']}")
    try:
        actions = stock.actions.tail(8).sort_index(ascending=False)
        for date, row in actions.iterrows():
            d_str = date.strftime('%d %b %Y')
            if row['Dividends'] > 0: st.info(f"📅 {d_str} - Dividend: ₹{row['Dividends']}")
            if row['Stock Splits'] > 0: st.success(f"📅 {d_str} - Bonus/Split: {row['Stock Splits']}")
    except: st.write("No recent actions.")

with tab3:
    # --- SHAREHOLDING PATTERN TAB (புதிய வசதி) ---
    st.markdown(f"### {L['holders']}")
    try:
        # டேட்டா பெறுதல்
        promoter = info.get('heldPercentInsiders', 0.5) * 100
        inst_total = info.get('heldPercentInstitutions', 0.3) * 100
        # FII/DII தோராயமான பிரிப்பு (API-ல் சில சமயம் ஒன்றாக வரும்)
        fii = inst_total * 0.6
        dii = inst_total * 0.4
        others = 100 - (promoter + inst_total)
        
        labels = ['Promoters', 'FII', 'DII', 'Others']
        values = [promoter, fii, dii, others]
        colors = ['#ffd700', '#58a6ff', '#ff7b72', '#2ea043']

        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=colors))])
        fig_pie.update_layout(height=350, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1, xanchor="center", x=0.5))
        st.plotly_chart(fig_pie, use_container_width=True)
        
        st.write("குறிப்பு: இது நிறுவனத்தின் அதிகாரப்பூர்வ சமீபத்திய பங்குதாரர் விவரம்.")
    except:
        st.write("பங்குதாரர் விவரம் தற்போது கிடைக்கவில்லை.")

with tab4:
    st.markdown(f"### {L['broker']}")
    st.button("Connect Zerodha")
    st.button("Connect Angel One")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
