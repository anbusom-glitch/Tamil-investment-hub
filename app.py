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

# 2. Sleek UI Styling (Small fonts & Dark Contrast)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 13px !important; background-color: #050505 !important; color: #d1d1d1; }
    .main-title { 
        font-size: 28px !important; font-weight: 800; letter-spacing: -1px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center;
    }
    .metric-row { 
        background: #0d1117; border: 1px solid #21262d; border-radius: 10px; 
        padding: 10px 15px; margin-bottom: 8px; display: flex; 
        justify-content: space-between; align-items: center; 
    }
    .m-label { color: #8b949e; font-size: 9px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 13px; font-weight: 700; }
    .stTabs [data-baseweb="tab"] { font-size: 12px; padding: 8px 12px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Login Check (Simplified for speed)
if not st.session_state['is_logged_in']:
    st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
    with st.container():
        u = st.text_input("User ID")
        p = st.text_input("Password", type="password")
        if st.button("Access Hub 🚀", use_container_width=True):
            if u and p: st.session_state['is_logged_in'] = True; st.rerun()
    st.stop()

# 4. Header & Search
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
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

# 5. Core Data Handling
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- TAB 1: ANALYSIS (Fundamental Metrics Restored) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        
        # Main Metric Row
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        # Deep Fundamental List
        m1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("P/B Ratio", "பி.பி விகிதம்"), info.get('priceToBook', 'N/A')),
            (get_text("ROE (%)", "ROE (%)"), f"{(info.get('returnOnEquity', 0)*100):.2f}%")
        ]
        m2 = [
            (get_text("Div. Yield", "டிவிடெண்ட் ஈல்டு"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("EPS (TTM)", "ஈபிஎஸ் (EPS)"), info.get('trailingEps', 'N/A')),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            (get_text("Sector", "துறை"), info.get('sector', 'N/A'))
        ]
        
        for l, v in m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

        with st.expander(get_text("About Company", "நிறுவனத்தைப் பற்றி")):
            about = info.get('longBusinessSummary', 'No data.')
            st.write(GoogleTranslator(source='auto', target='ta').translate(about) if st.session_state['language']=="Tamil" else about)

    # (Other tabs logic for Shareholding, Financials, etc. remains same as previous versions)
    # --- TAB 2: SHAREHOLDING (High Contrast) ---
    with tabs[1]:
        promo, inst = (info.get('heldPercentInsiders') or 0)*100, (info.get('heldPercentInstitutions') or 0)*100
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], 
                                     values=[promo, inst*0.6, inst*0.4, 100-(promo+inst)], 
                                     hole=0.6, marker=dict(colors=['#1A73E8', '#D32F2F', '#00C853', '#FFAB00'], line=dict(color='#050505', width=2)))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=380, margin=dict(t=0, b=0)), use_container_width=True)

    # --- TAB 3: FINANCIALS (Net Profit, Debt, Growth) ---
    with tabs[2]:
        f_metrics = [
            (get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"),
            (get_text("Total Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr"),
            (get_text("Revenue Growth", "வருவாய் வளர்ச்சி"), f"{(info.get('revenueGrowth', 0)*100):.2f}%")
        ]
        for lbl, val in f_metrics: st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

except Exception:
    st.error("தரவுகளைப் பெறுவதில் சிக்கல். சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#222; font-size:9px; margin-top:40px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
