import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. பக்க அமைப்பு (Configuration)
st.set_page_config(
    page_title="Tamil Invest Hub Pro",
    page_icon="👑",
    layout="wide"
)

# 2. ராயல் தீம் (CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050a0f; color: #e0e0e0; }
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 32px !important; font-weight: 800; text-align: center; margin-bottom: 20px;
    }
    .stMetric { background: #111418; padding: 15px; border-radius: 10px; border-bottom: 2px solid #ffd700; }
    .news-feed-card { background: #111418; border-radius: 12px; padding: 15px; margin-bottom: 12px; border-left: 5px solid #ffd700; }
    .stock-badge { background: #ffd700; color: #000; padding: 3px 10px; border-radius: 5px; font-size: 11px; font-weight: bold; display: inline-block; }
    .footer { font-size: 12px; color: #555; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 3. செஷன் ஸ்டேட்
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS']

st.markdown('<p class="royal-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
tab1, tab2 = st.tabs(["📊 Market Explorer", "⭐ Watchlist & News"])

# --- TAB 1: MARKET EXPLORER (Updated with PE, PB, PEG) ---
with tab1:
    search_ticker = st.text_input("Enter Symbol (e.g. SBIN.NS)", value="RELIANCE.NS").upper()
    
    try:
        stock = yf.Ticker(search_ticker)
        info = stock.info
        
        st.subheader(f"{info.get('longName', search_ticker)}")
        
        # முக்கிய விலைத் தகவல்கள்
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        
        # --- புதிய மெட்ரிக்குகள் (PE, PB, PEG) ---
        # .get() மூலம் பெறுவதால் தகவல் இல்லையென்றால் "N/A" எனக் காட்டும்
        pe_ratio = info.get('trailingPE', "N/A")
        pb_ratio = info.get('priceToBook', "N/A")
        peg_ratio = info.get('pegRatio', "N/A")
        
        # UI-ல் மெட்ரிக்குகளைக் காண்பித்தல்
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Current Price", f"₹{price:,.2f}")
        
        # PE Ratio-வை வடிவமைத்தல்
        pe_val = f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A"
        m2.metric("P/E Ratio", pe_val)
        
        # PB Ratio-வை வடிவமைத்தல்
        pb_val = f"{pb_ratio:.2f}" if isinstance(pb_ratio, (int, float)) else "N/A"
        m3.metric("P/B Ratio", pb_val)
        
        # PEG Ratio-வை வடிவமைத்தல்
        peg_val = f"{peg_ratio:.2f}" if isinstance(peg_ratio, (int, float)) else "N/A"
        m4.metric("PEG Ratio", peg_val)
        
        # கூடுதல் பட்டன்
        if st.button(f"➕ Add {search_ticker} to Watchlist"):
            if search_ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(search_ticker)
                st.success("Added!")
                st.rerun()

    except Exception as e:
        st.info("Stock information loading...")

# --- TAB 2: WATCHLIST & NEWS FEED ---
with tab2:
    if not st.session_state.watchlist:
        st.info("Watchlist is empty.")
    else:
        # வாட்ச் லிஸ்ட் விலைகள்
        w_cols = st.columns(len(st.session_state.watchlist))
        for idx, symbol in enumerate(st.session_state.watchlist):
            try:
                p = yf.Ticker(symbol).fast_info['last_price']
                w_cols[idx].metric(symbol, f"₹{p:,.1f}")
            except: continue
            
        st.divider()
        
        # நியூஸ் பீட் (முன்பு சரிசெய்யப்பட்ட அதே கோட்)
        all_news = []
        with st.spinner("செய்திகளைத் திரட்டுகிறேன்..."):
            for s in st.session_state.watchlist:
                try:
                    raw = yf.Ticker(s).news[:3]
                    for n in raw:
                        n['stock_ref'] = s
                        all_news.append(n)
                except: continue
        
        if all_news:
            all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
            for item in all_news[:10]:
                st.markdown(f"""
                    <div class="news-feed-card">
                        <div class="stock-badge">{item.get('stock_ref','Stock')}</div><br>
                        <a href="{item.get('link','#')}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">
                            {item.get('title','No Title')}
                        </a><br>
                        <span style="color:#666; font-size:10px;">{item.get('publisher','N/A')}</span>
                    </div>
                """, unsafe_allow_html=True)
        
        if st.button("Clear Watchlist"):
            st.session_state.watchlist = []
            st.rerun()

st.markdown('<div class="footer">© 2026 Tamil Invest Hub</div>', unsafe_allow_html=True)
