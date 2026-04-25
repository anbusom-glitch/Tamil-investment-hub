import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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
    
    .header-container { text-align: center; padding: 20px 0; margin-bottom: 10px; }
    .main-title { 
        font-size: 35px !important; font-weight: 800; margin-bottom: 0px;
        background: linear-gradient(90deg, #39FF14, #00D1FF, #FF3131);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    }
    .sub-title { 
        font-size: 12px !important; color: #8b949e; text-transform: lowercase; 
        letter-spacing: 2px; margin-top: 5px; opacity: 0.8; font-weight: 400;
        font-style: italic;
    }
    
    .metric-row {
        background: #161b22; border: 1px solid #30363d; border-radius: 12px;
        padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;
        box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    }
    .m-label { color: #8b949e !important; font-size: 10px; text-transform: uppercase; font-weight: 700; }
    .m-value { color: #ffffff !important; font-size: 17px; font-weight: 800; }
    
    .login-card { background: #1c2128; border: 1px solid #30363d; border-radius: 15px; padding: 30px; max-width: 450px; margin: auto; }
    .stExpander { background: rgba(57, 255, 20, 0.05) !important; border: 1px solid #39FF14 !important; border-radius: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 3. லாகின் வசதி
if not st.session_state['is_logged_in']:
    st.markdown('<div class="header-container"><p class="main-title">TAMIL INVEST HUB</p></div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="login-card">', unsafe_allow_html=True)
        st.subheader("Login / உள்நுழைக")
        st.text_input("Email or Mobile")
        st.text_input("Password", type="password")
        if st.button("Sign In 🚀", use_container_width=True):
            st.session_state['is_logged_in'] = True
            st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# 4. மெயின் ஆப் ஹெடர்
col_t1, col_t2 = st.columns([7, 3])
with col_t2:
    st.session_state['language'] = st.radio("Lang", ["Tamil", "English"], horizontal=True, label_visibility="collapsed")
    if st.button("Logout 🚪"):
        st.session_state['is_logged_in'] = False
        st.rerun()

st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. சர்ச்
u_input = st.text_input("Search Symbol", value="RELIANCE").upper().strip()
ticker = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

tabs = st.tabs([
    f"📊 {get_text('Analysis', 'பகுப்பாய்வு')}", 
    f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}", 
    f"⭐ {get_text('Rating', 'ரேட்டிங்')}", 
    f"📌 {get_text('Watchlist', 'வாட்ச்லிஸ்ட்')}"
])

# 6. தரவு கையாளுதல்
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")

    if not hist.empty:
        # Analysis Tab
        with tabs[0]:
            st.subheader(info.get('longName', ticker))
            
            # Metric Rows
            ltp = info.get('currentPrice') or info.get('regularMarketPrice') or hist['Close'].iloc[-1]
            st.markdown(f'<div class="metric-row"><span class="m-label">LTP (விலை)</span><span class="m-value">₹{ltp:,.2f}</span></div>', unsafe_allow_html=True)
            
            m_list = [
                (get_text("Sector", "துறை"), info.get('sector', 'N/A')),
                (get_text("52W High", "52 வார உச்சம்"), f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}"),
                (get_text("52W Low", "52 வார வீழ்ச்சி"), f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}"),
                (get_text("P/B Ratio", "பி.பி விகிதம்"), f"{info.get('priceToBook', 'N/A')}")
            ]
            for lbl, val in m_list:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

            # சார்ட்
            fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=400, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

            with st.expander(get_text("About Company ⬇️", "நிறுவனத்தைப் பற்றி ⬇️")):
                st.write(info.get('longBusinessSummary', 'No data.'))

        # Shareholding Tab
        with tabs[1]:
            promo = (info.get('heldPercentInsiders') or 0) * 100
            st.plotly_chart(go.Figure(data=[go.Pie(labels=['Promoters', 'Public'], values=[promo, 100-promo], hole=0.5)]).update_layout(template="plotly_dark"), use_container_width=True)

        # Rating Tab
        with tabs[2]:
            score = 85 if info.get('trailingPE', 100) < 30 else 55
            st.markdown(f'<div style="text-align:center; padding:30px; border:2px solid #39FF14; border-radius:15px;"><h1>{score}/100</h1></div>', unsafe_allow_html=True)

        # Watchlist Tab
        with tabs[3]:
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
    else:
        st.error("Data not available for this symbol.")

except Exception as e:
    st.error("சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<p style='text-align:center; color:#444; margin-top:50px;'>© 2026 TAMIL INVEST HUB PRO</p>", unsafe_allow_html=True)
