import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. PAGE CONFIGURATION
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. PRO LUXURY UI STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 13px !important; background-color: #050505 !important; color: #d1d1d1; font-family: 'Inter', sans-serif;
    }
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 28px !important; font-weight: 800;
        background: linear-gradient(90deg, #39FF14, #00D1FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 2px;
    }
    .sub-title { font-size: 10px !important; color: #666; letter-spacing: 2px; text-transform: uppercase; margin-top: 0px; }

    .metric-container {
        display: flex; justify-content: space-between; padding: 10px 0;
        border-bottom: 1px solid #21262d;
    }
    .m-label { color: #8b949e; font-size: 9px; text-transform: uppercase; font-weight: 600; }
    .m-value { color: #ffffff; font-size: 13px; font-weight: 700; }
    
    .section-card {
        background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #21262d; margin-bottom: 15px;
    }
    .price-card {
        background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #39FF1433; margin-bottom: 15px; text-align:center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. AUTHENTICATION
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    u = st.text_input("User ID", key="login_u")
    p = st.text_input("Password", type="password", key="login_p")
    if st.button("Login 🚀", use_container_width=True):
        if u and p: st.session_state['is_logged_in'] = True; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. MAIN HEADER (WITH CREDIT)
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>', unsafe_allow_html=True)

# SEARCH BOX
u_input = st.text_input("Search Symbol (eg: RELIANCE)", value="RELIANCE").upper().strip()
ticker_symbol = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🔮 {get_text('Rating', 'ரேட்டிங்')}",
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 5. CORE LOGIC
try:
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    hist = stock.history(period="1y")

    # --- TAB 1: ANALYSIS (Dynamic Metrics Added) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker_symbol))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="price-card"><span class="m-label">LTP (விலை)</span><br><span style="color:#39FF14; font-size:24px; font-weight:800;">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-container"><span class="m-label">52W High (உச்சம்)</span><span class="m-value" style="color:#39FF14;">₹{info.get("fiftyTwoWeekHigh", 0):,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Market Cap</span><span class="m-value">₹{info.get("marketCap", 0)/10000000:,.0f} Cr</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">P/E Ratio</span><span class="m-value">{info.get("trailingPE", "N/A")}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-container"><span class="m-label">52W Low (தாழ்வு)</span><span class="m-value" style="color:#FF3131;">₹{info.get("fiftyTwoWeekLow", 0):,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Sector</span><span class="m-value">{info.get("sector", "N/A")}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">EPS (TTM)</span><span class="m-value">{info.get("trailingEps", "N/A")}</span></div>', unsafe_allow_html=True)

        st.markdown(f"### 🏢 {get_text('About Company', 'நிறுவனத்தைப் பற்றி')}")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        about_text = info.get('longBusinessSummary', 'No description.')
        st.write(GoogleTranslator(source='auto', target='ta').translate(about_text) if st.session_state['language']=="Tamil" else about_text)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: DYNAMIC RATING (Expert Calculation) ---
    with tabs[1]:
        st.markdown(f"### 🔮 {get_text('Real-time Rating', 'நேரலை மதிப்பீடு')}")
        
        # 1. Fundamental Score (Max 60)
        f_score = 0
        roe = info.get('returnOnEquity', 0) * 100
        debt = info.get('debtToEquity', 100) / 100
        pe = info.get('trailingPE', 100)
        
        if roe > 15: f_score += 20
        if debt < 1: f_score += 20
        if 5 < pe < 30: f_score += 20  # Reasonable valuation
        
        # 2. Technical Score (Max 40)
        t_score = 0
        if not hist.empty and len(hist) > 50:
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rsi = 100 - (100 / (1 + (gain / loss))).iloc[-1]
            
            sma50 = hist['Close'].rolling(window=50).mean().iloc[-1]
            if 40 < rsi < 70: t_score += 20
            if ltp > sma50: t_score += 20
        
        total_score = f_score + t_score
        clr = "#39FF14" if total_score > 70 else ("#00D1FF" if total_score > 45 else "#FF3131")
        rec = get_text("STRONG BUY", "உறுதியாக வாங்கலாம்") if total_score > 75 else (get_text("HOLD", "தொடரலாம்") if total_score > 45 else get_text("AVOID", "விற்கலாம்"))

        st.markdown(f"""
            <div style="border:2px solid {clr}; padding:30px; border-radius:15px; text-align:center; background: {clr}10;">
                <h1 style="color:{clr}; font-size:48px; margin:0;">{total_score}%</h1>
                <h2 style="color:{clr}; margin:10px 0;">{rec}</h2>
                <p style="color:#8b949e; font-size:11px;">Fundamental: {f_score}/60 | Technical: {t_score}/40</p>
            </div>
        """, unsafe_allow_html=True)

    # --- TAB 3: FINANCIALS ---
    with tabs[2]:
        st.markdown(f"### 💰 {get_text('Key Metrics', 'நிதிநிலை விவரம்')}")
        balance = stock.balance_sheet
        reserves = balance.loc['Retained Earnings'].iloc[0] if not balance.empty and 'Retained Earnings' in balance.index else 0
        
        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown(f'<div class="metric-container"><span class="m-label">Net Profit (லாபம்)</span><span class="m-value">₹{info.get("netIncomeToCommon", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
        with fc2:
            st.markdown(f'<div class="metric-container"><span class="m-label">Total Debt (கடன்)</span><span class="m-value">₹{info.get("totalDebt", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Reserves (இருப்பு)</span><span class="m-value">₹{reserves/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)

    # --- TAB 4: SHAREHOLDING ---
    with tabs[3]:
        p, i = (info.get('heldPercentInsiders') or 0)*100, (info.get('heldPercentInstitutions') or 0)*100
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[p, i, 100-(p+i)], 
                                     hole=0.6, marker=dict(colors=['#1A73E8', '#00C853', '#FFAB00'], line=dict(color='#050505', width=2)))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- TAB 5: ACTIONS ---
    with tabs[4]:
        st.markdown(f"### 📅 {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        if not stock.actions.empty: st.dataframe(stock.actions.sort_index(ascending=False).head(15), use_container_width=True)
        else: st.info("No recent data found.")

    # --- TAB 6: WATCHLIST ---
    with tabs[5]:
        if st.button(f"🚀 Add {u_input}"):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for item in st.session_state['watchlist']:
            cw1, cw2 = st.columns([7, 1])
            cw1.markdown(f'<div class="section-card" style="padding:10px; margin-bottom:5px;">📈 {item}</div>', unsafe_allow_html=True)
            if cw2.button("❌", key=f"del_{item}"): st.session_state['watchlist'].remove(item); st.rerun()

except Exception:
    st.error("Error loading data. Check symbol.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
