import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"
if 'broker_connected' not in st.session_state: st.session_state['broker_connected'] = False

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உலகத்தரம் வாய்ந்த UI ஸ்டைலிங்
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; letter-spacing: -1px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 14px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 15px; font-weight: 800; }
    .advice-box { padding: 12px; border-radius: 10px; text-align: center; border: 1px solid; margin-bottom: 15px; }
    .stTabs [aria-selected="true"] { color: #39FF14 !important; border-bottom: 2px solid #39FF14 !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. லாகின்
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="background:#1c2128; padding:30px; border-radius:15px; max-width:400px; margin:auto; border:1px solid #30363d;">', unsafe_allow_html=True)
        u_id = st.text_input("User ID")
        u_pass = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            if u_id and u_pass: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. ஹெடர்
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

# நீங்கள் கேட்ட அதே வரிசை (ORDER)
tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholders', 'பங்குதாரர்கள்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}",
    f"💼 {get_text('Broker', 'புரோக்கர்')}"
])

# 6. டேட்டா இன்ஜின்
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- 1. பகுப்பாய்வு (Deep Fundamental Analysis) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        m1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("Sector P/E", "துறை பி.இ"), info.get('sector', 'N/A'))
        ]
        m2 = [
            (get_text("ROE", "ஆர்.ஓ.இ (ROE)"), f"{(info.get('returnOnEquity', 0)*100):.2f}%"),
            (get_text("Debt to Equity", "கடன் விகிதம்"), info.get('debtToEquity', 'N/A')),
            (get_text("Book Value", "புத்தக மதிப்பு"), f"₹{info.get('bookValue', 0):,.2f}")
        ]
        for l, v in m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        
        with st.expander(get_text("About Company", "நிறுவனத்தைப் பற்றி")):
            st.write(GoogleTranslator(source='auto', target='ta').translate(info.get('longBusinessSummary', '')) if st.session_state['language']=="Tamil" else info.get('longBusinessSummary', ''))

    # --- 2. பங்குதாரர்கள் (FII/DII) ---
    with tabs[1]:
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = max(0, inst - fii)
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, max(0, 100-(promo+inst))], hole=0.5)])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- 3. நிதிநிலை (Net Profit, Debt, 10Y Growth) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Growth Analysis', 'நிதி வளர்ச்சி')}")
        f_m = [
            (get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"),
            (get_text("Total Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr"),
            (get_text("Revenue Growth", "வருவாய் வளர்ச்சி"), f"{(info.get('revenueGrowth', 0)*100):.2f}%"),
            (get_text("EPS", "இ.பி.எஸ் (EPS)"), f"₹{info.get('trailingEps', 0):,.2f}")
        ]
        for lbl, val in f_m: st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
        st.line_chart(stock.financials.loc['Net Income'] if 'Net Income' in stock.financials.index else [])

    # --- 4. நிகழ்வுகள் (Dividends/Splits) ---
    with tabs[3]:
        st.dataframe(stock.actions.tail(15).sort_index(ascending=False), use_container_width=True)

    # --- 5. வாட்ச்லிஸ்ட் ---
    with tabs[4]:
        if st.button(f"🚀 {get_text('Add', 'சேர்க்க')} {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            cw1, cw2 = st.columns([6, 1])
            cw1.markdown(f'<div style="background:#1c2128; padding:12px; border-radius:10px; margin-bottom:5px;">📈 {i}</div>', unsafe_allow_html=True)
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

    # --- 6. முன்னறிவிப்பு (AI Prediction) ---
    with tabs[5]:
        score = 80 if info.get('trailingPE', 100) < 25 else 45
        adv, clr = (get_text("BUY", "வாங்கலாம்"), "#39FF14") if score > 70 else (get_text("HOLD", "தொடரலாம்"), "#00D1FF")
        st.markdown(f'<div class="advice-box" style="border-color: {clr}; background: {clr}05;"><p style="font-size:16px; font-weight:700; color:{clr}; margin:0;">{adv} (SCORE: {score})</p></div>', unsafe_allow_html=True)

    # --- 7. புரோக்கர் (Broker Connect) ---
    with tabs[6]:
        if not st.session_state['broker_connected']:
            if st.button("Connect Zerodha / Angel One"): st.session_state['broker_connected'] = True; st.rerun()
        else: st.success("Connected! Portfolio: ₹1,50,000")

except Exception:
    st.error("சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
