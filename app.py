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

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. Sleek UI Styling (Font sizes reduced for Pro look)
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 13px !important; 
        background-color: #050505 !important; 
        color: #d1d1d1; 
    }
    
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 28px !important; font-weight: 800; letter-spacing: -1px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 9px !important; color: #444; letter-spacing: 2px; text-transform: uppercase; }

    .auth-card, .metric-row { 
        background: #0d1117; 
        border: 1px solid #21262d; 
        border-radius: 12px; 
        padding: 12px; 
        margin-bottom: 8px;
    }
    
    .m-label { color: #8b949e; font-size: 9px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 14px; font-weight: 700; }
    
    .advice-box { padding: 15px; border-radius: 10px; text-align: center; border: 1px solid; margin-bottom: 15px; }
    .advice-text { font-size: 15px !important; font-weight: 700; margin: 0; }

    .watchlist-card {
        background: #10141b; border: 1px solid #21262d; border-radius: 10px;
        padding: 10px 15px; margin-bottom: 6px; display: flex;
        justify-content: space-between; align-items: center;
    }

    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        background: #0d1117; border-radius: 6px; padding: 8px 15px; color: #8b949e; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Login/Sign-up System
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    t_login, t_signup = st.tabs(["🔐 Login", "✍️ Sign Up"])
    
    with t_login:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        l_user = st.text_input("User ID", key="login_u")
        l_pass = st.text_input("Password", type="password", key="login_p")
        if st.button("Access Hub 🚀", use_container_width=True):
            if l_user and l_pass: st.session_state['is_logged_in'] = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    with t_signup:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.text_input("Mobile Number", key="reg_m")
        st.text_input("Create Password", type="password", key="reg_p")
        if st.button("Create Account", use_container_width=True):
            st.success("கணக்கு உருவாக்கப்பட்டது!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. Main Dashboard Header
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. Search & Tabs (Broker Removed)
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}"
])

# 6. Core Logic
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    with tabs[0]: # Analysis
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        m1 = [(get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"), (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A'))]
        m2 = [(get_text("ROE (%)", "ROE (%)"), f"{(info.get('returnOnEquity', 0)*100):.2f}%"), (get_text("Sector", "துறை"), info.get('sector', 'N/A'))]
        for l, v in m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

    with tabs[1]: # Shareholding (Contrast Colors)
        promo, inst = (info.get('heldPercentInsiders') or 0) * 100, (info.get('heldPercentInstitutions') or 0) * 100
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, inst*0.6, inst*0.4, 100-(promo+inst)], 
                                     hole=0.6, marker=dict(colors=['#1A73E8', '#D32F2F', '#00C853', '#FFAB00'], line=dict(color='#050505', width=2)))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400, margin=dict(t=0, b=0)), use_container_width=True)

    with tabs[2]: # Financials
        f_m = [(get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"), (get_text("Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr")]
        for lbl, val in f_m: st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

    with tabs[3]: # Actions
        if not stock.actions.empty: st.dataframe(stock.actions.tail(10), use_container_width=True)
        else: st.info("No actions.")

    with tabs[4]: # Watchlist
        if st.button(f"🚀 Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            cw1, cw2 = st.columns([7, 1])
            cw1.markdown(f'<div class="watchlist-card">📈 {i}</div>', unsafe_allow_html=True)
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

    with tabs[5]: # Forecast
        score = 80 if info.get('trailingPE', 100) < 25 else 45
        adv, clr = (get_text("BUY", "வாங்கலாம்"), "#39FF14") if score > 70 else (get_text("HOLD", "தொடரலாம்"), "#00D1FF")
        st.markdown(f'<div class="advice-box" style="border-color: {clr}; background: {clr}05;"><p class="advice-text" style="color: {clr};">{adv}</p></div>', unsafe_allow_html=True)

except Exception:
    st.error("Error loading data.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
