import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'is_logged_in' not in st.session_state: st.session_state['is_logged_in'] = False
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
    .header-container { text-align: center; padding: 15px 0; margin-bottom: 10px; }
    .main-title { 
        font-size: 35px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 11px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.8; font-style: italic; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    .stExpander { background: rgba(57, 255, 20, 0.05) !important; border: 1px solid #39FF14 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. லாகின்
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.text_input("User ID")
        if st.button("Login 🚀"): 
            st.session_state['is_logged_in'] = True
            st.rerun()
    st.stop()

# 4. மெயின் ஹெடர்
col_t1, col_t2 = st.columns([7, 3])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE)", value="TCS").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. டேட்டா ஹேண்ட்லிங்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")

    # --- ANALYSIS ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
        m_list = [
            (get_text("LTP", "விலை"), f"₹{ltp:,.2f}"),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
            (get_text("P/B Ratio", "பி.பி விகிதம்"), f"{info.get('priceToBook', 'N/A')}")
        ]
        for lbl, val in m_list:
            st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
        
        st.plotly_chart(go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])]).update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False), use_container_width=True)
        
        with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
            raw_about = info.get('longBusinessSummary', 'No data.')
            st.write(translate_text(raw_about, st.session_state['language']))

    # --- SHAREHOLDING (FII/DII Split) ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fii = info.get('foreignInstitutionalHolders', inst * 0.6) # Approximation if precise split hidden
        dii = inst - fii
        pub = max(0, 100 - (promo + inst))
        
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'FII', 'DII', 'Public'], values=[promo, fii, dii, pub], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark"), use_container_width=True)

    # --- FINANCIALS (Growth & Profit Graph) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Annual Growth & Profit', 'ஆண்டு வளர்ச்சி மற்றும் லாபம்')}")
        fin = stock_obj.financials
        if not fin.empty:
            revenue = fin.loc['Total Revenue'] if 'Total Revenue' in fin.index else pd.Series()
            profit = fin.loc['Net Income'] if 'Net Income' in fin.index else pd.Series()
            
            fig_fin = go.Figure()
            fig_fin.add_trace(go.Bar(x=revenue.index, y=revenue.values, name='Revenue'))
            fig_fin.add_trace(go.Scatter(x=profit.index, y=profit.values, name='Net Profit', line=dict(color='#39FF14', width=3)))
            fig_fin.update_layout(template="plotly_dark", height=400)
            st.plotly_chart(fig_fin, use_container_width=True)
        else:
            st.info("Financial data not available.")

    # --- CORPORATE ACTIONS ---
    with tabs[3]:
        st.markdown(f"### {get_text('Dividends & Splits', 'டிவிடெண்ட் மற்றும் போனஸ்')}")
        if not stock_obj.actions.empty:
            st.dataframe(stock_obj.actions.tail(10).sort_index(ascending=False), use_container_width=True)
        else:
            st.info("No recent actions.")

    # --- WATCHLIST ---
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
