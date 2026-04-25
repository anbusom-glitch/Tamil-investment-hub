import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# செஷன் ஸ்டேட் - தகவல்களைத் தக்கவைக்க
if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"
if 'broker_connected' not in st.session_state: st.session_state['broker_connected'] = False

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உயர் ரக UI ஸ்டைலிங்
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .login-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 15px;
        padding: 30px; max-width: 450px; margin: auto; box-shadow: 0 10px 25px rgba(0,0,0,0.5);
    }
    .metric-box { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .m-label { color: #8b949e; font-size: 11px; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. லாகின் பக்கம் (Login Screen)
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.subheader("Login to Your Account")
        
        login_option = st.radio("Choose Login Method", ["Email ID", "Mobile Number"], horizontal=True)
        
        if login_option == "Email ID":
            user_mail = st.text_input("Enter Email ID", placeholder="example@mail.com")
        else:
            user_mob = st.text_input("Enter Mobile Number", placeholder="+91 XXXXX XXXXX")
            
        password = st.text_input("Password", type="password")
        
        if st.button("Sign In 🚀", use_container_width=True):
            if (login_option == "Email ID" and user_mail) or (login_option == "Mobile Number" and user_mob):
                st.session_state['is_logged_in'] = True
                st.rerun()
            else:
                st.warning("Please enter your credentials.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop() # லாகின் ஆகும் வரை மற்ற பகுதிகளைக் காட்டாது

# 4. பிரதான பக்கம் (Main App) - லாகின் ஆன பிறகு
col_t1, col_t2 = st.columns([8, 2])
with col_t2:
    if st.button("Logout 🚪"):
        st.session_state['is_logged_in'] = False
        st.rerun()

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச் மற்றும் டேப்கள்
u_input = st.text_input("Search Symbol (eg: RELIANCE)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"💼 {get_text('Portfolio', 'போர்ட்ஃபோலியோ')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. டேட்டா லோடிங் & லாஜிக்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")

    # Analysis
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
        st.markdown(f'<div class="metric-box"><span class="m-label">LTP</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    # Portfolio & Broker Connect
    with tabs[1]:
        if not st.session_state['broker_connected']:
            st.markdown("### Connect Your Broker")
            cb1, cb2 = st.columns(2)
            if cb1.button("Zerodha", use_container_width=True): st.session_state['broker_connected'] = True; st.rerun()
            if cb2.button("Angel One", use_container_width=True): st.session_state['broker_connected'] = True; st.rerun()
        else:
            st.success("Broker Connected! ✅")
            st.markdown(f'<div class="metric-box"><span class="m-label">Invested</span><span class="m-value">₹50,000</span></div>', unsafe_allow_html=True)

    # Shareholding
    with tabs[2]:
        promo = (info.get('heldPercentInsiders') or 0) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Public'], values=[promo, 100-promo], hole=0.5)])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark"), use_container_width=True)

    # Rating
    with tabs[3]:
        score = 80 if info.get('trailingPE', 100) < 30 else 45
        st.markdown(f'<h1 style="text-align:center; color:#39FF14;">{score}/100</h1>', unsafe_allow_html=True)

    # Watchlist
    with tabs[4]:
        if st.button(f"➕ Add {u_input}"):
            st.session_state['watchlist'].append(u_input)
            st.rerun()
        for item in st.session_state['watchlist']:
            st.info(f"📌 {item}")

except:
    st.error("Please enter a valid stock symbol.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
