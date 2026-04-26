import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# Session State Initialization
if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. LUXURY DARK UI STYLING (Rich Dark Theme)
st.markdown("""
    <style>
    /* Global Background */
    html, body, [class*="css"] { 
        font-size: 14px !important; 
        background-color: #050505 !important; 
        color: #e0e0e0; 
    }
    
    /* Luxury Header */
    .header-container { text-align: center; padding: 30px 0; }
    .main-title { 
        font-size: 36px !important; font-weight: 900; letter-spacing: -1.5px;
        background: linear-gradient(90deg, #1db954, #191414, #1db954);
        background: linear-gradient(90deg, #39FF14, #00D1FF, #8B0000);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 11px !important; color: #666; letter-spacing: 3px; text-transform: uppercase; margin-top: 5px; }

    /* Login & Signup Box - Dark Contrast */
    .auth-card { 
        background: #0d1117; 
        border: 1px solid #21262d; 
        border-radius: 16px; 
        padding: 40px; 
        max-width: 450px; 
        margin: auto; 
        box-shadow: 0 20px 50px rgba(0,0,0,0.8); 
    }

    /* Dark Metric Row */
    .metric-row { 
        background: #0d1117; 
        border: 1px solid #21262d; 
        border-radius: 12px; 
        padding: 16px; 
        margin-bottom: 12px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
    }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #39FF14; font-size: 16px; font-weight: 800; }
    
    /* Custom Button Dark Green */
    .stButton>button {
        background-color: #013220 !important; 
        color: #39FF14 !important;
        border: 1px solid #39FF14 !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. SPLIT LOGIN & SIGN UP SYSTEM
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">Premium Access Only</p></div>', unsafe_allow_html=True)
    
    # லாகின் மற்றும் சைன்-அப் தனித்தனி பிரிவுகள்
    tab_login, tab_signup = st.tabs(["🔐 Login (உள்நுழைக)", "✍️ Sign Up (புதிய பதிவு)"])
    
    with tab_login:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.subheader("Login / உள்நுழைக")
        l_id = st.text_input("User ID / Mobile", key="l_user")
        l_pass = st.text_input("Password", type="password", key="l_pass")
        if st.button("Enter Pro Hub 🚀", use_container_width=True):
            if l_id and l_pass:
                st.session_state['is_logged_in'] = True
                st.rerun()
            else: st.warning("ID மற்றும் Password உள்ளிடவும்.")
        st.markdown('</div>', unsafe_allow_html=True)

    with tab_signup:
        st.markdown('<div class="auth-card">', unsafe_allow_html=True)
        st.subheader("Sign Up / பதிவு செய்தல்")
        s_name = st.text_input("Full Name / பெயர்")
        s_id = st.text_input("Mobile Number / மொபைல் எண்")
        s_pass = st.text_input("Create Password", type="password")
        if st.button("Create Account ✅", use_container_width=True):
            if s_name and s_id and s_pass:
                st.success("கணக்கு உருவாக்கப்பட்டது! இப்போது லாகின் செய்யவும்.")
            else: st.warning("அனைத்து விவரங்களையும் நிரப்பவும்.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. MAIN APP CONTENT (After Login)
col_h1, col_h2 = st.columns([8, 2])
with col_h2:
    st.session_state['language'] = st.radio("L", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p><p class="sub-title">created by somasundaram</p></div>""", unsafe_allow_html=True)

# --- 5. DATA FETCHING & APP LOGIC ---
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

try:
    stock = yf.Ticker(ticker)
    info = stock.info

    with tabs[0]: # Analysis
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="metric-row"><span class="m-label">Price</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="metric-row"><span class="m-label">Cap</span><span class="m-value">₹{info.get("marketCap", 0)/10000000:,.0f} Cr</span></div>', unsafe_allow_html=True)
        with st.expander("About Company"):
            st.write(info.get('longBusinessSummary', 'No data.'))

    with tabs[1]: # Shareholding
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        # Dark Deep Colors
        dark_colors = ['#002244', '#4b0000', '#004d00', '#222222']
        fig = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, inst*0.6, inst*0.4, 100-(promo+inst)], hole=0.5, marker=dict(colors=dark_colors))])
        st.plotly_chart(fig.update_layout(template="plotly_dark", height=400), use_container_width=True)

    with tabs[2]: # Financials
        f_m = [(get_text("Net Profit", "நிகர லாபம்"), f"₹{info.get('netIncomeToCommon', 0)/10000000:,.2f} Cr"), (get_text("Debt", "கடன்"), f"₹{info.get('totalDebt', 0)/10000000:,.2f} Cr")]
        for lbl, val in f_m: st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

except:
    st.error("Error loading data.")

st.markdown("<p style='text-align:center; color:#333; font-size:10px; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
