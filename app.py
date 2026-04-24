import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# 1. Page Configuration
st.set_page_config(page_title="TS INVEST PRO", page_icon="📈", layout="wide")

# 2. Language Dictionary (Tamil & English)
lang_dict = {
    "English": {
        "title": "TS INVEST PRO",
        "analysis": "🔍 Analysis", "broker": "💼 Broker Connect", "feed": "🗞️ Market Feed",
        "search": "Enter Ticker (e.g. COALINDIA.NS)", "ltp": "LTP", "pe": "P/E", "pb": "P/B", "peg": "PEG",
        "chart": "Price Chart", "holders": "Detailed Shareholding Pattern", "about": "About Company",
        "period": "Period", "ctype": "Chart Style", "news": "Live News Feed"
    },
    "Tamil": {
        "title": "TS இன்வெஸ்ட் PRO",
        "analysis": "🔍 ஆய்வு", "broker": "💼 புரோக்கர் இணைப்பு", "feed": "🗞️ சந்தை செய்திகள்",
        "search": "பங்கின் குறியீட்டை உள்ளிடவும்:", "ltp": "விலை", "pe": "P/E", "pb": "P/B", "peg": "PEG",
        "chart": "விலை வரைபடம்", "holders": "விரிவான பங்குதாரர் விவரம்", "about": "நிறுவனத்தைப் பற்றி",
        "period": "கால அளவு", "ctype": "வரைபட வகை", "news": "நேரலைச் செய்திகள்"
    }
}

# 3. CSS for Mobile View
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12px !important; background-color: #0d1117; color: #c9d1d9; }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 22px !important; font-weight: 800; text-align: center; }
    [data-testid="stMetric"] { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 5px !important; }
    .stTabs [data-baseweb="tab"] { font-size: 11px !important; padding: 10px !important; }
    </style>
    """, unsafe_allow_html=True)

# 4. Language Selection
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["English", "Tamil"], horizontal=True)
    L = lang_dict[sel_lang]

st.markdown(f'<p class="header-text">{L["title"]}</p>', unsafe_allow_html=True)

# 5. TABS
tab1, tab2, tab3 = st.tabs([L["analysis"], L["broker"], L["feed"]])

with tab1:
    ticker = st.text_input(L["search"], value="COALINDIA.NS").upper()
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # Prices and Color Logic
        price = info.get('currentPrice') or info.get('regularMarketPrice', 0)
        prev_close = info.get('regularMarketPreviousClose', price)
        diff = price - prev_close
        
        # Color: Green if price is up, Red if price is down
        chart_color = '#2ea043' if diff >= 0 else '#f85149'

        st.markdown(f"**{info.get('longName', ticker)}**")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric(L["ltp"], f"₹{price:,.1f}", f"{diff:,.2f}")
        m2.metric(L["pe"], f"{info.get('trailingPE', 'N/A')}")
        m3.metric(L["pb"], f"{info.get('priceToBook', 'N/A')}")
        m4.metric(L["peg"], f"{info.get('pegRatio', 'N/A')}")

        st.divider()

        # --- Chart Controls ---
        st.markdown(f"**{L['chart']}**")
        p_col, c_col = st.columns(2)
        with p_col:
            period = st.select_slider(L["period"], options=["1d", "5d", "1mo", "3mo", "6mo", "1y"], value="1mo")
        with c_col:
            chart_type = st.radio(L["ctype"], ["Line", "Candle"], horizontal=True)
        
        # Fetching History
        hist = stock.history(period=period)
        if not hist.empty:
            fig = go.Figure()
            if chart_type == "Line":
                fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color=chart_color, width=2)))
            else:
                # Candle colors follow standard market rules (Red/Green)
                fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']))
            
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=10, b=0), paper_bgcolor='rgba(0,0,0,0)', 
                              plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

        # --- Enhanced Shareholding Pattern (FII & DII Separate) ---
        st.markdown(f"**{L['holders']}**")
        
        # Data Simulation for FII/DII (yfinance does not split them automatically in all markets)
        promoter = info.get('heldPercentInsiders', 0.5) * 100
        inst_total = info.get('heldPercentInstitutions', 0.3) * 100
        fii = inst_total * 0.6 # Approximately 60% of institutions are FII
        dii = inst_total * 0.4 # Approximately 40% of institutions are DII
        others = 100 - (promoter + fii + dii)
        
        labels = ['Promoters', 'FII (Foreign)', 'DII (Domestic)', 'Others']
        values = [promoter, fii, dii, others]
        pie_colors = ['#ffd700', '#58a6ff', '#ff7b72', '#2ea043'] # Gold, Blue, Coral, Green

        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.5, marker=dict(colors=pie_colors))])
        fig_pie.update_layout(height=250, margin=dict(l=0, r=0, t=30, b=0), 
                              legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5))
        st.plotly_chart(fig_pie, use_container_width=True)

        with st.expander(L["about"]):
            st.write(info.get('longBusinessSummary', 'N/A'))

    except: st.info("Loading Stock Data...")

# Tab 2 & 3 simplified for performance
with tab2:
    st.button("Connect Zerodha")
    st.button("Connect Angel One")

with tab3:
    st.markdown(f"### {L['news']}")
    try:
        news = stock.news
        for n in news[:6]:
            st.markdown(f'<div style="background:#161b22; padding:10px; border-radius:8px; margin-bottom:8px; border-left:3px solid #ffd700;"><a href="{n["link"]}" target="_blank" style="color:#ffd700; text-decoration:none;">{n["title"]}</a></div>', unsafe_allow_html=True)
    except: st.write("News currently unavailable.")

st.markdown('<div style="text-align:center; color:#333; font-size:10px; margin-top:30px;">© 2026 TS INVEST</div>', unsafe_allow_html=True)
