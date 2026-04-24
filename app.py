import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64

# 1. Page Configuration
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# Logo Helper
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. Live Market Ticker Logic
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    ticker_text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            ticker_text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return ticker_text

# 3. Fundamental Scorer (சாதாரண மனிதர்களுக்கான எளிய கணிப்பு)
def fundamental_analyzer(info):
    score = 0
    checks = []
    
    roe = info.get('returnOnEquity', 0)
    if roe > 0.15: score += 2; checks.append("✅ ROE: முதலீட்டில் நல்ல லாபம் (High Efficiency)")
    
    debt = info.get('debtToEquity', 200)
    if debt < 100: score += 3; checks.append("✅ கடன் சுமை குறைவு (Debt Safe)")
    
    pe = info.get('trailingPE', 100)
    if pe < 25: score += 2; checks.append("✅ விலை குறைவாக உள்ளது (Value Buy)")
    
    cr = info.get('currentRatio', 0)
    if cr > 1.5: score += 3; checks.append("✅ போதுமான பணப்புழக்கம் உள்ளது (Cash Rich)")
    
    if score >= 8: return "Strong Buy 💎", "#2ea043", checks
    elif score >= 5: return "Watchlist 👀", "#ffd700", checks
    else: return "Avoid 🚫", "#f85149", checks

# 4. Premium CSS for Mobile & Desktop
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 5px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 11px; }
    .m-value { color: #ffd700; font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 5. Top Ticker Display
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# 6. Sidebar Controls
with st.sidebar:
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)
    L = {"Tamil": {"search": "பங்கின் பெயர்", "holders": "பங்குதாரர்", "actions": "நிகழ்வுகள்", "about": "நிறுவனத்தைப் பற்றி"},
         "English": {"search": "Search Stock", "holders": "Shareholding", "actions": "Actions", "about": "About Stock"}}[sel_lang]

# 7. Header Section
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:55px; border-radius:10px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 8. TABS (All-in-One Analysis)
tab1, tab2, tab3, tab4 = st.tabs(["📊 அனாலிசிஸ்", "📅 ஈவென்ட்ஸ்", "🤝 பங்குதாரர்கள்", "💼 புரோக்கர்"])

with tab1:
    u_input = st.text_input(L["search"], value="COALINDIA").upper()
    ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input
    
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        st.markdown(f"### {info.get('longName', ticker)}")

        # --- AI Verdict Section ---
        verdict, v_color, checks = fundamental_analyzer(info)
        st.markdown(f"""
            <div style="background:{v_color}22; border:2px solid {v_color}; border-radius:10px; padding:15px; text-align:center;">
                <span style="color:{v_color}; font-size:18px; font-weight:900;">{verdict}</span>
                <div style="font-size:11px; margin-top:5px;">{"<br>".join(checks)}</div>
            </div>
        """, unsafe_allow_html=True)

        # --- Compact Metrics Section ---
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">LTP</span><br><span class="m-value">₹{price:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        # --- Charting Section ---
        p_col, s_col = st.columns(2)
        pd_sel = p_col.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
        st_sel = s_col.radio("Type", ["Line", "Candle"], horizontal=True, label_visibility="collapsed")
        
        interval = "1m" if pd_sel == "1d" else "15m" if pd_sel == "5d" else "1d"
        hist = stock.history(period=pd_sel, interval=interval)
        
        if not hist.empty:
            fig = go.Figure()
            if st_sel == "Line":
                fig.add_trace(go.Scatter(x=hist.index, y=hist['Close'], fill='tozeroy', line=dict(color='#ffd700', width=2)))
            else:
                fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']))
            
            fig.update_layout(height=280, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # --- Bollinger Band Width (BBW) ---
            st.markdown("#### BBW (Volatility Indicator)")
            bb_data = stock.history(period="6mo")
            sma = bb_data['Close'].rolling(window=20).mean()
            std = bb_data['Close'].rolling(window=20).std()
            bbw = ((sma + 2*std) - (sma - 2*std)) / sma
            
            fig_bbw = go.Figure(data=[go.Scatter(x=bbw.index, y=bbw, line=dict(color='#58a6ff', width=1))])
            fig_bbw.update_layout(height=120, margin=dict(l=0,r=0,t=10,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_bbw, use_container_width=True)

        st.markdown(f"#### {L['about']}")
        st.write(info.get('longBusinessSummary', 'தகவல் இல்லை.'))

    except Exception as e: st.info(f"Searching Stock Data... {e}")

with tab2:
    st.markdown(f"### {L['actions']}")
    actions = stock.actions.tail(10).sort_index(ascending=False)
    for date, row in actions.iterrows():
        if row['Dividends'] > 0: st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{row['Dividends']}")
        if row['Stock Splits'] > 0: st.success(f"📅 {date.strftime('%d %b %Y')} - Bonus/Split: {row['Stock Splits']}")

with tab3:
    st.markdown(f"### {L['holders']}")
    p = info.get('heldPercentInsiders', 0.5) * 100
    fii = info.get('heldPercentInstitutions', 0.2) * 100
    fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, fii, 100-(p+fii)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
    fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
    st.plotly_chart(fig_pie, use_container_width=True)

with tab4:
    st.button("Connect Zerodha Kite")
    st.button("Connect Angel One")
    st.info("Portfolio connection features coming soon.")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:20px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
