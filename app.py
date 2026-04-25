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
    if target_lang == "English": return text
    try:
        return GoogleTranslator(source='auto', target='ta').translate(text)
    except: return text

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# 2. பிரீமியம் UI ஸ்டைலிங்
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 14px !important; background-color: #0d1117; color: #ffffff; }
    
    .header-container { text-align: center; padding: 20px 0; margin-bottom: 10px; }
    .main-title { 
        font-size: 32px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { 
        font-size: 10px !important; color: #8b949e; text-transform: lowercase; 
        letter-spacing: 2px; margin-top: 2px; opacity: 0.7; font-weight: 400;
    }
    
    .metric-box {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between;
    }
    .m-label { color: #8b949e; font-size: 11px; font-weight: 700; text-transform: uppercase; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    
    /* செய்திகளுக்கான கார்டு அமைப்பு */
    .news-card {
        background: #1c2128; border-radius: 10px; padding: 15px; margin-bottom: 10px;
        border-left: 4px solid #39FF14; transition: 0.3s;
    }
    .news-card:hover { background: #21262d; }
    
    .stExpander { background: rgba(57, 255, 20, 0.05) !important; border: 1px solid #39FF14 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி தேர்வு மற்றும் தலைப்பு
col_top1, col_top2 = st.columns([7, 3])
with col_top2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

# 5. டேப்கள் (News 🗞️ சேர்க்கப்பட்டுள்ளது)
tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🗞️ {get_text('News', 'செய்திகள்')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. தரவுகளைப் பெறுதல்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")
    
    if info and 'symbol' in info:
        # --- பகுப்பாய்வு (Analysis) ---
        with tabs[0]:
            st.subheader(info.get('longName', u_input))
            m_data = [
                (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
                (get_text("Price", "விலை"), f"₹{info.get('currentPrice', 0):,.2f}"),
                (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
                (get_text("P/B Ratio", "பி.பி விகிதம்"), f"{info.get('priceToBook', 'N/A')}")
            ]
            for lbl, val in m_data:
                st.markdown(f'<div class="metric-box"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
            
            st.plotly_chart(go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])]).update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False), use_container_width=True)
            
            with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
                raw_summary = info.get('longBusinessSummary', 'No description.')
                st.write(translate_text(raw_summary, st.session_state['language']))

        # --- செய்திகள் (News 🗞️) ---
        with tabs[1]:
            st.markdown(f"### {get_text('Live News Feed', 'நேரலைச் செய்திகள்')}")
            news_list = stock_obj.news
            if news_list:
                for news in news_list[:6]: # முதல் 6 செய்திகள்
                    with st.container():
                        st.markdown(f"""
                            <div class="news-card">
                                <a href="{news['link']}" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration:none;">{news['title']}</a><br>
                                <small style="color:#8b949e;">{news['publisher']} | {datetime.fromtimestamp(news['providerPublishTime']).strftime('%Y-%m-%d')}</small>
                            </div>
                        """, unsafe_allow_html=True)
            else:
                st.info(get_text("No recent news found.", "சமீபத்திய செய்திகள் ஏதுமில்லை."))

        # --- Corporate Actions ---
        with tabs[2]:
            st.markdown(f"### {get_text('Corporate Actions', 'நிகழ்வுகள்')}")
            if not stock_obj.actions.empty:
                st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)
            else: st.info("No actions found.")

        # --- பங்குதாரர் (Shareholding) ---
        with tabs[3]:
            promo = (info.get('heldPercentInsiders') or 0) * 100
            inst = (info.get('heldPercentInstitutions') or 0) * 100
            fii = info.get('foreignInstitutionalHolders', inst * 0.6)
            dii = inst - fii
            pub = max(0, 100 - (promo + inst))
            st.plotly_chart(go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], hole=0.5)]).update_layout(height=400, template="plotly_dark"), use_container_width=True)

        # --- ரேட்டிங் (Rating) ---
        with tabs[4]:
            score = 0
            if 0 < info.get('trailingPE', 100) < 30: score += 50
            if info.get('returnOnEquity', 0) > 0.15: score += 50
            color = "#39FF14" if score >= 50 else "#FF3131"
            st.markdown(f'<div style="text-align:center; padding:30px; border:2px solid {color}; border-radius:15px;"><h1>Score: {score}/100</h1></div>', unsafe_allow_html=True)

        # --- வாட்ச்லிஸ்ட் (Watchlist) ---
        with tabs[5]:
            if st.button(f"➕ Add {u_input}"):
                if u_input not in st.session_state['watchlist']:
                    st.session_state['watchlist'].append(u_input)
                    st.rerun()
            for item in st.session_state['watchlist']:
                cw1, cw2 = st.columns([5, 1])
                cw1.info(f"📌 {item}")
                if cw2.button("❌", key=f"del_{item}"):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()

except Exception as e:
    st.error(get_text("Enter a valid Symbol.", "சரியான பங்கு குறியீட்டை உள்ளிடவும்."))

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
