import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# Session State Initialization
if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. ADVANCED UI STYLING (Moneycontrol Style)
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 12px !important; 
        background-color: #050505 !important; 
        color: #d1d1d1; 
    }
    .main-title { 
        font-size: 26px !important; font-weight: 800;
        background: linear-gradient(90deg, #39FF14, #00D1FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 10px;
    }
    .metric-container {
        display: flex;
        justify-content: space-between;
        padding: 8px 0;
        border-bottom: 1px solid #21262d;
    }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 600; }
    .m-value { color: #ffffff; font-size: 13px; font-weight: 700; }
    .auth-card { background: #0d1117; border: 1px solid #21262d; border-radius: 12px; padding: 20px; max-width: 400px; margin: auto; }
    .watchlist-card { background: #10141b; border: 1px solid #21262d; border-radius: 10px; padding: 10px 15px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN & SIGNUP SYSTEM
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
    t_login, t_signup = st.tabs(["🔐 Login", "✍️ Sign Up"])
    with t_login:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        l_u = st.text_input("User ID", key="l_u")
        l_p = st.text_input("Password", type="password", key="l_p")
        if st.button("Access Hub 🚀", use_container_width=True):
            if l_u and l_p: st.session_state['is_logged_in'] = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    with t_signup:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.text_input("Mobile Number", key="s_m")
        st.text_input("Password", type="password", key="s_p")
        if st.button("Create Account ✅", use_container_width=True): st.success("Account Created!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. HEADER & SEARCH
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
u_input = st.text_input("Search Symbol", value="HDFCBANK").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}"
])

# 5. DATA ENGINE
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- TAB 0: ANALYSIS (Two Column Stats) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div style="background:#0d1117; padding:10px; border-radius:10px; border:1px solid #21262d;"><span style="color:#8b949e; font-size:10px;">LTP</span><br><span style="color:#39FF14; font-size:20px; font-weight:800;">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        st.markdown(f"### {get_text('Key Statistics', 'முக்கிய விவரங்கள்')}")
        col1, col2 = st.columns(2)
        m1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("TTM P/E", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("Price to Book", "பி.பி விகிதம்"), info.get('priceToBook', 'N/A')),
            (get_text("Face Value", "முக மதிப்பு"), info.get('faceValue', 'N/A'))
        ]
        m2 = [
            (get_text("Book Value", "புத்தக மதிப்பு"), f"₹{info.get('bookValue', 0):,.2f}"),
            (get_text("Div. Yield", "டிவிடெண்ட்"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("EPS (TTM)", "ஈபிஎஸ் (EPS)"), info.get('trailingEps', 'N/A')),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}")
        ]
        with col1:
            for l, v in m1: st.markdown(f'<div class="metric-container"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        with col2:
            for l, v in m2: st.markdown(f'<div class="metric-container"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

    # --- TAB 1: SHAREHOLDING (High Contrast) ---
    with tabs[1]:
        p, i = (info.get('heldPercentInsiders') or 0)*100, (info.get('heldPercentInstitutions') or 0)*100
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[p, i*0.6, i*0.4, 100-(p+i)], 
                                     hole=0.6, marker=dict(colors=['#1A73E8', '#D32F2F', '#00C853', '#FFAB00'], line=dict(color='#050505', width=2)))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=350, margin=dict(t=0, b=0)), use_container_width=True)

    # --- TAB 2: FINANCIALS ---
    with tabs[2]:
        f_m = [(get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"), (get_text("Total Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr")]
        for l, v in f_m: st.markdown(f'<div class="metric-container"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

    # --- TAB 3: ACTIONS ---
    with tabs[3]:
        if not stock.actions.empty: st.dataframe(stock.actions.tail(10), use_container_width=True)

    # --- TAB 4: WATCHLIST ---
    with tabs[4]:
        if st.button(f"🚀 Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            c_w1, c_w2 = st.columns([7, 1])
            c_w1.markdown(f'<div class="watchlist-card">📈 {i}</div>', unsafe_allow_html=True)
            if c_w2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

    # --- TAB 5: FORECAST ---
    with tabs[5]:
        score = 80 if info.get('trailingPE', 100) < 25 else 45
        adv, clr = (get_text("BUY", "வாங்கலாம்"), "#39FF14") if score > 70 else (get_text("HOLD", "தொடரலாம்"), "#00D1FF")
        st.markdown(f'<div style="border:1px solid {clr}; padding:15px; border-radius:10px; text-align:center;"><h3 style="color:{clr};">{adv}</h3></div>', unsafe_allow_html=True)

except Exception:
    st.error("Invalid Symbol. Please search again.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
