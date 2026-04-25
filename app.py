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
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 15px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. LOGIN
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="background:#1c2128; padding:35px; border-radius:15px; max-width:400px; margin:auto; border:1px solid #30363d;">', unsafe_allow_html=True)
        st.subheader("Login / உள்நுழைக")
        u_id = st.text_input("User ID")
        u_pass = st.text_input("Password", type="password")
        if st.button("Login 🚀", use_container_width=True):
            if u_id and u_pass: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. DASHBOARD HEADER
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. SEARCH
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. DATA ENGINE
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- TAB 1: ANALYSIS ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        with st.expander(get_text("About Company", "நிறுவனத்தைப் பற்றி")):
            about = info.get('longBusinessSummary', 'No data.')
            st.write(GoogleTranslator(source='auto', target='ta').translate(about) if st.session_state['language']=="Tamil" else about)

    # --- TAB 2: SHAREHOLDING (FII/DII) ---
    with tabs[1]:
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = inst - fii
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, max(0, 100-(promo+inst))], hole=0.5)])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- 🌟 TAB 3: FINANCIALS (10 YEAR GROWTH ADDED) 🌟 ---
    with tabs[2]:
        st.markdown(f"### {get_text('Financial Performance', 'நிதிநிலை செயல்பாடு')}")
        
        # 1. 10 Year Profit Growth Graph
        fin_annual = stock.financials
        if not fin_annual.empty:
            try:
                # 'Net Income' அல்லது 'Net Profit' தரவை எடுத்தல்
                row_label = 'Net Income' if 'Net Income' in fin_annual.index else fin_annual.index[0]
                profit_history = fin_annual.loc[row_label].sort_index()
                
                fig_grow = go.Figure()
                fig_grow.add_trace(go.Scatter(x=profit_history.index, y=profit_history.values, mode='lines+markers', name='Profit', line=dict(color='#39FF14', width=3)))
                fig_grow.update_layout(title=get_text("Profit History", "லாப வரலாறு"), template="plotly_dark", height=300, margin=dict(l=0,r=0,t=40,b=0))
                st.plotly_chart(fig_grow, use_container_width=True)
            except: st.info("வரலாற்று வரைபடம் கிடைக்கவில்லை.")

        # 2. Key Pro Metrics
        f_m = [
            (get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"),
            (get_text("Total Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr"),
            (get_text("Cash Flow", "பணப்புழக்கம்"), f"₹{info.get('totalCash', 0)/10000000:,.2f} Cr"),
            (get_text("Revenue Growth", "வருவாய் வளர்ச்சி"), f"{(info.get('revenueGrowth', 0)*100):.2f}%"),
            (get_text("Earnings (EPS)", "ஈட்டி வரும் லாபம் (EPS)"), f"₹{info.get('trailingEps', 0):,.2f}")
        ]
        for lbl, val in f_m:
            st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

    # --- TAB 4: WATCHLIST ---
    with tabs[3]:
        if st.button(f"🚀 {get_text('Add', 'சேர்க்க')} {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            cw1, cw2 = st.columns([6, 1])
            cw1.markdown(f'<div style="background:#1c2128; padding:12px; border-radius:10px; margin-bottom:5px;">📈 {i}</div>', unsafe_allow_html=True)
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

except Exception:
    st.error("Error loading data.")

st.markdown("<p style='text-align:center; color:#444; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
