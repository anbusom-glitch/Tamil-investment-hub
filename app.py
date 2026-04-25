import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. PAGE SETUP
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. PREMIUM UI STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    .header-container { text-align: center; padding: 20px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; letter-spacing: -1px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; letter-spacing: 2px; text-transform: uppercase; margin-top: 5px; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 15px; font-weight: 800; }
    .advice-box { padding: 15px; border-radius: 12px; text-align: center; border: 1px solid; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN SYSTEM
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="background:#1c2128; padding:35px; border-radius:15px; max-width:400px; margin:auto; border:1px solid #30363d;">', unsafe_allow_html=True)
        u_id = st.text_input("User ID")
        u_pass = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            if u_id and u_pass: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. DASHBOARD HEADER
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. SEARCH ENGINE
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. DATA HANDLING
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- TAB 1: ANALYSIS (METRICS ADDED BACK) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        
        # Fundamental Grid
        c1, c2 = st.columns(2)
        m1 = [
            (get_text("LTP", "தற்போதைய விலை"), f"₹{ltp:,.2f}"),
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            (get_text("52W Low", "52 வார நீச்சம்"), f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}")
        ]
        m2 = [
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("ROE", "ROE (%)"), f"{(info.get('returnOnEquity', 0)*100):.2f}%"),
            (get_text("Dividend Yield", "டிவிடெண்ட்"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("Sector", "துறை"), info.get('sector', 'N/A'))
        ]
        
        for l, v in m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        
        with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
            about = info.get('longBusinessSummary', 'No description.')
            st.write(GoogleTranslator(source='auto', target='ta').translate(about) if st.session_state['language']=="Tamil" else about)

    # --- TAB 2: FORECAST ---
    with tabs[1]:
        score = 80 if info.get('trailingPE', 100) < 25 else 45
        adv, clr = (get_text("Buy", "வாங்கலாம்"), "#39FF14") if score > 70 else (get_text("Hold", "தொடரலாம்"), "#00D1FF")
        st.markdown(f'<div class="advice-box" style="border-color: {clr}; background: {clr}05;"><p style="font-size:16px; font-weight:700; color:{clr}; margin:0;">{adv}</p></div>', unsafe_allow_html=True)

    # --- TAB 3: SHAREHOLDING (FII/DII) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = inst - fii
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, max(0, 100-(promo+inst))], hole=0.5)])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- TAB 4: FINANCIALS (PROFIT, DEBT, GROWTH, RESERVES) ---
    with tabs[3]:
        st.markdown(f"### {get_text('Key Financials', 'நிதிநிலை விவரங்கள்')}")
        balance_sheet = stock.balance_sheet
        reserves = 0
        if not balance_sheet.empty and 'Retained Earnings' in balance_sheet.index:
            reserves = balance_sheet.loc['Retained Earnings'].iloc[0]

        f_metrics = [
            (get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"),
            (get_text("Total Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr"),
            (get_text("Cash", "பணப்புழக்கம்"), f"₹{info.get('totalCash', 0)/10000000:,.2f} Cr"),
            (get_text("Revenue Growth", "வருவாய் வளர்ச்சி"), f"{(info.get('revenueGrowth', 0)*100):.2f}%"),
            (get_text("Reserves", "இருப்பு நிதி"), f"₹{reserves/10000000:,.2f} Cr")
        ]
        for lbl, val in f_metrics:
            st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        if st.button(f"Add {u_input}"):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']: st.info(f"📌 {i}")

except Exception:
    st.error("சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
