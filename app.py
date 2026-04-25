import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from datetime import datetime

# 1. பக்க அமைப்பு மற்றும் செஷன்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state: st.session_state['watchlist'] = []
if 'language' not in st.session_state: st.session_state['language'] = "Tamil"

# மொழிபெயர்ப்பு உதவியாளர்
@st.cache_data(show_spinner=False)
def translate_text(text, target_lang):
    if not text or target_lang == "English": return text
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except: return text

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. உயர் ரக UI
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    .header-container { text-align: center; padding: 15px 0; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 10px !important; color: #8b949e; letter-spacing: 2px; margin-top: 2px; opacity: 0.7; }
    .metric-box { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    .stExpander { background: rgba(57, 255, 20, 0.05) !important; border: 1px solid #39FF14 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி தேர்வு
col_t1, col_t2 = st.columns([7, 3])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol (eg: RELIANCE)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

# 5. டேப்கள் (News டேப் நீக்கப்பட்டுள்ளது)
tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. தரவுகளைப் பெறுதல்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")

    # --- Analysis Tab ---
    with tabs[0]:
        try:
            st.subheader(info.get('longName', ticker))
            ltp = info.get('currentPrice') or info.get('regularMarketPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
            
            m_data = [
                (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
                (get_text("LTP", "விலை"), f"₹{ltp:,.2f}"),
                (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
                (get_text("P/B Ratio", "பி.பி விகிதம்"), f"{info.get('priceToBook', 'N/A')}")
            ]
            for lbl, val in m_data:
                st.markdown(f'<div class="metric-box"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
            
            if not hist.empty:
                fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
                fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True)
            
            with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
                summary = info.get('longBusinessSummary', 'No data.')
                st.write(translate_text(summary, st.session_state['language']))
        except: st.error("Analysis loading error.")

    # --- Shareholding Tab (FII/DII விபரங்களுடன்) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        try:
            promo = (info.get('heldPercentInsiders') or 0) * 100
            inst_total = (info.get('heldPercentInstitutions') or 0) * 100
            
            # FII/DII பிரிப்பு
            fii = info.get('foreignInstitutionalHolders', inst_total * 0.6)
            if fii > inst_total: fii = inst_total * 0.6
            dii = inst_total - fii
            public = max(0, 100 - (promo + inst_total))

            fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, public], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
            fig_pie.update_layout(height=400, template="plotly_dark")
            st.plotly_chart(fig_pie, use_container_width=True)
            
            st.write(f"🔹 Promoters: **{promo:.2f}%** | 🔹 FII: **{fii:.2f}%**")
            st.write(f"🔹 DII: **{dii:.2f}%** | 🔹 Public: **{public:.2f}%**")
        except: st.info("Shareholding data error.")

    # --- Rating ---
    with tabs[2]:
        score = 80 if (info.get('trailingPE', 100) < 30) else 50
        st.markdown(f'<div style="text-align:center; padding:30px; border:2px solid #39FF14; border-radius:15px;"><h1>Score: {score}/100</h1></div>', unsafe_allow_html=True)

    # --- Actions ---
    with tabs[3]:
        try: st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)
        except: st.info("No actions found.")

    # --- Watchlist ---
    with tabs[4]:
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        for item in st.session_state['watchlist']:
            c1, c2 = st.columns([5, 1])
            c1.info(f"📌 {item}")
            if c2.button("❌", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

except Exception as e:
    st.error("சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
