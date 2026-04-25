import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உலகத்தரம் வாய்ந்த நவீன UI (Sleek & Professional)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ 
        font-size: 14px !important; 
        background-color: #0d1117; 
        color: #ffffff; 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}
    
    /* டிக்கர் ஸ்டைல் */
    .ticker-wrap {{ 
        width: 100%; overflow: hidden; background: rgba(22, 27, 34, 0.9); 
        border-bottom: 1px solid rgba(57, 255, 20, 0.2); 
        padding: 8px 0; position: sticky; top: 0; z-index: 999;
        backdrop-filter: blur(12px);
    }}
    .ticker-move {{ display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 12px; font-weight: 500; }}
    @keyframes ticker {{ 0% {{ transform: translateX(100%); }} 100% {{ transform: translateX(-100%); }} }}
    
    /* SLEEK WORLD-CLASS HEADER (FONT SIZE REDUCED) */
    .header-container {{ 
        text-align: center; 
        padding: 20px 0; 
        margin-bottom: 10px;
    }}
    .main-title {{ 
        font-size: 32px !important; /* அளவை குறைத்துள்ளேன் (Reduced Size) */
        font-weight: 800; 
        margin-bottom: 0px;
        letter-spacing: 1px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        filter: drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.3));
    }}
    .sub-title {{ 
        font-size: 10px !important; 
        color: #8b949e; 
        text-transform: lowercase; 
        letter-spacing: 3px;
        margin-top: 2px;
        font-weight: 300;
        opacity: 0.6;
    }}
    
    /* மெட்ரிக் கார்டுகள் */
    .metric-row {{ 
        background: #161b22; 
        border: 1px solid #30363d; 
        border-radius: 10px; 
        padding: 15px; 
        margin-bottom: 10px;
        transition: 0.3s;
    }}
    .metric-row:hover {{ border-color: #39FF14; box-shadow: 0 0 10px rgba(57, 255, 20, 0.1); }}
    .m-label {{ color: #8b949e !important; font-size: 9px; text-transform: uppercase; font-weight: 600; }}
    .m-value {{ color: #ffffff !important; font-size: 16px; font-weight: 700; }}
    
    /* ரேட்டிங் கார்டு */
    .rating-card {{ 
        padding: 20px; border-radius: 12px; text-align: center; 
        border: 1px solid rgba(255,255,255,0.1); 
        background: rgba(255,255,255,0.03); 
    }}
    .score-text {{ font-size: 42px; font-weight: 800; }}
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

# 4. நேர்த்தியான ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. பங்குத் தேடல் மற்றும் டேப்கள்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# டேட்டா லோடிங் செக்ஷன்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and 'symbol' in info:
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except: stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get("fiftyTwoWeekLow", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="metric-row"><div><span class="m-label">52W High</span><br><span class="m-value">₹{info.get("fiftyTwoWeekHigh", 0):,.1f}</span></div></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
        
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)

    with tabs[1]:
        st.markdown(f"#### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        pub = max(0, 100 - (promo + inst))
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, pub], hole=0.5)])
        fig_pie.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    with tabs[2]:
        st.markdown(f"#### {get_text('Quality Score', 'பங்கின் தரம்')}")
        score = 80 if (info.get('trailingPE', 100) < 30 and info.get('returnOnEquity', 0) > 0.15) else 45
        color = "#39FF14" if score > 70 else "#FF3131"
        st.markdown(f'<div class="rating-card"><p class="score-text" style="color:{color};">{score}/100</p></div>', unsafe_allow_html=True)

    with tabs[3]:
        st.markdown(f"#### {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)

    with tabs[4]:
        st.markdown(f"#### {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        st.write(st.session_state['watchlist'])

else:
    st.info("Loading Stock Data... (eg: TCS, RELIANCE)")

st.markdown("<p style='text-align:center;color:#444;font-size:11px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
