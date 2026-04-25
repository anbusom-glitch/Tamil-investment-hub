import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

# மொழிபெயர்ப்பு உதவியாளர்
@st.cache_data(show_spinner=False)
def translate_text(text, target_lang):
    if target_lang == "English":
        return text
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except:
        return text

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
    .metric-box {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between;
    }
    .m-label { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    
    /* Expandable About Box Styling */
    .stExpander {
        background: rgba(57, 255, 20, 0.05) !important;
        border: 1px solid #39FF14 !important;
        border-radius: 12px !important;
        margin-top: 15px !important;
    }
    .about-content {
        line-height: 1.8; font-size: 15px; padding: 10px; color: #e6edf3;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி மற்றும் தலைப்பு
col_l1, col_l2 = st.columns([7, 3])
with col_l2:
    lang_choice = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    st.session_state['language'] = lang_choice

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

# 5. தரவுகளைப் பெறுதல்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")
    
    if info and 'symbol' in info:
        # --- பகுப்பாய்வு பகுதி (TAB 1) ---
        with tabs[0]:
            st.subheader(info.get('longName', u_input))
            
            # மெட்ரிக்ஸ்
            m_data = [
                (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
                (get_text("LTP", "தற்போதைய விலை"), f"₹{info.get('currentPrice', 0):,.2f}"),
                (get_text("52 Week High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
                (get_text("P/B Ratio", "பி.பி விகிதம்"), f"{info.get('priceToBook', 'N/A')}")
            ]
            
            for lbl, val in m_data:
                st.markdown(f'<div class="metric-box"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
            
            st.plotly_chart(go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])]).update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False), use_container_width=True)
            
            # --- புதிய மாற்றப்பட்ட பகுதி: விரிவடையும் நிறுவன விளக்கம் ---
            about_label = get_text("Click to read About Company ⬇️", "நிறுவனத்தைப் பற்றி படிக்க இங்கே தொடவும் ⬇️")
            with st.expander(about_label):
                raw_summary = info.get('longBusinessSummary', 'No description available.')
                with st.spinner(get_text("Translating...", "மொழிபெயர்க்கிறேன்...")):
                    translated_summary = translate_text(raw_summary, st.session_state['language'])
                    st.markdown(f'<div class="about-content">{translated_summary}</div>', unsafe_allow_html=True)

        # --- பங்குதாரர் பகுதி (TAB 2) ---
        with tabs[1]:
            promo = (info.get('heldPercentInsiders') or 0) * 100
            inst = (info.get('heldPercentInstitutions') or 0) * 100
            fii = info.get('foreignInstitutionalHolders', inst * 0.6)
            dii = inst - fii
            pub = max(0, 100 - (promo + inst))
            st.plotly_chart(go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], hole=0.5)]).update_layout(height=400, template="plotly_dark"), use_container_width=True)

        # --- ரேட்டிங் பகுதி (TAB 3) ---
        with tabs[2]:
            score = 0
            pe = info.get('trailingPE', 0)
            roe = info.get('returnOnEquity', 0)
            if 0 < pe < 30: score += 50
            if roe > 0.15: score += 50
            color = "#39FF14" if score >= 50 else "#FF3131"
            st.markdown(f'<div style="text-align:center; padding:30px; border:2px solid {color}; border-radius:15px;"><h1>Score: {score}/100</h1></div>', unsafe_allow_html=True)

        # --- வாட்ச்லிஸ்ட் பகுதி (TAB 4) ---
        with tabs[3]:
            if st.button(f"➕ Add {u_input}"):
                if u_input not in st.session_state['watchlist']:
                    st.session_state['watchlist'].append(u_input)
                    st.rerun()
            for item in st.session_state['watchlist']:
                c1, c2 = st.columns([5, 1])
                c1.info(f"📌 {item}")
                if c2.button("❌", key=item):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()

except Exception as e:
    st.error(get_text("Enter a valid Stock Symbol.", "சரியான பங்கு குறியீட்டை உள்ளிடவும்."))

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
