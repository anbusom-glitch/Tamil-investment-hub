import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from datetime import datetime

# 1. ராயல் தீம் மற்றும் பக்க அமைப்பு
st.set_page_config(
    page_title="Tamil Invest Hub Pro",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. அல்டிமேட் ராயல் டிசைன் (Elite Compact CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050a0f; color: #e0e0e0; }
    
    /* Live Ticker Bar */
    .ticker-wrapper {
        width: 100%; background: #161b22; color: #ffd700;
        padding: 5px 0; overflow: hidden; border-bottom: 1px solid #ffd700;
        font-size: 11px; font-weight: bold; position: sticky; top: 0; z-index: 999;
    }
    
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 24px !important; font-weight: 800; text-align: center; margin-top: 15px;
    }
    
    /* கச்சிதமான Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 5px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 35px; border-radius: 12px; font-size: 11px; background-color: #161b22; padding: 0 15px; }
    .stTabs [aria-selected="true"] { background: linear-gradient(45deg, #b8860b, #ffd700) !important; color: #000 !important; font-weight: bold; }
    
    /* Card Styles */
    .card { background: #111418; border-radius: 10px; padding: 12px; margin-bottom: 8px; border: 1px solid #1e2630; }
    .gold-text { color: #ffd700; font-weight: bold; }
    .footer { font-size: 10px; color: #444; text-align: center; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# 3. செஷன் ஸ்டேட் (Data Storage for Watchlist)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# 4. லைவ் டிக்கர் (Top Bar)
try:
    indices = {'^NSEI': 'NIFTY 50', '^BSESN': 'SENSEX'}
    t_data = " • ".join([f"{name}: ₹{yf.Ticker(id).fast_info['last_price']:,.0f}" for id, name in indices.items()])
    st.markdown(f'<div class="ticker-wrapper"><marquee>{t_data} | {t_data}</marquee></div>', unsafe_allow_html=True)
except:
    st.markdown('<div class="ticker-wrapper"><marquee>Live Market Tracking Active...</marquee></div>', unsafe_allow_html=True)

# 5. மெயின் டைட்டில்
st.markdown('<p class="royal-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 6. ஸ்மார்ட் சர்ச் (Smart Search Fix)
raw_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, Coal India)", value="RELIANCE")
ticker = raw_input.strip().replace(" ", "").upper()
if ticker and not (ticker.endswith(".NS") or ticker.endswith(".BO")):
    ticker = f"{ticker}.NS"

# 7. ஆப் லாஜிக் (Full Features with Tabs)
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1mo")

    if hist.empty:
        st.error(f"'{ticker}' பற்றிய தகவல்கள் Yahoo Finance-ல் இல்லை. சரியான பெயரைக் கொடுங்கள்.")
    else:
        # டாப் மெட்ரிக்ஸ்
        st.markdown(f"<p style='text-align:center; color:#ffd700; font-size:18px; margin-bottom:15px;'>{info.get('longName', ticker)}</p>", unsafe_allow_html=True)
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Analysis", "🤝 Shareholding", "👀 Watchlist", "📰 News", "💡 Overview"])

        # --- TAB 1: அனாலிசிஸ் (Live Chart) ---
        with tab1:
            curr_p = info.get('currentPrice', hist['Close'].iloc[-1])
            prev_c = info.get('previousClose', curr_p)
            chg = ((curr_p - prev_c) / prev_c) * 100
            
            c1, c2 = st.columns(2)
            c1.metric("Current Price", f"₹{curr_p:,.2f}")
            c2.metric("Day Change", f"{chg:+.2f}%")
            
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        # --- TAB 2: பங்குதாரர்கள் (Compact Pie Chart) ---
        with tab2:
            st.markdown("<p class='gold-text'>Shareholding Pattern</p>", unsafe_allow_html=True)
            labels = ['Promoters', 'Institutions', 'Others']
            vals = [info.get('heldPercentInsiders', 0.5)*100, info.get('heldPercentInstitutions', 0.2)*100]
            vals.append(100 - sum(vals))
            
            fig_pie = go.Figure(data=[go.Pie(labels=labels, values=vals, hole=.4, marker_colors=['#ffd700', '#4285F4', '#34A853'])])
            fig_pie.update_layout(height=280, margin=dict(t=0, b=0, l=0, r=0), paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- TAB 3: வாட்ச் லிஸ்ட் (Persistent Fix) ---
        with tab3:
            st.markdown("<p class='gold-text'>My Watchlist</p>", unsafe_allow_html=True)
            if st.button(f"➕ Add {ticker} to Watchlist"):
                if ticker not in st.session_state.watchlist:
                    st.session_state.watchlist.append(ticker)
                    st.rerun()
            
            if st.session_state.watchlist:
                for w in st.session_state.watchlist:
                    st.markdown(f"<div class='card'><span class='gold-text'>{w}</span> <span style='float:right; font-size:12px;'>Tracked ✅</span></div>", unsafe_allow_html=True)
                if st.button("🗑️ Clear Watchlist"):
                    st.session_state.watchlist = []
                    st.rerun()
            else:
                st.info("Watchlist is empty.")

        # --- TAB 4: செய்திகள் (Dynamic News) ---
        with tab4:
            st.markdown("<p class='gold-text'>Recent News Feed</p>", unsafe_allow_html=True)
            for n in stock.news[:5]:
                st.markdown(f"""
                    <div class='card'>
                        <a href='{n['link']}' target='_blank' style='color:#ffd700; text-decoration:none; font-size:13px; font-weight:bold;'>{n['title']}</a><br>
                        <span style='color:#555; font-size:10px;'>{n['publisher']} • {datetime.fromtimestamp(n['providerPublishTime']).strftime('%Y-%m-%d')}</span>
                    </div>
                """, unsafe_allow_html=True)

        # --- TAB 5: விவரம் (Company Overview) ---
        with tab5:
            st.markdown("<p class='gold-text'>Company Business Profile</p>", unsafe_allow_html=True)
            st.write(f"**Sector:** {info.get('sector', 'N/A')}")
            st.write(f"**Industry:** {info.get('industry', 'N/A')}")
            st.caption(info.get('longBusinessSummary', 'Description not available.')[:800] + "...")

except Exception as e:
    st.info("பங்கின் பெயரை உள்ளிட்டு உங்கள் ஆய்வைத் தொடங்குங்கள்.")

# 8. ஃபூட்டர்
st.markdown('<div class="footer">© 2026 Tamil Invest Hub - Elite Analytics<br>Focus on Action. Driven by Insight.</div>', unsafe_allow_html=True)
