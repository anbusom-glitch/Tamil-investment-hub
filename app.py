import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator
from datetime import datetime
import time

# 1. பக்க அமைப்பு
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

# 2. உயர் ரக UI ஸ்டைலிங்
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
    .m-value { color: #ffffff; font-size: 17px; font-weight: 800; }
    .news-card { background: #1c2128; border-radius: 10px; padding: 15px; margin-bottom: 10px; border-left: 4px solid #39FF14; }
    .stExpander { background: rgba(57, 255, 20, 0.05) !important; border: 1px solid #39FF14 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி தேர்வு மற்றும் தலைப்பு
col_t1, col_t2 = st.columns([7, 3])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 4. சர்ச் - ஸ்மார்ட் டிக்கர் லாஜிக்
u_input = st.text_input("Search Symbol (eg: RELIANCE)", value="RELIANCE").upper().strip()

if u_input:
    # டிக்கர் சரிசெய்தல்
    ticker = u_input if any(x in u_input for x in [".NS", ".BO", "^"]) else f"{u_input}.NS"

    # 5. டேப்கள்
    tabs = st.tabs([
        f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
        f"🗞️ {get_text('News', 'செய்திகள்')}",
        f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
        f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
        f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
        f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
    ])

    # 6. டேட்டா லோடிங் (Safe Loading)
    try:
        with st.spinner(get_text("Fetching Live Data...", "நேரலைத் தகவல்களைப் பெறுகிறேன்...")):
            stock_obj = yf.Ticker(ticker)
            # முக்கியமான தரவுகளை முதலில் எடுக்க முயற்சித்தல்
            hist = stock_obj.history(period="5d")
            
            if hist.empty:
                # NSE-ல் இல்லை என்றால் BSE-ல் தேட முயற்சித்தல்
                ticker = f"{u_input}.BO"
                stock_obj = yf.Ticker(ticker)
                hist = stock_obj.history(period="5d")

        if not hist.empty:
            info = stock_obj.info
            ltp = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]

            # --- Analysis ---
            with tabs[0]:
                st.subheader(info.get('longName', u_input))
                m_data = [
                    (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
                    (get_text("LTP", "விலை"), f"₹{ltp:,.2f}"),
                    (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
                    (get_text("P/B Ratio", "பி.பி விகிதம்"), f"{info.get('priceToBook', 'N/A')}")
                ]
                for lbl, val in m_data:
                    st.markdown(f'<div class="metric-box"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
                
                chart_data = stock_obj.history(period="1y")
                fig = go.Figure(data=[go.Candlestick(x=chart_data.index[-60:], open=chart_data['Open'], high=chart_data['High'], low=chart_data['Low'], close=chart_data['Close'])])
                fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
                st.plotly_chart(fig, use_container_width=True)
                
                with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
                    raw_summary = info.get('longBusinessSummary', 'No data.')
                    translated_summary = translate_text(raw_summary, st.session_state['language'])
                    st.markdown(f'<div style="line-height:1.8;">{translated_summary}</div>', unsafe_allow_html=True)

            # --- News ---
            with tabs[1]:
                st.markdown(f"### {get_text('Latest News', 'சமீபத்திய செய்திகள்')}")
                news_list = stock_obj.news
                if news_list:
                    for news in news_list[:5]:
                        st.markdown(f"""
                            <div class="news-card">
                                <a href="{news['link']}" target="_blank" style="color:#39FF14; font-weight:bold; text-decoration:none;">{news['title']}</a><br>
                                <small style="color:#8b949e;">{news['publisher']}</small>
                            </div>
                        """, unsafe_allow_html=True)
                else: st.info("No news found.")

            # --- Shareholding ---
            with tabs[2]:
                promo = (info.get('heldPercentInsiders') or 0) * 100
                inst = (info.get('heldPercentInstitutions') or 0) * 100
                fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, 100-(promo+inst)], hole=0.5)])
                st.plotly_chart(fig_pie.update_layout(height=400, template="plotly_dark"), use_container_width=True)

            # --- Rating ---
            with tabs[3]:
                pe = info.get('trailingPE', 100)
                score = 80 if pe < 30 else 45
                color = "#39FF14" if score > 70 else "#FF3131"
                st.markdown(f'<div style="text-align:center; padding:30px; border:2px solid {color}; border-radius:15px;"><h1>{score}/100</h1></div>', unsafe_allow_html=True)

            # --- Actions ---
            with tabs[4]:
                st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)

            # --- Watchlist ---
            with tabs[5]:
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
        else:
            st.error(get_text("Stock not found. Check if the market is open or symbol is correct.", "தகவல்கள் கிடைக்கவில்லை. குறியீட்டைச் சரிபார்க்கவும்."))

    except Exception as e:
        st.error(get_text("Could not fetch data. Try again in a few seconds.", "தகவல்களைப் பெறுவதில் சிக்கல். சற்று நேரத்தில் மீண்டும் முயலவும்."))

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
