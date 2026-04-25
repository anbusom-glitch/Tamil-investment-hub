import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உலகத்தரம் வாய்ந்த UI (Sleek High-End Design)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; text-transform: lowercase; letter-spacing: 2px; opacity: 0.6; }
    
    /* Metrics High Look */
    .metric-card {
        background: #161b22;
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .m-label { color: #8b949e !important; font-size: 11px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff !important; font-size: 17px; font-weight: 800; }
    </style>
    """, unsafe_allow_html=True)

# 3. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 5. டேட்டா லோடிங்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    # --- TAB 1: ANALYSIS ---
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        metrics = [
            ("LTP (Price)", f"₹{ltp:,.2f}"),
            ("52W High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            ("52W Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}"),
            ("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
        ]
        for label, value in metrics:
            st.markdown(f'<div class="metric-card"><span class="m-label">{label}</span><span class="m-value">{value}</span></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: SHAREHOLDING (FII & DII பிரிக்கப்பட்டுள்ளது) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        
        # தரவுகளைப் பெற்று சதவீதமாக மாற்றுதல்
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst_total = (info.get('heldPercentInstitutions') or 0) * 100
        
        # FII/DII பிரிக்கப்படாத போது தோராயமான மதிப்பீடு (Logic for Detailed View)
        fii = info.get('foreignInstitutionalHolders', inst_total * 0.6) # வழக்கமாக 60% FII இருக்கும்
        if fii > inst_total: fii = inst_total * 0.6
        dii = inst_total - fii
        
        public = max(0, 100 - (promo + inst_total))

        labels = ['Promoters', 'FII (Foreign)', 'DII (Domestic)', 'Public']
        values = [promo, fii, dii, public]
        colors = ['#58a6ff', '#f85149', '#39FF14', '#ffd700']

        fig_pie = go.Figure(data=[go.Pie(
            labels=labels, 
            values=values, 
            hole=0.5,
            marker=dict(colors=colors)
        )])
        
        fig_pie.update_layout(height=450, template="plotly_dark", showlegend=True)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # விரிவான புள்ளிவிவரங்கள்
        st.markdown("#### Stats:")
        c1, c2 = st.columns(2)
        c1.write(f"🔹 Promoters: **{promo:.2f}%**")
        c1.write(f"🔹 FII (வெளிநாட்டு முதலீடு): **{fii:.2f}%**")
        c2.write(f"🔹 DII (உள்நாட்டு முதலீடு): **{dii:.2f}%**")
        c2.write(f"🔹 Public: **{public:.2f}%**")

    # --- மற்ற டேப்கள் (ரேட்டிங், வாட்ச்லிஸ்ட் போன்றவை) ---
    with tabs[4]:
        st.markdown(f"### {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        for item in st.session_state['watchlist']:
            st.write(f"📌 {item}")

else:
    st.info("Loading Stock Data...")

st.markdown("<p style='text-align:center;color:#444;font-size:11px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
