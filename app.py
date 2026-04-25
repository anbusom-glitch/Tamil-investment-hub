import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(str(text)[:1000])
    except: return str(text)

# 2. பிரீமியம் CSS (பெரிய எழுத்துக்கள் & குவாலிட்டி UI)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 15px !important; background-color: #0d1117; color: #ffffff; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 2px solid #39FF14; padding: 12px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 14px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .main-title { 
        text-align: center; font-size: 45px !important; font-weight: 950; 
        background: linear-gradient(90deg, #39FF14, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-shadow: 0px 0px 20px rgba(57, 255, 20, 0.4);
    }
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; }
    .m-label { color: #ffffff !important; font-size: 12px; text-transform: uppercase; opacity: 0.8; }
    .m-value { color: #ffffff !important; font-size: 18px; font-weight: bold; }
    .rating-card { padding: 25px; border-radius: 15px; text-align: center; margin: 15px 0; border: 2px solid rgba(255,255,255,0.1); }
    .score-text { font-size: 48px; font-weight: 900; margin: 10px 0; }
    .news-card { background: #161b22; border-radius: 8px; padding: 15px; margin-bottom: 10px; border-left: 5px solid #39FF14; }
    </style>
    """, unsafe_allow_html=True)

# 3. லைவ் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
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
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Stock", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

# 5. டேப்கள்
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 பகுப்பாய்வு", "⭐ ரேட்டிங் (Rating)", "📅 Corporate Action", "🔮 கணிப்பு", "🗞️ செய்திகள்", "📌 Watchlist"
])

stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except: pass

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    with tab1:
        st.markdown(f"### {info.get('longName')}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E RATIO</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 🏆 Stock Quality Score (0 - 100)")
        # ரேட்டிங் லாஜிக் (Easy Handling)
        score = 0
        pe = info.get('trailingPE', 100)
        roe = info.get('returnOnEquity', 0)
        debt = info.get('debtToEquity', 150)
        
        if pe < 25: score += 35
        elif pe < 40: score += 20
        if roe > 0.18: score += 35
        elif roe > 0.12: score += 20
        if debt < 100: score += 30
        
        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        verdict = "நிச்சயமாக வாங்கலாம் (BUY) 🚀" if score >= 70 else ("தற்போது வைத்திருக்கலாம் (HOLD) ⚖️" if score >= 40 else "தவிர்ப்பது நல்லது (AVOID) ⚠️")
        
        st.markdown(f"""
            <div class="rating-card" style="background: rgba(255,255,255,0.05);">
                <p style="font-size: 20px; color: #8b949e;">பங்கின் தரம் (Total Score)</p>
                <p class="score-text" style="color: {color};">{score} / 100</p>
                <p style="font-size: 24px; font-weight: bold; color: {color};">{verdict}</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.write(f"🔹 **ROE:** {roe*100:.2f}% | **Debt/Equity:** {debt} | **P/E:** {pe}")

    with tab3:
        st.markdown("### 📅 Corporate Actions (டிவிடெண்ட் & போனஸ்)")
        actions = stock_obj.actions.tail(10).sort_index(ascending=False)
        if not actions.empty:
            st.table(actions)
        else:
            st.info("சமீபத்திய நிகழ்வுகள் ஏதுமில்லை.")

    with tab4:
        st.markdown("### 🔮 கணிப்பு (Analyst Forecast)")
        target = info.get('targetMeanPrice')
        if target:
            diff = ((target - ltp) / ltp) * 100
            st.metric("எதிர்பார்க்கப்படும் விலை", f"₹{target:,.2f}", f"{diff:.2f}% உயர்வு")
        else: st.write("கணிப்புகள் கிடைக்கவில்லை.")

    with tab5:
        st.markdown("### 🗞️ நேரலைச் செய்திகள்")
        for n in stock_obj.news[:5]:
            st.markdown(f'<div class="news-card"><a href="{n.get("link","#")}" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration:none;">{n.get("title")}</a></div>', unsafe_allow_html=True)

    with tab6:
        st.markdown("### 📌 Watchlist")
        if st.button(f"Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        for item in st.session_state['watchlist']:
            st.write(f"✅ {item}")

else:
    st.info("Loading Stock Data... (eg: TCS, RELIANCE)")

st.markdown("<p style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
