import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. எலைட் தீம் மற்றும் பக்க அமைப்பு
st.set_page_config(
    page_title="Tamil Invest Hub Pro",
    page_icon="🗞️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. ராயல் டிசைன் (News Feed UI CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050a0f; color: #e0e0e0; }
    
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 10px;
    }
    
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 40px; border-radius: 20px; font-size: 12px; background-color: #161b22; color: #888; border: 1px solid #30363d; padding: 0 20px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(45deg, #b8860b, #ffd700) !important; color: #000 !important; font-weight: bold; }
    
    .news-feed-card {
        background: #111418; border-radius: 10px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700;
    }
    .stock-badge {
        background: #ffd700; color: #000; padding: 2px 8px; border-radius: 5px; font-size: 10px; font-weight: bold; margin-bottom: 5px; display: inline-block;
    }
    .footer { font-size: 10px; color: #333; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 3. செஷன் ஸ்டேட் (Data Storage)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS']

# 4. மெயின் டைட்டில்
st.markdown('<p class="royal-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 Market Explorer", "⭐ Watchlist & News Feed"])

# --- TAB 1: MARKET EXPLORER ---
with tab1:
    search_ticker = st.text_input("Enter Symbol (e.g. SBIN.NS)", value="RELIANCE.NS").upper()
    try:
        s_stock = yf.Ticker(search_ticker)
        s_info = s_stock.info
        st.subheader(f"{s_info.get('longName', search_ticker)}")
        
        c1, c2 = st.columns(2)
        c1.metric("Current Price", f"₹{s_info.get('currentPrice', 0):,.2f}")
        
        if st.button(f"➕ Add {search_ticker} to Watchlist"):
            if search_ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(search_ticker)
                st.success("Added to Watchlist!")
    except: st.info("Search a stock and add to your personalized feed.")

# --- TAB 2: WATCHLIST & NEWS FEED ---
with tab2:
    if not st.session_state.watchlist:
        st.info("Your Watchlist is empty. Add stocks from the Market Explorer tab.")
    else:
        st.markdown("### ⭐ Your Watchlist")
        
        # Display Watchlist Cards
        cols = st.columns(len(st.session_state.watchlist))
        for idx, w_symbol in enumerate(st.session_state.watchlist):
            try:
                w_data = yf.Ticker(w_symbol).fast_info['last_price']
                cols[idx].metric(w_symbol, f"₹{w_data:,.0f}")
            except: continue
            
        st.divider()
        
        # --- NEW FEATURE: DYNAMIC NEWS FEED ---
        st.markdown("### 🗞️ Watchlist News Feed")
        st.caption("ஆய்வு: உங்கள் வாட்ச் லிஸ்டில் உள்ள பங்குகளின் சமீபத்திய செய்திகள் மட்டும் இங்கே.")
        
        all_news = []
        with st.spinner("Fetching your personalized feed..."):
            for w_symbol in st.session_state.watchlist:
                try:
                    raw_news = yf.Ticker(w_symbol).news[:3] # ஒரு பங்கிற்கு 3 செய்திகள் வீதம்
                    for n in raw_news:
                        n['stock_ref'] = w_symbol # எந்தப் பங்கு என்பதை அடையாளம் காண
                        all_news.append(n)
                except: continue
        
        if all_news:
            # செய்திகளை நேரப்படி வரிசைப்படுத்துதல்
            all_news.sort(key=lambda x: x['providerPublishTime'], reverse=True)
            
            for news_item in all_news[:15]: # மொத்தம் 15 முக்கியச் செய்திகள்
                pub_time = datetime.fromtimestamp(news_item['providerPublishTime']).strftime('%Y-%m-%d %H:%M')
                st.markdown(f"""
                    <div class="news-feed-card">
                        <div class="stock-badge">{news_item['stock_ref']}</div><br>
                        <a href="{news_item['link']}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold; font-size:14px;">
                            {news_item['title']}
                        </a><br>
                        <span style="color:#666; font-size:10px;">{news_item['publisher']} • {pub_time}</span>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("No recent news found for your watchlist stocks.")
            
        if st.button("Clear All from Watchlist"):
            st.session_state.watchlist = []
            st.rerun()

st.markdown('<div class="footer">© 2026 Tamil Invest Hub - Elite Analytics<br>Data Driven. Results Oriented.</div>', unsafe_allow_html=True)
