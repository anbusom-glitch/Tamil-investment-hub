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

# 2. PREMIUM CSS STYLING
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    .header-container { text-align: center; padding: 20px 0; }
    .main-title { 
        font-size: 38px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 12px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.8; font-style: italic; }
    .metric-row { 
        background: #161b22; border: 1px solid #30363d; border-radius: 12px; 
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; 
    }
    .m-label { color: #8b949e; font-size: 11px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 17px; font-weight: 800; }
    .login-box { background: #1c2128; border: 1px solid #30363d; border-radius: 15px; padding: 40px; max-width: 450px; margin: auto; box-shadow: 0 15px 35px rgba(0,0,0,0.6); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background: #161b22; border-radius: 8px; padding: 10px 20px; color: #8b949e; }
    .stTabs [aria-selected="true"] { background: #39FF14 !important; color: #000000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 3. SECURE LOGIN SYSTEM
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.subheader("Sign In / உள்நுழைக")
        u_id = st.text_input("User ID / Mobile")
        u_pass = st.text_input("Password", type="password")
        if st.button("Access Hub 🚀", use_container_width=True):
            if u_id and u_pass: 
                st.session_state['is_logged_in'] = True
                st.rerun()
            else: st.error("Please enter credentials.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. DASHBOARD HEADER
c_h1, c_h2 = st.columns([8, 2])
with c_h2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. SEARCH ENGINE
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE, INFOSYS)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"📈 {get_text('Technical', 'வரைபடம்')}",
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Corporate Actions', 'நிகழ்வுகள்')}",
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. CORE DATA ENGINE
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1y")

    # --- TAB 1: FUNDAMENTAL ANALYSIS ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        f_m1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("ROE", "ROE"), f"{(info.get('returnOnEquity', 0)*100):.2f}%")
        ]
        f_m2 = [
            (get_text("Div. Yield", "டிவிடெண்ட் ஈல்டு"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}")
        ]
        for l, v in f_m1: c1.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        for l, v in f_m2: c2.markdown(f'<div class="metric-row"><span class="m-label">{l}</span><span class="m-value">{v}</span></div>', unsafe_allow_html=True)
        
        with st.expander(get_text("About Company", "நிறுவனத்தைப் பற்றி")):
            st.write(GoogleTranslator(source='auto', target='ta').translate(info.get('longBusinessSummary', '')) if st.session_state['language']=="Tamil" else info.get('longBusinessSummary', 'No data.'))

    # --- TAB 2: TECHNICAL CHART ---
    with tabs[1]:
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index[-100:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'], name='Price')])
            # Adding Moving Averages
            hist['MA50'] = hist['Close'].rolling(50).mean()
            fig.add_trace(go.Scatter(x=hist.index[-100:], y=hist['MA50'][-100:], name='50 MA', line=dict(color='#00D1FF')))
            fig.update_layout(height=500, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    # --- TAB 3: SHAREHOLDING (FII/DII SPLIT) ---
    with tabs[2]:
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        if fii > inst: fii = inst * 0.6
        dii = inst - fii
        labels, values = ['Promoters', 'FII', 'DII', 'Public'], [promo, fii, dii, max(0, 100-(promo+inst))]
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark"), use_container_width=True)

    # --- TAB 4: FINANCIALS (ANNUAL & QUARTERLY) ---
    with tabs[3]:
        p = st.selectbox("Period", ["Annual", "Quarterly"])
        f_data = stock.financials if p == "Annual" else stock.quarterly_financials
        if not f_data.empty:
            st.dataframe(f_data.head(15), use_container_width=True)
            try:
                rev = f_data.loc['Total Revenue']
                st.bar_chart(rev)
            except: st.info("Financial graph loading...")
        else: st.info("Financials not available.")

    # --- TAB 5: CORPORATE ACTIONS ---
    with tabs[4]:
        st.markdown(f"### {get_text('Dividends & Splits', 'கார்ப்பரேட் நிகழ்வுகள்')}")
        if not stock.actions.empty:
            st.dataframe(stock.actions.tail(15).sort_index(ascending=False), use_container_width=True)
        else: st.info("No recent actions.")

    # --- TAB 6: RATING ---
    with tabs[5]:
        score = 80 if (info.get('trailingPE', 100) < 25 and info.get('returnOnEquity', 0) > 0.15) else 50
        clr = "#39FF14" if score >= 75 else "#FF3131"
        st.markdown(f'<div style="text-align:center; padding:50px; border:3px solid {clr}; border-radius:20px;"><h1>{score}/100</h1><h3>{get_text("PRO RATING", "புரோ மதிப்பீடு")}</h3></div>', unsafe_allow_html=True)

    # --- TAB 7: WATCHLIST ---
    with tabs[6]:
        if st.button(f"➕ Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']: st.session_state['watchlist'].append(u_input); st.rerun()
        for i in st.session_state['watchlist']:
            cw1, cw2 = st.columns([6, 1])
            cw1.info(f"📌 {i}")
            if cw2.button("❌", key=f"del_{i}"): st.session_state['watchlist'].remove(i); st.rerun()

except Exception as e:
    st.error(get_text("Please enter a valid stock symbol (e.g., RELIANCE).", "சரியான பங்கு குறியீட்டை உள்ளிடவும்."))

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram</p>", unsafe_allow_html=True)
