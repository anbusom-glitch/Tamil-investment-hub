import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import time
import base64

# 1. பக்க அமைப்பு
st.set_page_config(
    page_title="TS INVEST PRO",
    page_icon="📈",
    layout="wide"
)

# லோகோவை Base64-ஆக மாற்றி HTML-ல் பயன்படுத்தும் வசதி
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# 2. பிரீமியம் மொபைல் சிஎஸ்எஸ் (Small Fonts & Compact UI)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* குளோபல் பாண்ட் - சிறிய மற்றும் தெளிவானது */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #0d1117; 
        color: #c9d1d9;
        font-size: 12.5px !important;
        line-height: 1.3;
    }

    /* ஸ்பிளாஷ் ஸ்கிரீன் ஸ்டைல் */
    .splash-box {
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        height: 80vh; animation: fadeIn 1.5s;
    }
    @keyframes fadeIn { from {opacity: 0;} to {opacity: 1;} }

    /* ஹெட்ர் லோகோ */
    .header-container { display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 15px; }
    .header-logo { width: 40px; border-radius: 8px; }
    .header-text {
        background: linear-gradient(90deg, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 20px !important; font-weight: 800; letter-spacing: 1px;
    }

    /* மெட்ரிக்ஸ் - காம்பாக்ட் மொபைல் வியூ */
    [data-testid="stMetric"] {
        background: #161b22; border: 1px solid #30363d; border-radius: 8px;
        padding: 5px 8px !important;
    }
    [data-testid="stMetricLabel"] { font-size: 10px !important; color: #8b949e !important; }
    [data-testid="stMetricValue"] { font-size: 14px !important; color: #ffd700 !important; }

    /* ப்ரோக்கர் கார்டுகள் */
    .broker-card {
        background: #1c2128; border: 1px solid #30363d; border-radius: 10px;
        padding: 12px; text-align: center; margin-bottom: 10px;
    }
    .status-dot { color: #2ea043; font-size: 10px; font-weight: bold; }

    /* பட்டன் ஸ்டைல் */
    .stButton>button { width: 100%; border-radius: 6px; height: 35px; font-size: 12px; font-weight: 600; }
    
    /* நியூஸ் கார்டு */
    .news-card {
        background: #161b22; border-radius: 8px; padding: 10px; 
        margin-bottom: 8px; border-left: 3px solid #ffd700;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SPLASH SCREEN (LOGO DISPLAY) ---
if 'startup' not in st.session_state:
    placeholder = st.empty()
    try:
        # லோகோ படம் இருந்தால் அதைக் காட்டும்
        logo_base64 = get_base64("logo.png")
        placeholder.markdown(f"""
            <div class="splash-box">
                <img src="data:image/png;base64,{logo_base64}" style="width:120px; margin-bottom:20px; border-radius:20px;">
                <h2 style="color:#ffd700; letter-spacing:2px;">TS INVEST</h2>
                <p style="color:#58a6ff; font-size:12px;">Loading Your Financial Galaxy...</p>
            </div>
        """, unsafe_allow_html=True)
    except:
        # படம் இல்லையென்றால் டெக்ஸ்ட் காட்டும்
        placeholder.markdown("<div class='splash-box'><h1 style='color:#ffd700;'>TS INVEST</h1></div>", unsafe_allow_html=True)
    
    time.sleep(2.5)
    st.session_state.startup = True
    placeholder.empty()

# --- 4. HEADER SECTION ---
try:
    l_base = get_base64("logo.png")
    st.markdown(f"""
        <div class="header-container">
            <img src="data:image/png;base64,{l_base}" class="header-logo">
            <span class="header-text">TS INVEST PRO</span>
        </div>
    """, unsafe_allow_html=True)
except:
    st.markdown('<p class="header-text" style="text-align:center;">TS INVEST PRO</p>', unsafe_allow_html=True)

# --- 5. APP TABS ---
tab1, tab2, tab3 = st.tabs(["🔍 Analysis", "💼 Broker Connect", "🗞️ Market Feed"])

with tab1:
    # தேடல் பகுதி
    search_ticker = st.text_input("", value="RELIANCE.NS", placeholder="Enter Ticker...").upper()
    
    try:
        stock = yf.Ticker(search_ticker)
        info = stock.info
        
        # முக்கிய விவரங்கள் (Compact)
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        st.markdown(f"**{info.get('longName', search_ticker)}**")
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("LTP", f"₹{price:,.0f}")
        c2.metric("P/E", f"{info.get('trailingPE', 'N/A')}")
        c3.metric("P/B", f"{info.get('priceToBook', 'N/A')}")
        c4.metric("PEG", f"{info.get('pegRatio', 'N/A')}")

        # விலை வரைபடம்
        hist = stock.history(period="6mo")
        fig = go.Figure(data=[go.Scatter(x=hist.index, y=hist['Close'], line=dict(color='#ffd700', width=1.5))])
        fig.update_layout(height=220, margin=dict(l=0, r=0, t=5, b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                         xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='#1e2329', side="right"))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
        
        # சுருக்கமான விவரம்
        with st.expander("About Company"):
            st.write(info.get('longBusinessSummary', 'No info available.'))
            
    except:
        st.info("Searching for Stock Data...")

with tab2:
    st.markdown("<p style='font-weight:bold; color:#ffd700;'>🔌 Connect Your Broker</p>", unsafe_allow_html=True)
    st.write("பாதுகாப்பாக உங்கள் போர்ட்போலியோவை இணைத்து லாப நஷ்டத்தைப் பாருங்கள்.")
    
    b1, b2 = st.columns(2)
    with b1:
        st.markdown('<div class="broker-card"><p>Zerodha</p><p class="status-online">● Ready</p></div>', unsafe_allow_html=True)
        if st.button("Link Kite"): st.toast("Connecting to Zerodha...")
    with b2:
        st.markdown('<div class="broker-card"><p>Angel One</p><p class="status-online">● Ready</p></div>', unsafe_allow_html=True)
        if st.button("Link Angel"): st.toast("Connecting to Angel One...")

    st.divider()
    
    # Portfolio Mock-up (லாப நஷ்ட கணக்கு)
    st.markdown("<p style='font-size:11px; font-weight:bold;'>LIVE PORTFOLIO SUMMARY</p>", unsafe_allow_html=True)
    p_col1, p_col2 = st.columns(2)
    p_col1.metric("Total Investment", "₹4,50,000")
    p_col2.metric("Current Value", "₹5,12,000", "+₹62,000")
    
    st.dataframe(pd.DataFrame({
        'Symbol': ['RELIANCE', 'TCS', 'SBIN'],
        'Qty': [20, 10, 100],
        'P&L': ['+₹4,500', '-₹1,200', '+₹12,000']
    }), use_container_width=True, hide_index=True)

with tab3:
    st.markdown("<p style='font-weight:bold;'>🗞️ Live News Feed</p>", unsafe_allow_html=True)
    try:
        news = yf.Ticker(search_ticker).news[:6]
        for n in news:
            st.markdown(f"""
                <div class="news-card">
                    <a href="{n['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:600; font-size:12px;">{n['title'][:70]}...</a><br>
                    <span style="color:#666; font-size:10px;">{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%d %b')}</span>
                </div>
            """, unsafe_allow_html=True)
    except:
        st.write("News currently unavailable.")

# 6. அடிக்குறிப்பு
st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:30px;">© 2026 TS INVEST | Intelligent Trading Suite</div>', unsafe_allow_html=True)
