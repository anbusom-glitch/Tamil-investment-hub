import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# --- 1. பக்க அமைப்பு ---
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# லோகோ உதவியாளர்
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# உறுதியான மொழிபெயர்ப்பு
def translate_to_tamil(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:1000])
    except:
        return text

# --- 2. ஸ்மார்ட் சர்ச் மேப்பிங் ---
def get_clean_ticker(user_val):
    mapping = {
        "RELIANCE": "RELIANCE.NS",
        "SBI": "SBIN.NS",
        "SBIN": "SBIN.NS",
        "COAL INDIA": "COALINDIA.NS",
        "TCS": "TCS.NS",
        "ITC": "ITC.NS",
        "HDFC": "HDFCBANK.NS",
        "INFOSYS": "INFY.NS",
        "ADANI": "ADANIENT.NS",
        "TATA MOTORS": "TATAMOTORS.NS"
    }
    val = user_val.strip().upper()
    if val in mapping:
        return mapping[val]
    if ".NS" not in val and ".BO" not in val:
        return f"{val}.NS"
    return val

# --- 3. லைவ் டிக்கர் ---
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS"]
    t_text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            t_text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return t_text

# --- 4. வடிவமைப்பு (CSS) ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .metric-box { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .m-label { color: #8b949e; font-size: 11px; }
    .m-value { color: #ffd700; font-size: 15px; font-weight: bold; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# முகப்பு மொழித் தேர்வு
sel_lang = st.radio("மொழியைத் தேர்ந்தெடுக்கவும் / Language", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:60px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# --- 5. டேட்டா தேடல் ---
u_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, Coal India)", value="SBI").upper()
ticker = get_clean_ticker(u_input)

try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    
    if 'longName' in info:
        # TABS (சரியான வரிசைமுறை)
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs([
            "📊 Analysis", "📝 Overview", "🤝 Shareholding", 
            "🔮 Forecast", "📅 Action", "🗞️ News", "👀 Watchlist", "💼 Broker"
        ])

        with tab1:
            st.markdown(f"### {info.get('longName', ticker)}")
            price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
            
            # மெட்ரிக்ஸ் (PE, PB, PEG, 52W High/Low)
            st.markdown(f"""
                <div class="metric-box">
                    <div><span class="m-label">விலை</span><br><span class="m-value">₹{price:,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
                </div>
                <div class="metric-box">
                    <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{info.get('priceToBook', 'N/A')}</span></div>
                    <div style="text-align:right;"><span class="m-label">PEG Ratio</span><br><span class="m-value">{info.get('pegRatio', 'N/A')}</span></div>
                </div>
                <div class="metric-box">
                    <div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
                </div>
            """, unsafe_allow_html=True)

            # கேண்டில் ஸ்டிக் சார்ட்
            pd_s = st.radio("கால அளவு", ["1d", "5d", "1mo", "1y"], horizontal=True)
            hist = stock_obj.history(period=pd_s, interval="1m" if pd_s=="1d" else "1d")
            
            if not hist.empty:
                fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'],
                                                    increasing_line_color='#2ea043', decreasing_line_color='#f85149')])
                fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown("### 📝 Overview")
            desc = info.get('longBusinessSummary', 'தகவல் இல்லை.')
            if sel_lang == "Tamil":
                with st.spinner("தமிழில் மாற்றுகிறேன்..."):
                    st.write(translate_to_tamil(desc))
            else: st.write(desc)

        with tab3:
            st.markdown("### 🤝 Shareholding")
            try:
                p_val = info.get('heldPercentInsiders', 0.5) * 100
                inst_val = info.get('heldPercentInstitutions', 0.3) * 100
                fig_p = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p_val, inst_val, 100-(p_val+inst_val)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
                fig_p.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0))
                st.plotly_chart(fig_p, use_container_width=True)
            except: st.write("தகவல் இல்லை.")

        with tab4:
            st.markdown("### 🔮 Forecast")
            roe = info.get('returnOnEquity', 0)
            if roe > 0.15: st.success("நல்ல அடிப்படை பலம் உள்ளது! 🚀")
            else: st.warning("நடுத்தரமான வளர்ச்சி. ⚖️")
            st.write(f"ROE: {roe*100:.2f}%")

        with tab5:
            st.markdown("### 📅 Action (Dividends)")
            acts = stock_obj.actions.tail(10).sort_index(ascending=False)
            if not acts.empty:
                for date, row in acts.iterrows():
                    if row.get('Dividends', 0) > 0:
                        st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{row.get('Dividends')}")
            else: st.write("தகவல் இல்லை.")

        with tab6:
            st.markdown("### 🗞️ News (நேரலைச் செய்திகள்)")
            try:
                news_items = stock_obj.news
                if news_items:
                    for n in news_items[:8]:
                        # பிழை வராமல் இருக்க .get() பயன்படுத்தப்பட்டுள்ளது
                        pts = n.get('providerPublishTime', 0)
                        dt = datetime.fromtimestamp(pts).strftime('%d %b, %H:%M') if pts else "சமீபத்திய"
                        st.markdown(f'<div class="news-card"><a href="{n.get("link","#")}" target="_blank" style="color:#ffd700; font-weight:bold; text-decoration:none;">{n.get("title","News")}</a><br><small>{n.get("publisher","Market")} • {dt}</small></div>', unsafe_allow_html=True)
                else: st.info("செய்திகள் இல்லை.")
            except: st.write("செய்திகளைப் பெற முடியவில்லை.")

        with tab7:
            st.markdown("### 👀 Watchlist")
            if st.button(f"➕ {u_input} வாட்ச்லிஸ்டில் சேர்க்க"):
                if u_input not in st.session_state['watchlist']:
                    st.session_state['watchlist'].append(u_input)
                    st.rerun()
            st.write(st.session_state['watchlist'])

        with tab8:
            st.markdown("### 💼 Broker")
            st.button("🔗 Connect Zerodha", use_container_width=True)
            st.button("🔗 Connect Angel One", use_container_width=True)

    else: st.warning("சரியான பெயரை உள்ளிடவும்.")
except Exception as e:
    st.info("தயவுசெய்து காத்திருக்கவும்... தரவுகள் லோடு ஆகின்றன.")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
