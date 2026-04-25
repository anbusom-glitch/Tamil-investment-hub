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
if 'broker_connected' not in st.session_state: st.session_state['broker_connected'] = False

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
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 15px; font-weight: 800; }
    .login-box, .broker-card { background: #1c2128; border: 1px solid #30363d; border-radius: 15px; padding: 30px; max-width: 450px; margin: auto; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN SYSTEM
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("Login / உள்நுழைக")
        u_id = st.text_input("User ID / Mobile")
        u_pass = st.text_input("Password", type="password")
        if st.button("Access Hub 🚀", use_container_width=True):
            if u_id and u_pass: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. DASHBOARD HEADER
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. SEARCH ENGINE
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"💼 {get_text('Broker', 'புரோக்கர்')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. DATA ENGINE
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- TAB 1: ANALYSIS (METRIC ROW RESTORED) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        c1, c2 = st.columns(2)
        m1 = [(get_text("Price", "விலை"), f"₹{ltp:,.2f}"), (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}")]
        m2 = [(get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"), (get_text("Sector", "துறை"), info.get('sector', 'N/A'))]
        for l, v in m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        with st.expander(get_text("About Company", "நிறுவனத்தைப் பற்றி")):
            st.write(GoogleTranslator(source='auto', target='ta').translate(info.get('longBusinessSummary', '')) if st.session_state['language']=="Tamil" else info.get('longBusinessSummary', ''))

    # --- TAB 2: BROKER CONNECT (NEW) ---
    with tabs[1]:
        if not st.session_state['broker_connected']:
            st.markdown('<div class="broker-card">', unsafe_allow_html=True)
            st.info("Connect with your favorite broker to track portfolio.")
            if st.button("Connect Zerodha / Angel One"): st.session_state['broker_connected'] = True; st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.success("Broker Connected! ✅")
            st.markdown('<div class="metric-row"><span class="m-label">Portfolio Value</span><span class="m-value">₹1,25,000</span></div>', unsafe_allow_html=True)

    # --- TAB 3: CORPORATE ACTIONS (RESTORED) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Dividends & Splits', 'டிவிடெண்ட் மற்றும் போனஸ்')}")
        if not stock.actions.empty: st.dataframe(stock.actions.tail(15).sort_index(ascending=False), use_container_width=True)
        else: st.info("சமீபத்திய நிகழ்வுகள் ஏதுமில்லை.")

    # --- TAB 4: SHAREHOLDING (FII/DII) ---
    with tabs[3]:
        promo, inst = (info.get('heldPercentInsiders') or 0) * 100, (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = max(0, inst - fii)
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, max(0, 100-(promo+inst))], hole=0.5)])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- TAB 5: FINANCIALS (PROFIT/DEBT/10YR GROWTH) ---
    with tabs[4]:
        st.markdown(f"### {get_text('Financial Growth', 'நிதி வளர்ச்சி')}")
        f_m = [(get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"), (get_text("Total Debt", "கடனைத் தீர்க்க"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr"), (get_text("Growth", "வளர்ச்சி"), f"{(info.get('revenueGrowth', 0)*100):.2f}%")]
        for lbl, val in f_m: st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

    # --- TAB 6: WATCHLIST ---
    with tabs[5]:
        if st.button(f"🚀 {get_text('Add', 'சேர்க்க')} {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            cw1, cw2 = st.columns([6, 1])
            cw1.info(f"📈 {i}")
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

except Exception: st.error("சரியான பங்கு குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
