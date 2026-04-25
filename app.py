import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# 1. பக்க அமைப்பு மற்றும் செஷன் மேனேஜ்மென்ட்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []
if 'language' not in st.session_state:
    st.session_state['language'] = "Tamil"

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
        letter-spacing: 0.5px;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; text-transform: lowercase; letter-spacing: 2px; opacity: 0.6; }
    
    /* Rating Card Styles */
    .rating-card {
        padding: 25px;
        border-radius: 15px;
        text-align: center;
        margin: 15px 0;
        border: 2px solid rgba(255,255,255,0.1);
        background: rgba(255,255,255,0.05);
    }
    .score-text { font-size: 50px; font-weight: 900; margin: 5px 0; }
    
    /* News/Action Cards */
    .action-row { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 8px; border-left: 4px solid #39FF14; }
    </style>
    """, unsafe_allow_html=True)

# 3. ஹெடர்
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 5. டேட்டா லோடிங் செக்ஷன்
stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    # .info-வை நேரடியாக அழைப்பதற்கு முன் .fast_info செக் செய்வது நல்லது
    info = stock_obj.info
    if info and (info.get('symbol') or info.get('longName')):
        hist = stock_obj.history(period="1y")
        stock_loaded = True
except:
    stock_loaded = False

if stock_loaded:
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0

    # --- TAB 1: ANALYSIS ---
    with tabs[0]:
        st.markdown(f"#### {info.get('longName', u_input)}")
        st.metric(label="Price", value=f"₹{ltp:,.2f}")
        fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
        fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False)
        st.plotly_chart(fig, use_container_width=True)

    # --- TAB 2: SHAREHOLDING (FII/DII Split) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst_total = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst_total * 0.6)
        dii = inst_total - fii
        public = max(0, 100 - (promo + inst_total))
        
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, public], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
        fig_pie.update_layout(height=400, template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- TAB 3: ⭐ RATING (WORKING LOGIC) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Quality Rating Score', 'தர மதிப்பீடு (0-100)')}")
        
        # ஸ்கோர் கணக்கிடுதல்
        score = 0
        pe = info.get('trailingPE', 0)
        roe = info.get('returnOnEquity', 0)
        
        # கண்டிஷன் 1: P/E Ratio (குறைந்த P/E நல்லது)
        if 0 < pe < 25: score += 40
        elif 25 <= pe < 40: score += 20
        
        # கண்டிஷன் 2: ROE (அதிக ROE நல்லது)
        if roe > 0.18: score += 40
        elif roe > 0.12: score += 20
        
        # கண்டிஷன் 3: Trend (விலை 50 நாள் சராசரிக்கு மேல் இருந்தால்)
        if not hist.empty and ltp > hist['Close'].rolling(50).mean().iloc[-1]:
            score += 20

        color = "#39FF14" if score >= 70 else ("#ffd700" if score >= 40 else "#FF3131")
        verdict = get_text("STRONG BUY 🚀", "நிச்சயமாக வாங்கலாம் 🚀") if score >= 70 else (get_text("HOLD ⚖️", "வைத்திருக்கலாம் ⚖️") if score >= 40 else get_text("AVOID ⚠️", "தவிர்ப்பது நல்லது ⚠️"))
        
        st.markdown(f"""
            <div class="rating-card">
                <p class="score-text" style="color: {color};">{score} / 100</p>
                <p style="font-size: 22px; font-weight: bold; color: {color};">{verdict}</p>
            </div>
        """, unsafe_allow_html=True)
        st.write(f"📊 **ROE:** {roe*100:.2f}% | **P/E:** {pe if pe > 0 else 'N/A'}")

    # --- TAB 4: 📅 ACTIONS (WORKING LOGIC) ---
    with tabs[3]:
        st.markdown(f"### {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        try:
            # டிவிடெண்ட் மற்றும் போனஸ் விவரங்கள்
            acts = stock_obj.actions
            if not acts.empty:
                # சமீபத்திய 10 நிகழ்வுகளை மட்டும் காட்டுதல்
                st.dataframe(acts.tail(10).sort_index(ascending=False), use_container_width=True)
            else:
                st.info(get_text("No recent corporate actions found.", "சமீபத்திய நிகழ்வுகள் ஏதுமில்லை."))
        except Exception as e:
            st.error(get_text("Error fetching actions data.", "நிகழ்வுகளைப் பெறுவதில் பிழை."))

    # --- TAB 5: WATCHLIST ---
    with tabs[4]:
        st.markdown(f"### {get_text('My Watchlist', 'எனது வாட்ச்லிஸ்ட்')}")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        
        st.divider()
        if st.session_state['watchlist']:
            for item in st.session_state['watchlist']:
                cw1, cw2 = st.columns([5, 1])
                cw1.write(f"📌 **{item}**")
                if cw2.button("Remove", key=f"del_{item}"):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()
else:
    st.info("Loading Stock Data... (eg: TCS, RELIANCE)")

st.markdown("<p style='text-align:center;color:#444;font-size:12px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
