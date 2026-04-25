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
    .sub-title { font-size: 11px !important; color: #8b949e; letter-spacing: 2px; opacity: 0.8; font-style: italic; margin-top: 5px; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff; font-size: 16px; font-weight: 800; }
    .stExpander { background: rgba(57, 255, 20, 0.05) !important; border: 1px solid #39FF14 !important; border-radius: 12px !important; margin-top: 15px; }
    
    /* Fundamental Card Styling */
    .f-card {
        background: rgba(0, 209, 255, 0.05); border: 1px solid #00D1FF;
        border-radius: 12px; padding: 15px; margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. லாகின் வசதி
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div style="background:#1c2128; padding:30px; border-radius:15px; max-width:400px; margin:auto; border:1px solid #30363d;">', unsafe_allow_html=True)
        u_id = st.text_input("User ID / Mobile")
        if st.button("Login 🚀", use_container_width=True):
            if u_id: st.session_state['is_logged_in'] = True; st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. மெயின் ஹெடர்
col_t1, col_t2 = st.columns([7, 3])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪", use_container_width=True): st.session_state['is_logged_in'] = False; st.rerun()

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE)", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. தரவு கையாளுதல்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info

    # --- Analysis Tab (Chart Removed, Fundamental Added) ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        
        # தற்போதைய விலை (LTP)
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)

        # 🚀 Fundamental Analysis Section
        st.markdown(f"### {get_text('Fundamental Analysis', 'அடிப்படை பகுப்பாய்வு')}")
        
        # 2 காலம்களாகப் பிரித்து முக்கிய விபரங்களைக் காட்டுதல்
        col1, col2 = st.columns(2)
        
        f_metrics_1 = [
            (get_text("Market Cap", "சந்தை மதிப்பு"), f"₹{info.get('marketCap', 0)/10000000:,.0f} Cr"),
            (get_text("P/E Ratio", "பி.இ விகிதம்"), info.get('trailingPE', 'N/A')),
            (get_text("P/B Ratio", "பி.பி விகிதம்"), info.get('priceToBook', 'N/A')),
            (get_text("ROE", "ஆர்.ஓ.இ"), f"{(info.get('returnOnEquity', 0)*100):.2f}%")
        ]
        
        f_metrics_2 = [
            (get_text("Debt to Equity", "கடனுக்கும் பங்கிற்கும் விகிதம்"), info.get('debtToEquity', 'N/A')),
            (get_text("Div. Yield", "டிவிடெண்ட் ஈல்டு"), f"{(info.get('dividendYield', 0)*100):.2f}%"),
            (get_text("Book Value", "புத்தக மதிப்பு"), f"₹{info.get('bookValue', 0):,.2f}"),
            (get_text("Sector", "துறை"), info.get('sector', 'N/A'))
        ]
        
        for lbl, val in f_metrics_1:
            col1.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
            
        for lbl, val in f_metrics_2:
            col2.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

        # நிறுவன விளக்கம் (About Us)
        with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
            raw_about = info.get('longBusinessSummary', 'தகவல்கள் ஏதுமில்லை.')
            st.write(translate_text(raw_about, st.session_state['language']))

    # --- Shareholding Tab ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, 100-(promo+inst)], hole=0.5, marker=dict(colors=['#58a6ff', '#f85149', '#39FF14', '#ffd700']))])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- Financials Tab ---
    with tabs[2]:
        st.markdown(f"### {get_text('Financial Statement', 'நிதிநிலை அறிக்கை')}")
        period = st.selectbox(get_text("Select Period", "காலம்"), ["Annual", "Quarterly"])
        try:
            fin_data = stock_obj.financials if period == "Annual" else stock_obj.quarterly_financials
            if not fin_data.empty:
                rev_idx = [i for i in fin_data.index if 'Revenue' in i or 'Sales' in i]
                prof_idx = [i for i in fin_data.index if 'Net Income' in i or 'Profit' in i]
                if rev_idx and prof_idx:
                    rev_values = fin_data.loc[rev_idx[0]]
                    prof_values = fin_data.loc[prof_idx[0]]
                    fig_fin = go.Figure()
                    fig_fin.add_trace(go.Bar(x=rev_values.index, y=rev_values.values, name=get_text('Revenue', 'வருவாய்'), marker_color='#00D1FF'))
                    fig_fin.add_trace(go.Scatter(x=prof_values.index, y=prof_values.values, name=get_text('Net Profit', 'நிகர லாபம்'), line=dict(color='#39FF14', width=4)))
                    fig_fin.update_layout(template="plotly_dark", height=400)
                    st.plotly_chart(fig_fin, use_container_width=True)
                st.dataframe(fin_data.head(10), use_container_width=True)
        except: st.info("Financial details not available.")

    # --- Rating Tab ---
    with tabs[3]:
        score = 80 if info.get('trailingPE', 100) < 30 else 50
        st.markdown(f'<div style="text-align:center; padding:40px; border:2px solid #39FF14; border-radius:15px;"><h1>{score}/100</h1></div>', unsafe_allow_html=True)

    # --- Watchlist Tab ---
    with tabs[4]:
        if st.button(f"➕ Add {u_input}", use_container_width=True):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        for item in st.session_state['watchlist']:
            c1, c2 = st.columns([5, 1])
            c1.info(f"📌 {item}")
            if c2.button("❌", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

except:
    st.error("சரியான பங்கு குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | created by somasundaram</p>", unsafe_allow_html=True)
