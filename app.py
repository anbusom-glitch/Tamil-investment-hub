import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# செஷன் ஸ்டேட்
if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உலகத்தரம் வாய்ந்த UI (Premium Glassmorphism)
st.markdown(f"""
    <style>
    html, body, [class*="css"] {{ font-size: 14px !important; background-color: #0d1117; color: #ffffff; }}
    
    .header-container {{ text-align: center; padding: 15px 0; }}
    .main-title {{ 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        letter-spacing: 0.5px;
    }}
    .sub-title {{ font-size: 10px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.6; }}
    
    .metric-card {{
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
    }}
    .m-label {{ color: #8b949e !important; font-size: 11px; text-transform: uppercase; font-weight: 700; }}
    .m-value {{ color: #ffffff !important; font-size: 17px; font-weight: 800; }}
    
    .rating-card {{ 
        padding: 20px; border-radius: 15px; text-align: center; 
        margin: 15px 0; border: 2px solid rgba(255,255,255,0.1); 
        background: rgba(255,255,255,0.05); 
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி தேர்வு
col_lang1, col_lang2 = st.columns([8, 2])
with col_lang2:
    lang_btn = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    st.session_state['language'] = lang_btn

# 4. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. டேட்டா லோடிங் (Safety Logic)
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if info and 'symbol' in info:
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    # Analysis Tab
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        st.markdown(f'<div class="metric-card"><span class="m-label">LTP (Price)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
        fig_price = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig_price.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig_price, use_container_width=True)

    # Shareholding Tab (FII/DII Split)
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6)
        dii = inst - fii
        pub = max(0, 100 - (promo + inst))
        
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
        fig_pie.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Rating Tab
    with tabs[2]:
        st.markdown(f"### {get_text('Rating Score', 'ரேட்டிங் ஸ்கோர்')}")
        pe = info.get('trailingPE', 0)
        roe = info.get('returnOnEquity', 0)
        score = 0
        if 0 < pe < 25: score += 40
        if roe > 0.15: score += 40
        if not hist.empty and ltp > hist['Close'].rolling(50).mean().iloc[-1]: score += 20
        
        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        st.markdown(f'<div class="rating-card"><h1 style="color:{color};">{score}/100</h1></div>', unsafe_allow_html=True)

    # Actions Tab
    with tabs[3]:
        st.markdown(f"### {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        if not stock_obj.actions.empty:
            st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)
        else:
            st.info("சமீபத்திய நிகழ்வுகள் ஏதுமில்லை.")

    # Watchlist Tab
    with tabs[4]:
        st.markdown(f"### {get_text('My Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        st.divider()
        if st.session_state['watchlist']:
            for item in st.session_state['watchlist']:
                cw1, cw2 = st.columns([5, 1])
                cw1.markdown(f'<div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px;">📌 {item}</div>', unsafe_allow_html=True)
                if cw2.button("❌", key=f"del_{item}"):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()
else:
    st.info("Loading Stock Data... (eg: RELIANCE, TCS)")

st.markdown("<p style='text-align:center;color:#444;font-size:11px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
