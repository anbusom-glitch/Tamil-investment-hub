import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# --- 1. பக்க அமைப்பு (Elite UI) ---
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# வாட்ச்லிஸ்ட் நினைவகம் (Session State)
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# தமிழ் மொழிபெயர்ப்பு
def translate_to_tamil(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:1000])
    except:
        return text

# ஸ்மார்ட் சர்ச்
def get_clean_ticker(user_val):
    mapping = {
        "RELIANCE": "RELIANCE.NS", "SBI": "SBIN.NS", "SBIN": "SBIN.NS",
        "COAL INDIA": "COALINDIA.NS", "TCS": "TCS.NS", "ITC": "ITC.NS",
        "HDFC": "HDFCBANK.NS", "INFOSYS": "INFY.NS",
        "ADANI": "ADANIENT.NS", "TATA MOTORS": "TATAMOTORS.NS"
    }
    val = user_val.strip().upper()
    if val in mapping: return mapping[val]
    if ".NS" not in val and ".BO" not in val: return f"{val}.NS"
    return val

# 2. லைவ் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    t_text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr_arrow = "🟢" if c >= 0 else "🔴"
            sym = t.replace(".NS", "").replace("^", "")
            t_text += f" | {sym}: <span style='color:white;'>₹{p:,.1f}</span> {clr_arrow} "
        except: continue
    return t_text

# 3. CSS
st.markdown("""
    <style>
    html, body, [class*="css"] { 
        font-size: 13.5px !important; 
        background-color: #0d1117; 
        color: #ffffff; 
    }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffffff; padding: 8px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    .header-text { 
        background: linear-gradient(90deg, #2ea043, #f85149); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent; 
        font-size: 28px !important; 
        font-weight: 800; 
        text-align: center; 
        margin-bottom: 5px; 
    }
    .created-by { 
        font-size: 11px !important; 
        color: #8b949e; 
        text-align: center; 
        margin-top: -8px; 
        margin-bottom: 20px; 
    }
    
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 10.5px !important; text-transform: uppercase; }
    .m-value { color: #ffffff !important; font-size: 17px !important; font-weight: bold; }
    
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffffff; }
    .news-title { color: #ffffff !important; font-size: 14.5px !important; font-weight: bold; text-decoration: none; }
    
    .stTabs [data-baseweb="tab"] {
        font-size: 12px !important;
        padding: 10px !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

sel_lang = st.radio("Choose Language / மொழி", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:50px; border-radius:10px;"></div>', unsafe_allow_html=True)

st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
st.markdown('<p class="created-by">created by somasundaram</p>', unsafe_allow_html=True)

# 4. தேடல்
u_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, Coal India)", value="SBI").upper()
ticker = get_clean_ticker(u_input)

stock_loaded = False
info = {}
stock_obj = None

try:
    with st.spinner('Loading...'):
        stock_obj = yf.Ticker(ticker)
        info = stock_obj.info
        if 'longName' in info:
            stock_loaded = True
except:
    pass

# 5. TABS (வாட்ச்லிஸ்டில் கண் ஐகான் நீக்கப்பட்டது)
if stock_loaded:
    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
        "📊 Analysis", "📝 Overview", "🤝 Shareholding", 
        "🔮 Forecast", "📅 Action", "🗞️ News", "Watchlist", "💼 Broker"
    ])

    with tab1:
        st.markdown(f"### {info.get('longName', ticker)}")
        
        # --- ADD BUTTON ---
        if st.button(f"Add {u_input} to Watchlist"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()

        ltp = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
        
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{info.get('priceToBook', 'N/A')}</span></div>
                <div style="text-align:right;"><span class="m-label">PEG Ratio</span><br><span class="m-value">{info.get('pegRatio', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        pd_s = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, key="main_chart")
        hist = stock_obj.history(period=pd_s, interval="1m" if pd_s=="1d" else "1d")
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'],
                                                increasing_line_color='#2ea043', decreasing_line_color='#f85149')])
            fig.update_layout(height=380, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        st.markdown("### 📝 Overview")
        desc_en = info.get('longBusinessSummary', 'தகவல் இல்லை.')
        if sel_lang == "Tamil":
            with st.spinner("தமிழில் மாற்றுகிறேன்..."):
                st.write(translate_to_tamil(desc_en))
        else: st.write(desc_en)

    with tab3:
        st.markdown("### 🤝 Shareholding Pattern")
        try:
            p_v = info.get('heldPercentInsiders', 0.5) * 100
            inst_v = info.get('heldPercentInstitutions', 0.3) * 100
            fig_p = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p_v, inst_v, 100-(p_v+inst_v)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
            fig_p.update_layout(height=240, margin=dict(l=0,r=0,t=10,b=10), legend=dict(orientation="h", y=-0.2))
            st.plotly_chart(fig_p, use_container_width=True)
        except: st.write("தகவல் இல்லை.")

    with tab4:
        st.markdown("### 🔮 Forecast")
        roe = info.get('returnOnEquity', 0)
        if roe > 0.15: st.success("Strong Fundamental 🚀")
        else: st.warning("Neutral Outlook ⚖️")
        st.write(f"ROE: {roe*100:.2f}%")

    with tab5:
        st.markdown("### 📅 Action (Dividends)")
        try:
            acts = stock_obj.actions.tail(10).sort_index(ascending=False)
            if not acts.empty:
                for date, row in acts.iterrows():
                    if row.get('Dividends', 0) > 0: st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{row.get('Dividends')}")
            else: st.write("தகவல் இல்லை.")
        except: pass

    with tab6:
        st.markdown("### 🗞️ News")
        try:
            for n in stock_obj.news[:10]:
                ts = n.get('providerPublishTime', 0)
                dt_s = datetime.fromtimestamp(ts).strftime('%d %b, %H:%M') if ts else "சமீபத்தில்"
                st.markdown(f'<div class="news-card"><a href="{n.get("link","#")}" target="_blank" class="news-title">{n.get("title","News")}</a><br><small>{n.get("publisher","Market")} • {dt_s}</small></div>', unsafe_allow_html=True)
        except: pass

    with tab7:
        st.markdown("### My Watchlist")
        if st.session_state['watchlist']:
            for item in st.session_state['watchlist']:
                col_name, col_del = st.columns([4, 1])
                col_name.markdown(f"📈 **{item}**")
                # --- REMOVE BUTTON ---
                if col_del.button("Delete 🗑️", key=f"del_{item}"):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()
        else:
            st.info("வாட்ச்லிஸ்ட் காலியாக உள்ளது.")

    with tab8:
        st.markdown("### 💼 Broker Connect")
        st.button("🔗 Connect Zerodha", use_container_width=True)
        st.button("🔗 Connect Angel One", use_container_width=True)

else:
    st.info("Loading Data...")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
