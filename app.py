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

# 2. ராயல் டிசைன் (Elite CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #050a0f; color: #e0e0e0; }
    
    .ticker-wrapper {
        width: 100%; background: #161b22; color: #ffd700;
        padding: 5px 0; overflow: hidden; border-bottom: 1px solid #ffd700;
        font-size: 11px; font-weight: bold;
    }
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 22px !important; font-weight: 800; text-align: center; margin-top: 10px;
    }
    .stTabs [data-baseweb="tab-list"] { gap: 5px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { height: 35px; border-radius: 12px; font-size: 11px; }
    .stTabs [aria-selected="true"] { background-color: #ffd700 !important; color: #000 !important; font-weight: bold; }
    
    /* Watchlist Card */
    .watchlist-card { background: #111418; border-radius: 8px; padding: 10px; margin-bottom: 5px; border-left: 3px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# 3. செஷன் ஸ்டேட் (Watchlist Fix)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# 4. லைவ் டிக்கர் (Market Ticker)
indices = {'^NSEI': 'NSEI', '^BSESN': 'BSESN'}
ticker_data = ""
for id, name in indices.items():
    try:
        val = yf.Ticker(id).fast_info['last_price']
        ticker_data += f" | {name}: ₹{val:,.1f}"
    except: pass
st.markdown(f'<div class="ticker-wrapper"><marquee>{ticker_data} | {ticker_data}</marquee></div>', unsafe_allow_html=True)

# 5. மெயின் ஆப்
st.markdown('<p class="royal-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

ticker = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, TCS)", value="COALINDIA.NS").upper()

try:
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="1mo")

    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "🤝 Shareholding", "👀 Watchlist", "📰 News"])

    # --- TAB 1: Analysis ---
    with tab1:
        st.subheader(f"{info.get('longName', ticker)}")
        curr_p = info.get('currentPrice', hist['Close'].iloc[-1])
        st.metric("Price", f"₹{curr_p:,.2f}", f"{((curr_p-info.get('previousClose',0))/info.get('previousClose',1))*100:+.2f}%")
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(template="plotly_dark", xaxis_rangeslider_visible=False, height=350, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # --- TAB 2: Shareholding (Fixed Size) ---
    with tab2:
        st.markdown("### 🤝 Shareholding Pattern")
        labels = ['Promoters', 'Institutions', 'Others']
        values = [info.get('heldPercentInsiders', 0.5)*100, 
                  info.get('heldPercentInstitutions', 0.3)*100, 
                  (1 - info.get('heldPercentInsiders', 0.5) - info.get('heldPercentInstitutions', 0.3))*100]
        
        # சிறிதாக்கப்பட்ட Pie Chart (Compact Size)
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker_colors=['#ffd700', '#4285F4', '#34A853'])])
        fig_pie.update_layout(
            height=280, # அளவைக் குறைத்துள்ளேன்
            margin=dict(l=20, r=20, t=10, b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.1, xanchor="center", x=0.5),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 3: Watchlist (Working Fix) ---
    with tab3:
        st.markdown("### 👀 My Watchlist")
        if st.button(f"➕ Add {ticker} to Watchlist"):
            if ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(ticker)
                st.rerun() # பக்கத்தை ரிஃப்ரெஷ் செய்து டேட்டாவைக் காட்டும்
        
        if st.session_state.watchlist:
            for w in st.session_state.watchlist:
                st.markdown(f"""
                    <div class="watchlist-card">
                        <span style="color:#ffd700; font-weight:bold;">{w}</span>
                        <span style="float:right; font-size:12px;">Saved ✅</span>
                    </div>
                """, unsafe_allow_html=True)
            
            if st.button("🗑️ Clear Watchlist"):
                st.session_state.watchlist = []
                st.rerun()
        else:
            st.info("Watchlist is empty.")

    # --- TAB 4: News ---
    with tab4:
        for n in stock.news[:5]:
            st.markdown(f"**[{n['title']}]({n['link']})**")
            st.caption(f"Source: {n['publisher']}")

except:
    st.error("சரியான குறியீட்டை இடவும் (eg: SBIN.NS)")

st.markdown("<br><center style='color:#333; font-size:10px;'>© 2026 TAMIL INVEST HUB</center>", unsafe_allow_html=True)
