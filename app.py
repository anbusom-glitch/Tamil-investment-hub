import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு (Page Configuration)
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# Session State தொடக்கம்
if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"
if 'broker_connected' not in st.session_state: st.session_state['broker_connected'] = False

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. LUXURY DARK UI STYLING (ஒட்டுமொத்த தோற்றம்)
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 14px !important; 
        background-color: #050505 !important; 
        color: #e0e0e0; 
        font-family: 'Segoe UI', sans-serif;
    }
    
    /* Luxury Header */
    .header-container { text-align: center; padding: 25px 0; }
    .main-title { 
        font-size: 38px !important; font-weight: 900; letter-spacing: -1.5px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 11px !important; color: #555; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }

    /* Login & Metric Cards */
    .auth-card, .metric-row { 
        background: #0d1117; 
        border: 1px solid #21262d; 
        border-radius: 16px; 
        padding: 20px; 
        margin-bottom: 12px;
        transition: 0.3s;
    }
    .metric-row:hover { border-color: #39FF14; }
    
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    
    /* Forecast Advice Box */
    .advice-box { padding: 20px; border-radius: 12px; text-align: center; border: 1px solid; margin-bottom: 20px; }
    
    /* Custom Watchlist Card */
    .watchlist-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 12px 18px; margin-bottom: 8px; display: flex;
        justify-content: space-between; align-items: center;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { 
        background: #0d1117; border-radius: 8px; padding: 10px 20px; color: #8b949e; border: 1px solid #21262d;
    }
    .stTabs [aria-selected="true"] { 
        background: rgba(57, 255, 20, 0.1) !important; color: #39FF14 !important; border-color: #39FF14 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. லாகின் மற்றும் சைன்-அப் சிஸ்டம்
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">Ultimate Pro Experience</p></div>', unsafe_allow_html=True)
    
    t_login, t_signup = st.tabs(["🔐 Login (உள்நுழைக)", "✍️ Sign Up (பதிவு செய்க)"])
    
    with t_login:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        l_user = st.text_input("User ID", key="login_u")
        l_pass = st.text_input("Password", type="password", key="login_p")
        if st.button("Enter Hub 🚀", use_container_width=True):
            if l_user and l_pass: st.session_state['is_logged_in'] = True; st.rerun()
            else: st.warning("Please enter credentials.")
        st.markdown('</div>', unsafe_allow_html=True)

    with t_signup:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.text_input("Full Name", key="reg_n")
        st.text_input("Mobile Number", key="reg_m")
        st.text_input("Create Password", type="password", key="reg_p")
        if st.button("Create Account ✅", use_container_width=True):
            st.success("கணக்கு உருவாக்கப்பட்டது! இப்போது லாகின் செய்யவும்.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. மெயின் ஆப் ஹெடர் (Main Dashboard Header)
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. சர்ச் மற்றும் டேப்கள் (Search & Tab Order)
u_input = st.text_input("Search Symbol (eg: RELIANCE, TCS)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}",
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}",
    f"💼 {get_text('Broker', 'புரோக்கர்')}"
])

# 6. தரவு கையாளுதல் (Core Logic)
try:
    stock = yf.Ticker(ticker)
    info = stock.info

    # --- TAB 1: ஆழமான பகுப்பாய்வு (Analysis) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="metric-row"><span class="m-label">Current Price (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        m1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("ROE (%)", "ROE (%)"), f"{(info.get('returnOnEquity', 0)*100):.2f}%"),
            (get_text("Debt to Equity", "கடன் விகிதம்"), info.get('debtToEquity', 'N/A'))
        ]
        m2 = [
            (get_text("Dividend Yield", "டிவிடெண்ட்"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("EPS (TTM)", "ஈபிஎஸ் (EPS)"), info.get('trailingEps', 'N/A')),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            (get_text("Sector", "துறை"), info.get('sector', 'N/A'))
        ]
        for l, v in m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        
        with st.expander(get_text("About Company", "நிறுவனத்தைப் பற்றி")):
            about = info.get('longBusinessSummary', 'No description available.')
            st.write(GoogleTranslator(source='auto', target='ta').translate(about) if st.session_state['language']=="Tamil" else about)

    # --- TAB 2: பங்குதாரர் விபரம் (Shareholding - High Contrast) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = max(0, inst - fii)
        pub = max(0, 100 - (promo + inst))
        
        # 🎨 HIGH CONTRAST DARK COLORS 🎨
        contrast_colors = ['#1A73E8', '#D32F2F', '#00C853', '#FFAB00']
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], 
                                     hole=0.6, marker=dict(colors=contrast_colors, line=dict(color='#050505', width=3)))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=450), use_container_width=True)

    # --- TAB 3: நிதிநிலை (Financials) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Financial Growth', 'நிதிநிலை வளர்ச்சி')}")
        f_m = [
            (get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"),
            (get_text("Total Debt", "மொத்த கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr"),
            (get_text("Cash Flow", "பணப்புழக்கம்"), f"₹{info.get('totalCash', 0)/10000000:,.2f} Cr"),
            (get_text("Revenue Growth", "வருவாய் வளர்ச்சி"), f"{(info.get('revenueGrowth', 0)*100):.2f}%")
        ]
        for lbl, val in f_m: st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

    # --- TAB 4: நிறுவன நிகழ்வுகள் (Actions) ---
    with tabs[3]:
        st.markdown(f"### {get_text('Dividends & Splits', 'நிறுவன நிகழ்வுகள்')}")
        if not stock.actions.empty: st.dataframe(stock.actions.tail(15).sort_index(ascending=False), use_container_width=True)
        else: st.info("No recent corporate actions.")

    # --- TAB 5: வாட்ச்லிஸ்ட் (Watchlist) ---
    with tabs[4]:
        if st.button(f"🚀 {get_text('Add to Watchlist', 'வாட்ச்லிஸ்ட்டில் சேர்')} {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        st.write("---")
        for i in st.session_state['watchlist']:
            cw1, cw2 = st.columns([7, 1])
            cw1.markdown(f'<div class="watchlist-card">📈 {i}</div>', unsafe_allow_html=True)
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

    # --- TAB 6: முன்னறிவிப்பு (Forecast) ---
    with tabs[5]:
        score = 80 if info.get('trailingPE', 100) < 25 else 45
        adv, clr = (get_text("BUY", "வாங்கலாம்"), "#39FF14") if score > 70 else (get_text("HOLD", "தொடரலாம்"), "#00D1FF")
        st.markdown(f'<div class="advice-box" style="border-color: {clr}; background: {clr}05;"><h2 style="color: {clr}; margin:0;">{adv}</h2><p>Analysis Score: {score}/100</p></div>', unsafe_allow_html=True)

    # --- TAB 7: புரோக்கர் (Broker) ---
    with tabs[6]:
        if not st.session_state['broker_connected']:
            if st.button("Connect Zerodha / Angel One", use_container_width=True): st.session_state['broker_connected'] = True; st.rerun()
        else:
            st.success("Broker Connected! ✅")
            st.markdown('<div class="metric-row"><span class="m-label">Portfolio Value</span><span class="m-value">₹1,50,000</span></div>', unsafe_allow_html=True)

except Exception:
    st.error("சரியான பங்கு குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#333; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
