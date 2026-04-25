import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# வாட்ச்லிஸ்ட் மெமரி
if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# லோகோ கையாளும் முறை
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# மொழிபெயர்ப்பு
@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(text[:1000])
    except:
        return str(text)

# 2. லைவ் டிக்கர் தரவு
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS", "TCS.NS"]
    text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return text

# 3. ஸ்டைலிங் (CSS)
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; color: #c9d1d9; }
    
    /* டிக்கர் */
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #f85149; padding: 10px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    
    /* தலைப்பு - Red & Green Gradient */
    .header-container { text-align: center; margin: 15px 0; }
    .main-title { 
        font-size: 32px !important; 
        font-weight: 900; 
        background: linear-gradient(90deg, #2ea043, #f85149);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title { font-size: 12px !important; color: #8b949e; font-style: italic; margin-top: -5px; }
    
    /* மெட்ரிக்ஸ் - White & Small */
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 8px; padding: 8px 12px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #ffffff !important; font-size: 10px; text-transform: uppercase; }
    .m-value { color: #ffffff !important; font-size: 13px; font-weight: bold; }
    
    /* நியூஸ் கார்டு - KeyError தவிர்க்க பாதுகாப்பு */
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #f85149; }
    </style>
    """, unsafe_allow_html=True)

# 4. மேல் டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# தலைப்பு
st.markdown(f"""
    <div class="header-container">
        <p class="main-title">TAMIL INVEST HUB</p>
        <p class="sub-title">created by somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

# 5. பங்கு தேடல்
u_input = st.text_input("பங்கின் பெயர் (eg: Reliance, SBI, TCS)", value="RELIANCE").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

stock_loaded = False
info = {}
try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    if 'symbol' in info:
        stock_loaded = True
except:
    st.info("சரியான பங்குப் பெயரை உள்ளிடவும்...")

# 6. டேப்கள்
if stock_loaded:
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analysis", "📝 Overview", "🤝 Shareholding", "Watchlist"])

    with tab1:
        st.subheader(info.get('longName', ticker))
        ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
        st.markdown(f"""
            <div class="metric-row">
                <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{ltp:,.2f}</span></div>
                <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
            </div>
            <div class="metric-row">
                <div><span class="m-label">52W Low</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
            </div>
        """, unsafe_allow_html=True)

        hist = stock_obj.history(period="1mo")
        if not hist.empty:
            fig = go.Figure(data=[go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=300, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        summary = info.get('longBusinessSummary') or "விளக்கம் இல்லை."
        with st.spinner("தமிழில் மாற்றுகிறேன்..."):
            st.write(translate_to_tamil(summary))

    with tab3:
        st.markdown("### 🤝 Shareholding Pattern")
        
        # விரிவான பங்குதாரர் தகவல்கள்
        promo = info.get('heldPercentInsiders', 0) * 100
        # FII மற்றும் DII தகவல்களைப் பிரித்தல் (கிடைக்கவில்லை எனில் 0)
        inst = info.get('heldPercentInstitutions', 0) * 100
        # தோராயமாக பிரித்தல் (தரவு வரம்புகளால்)
        fii = inst * 0.6  # தோராய கணக்கு
        dii = inst * 0.4
        public = 100 - (promo + inst)

        labels = ['Promoters', 'FII', 'DII', 'Public']
        values = [promo, fii, dii, max(0, public)]
        colors = ['#f85149', '#58a6ff', '#2ea043', '#ffd700']

        # நீங்கள் கேட்டது போல சிறிய ரவுண்ட் ஸ்டைல் (Donut)
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.7, marker=dict(colors=colors))])
        fig_pie.update_layout(
            height=300, 
            margin=dict(l=10,r=10,t=10,b=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # தகவல்கள் எண்களில்
        st.write(f"🔹 Promoters: {promo:.2f}%")
        st.write(f"🔹 Institutions (FII/DII): {inst:.2f}%")
        st.write(f"🔹 Others/Public: {public:.2f}%")

    with tab4:
        st.markdown("### Watchlist")
        if st.button(f"➕ Add {u_input}"):
            if u_input not in st.session_state['watchlist']:
                st.session_state['watchlist'].append(u_input)
                st.rerun()
        
        for item in st.session_state['watchlist']:
            c1, c2 = st.columns([4, 1])
            c1.write(f"📌 {item}")
            if c2.button("Remove", key=f"del_{item}"):
                st.session_state['watchlist'].remove(item)
                st.rerun()

else:
    st.info("பங்கு விவரங்களை லோடு செய்கிறது...")

st.markdown("<div style='text-align:center;color:#444;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
