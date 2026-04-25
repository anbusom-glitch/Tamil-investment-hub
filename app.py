import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from datetime import datetime

# 1. PAGE SETUP
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. WORLD-CLASS PRO UI STYLING (Font sizes & cards refined)
st.markdown("""
    <style>
    /* Global Styles */
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; font-family: 'Segoe UI', Roboto, sans-serif; }
    
    /* Header & Title */
    .header-container { text-align: center; padding: 25px 0; margin-bottom: 15px; }
    .main-title { 
        font-size: 36px !important; font-weight: 800; margin-bottom: 0px; letter-spacing: -1px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.7; text-transform: uppercase; margin-top: 5px; }
    
    /* Metric Rows */
    .metric-row { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; 
        transition: 0.3s;
    }
    .metric-row:hover { border-color: #00D1FF; background: #1c2128; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; letter-spacing: 1px; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    
    /* Login & Pro Cards */
    .pro-card { background: #1c2128; border: 1px solid #30363d; border-radius: 16px; padding: 35px; max-width: 450px; margin: auto; box-shadow: 0 15px 40px rgba(0,0,0,0.6); }
    
    /* 💥 REFINE FONT SIZE (eg: விற்கலாம்) 💥 */
    .advice-text { font-size: 18px !important; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
    .score-text { font-size: 12px !important; color: #8b949e; margin-top: 4px; }
    
    /* Expander & Tabs */
    .stExpander { background: rgba(57, 255, 20, 0.03) !important; border: 1px solid #30363d !important; border-radius: 12px !important; margin-top: 15px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { background: #161b22; border-radius: 8px; padding: 10px 18px; color: #8b949e; border: 1px solid transparent; }
    .stTabs [aria-selected="true"] { background: rgba(57, 255, 20, 0.1) !important; color: #39FF14 !important; border-color: #39FF14; font-weight: 700; }
    </style>
    """, unsafe_allow_html=True)

# 3. SECURE LOGIN
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="pro-card">', unsafe_allow_html=True)
        st.subheader("Pro Access / உள்நுழைக")
        u_id = st.text_input("Username")
        u_pass = st.text_input("Password", type="password")
        if st.button("Enter Hub 🚀", use_container_width=True):
            if u_id and u_pass: st.session_state['is_logged_in'] = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. HEADER
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# 5. SEARCH
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🔮 {get_text('Forecast', 'முன்னறிவிப்பு')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. DATA ENGINE
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1y")

    # --- TAB 1: ANALYSIS & ABOUT US (About Us மீண்டும் சேர்க்கப்பட்டுள்ளது) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        f_list = [(get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"), (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')), (get_text("Sector", "துறை"), info.get('sector', 'N/A'))]
        for i, (l, v) in enumerate(f_list):
            (c1 if i % 2 == 0 else c2).markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)

        # இதோ நீங்கள் கேட்ட "About Us" பகுதி
        with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
            raw_about = info.get('longBusinessSummary', 'No description.')
            st.write(translate_text(raw_about, st.session_state['language']))

    # --- TAB 2: FORECAST (BUY/SELL/HOLD) (Font sizes refined) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Pro Forecast', 'நிபுணர் முன்னறிவிப்பு')}")
        
        # Simple Prediction Logic
        pe, roe = info.get('trailingPE', 100), info.get('returnOnEquity', 0)
        score = 0
        if pe < 28: score += 50
        if roe > 0.12: score += 50
        
        if score >= 80: advice, color = get_text("STRONG BUY", "வாங்கலாம்"), "#39FF14"
        elif score >= 50: advice, color = get_text("HOLD", "தொடரலாம்"), "#00D1FF"
        else: advice, color = get_text("SELL / AVOID", "விற்கலாம் / தவிர்க்கவும்"), "#FF3131"
            
        st.markdown(f"""
            <div style="padding: 20px; border-radius: 12px; background: {color}05; border: 1px solid {color}; text-align: center;">
                <p class="advice-text" style="color: {color};">{advice}</p>
                <p class="score-text">{get_text("Pro Score", "புரோ ஸ்கோர்")}: {score}/100</p>
            </div>
        """, unsafe_allow_html=True)

    # --- TAB 3: SHAREHOLDING ---
    with tabs[2]:
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, 100-(promo+inst)], hole=0.6, marker=dict(colors=['#58a6ff', '#f85149', '#ffd700']))])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- TAB 4: FINANCIALS ---
    with tabs[3]:
        p = st.selectbox("Period", ["Annual", "Quarterly"])
        f_data = stock.financials if p == "Annual" else stock.quarterly_financials
        if not f_data.empty: st.dataframe(f_data.head(10), use_container_width=True)

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        if st.button(f"➕ Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            c1, c2 = st.columns([6, 1])
            c1.info(f"📌 {i}")
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

except Exception:
    st.error("சரியான பங்கு குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
