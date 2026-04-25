import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. பிரீமியம் UI ஸ்டைலிங்
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; 
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    
    /* விவரங்களுக்கான கார்டுகள் */
    .metric-box {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between;
    }
    .m-label { color: #8b949e; font-size: 12px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    
    /* கட்டுரை பகுதி (About Section) */
    .about-box {
        background: rgba(57, 255, 20, 0.05); border: 1px solid #39FF14;
        border-radius: 12px; padding: 20px; margin-top: 20px; line-height: 1.6;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி மற்றும் தலைப்பு
col_l1, col_l2 = st.columns([8, 2])
with col_l2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")

st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)

# 4. தேடுதல்
u_input = st.text_input("Search Symbol", value="RELIANCE").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 5. தரவுகளைப் பெறுதல் (Robust Logic)
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")
    
    if info and 'symbol' in info:
        # --- பகுப்பாய்வு பகுதி (TAB 1) ---
        with tabs[0]:
            st.subheader(info.get('longName', u_input))
            
            # முக்கிய விவரங்கள் (Metrics)
            m_data = [
                ("Sector", info.get('sector', 'N/A')),
                ("LTP (Price)", f"₹{info.get('currentPrice', 0):,.2f}"),
                ("52 Week High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
                ("52 Week Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}"),
                ("P/B Ratio", f"{info.get('priceToBook', 'N/A')}"),
                ("P/E Ratio", f"{info.get('trailingPE', 'N/A')}")
            ]
            
            for lbl, val in m_data:
                st.markdown(f'<div class="metric-box"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
            
            # சார்ட்
            fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)
            
            # நிறுவனத்தைப் பற்றிய சிறு கட்டுரை (About Section)
            st.markdown(f"### {get_text('About Company', 'நிறுவனத்தைப் பற்றி')}")
            summary = info.get('longBusinessSummary', 'தகவல் இல்லை.')
            st.markdown(f'<div class="about-box">{summary}</div>', unsafe_allow_html=True)

        # --- பங்குதாரர் பகுதி (TAB 2) ---
        with tabs[1]:
            promo = (info.get('heldPercentInsiders') or 0) * 100
            inst = (info.get('heldPercentInstitutions') or 0) * 100
            fii = info.get('foreignInstitutionalHolders', inst * 0.6)
            dii = inst - fii
            pub = max(0, 100 - (promo + inst))
            fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], hole=0.5)])
            st.plotly_chart(fig_pie, use_container_width=True)

        # --- ரேட்டிங் பகுதி (TAB 3) ---
        with tabs[2]:
            score = 0
            pe = info.get('trailingPE', 0)
            roe = info.get('returnOnEquity', 0)
            if 0 < pe < 25: score += 40
            if roe > 0.15: score += 40
            if not hist.empty and info.get('currentPrice', 0) > hist['Close'].rolling(50).mean().iloc[-1]: score += 20
            color = "#39FF14" if score >= 70 else "#FF3131"
            st.markdown(f'<div style="text-align:center; padding:30px; border-radius:15px; border:2px solid {color};"><h1>Score: {score}/100</h1></div>', unsafe_allow_html=True)

        # --- வாட்ச்லிஸ்ட் பகுதி (TAB 4) ---
        with tabs[3]:
            if st.button(f"➕ Add {u_input}"):
                if u_input not in st.session_state['watchlist']:
                    st.session_state['watchlist'].append(u_input)
                    st.rerun()
            for item in st.session_state['watchlist']:
                c1, c2 = st.columns([5,1])
                c1.info(f"📌 {item}")
                if c2.button("❌", key=item):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()

except Exception as e:
    st.error(f"Error: {e}. சரியான குறியீட்டை (Symbol) உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
