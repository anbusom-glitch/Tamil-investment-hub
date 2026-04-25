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
u_input = st.text_input("Search Symbol (eg: TCS, RELIANCE)", value="TCS").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"💰 {get_text('Financials', 'நிதிநிலை')}",
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}",
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. தரவு கையாளுதல் (Safe Loading)
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")

    # --- Analysis Tab ---
    with tabs[0]:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or (hist['Close'].iloc[-1] if not hist.empty else 0)
        m_list = [
            (get_text("Price", "விலை"), f"₹{ltp:,.2f}"),
            (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
            (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}")
        ]
        for lbl, val in m_list:
            st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
        
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    # --- Shareholding Tab ---
    with tabs[1]:
        st.markdown(f"### {get_text('Shareholding Pattern', 'பங்குதாரர் விபரம்')}")
        promo = (info.get('heldPercentInsiders') or 0) * 100
        inst = (info.get('heldPercentInstitutions') or 0) * 100
        fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[promo, inst, 100-(promo+inst)], hole=0.5, marker=dict(colors=['#58a6ff', '#39FF14', '#ffd700']))])
        st.plotly_chart(fig_pie.update_layout(template="plotly_dark", height=400), use_container_width=True)

    # --- Financials Tab (Protected against KeyErrors) ---
    with tabs[2]:
        st.markdown(f"### {get_text('Financial Statement', 'நிதிநிலை அறிக்கை')}")
        period = st.selectbox(get_text("Select Period", "காலம்"), ["Annual", "Quarterly"])
        
        try:
            fin_data = stock_obj.financials if period == "Annual" else stock_obj.quarterly_financials
            if not fin_data.empty:
                # சாத்தியமான பெயர்களைத் தேடுதல்
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
                
                st.markdown(f"#### {get_text('Data Table', 'தரவு அட்டவணை')}")
                st.dataframe(fin_data.head(10), use_container_width=True)
            else:
                st.info("Financial data not available.")
        except:
            st.info("காலாண்டு தரவுகள் தற்போது கிடைக்கவில்லை.")

    # --- Rating Tab ---
    with tabs[3]:
        score = 85 if (info.get('trailingPE', 100) < 30) else 55
        color = "#39FF14" if score > 70 else "#FF3131"
        st.markdown(f'<div style="text-align:center; padding:40px; border:2px solid {color}; border-radius:15px;"><h1>{score}/100</h1></div>', unsafe_allow_html=True)

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

except Exception as e:
    st.error("சரியான பங்கு குறியீட்டை (Symbol) உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO | created by somasundaram</p>", unsafe_allow_html=True)
