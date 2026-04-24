import streamlit as st
import yfinance as yf
import pandas as pd
from datetime import datetime

# 1. பக்க அமைப்பு மற்றும் லோகோ (Elite Configuration)
st.set_page_config(
    page_title="Tamil Invest Hub Pro",
    page_icon="👑",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. பிரீமியம் ராயல் தீம் (Custom CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* மெயின் பேக்ரவுண்ட் */
    html, body, [class*="css"] { 
        font-family: 'Inter', sans-serif; 
        background-color: #050a0f; 
        color: #e0e0e0; 
    }
    
    /* ராயல் கோல்ட் தலைப்பு */
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        font-size: 32px !important; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 20px;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    /* டேப்ஸ் (Tabs) ஸ்டைல் */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { 
        height: 45px; border-radius: 25px; font-size: 14px; 
        background-color: #161b22; color: #888; 
        border: 1px solid #30363d; padding: 0 30px; 
    }
    .stTabs [aria-selected="true"] { 
        background: linear-gradient(45deg, #b8860b, #ffd700) !important; 
        color: #000 !important; font-weight: bold; 
        border: none;
    }
    
    /* செய்தி கார்டுகள் (News Cards) */
    .news-feed-card {
        background: #111418; 
        border-radius: 12px; 
        padding: 15px; 
        margin-bottom: 12px; 
        border-left: 5px solid #ffd700;
        transition: 0.3s;
    }
    .news-feed-card:hover { background: #1c2128; }
    
    .stock-badge {
        background: #ffd700; color: #000; padding: 3px 10px; 
        border-radius: 5px; font-size: 11px; font-weight: bold; 
        display: inline-block; margin-bottom: 8px;
    }
    
    .footer { 
        font-size: 12px; color: #555; text-align: center; 
        margin-top: 50px; padding: 20px; border-top: 1px solid #161b22;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. செஷன் ஸ்டேட் (டேட்டா மேலாண்மை)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ['RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS']

# 4. ஆப் தலைப்பு
st.markdown('<p class="royal-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📊 சந்தை ஆய்வு (Market)", "⭐ வாட்ச் லிஸ்ட் (Watchlist)"])

# --- TAB 1: MARKET EXPLORER ---
with tab1:
    search_ticker = st.text_input("பங்கின் குறியீட்டை உள்ளிடவும் (e.g. SBIN.NS)", value="RELIANCE.NS").upper()
    
    try:
        stock = yf.Ticker(search_ticker)
        info = stock.info
        
        # தகவல்கள் விடுபட்டிருந்தால் மாற்று வழியில் பெறுதல்
        name = info.get('longName', search_ticker)
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        currency = info.get('currency', 'INR')
        
        st.subheader(f"{name}")
        
        c1, c2, c3 = st.columns(3)
        c1.metric("தற்போதைய விலை", f"₹{price:,.2f}")
        c2.metric("சந்தை மதிப்பு", f"{info.get('marketCap', 0):,}")
        c3.metric("டிவிடெண்ட்", f"{info.get('dividendYield', 0)*100:.2f}%" if info.get('dividendYield') else "0.00%")
        
        if st.button(f"➕ {search_ticker}-ஐ வாட்ச் லிஸ்டில் சேர்க்க"):
            if search_ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(search_ticker)
                st.success(f"{search_ticker} வெற்றிகரமாக சேர்க்கப்பட்டது!")
                st.rerun()
            else:
                st.warning("இந்தப் பங்கு ஏற்கனவே பட்டியலில் உள்ளது.")
    except Exception:
        st.error("சரியான குறியீட்டை உள்ளிடவும். (உதாரணம்: RELIANCE.NS)")

# --- TAB 2: WATCHLIST & NEWS FEED ---
with tab2:
    if not st.session_state.watchlist:
        st.info("உங்கள் வாட்ச் லிஸ்ட் காலியாக உள்ளது.")
    else:
        st.markdown("### ⭐ உங்கள் பங்குகள்")
        
        # வாட்ச் லிஸ்ட் விலைகள் (Metrics)
        cols = st.columns(min(len(st.session_state.watchlist), 4))
        for i, symbol in enumerate(st.session_state.watchlist):
            try:
                t = yf.Ticker(symbol)
                # வேகமான தரவுகளுக்கு fast_info, இல்லையெனில் info
                try:
                    p = t.fast_info['last_price']
                except:
                    p = t.info.get('regularMarketPrice', 0)
                
                cols[i % 4].metric(symbol, f"₹{p:,.1f}")
            except:
                continue
        
        st.divider()
        
        # --- செய்திகள் பகுதி (Error-Free News Feed) ---
        st.markdown("### 🗞️ நேரலைச் செய்திகள் (Watchlist News)")
        
        all_news = []
        with st.spinner("செய்திகளைத் திரட்டுகிறேன்..."):
            for symbol in st.session_state.watchlist:
                try:
                    news_data = yf.Ticker(symbol).news
                    if news_data:
                        for n in news_data[:3]: # ஒரு பங்கிற்கு 3 செய்திகள்
                            n['stock_ref'] = symbol
                            all_news.append(n)
                except:
                    continue
        
        if all_news:
            # பிழை வராமல் இருக்க .get() மூலம் வரிசைப்படுத்துதல்
            all_news.sort(key=lambda x: x.get('providerPublishTime', 0), reverse=True)
            
            for item in all_news[:12]: # டாப் 12 செய்திகள்
                title = item.get('title', 'No Title Available')
                link = item.get('link', '#')
                source = item.get('publisher', 'Financial News')
                ts = item.get('providerPublishTime', 0)
                
                # நேரத்தை மாற்றுதல்
                time_str = datetime.fromtimestamp(ts).strftime('%d %b, %I:%M %p') if ts else "Just now"
                ref = item.get('stock_ref', 'Market')

                st.markdown(f"""
                    <div class="news-feed-card">
                        <div class="stock-badge">{ref}</div><br>
                        <a href="{link}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:800; font-size:16px;">
                            {title}
                        </a><br>
                        <p style="color:#888; font-size:12px; margin-top:8px;">{source} • {time_str}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.warning("சமீபத்திய செய்திகள் எதுவும் கிடைக்கவில்லை.")
            
        if st.button("🗑️ வாட்ச் லிஸ்டை காலி செய்"):
            st.session_state.watchlist = []
            st.rerun()

# 5. அடிக்குறிப்பு (Footer)
st.markdown(f"""
    <div class="footer">
        © {datetime.now().year} Tamil Invest Hub - Premium Analytics<br>
        வளர்ச்சியை நோக்கி ஒரு பயணம்
    </div>
""", unsafe_allow_html=True)
