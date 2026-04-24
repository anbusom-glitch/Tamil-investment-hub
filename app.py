import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from translate import Translator

# --- 1. PAGE SETUP ---
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# --- 2. ROBUST TRANSLATION (தமிழில் உறுதியாக வர) ---
def get_tamil_translation(text):
    if not text or len(text) < 5: 
        return "தகவல் இல்லை."
    try:
        # MyMemory API வழியாக தமிழுக்கு மாற்றுகிறது
        translator = Translator(to_lang="ta", from_lang="en")
        # பெரிய தகவலைப் பிரித்து மொழிபெயர்க்கிறது
        translation = translator.translate(text[:500])
        return translation
    except:
        return f"மொழிபெயர்ப்புத் தோல்வி. ஆங்கிலத் தகவல்: \n\n {text}"

# --- 3. LIVE TICKER ---
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

# --- 4. PREMIUM CSS ---
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; }
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .m-value { color: #ffd700; font-size: 15px; font-weight: bold; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# UI Elements
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### ⚙️ Settings")
    sel_lang = st.radio("Language / மொழி", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:60px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# --- 5. DATA LOADING ---
u_input = st.text_input("Enter Stock Name (eg: Reliance, SBI, TCS)", value="TCS").upper()
t_symbol = f"{u_input}.NS" if ".NS" not in u_input else u_input

try:
    stock_obj = yf.Ticker(t_symbol)
    s_info = stock_obj.info
    
    if 'longName' in s_info:
        # TAB ORDER: 1.Analysis, 2.Overview, 3.Shareholding, 4.Forecast, 5.Action, 6.News
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📊 Analysis", "📝 Overview", "🤝 Shareholding", "🔮 Forecast", "📅 Action", "🗞️ News"])

        with tab1:
            st.markdown(f"### 📊 Analysis - {s_info.get('longName', t_symbol)}")
            ltp = s_info.get('currentPrice', 0) or s_info.get('regularMarketPrice', 0)
            
            # --- PE, PB, PEG, 52W High/Low ---
            st.markdown(f"""
                <div class="metric-row">
                    <div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{ltp:,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{s_info.get('trailingPE', 'N/A')}</span></div>
                </div>
                <div class="metric-row">
                    <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{s_info.get('priceToBook', 'N/A')}</span></div>
                    <div style="text-align:right;"><span class="m-label">PEG Ratio</span><br><span class="m-value">{s_info.get('pegRatio', 'N/A')}</span></div>
                </div>
                <div class="metric-row">
                    <div><span class="m-label">52W Low (தாழ்வு)</span><br><span class="m-value">₹{s_info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">52W High (உயர்வு)</span><br><span class="m-value">₹{s_info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
                </div>
            """, unsafe_allow_html=True)

            # Candlestick Chart
            pd_s = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
            hist = stock_obj.history(period=pd_s, interval="1m" if pd_s=="1d" else "1d")
            
            if not hist.empty:
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index, open=hist['Open'], high=hist['High'],
                    low=hist['Low'], close=hist['Close'],
                    increasing_line_color='#2ea043', decreasing_line_color='#f85149'
                )])
                fig.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
                st.markdown("<p style='text-align:center; font-size:10px; color:#8b949e;'>நன்றி - TAMIL INVEST HUB</p>", unsafe_allow_html=True)

        with tab2:
            st.markdown("### 📝 Overview (நிறுவனத் தகவல்)")
            desc_en = s_info.get('longBusinessSummary', 'தகவல் இல்லை.')
            if sel_lang == "Tamil":
                with st.spinner("தமிழில் மொழிபெயர்க்கிறேன்..."):
                    st.write(get_tamil_translation(desc_en))
            else:
                st.write(desc_en)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Market Cap", f"₹{s_info.get('marketCap', 0)//10**7:,.0f} Cr")
            c2.metric("Sector", s_info.get('sector', 'N/A'))

        with tab3:
            st.markdown("### 🤝 Shareholding Pattern")
            p_val = s_info.get('heldPercentInsiders', 0.5) * 100
            inst_val = s_info.get('heldPercentInstitutions', 0.3) * 100
            fig_p = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p_val, inst_val, 100-(p_val+inst_val)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
            fig_p.update_layout(height=350, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_p, use_container_width=True)

        with tab4:
            st.markdown("### 🔮 Forecast (கணிப்பு)")
            roe = s_info.get('returnOnEquity', 0)
            if roe > 0.15: st.success("Strong Fundamental Strength 🚀")
            else: st.warning("Neutral Growth Outlook ⚖️")
            st.write(f"ROE: {roe*100:.2f}%")

        with tab5:
            st.markdown("### 📅 Action (நிகழ்வுகள்)")
            acts = stock_obj.actions.tail(10).sort_index(ascending=False)
            if not acts.empty:
                for d, r in acts.iterrows():
                    d_amt = r.get('Dividends', 0)
                    s_amt = r.get('Stock Splits', 0)
                    if d_amt > 0: st.info(f"📅 {d.strftime('%d %b %Y')} - Dividend: ₹{d_amt}")
                    if s_amt > 0: st.success(f"📅 {d.strftime('%d %b %Y')} - Split: {s_amt}")
            else: st.write("நிகழ்வுகள் எதுவும் இல்லை.")

        with tab6:
            st.markdown("### 🗞️ News (நேரலைச் செய்திகள்)")
            try:
                n_feed = stock_obj.news
                if n_feed:
                    for n in n_feed[:10]:
                        ts = n.get('providerPublishTime', 0)
                        dt_s = datetime.fromtimestamp(ts).strftime('%d %b, %H:%M') if ts else ""
                        st.markdown(f"""
                            <div class="news-card">
                                <a href="{n.get('link','#')}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">{n.get('title','News Title')}</a><br>
                                <small style="color:#8b949e;">{n.get('publisher','Market')} • {dt_s}</small>
                            </div>
                        """, unsafe_allow_html=True)
                else: st.info("செய்திகள் இல்லை.")
            except: st.write("செய்திகளைப் பெற முடியவில்லை.")

    else: st.warning("சரியான பெயரை உள்ளிடவும்.")
except Exception as e:
    st.info("தரவுகள் லோடு ஆகின்றன (Loading)...")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
