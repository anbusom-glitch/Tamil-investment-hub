import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு மற்றும் பிரீமியம் கான்ஃபிக்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# அதிவேக மொழிபெயர்ப்பு - பிழைகளைத் தவிர்க்க try-except
@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(str(text)[:1000])
    except: return str(text)

# 2. உலகத்தரம் வாய்ந்த CSS (பெரிய எழுத்துக்கள் & பிரகாசமான தலைப்பு)
st.markdown("""
    <style>
    /* Global Big Font */
    html, body, [class*="css"] { font-size: 15px !important; background-color: #0d1117; color: #ffffff; }
    
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 2px solid #39FF14; padding: 12px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 14px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* Neon Glow Title */
    .header-container { text-align: center; margin: 20px 0; }
    .main-title { 
        font-size: 45px !important; 
        font-weight: 950; 
        background: linear-gradient(90deg, #39FF14, #FF3131);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(57, 255, 20, 0.4);
    }
    .sub-title { font-size: 15px !important; color: #8b949e; font-style: italic; margin-top: -5px; }
    
    /* Metric Boxes - White Labels */
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #ffffff !important; font-size: 12px; text-transform: uppercase; opacity: 0.8; }
    .m-value { color: #ffffff !important; font-size: 18px; font-weight: bold; }
    
    /* UI Buttons & Tabs */
    .news-card { background: #161b22; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #39FF14; }
    .rating-box { padding: 20px; border-radius: 12px; text-align: center; font-weight: bold; font-size: 22px; border: 1px solid rgba(255,255,255,0.2); }
    [data-testid="stHeader"] { height: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. லைவ் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS", "HDFCBANK.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#39FF14" if c >= 0 else "#FF3131"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச் இன்ஜின்
u_input = st.text_input("Search Stock (eg: RELIANCE, TCS, ZOMATO)", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

# 5. டேப்கள் (Overview மீண்டும் சேர்க்கப்பட்டுள்ளது)
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Analysis", "📝 Overview", "🤝 Shareholding", "⭐ Ratings", "🔮 Forecast", "🗞️ News", "📌 Watchlist"
])

# டேட்டா லோடிங் செக்ஷன்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except Exception as e:
    stock_loaded = False

if stock_loaded:
    with tab1:
        st.markdown(f"### {info.get('longName', u_input)}")
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">Market Cap</span><br><span class="m-value">₹{info.get("marketCap", 0)//10**7:,.0f} Cr</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">ROE</span><br><span class="m-value">{info.get("returnOnEquity", 0)*100:.2f}%</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=450, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📝 Overview (நிறுவன விளக்கம்)")
        # இங்கே பிழை ஏற்படாமல் இருக்க பாதுகாப்பான முறையில் டேட்டா எடுக்கப்படுகிறது
        summary = info.get('longBusinessSummary') or info.get('description') or "விளக்கம் கிடைக்கவில்லை."
        with st.spinner("தமிழில் மொழிபெயர்க்கிறேன்..."):
            tamil_summary = translate_to_tamil(summary)
            st.write(tamil_summary)
        
        st.divider()
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Website:** {info.get('website', 'N/A')}")

    with tab3:
        st.markdown("### Shareholding Pattern")
        p, i = info.get('heldPercentInsiders', 0)*100, info.get('heldPercentInstitutions', 0)*100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[p, i, 100-(p+i)], hole=0.5)])
        fig_pie.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tab4:
        st.markdown("### Stock Ratings (AI Verdict)")
        score = 0
        pe = info.get('trailingPE', 100)
        roe = info.get('returnOnEquity', 0)
        ltp = info.get('currentPrice', 0)
        ma50 = hist['Close'].rolling(50).mean().iloc[-1] if not hist.empty else 0
        
        if pe < 30: score += 1
        if roe > 0.15: score += 1
        if ltp > ma50: score += 1

        if score == 3: st.markdown('<div class="rating-box" style="background:#39FF14; color:black;">STRONG BUY 🚀</div>', unsafe_allow_html=True)
        elif score == 2: st.markdown('<div class="rating-box" style="background:#ffd700; color:black;">HOLD / NEUTRAL ⚖️</div>', unsafe_allow_html=True)
        else: st.markdown('<div class="rating-box" style="background:#FF3131; color:white;">AVOID / SELL ⚠️</div>', unsafe_allow_html=True)

    with tab5:
        st.markdown("### Forecast (கணிப்பு)")
        target = info.get('targetMeanPrice')
        if target:
            upside = ((target - ltp) / ltp) * 100
            st.metric("Target Price", f"₹{target:,.2f}", f"{upside:.2f}% Upside")
        else: st.info("தரவுகள் கிடைக்கவில்லை.")

    with tab6:
        st.markdown("### Live News Feed")
        try:
            news_list = stock_obj.news
            if news_list:
                for n in news_list[:5]:
                    st.markdown(f'<div class="news-card"><a href="{n.get("link","#")}" target="_blank" style="color:#39FF14; font-weight:bold; font-size:17px; text-decoration:none;">{n.get("title")}</a><br><small style="color:#8b949e;">{n.get("publisher")}</small></div>', unsafe_allow_html=True)
            else: st.write("செய்திகள் ஏதுமில்லை.")
        except: st.error("செய்திகளை லோடு செய்வதில் பிழை.")

    with tab7:
        st.markdown("### My Watchlist")
        if st.button(f"➕ Add {u_input} to Watchlist"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        
        st.divider()
        for item in st.session_state['watchlist']:
            cw1, cw2 = st.columns([5, 1])
            cw1.write(f"**📌 {item}**")
            if cw2.button("Remove", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("Loading Stock Data... சரியான பங்கு பெயரைக் குறிப்பிடவும்.")

st.markdown("<div style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</div>", unsafe_allow_html=True)
