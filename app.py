import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. PREMIUM CSS
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    .header-container { text-align: center; padding: 20px 0; }
    .main-title { 
        font-size: 38px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 11px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.8; font-style: italic; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    .forecast-card { padding: 30px; border-radius: 20px; text-align: center; margin-top: 20px; border: 2px solid; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="background:#1c2128; padding:40px; border-radius:15px; max-width:400px; margin:auto; border:1px solid #30363d;">', unsafe_allow_html=True)
        st.subheader("Sign In / உள்நுழைக")
        u_id = st.text_input("User ID")
        u_pass = st.text_input("Password", type="password")
        if st.button("Access Hub 🚀", use_container_width=True):
            if u_id and u_pass: st.session_state['is_logged_in'] = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. HEADER
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. SEARCH
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. DATA ENGINE
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1y")

    # --- TAB 1: ANALYSIS ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        f_list = [(get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"), (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')), (get_text("ROE", "ROE"), f"{(info.get('returnOnEquity', 0)*100):.2f}%"), (get_text("Sector", "துறை"), info.get('sector', 'N/A'))]
        for i, (l, v) in enumerate(f_list):
            (c1 if i % 2 == 0 else c2).markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

    # --- TAB 2: FORECAST (BUY/SELL/HOLD) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Investment Forecast', 'முதலீடு முன்னறிவிப்பு')}")
        
        # Simple Prediction Logic
        pe = info.get('trailingPE', 100)
        roe = info.get('returnOnEquity', 0)
        ma50 = hist['Close'].rolling(50).mean().iloc[-1] if not hist.empty else 0
        
        score = 0
        if pe < 25: score += 35
        if roe > 0.15: score += 35
        if ltp > ma50: score += 30
        
        if score >= 70:
            advice, color, icon = get_text("STRONG BUY", "உறுதியாக வாங்கலாம்"), "#39FF14", "✅"
        elif score >= 40:
            advice, color, icon = get_text("HOLD", "தொடரலாம் (காத்திருக்கவும்)"), "#00D1FF", "⚖️"
        else:
            advice, color, icon = get_text("SELL / AVOID", "விற்கலாம் அல்லது தவிர்க்கவும்"), "#FF3131", "⚠️"
            
        st.markdown(f"""
            <div class="forecast-card" style="border-color: {color}; background: {color}10;">
                <h1 style="color: {color}; font-size: 50px; margin: 0;">{icon} {advice}</h1>
                <p style="color: white; font-size: 18px; margin-top: 10px;">{get_text("Analysis Score", "ஆய்வு மதிப்பெண்")}: {score}/100</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.info(get_text("Note: This is an AI-generated suggestion based on fundamentals. Consult a financial advisor.", "குறிப்பு: இது நிதிநிலைகளை அடிப்படையாகக் கொண்ட தானியங்கி பரிந்துரை. முதலீடு செய்வதற்கு முன் ஆலோசகரை அணுகவும்."))

    # --- TAB 3: SHAREHOLDING ---
    with tabs[2]:
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, 100-(promo+inst)], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#ffd700']))])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark"), use_container_width=True)

    # --- TAB 4: FINANCIALS ---
    with tabs[3]:
        p = st.selectbox("Period", ["Annual", "Quarterly"])
        f_data = stock.financials if p == "Annual" else stock.quarterly_financials
        if not f_data.empty: st.dataframe(f_data.head(10), use_container_width=True)

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        if st.button(f"➕ Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            c1, c2 = st.columns([6, 1])
            c1.info(f"📌 {i}")
            if c2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

except Exception:
    st.error("Enter a valid stock symbol.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
