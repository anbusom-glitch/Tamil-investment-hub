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

# 2. LUXURY SLEEK UI STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 13px !important; background-color: #050505 !important; color: #d1d1d1; font-family: 'Inter', sans-serif;
    }
    .main-title { 
        font-size: 28px !important; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #39FF14, #00D1FF);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }
    .metric-container {
        display: flex; justify-content: space-between; padding: 10px 0;
        border-bottom: 1px solid #21262d;
    }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 600; }
    .m-value { color: #ffffff; font-size: 13px; font-weight: 700; }
    
    .section-card {
        background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #21262d; margin-bottom: 20px;
    }
    .price-card {
        background: #0d1117; padding: 15px; border-radius: 12px; border: 1px solid #39FF1433; margin-bottom: 20px; text-align:center;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. AUTHENTICATION
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    u = st.text_input("User ID", key="login_u")
    p = st.text_input("Password", type="password", key="login_p")
    if st.button("Login 🚀", use_container_width=True):
        if u and p: st.session_state['is_logged_in'] = True; st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. HEADER
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker_symbol = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
    f"🔮 {get_text('Rating', 'ரேட்டிங்')}"
])

# 5. DATA ENGINE
try:
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    hist = stock.history(period="1y")

    # --- TAB 1: ANALYSIS (52W Side-by-Side & About Us Section) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker_symbol))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="price-card"><span class="m-label">LTP (விலை)</span><br><span style="color:#39FF14; font-size:26px; font-weight:800;">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-container"><span class="m-label">52W High (உச்சம்)</span><span class="m-value" style="color:#39FF14;">₹{info.get("fiftyTwoWeekHigh", 0):,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Market Cap</span><span class="m-value">₹{info.get("marketCap", 0)/10000000:,.0f} Cr</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">P/E Ratio</span><span class="m-value">{info.get("trailingPE", "N/A")}</span></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-container"><span class="m-label">52W Low (தாழ்வு)</span><span class="m-value" style="color:#FF3131;">₹{info.get("fiftyTwoWeekLow", 0):,.2f}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Sector</span><span class="m-value">{info.get("sector", "N/A")}</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">EPS (TTM)</span><span class="m-value">{info.get("trailingEps", "N/A")}</span></div>', unsafe_allow_html=True)

        # Dedicated About Us Section
        st.markdown(f"### 🏢 {get_text('About Company', 'நிறுவனத்தைப் பற்றி')}")
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        about_text = info.get('longBusinessSummary', 'No description.')
        st.write(GoogleTranslator(source='auto', target='ta').translate(about_text) if st.session_state['language']=="Tamil" else about_text)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TAB 2: FINANCIALS (Expanded Metrics & Growth Chart) ---
    with tabs[1]:
        st.markdown(f"### 💰 {get_text('Key Financials', 'முக்கிய நிதிநிலை விவரங்கள்')}")
        
        balance_sheet = stock.balance_sheet
        financials = stock.financials
        
        # Reserves calculation (Approximate logic if specific field not present)
        reserves = 0
        if not balance_sheet.empty and 'Retained Earnings' in balance_sheet.index:
            reserves = balance_sheet.loc['Retained Earnings'].iloc[0]

        fc1, fc2 = st.columns(2)
        with fc1:
            st.markdown(f'<div class="metric-container"><span class="m-label">Net Profit (நிகர லாபம்)</span><span class="m-value">₹{info.get("netIncomeToCommon", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Total Debt (கடன்)</span><span class="m-value">₹{info.get("totalDebt", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Reserves (இருப்பு நிதி)</span><span class="m-value">₹{reserves/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
        with fc2:
            st.markdown(f'<div class="metric-container"><span class="m-label">Revenue Growth</span><span class="m-value">{(info.get("revenueGrowth", 0)*100):.2f}%</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Cash (பணப்புழக்கம்)</span><span class="m-value">₹{info.get("totalCash", 0)/10000000:,.2f} Cr</span></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-container"><span class="m-label">Profit Margin</span><span class="m-value">{(info.get("profitMargins", 0)*100):.2f}%</span></div>', unsafe_allow_html=True)

        # Historical Growth Chart
        if not financials.empty:
            st.markdown(f"### 📈 {get_text('Historical Net Income', 'கடந்த ஆண்டுகளின் லாப வளர்ச்சி')}")
            # Filter for Net Income
            income_row = 'Net Income' if 'Net Income' in financials.index else financials.index[0]
            profit_data = financials.loc[income_row].sort_index()
            
            fig_prof = go.Figure()
            fig_prof.add_trace(go.Scatter(x=profit_data.index, y=profit_data.values/10000000, mode='lines+markers', name='Profit', line=dict(color='#39FF14', width=3)))
            fig_prof.update_layout(template="plotly_dark", height=300, margin=dict(l=0,r=0,t=20,b=0), yaxis_title="Cr")
            st.plotly_chart(fig_prof, use_container_width=True)

except Exception as e:
    st.error("Error loading data. Check symbol.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
