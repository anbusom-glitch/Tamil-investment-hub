import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. பக்க அமைப்பு மற்றும் தீம்
st.set_page_config(page_title="Tamil Invest Hub", layout="wide", initial_sidebar_state="collapsed")

# 2. ஸ்க்ரீன்ஷாட்டில் உள்ளவாறே பிரத்யேக டிசைன் (Advanced CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #0e1117; color: #ffffff; }
    
    /* கிரேடியன்ட் தலைப்பு (As per screenshot) */
    .main-header {
        background: linear-gradient(to right, #4caf50, #ff9800, #f44336);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        font-size: 28px; font-weight: bold; text-align: center; margin-bottom: 20px;
    }
    
    /* மெட்ரிக் கார்டுகள் (The 3-Row Grid Style) */
    .metric-card {
        background-color: #161b22;
        border: 1px solid #30363d;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 10px;
    }
    .label-text { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .value-text { color: #f9d71c; font-size: 18px; font-weight: bold; }
    
    /* Tabs ஸ்டைல் */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] { 
        height: 35px; border-radius: 5px; font-size: 12px; 
        background-color: #161b22; color: #8b949e; 
    }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #f44336 !important; color: #ffffff !important; }
    
    /* பட்டன் ஸ்டைல் */
    .stButton>button {
        background-color: #161b22; color: #ffffff; border: 1px solid #30363d;
        border-radius: 5px; font-size: 12px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. செஷன் ஸ்டேட் (Watchlist)
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []

# 4. ஹெடர்
st.markdown('<p class="main-header">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 5. சர்ச் வசதி
raw_query = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, Coal India)", value="SBI")
ticker = raw_query.strip().upper()
# இந்தியப் பங்குகளுக்கு தானாகவே .NS சேர்த்தல்
if ticker and ticker in ["SBI", "RELIANCE", "TCS", "INFY", "TATASTEEL"]:
    mapping = {"SBI": "SBIN.NS", "RELIANCE": "RELIANCE.NS", "TCS": "TCS.NS"}
    ticker = mapping.get(ticker, f"{ticker}.NS")
elif ticker and not (ticker.endswith(".NS") or ticker.endswith(".BO")):
    ticker = f"{ticker}.NS"

# 6. டேட்டா பெறுதல்
try:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # டேப்கள் உருவாக்கம் (Icons உடன்)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📊 Analysis", "📝 Overview", "🤝 Shareholding", "🔮 Forecast", "📅 Action", "📰 News"
    ])

    with tab1:
        st.subheader(info.get('longName', ticker))
        
        if st.button(f"⭐ Add {ticker.split('.')[0]} to Watchlist"):
            if ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(ticker)
                st.toast("Added to Watchlist!")

        # --- மெட்ரிக்ஸ் கிரிட் (3 Rows as per Screenshot) ---
        curr_p = info.get('currentPrice', 0)
        pe = info.get('trailingPE', 0)
        pb = info.get('priceToBook', 0)
        peg = info.get('pegRatio', 0)
        high_52 = info.get('fiftyTwoWeekHigh', 0)
        low_52 = info.get('fiftyTwoWeekLow', 0)

        # Row 1
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-card"><p class="label-text">விலை (LTP)</p><p class="value-text">₹{curr_p:,.1f}</p></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-card"><p class="label-text" style="text-align:right">P/E RATIO</p><p class="value-text" style="text-align:right">{pe:.6f}</p></div>', unsafe_allow_html=True)

        # Row 2
        c3, c4 = st.columns(2)
        with c3:
            st.markdown(f'<div class="metric-card"><p class="label-text">P/B RATIO</p><p class="value-text">{pb:.7f}</p></div>', unsafe_allow_html=True)
        with c4:
            st.markdown(f'<div class="metric-card"><p class="label-text" style="text-align:right">PEG RATIO</p><p class="value-text" style="text-align:right">{peg:.2f}</p></div>', unsafe_allow_html=True)

        # Row 3
        c5, c6 = st.columns(2)
        with c5:
            st.markdown(f'<div class="metric-card"><p class="label-text">52W LOW</p><p class="value-text">₹{low_52:,.1f}</p></div>', unsafe_allow_html=True)
        with c6:
            st.markdown(f'<div class="metric-card"><p class="label-text" style="text-align:right">52W HIGH</p><p class="value-text" style="text-align:right">₹{high_52:,.1f}</p></div>', unsafe_allow_html=True)

        # --- பீரியட் செலக்டர் மற்றும் சார்ட் ---
        period = st.radio("Period", ["1d", "5d", "1mo", "1y"], index=0, horizontal=True)
        interval = "5m" if period == "1d" else "1d"
        hist = stock.history(period=period, interval=interval)

        if not hist.empty:
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], mode='lines', line=dict(color='#30363d', width=2)))
            fig.update_layout(
                template="plotly_dark",
                height=300,
                margin=dict(l=0, r=0, t=0, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, showline=False, zeroline=False),
                yaxis=dict(showgrid=True, gridcolor='#1f2328', side='left')
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    with tab3:
        st.markdown("### 🤝 Shareholding Pattern")
        # முந்தைய வட்ட வரைபடம் (Pie Chart) இங்கும் வரும்
        labels = ['Promoters', 'Institutions', 'Others']
        vals = [info.get('heldPercentInsiders', 0.5)*100, info.get('heldPercentInstitutions', 0.3)*100]
        vals.append(100 - sum(vals))
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=vals, hole=.5, marker_colors=['#f9d71c', '#4285F4', '#34A853'])])
        fig_pie.update_layout(height=300, margin=dict(t=0, b=0), paper_bgcolor='rgba(0,0,0,0)', legend=dict(orientation="h", y=-0.1))
        st.plotly_chart(fig_pie, use_container_width=True)

except Exception:
    st.error("சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<br><center style='color:#333; font-size:10px;'>© 2026 TAMIL INVEST HUB</center>", unsafe_allow_html=True)
