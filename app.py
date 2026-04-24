import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from translate import Translator

# 1. பக்க அமைப்பு
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# 2. உறுதியான மொழிபெயர்ப்பு வசதி
def safe_translate(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        # தமிழ் மொழிபெயர்ப்புக்கான செட்டிங்ஸ்
        translator = Translator(to_lang="ta", from_lang="en")
        # பெரிய பாராவை சிறியதாகப் பிரித்து மொழிபெயர்க்கும்
        translated = translator.translate(text[:500])
        return translated
    except Exception:
        return text # பிழை வந்தால் ஆங்கிலத்திலேயே காட்டும்

# 3. லைவ் மார்க்கெட் டிக்கர்
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS"]
    ticker_text = ""
    for t in indices:
        try:
            d = yf.Ticker(t).fast_info
            p, c = d['last_price'], d['year_change']*100
            clr = "#2ea043" if c >= 0 else "#f85149"
            sym = t.replace(".NS", "").replace("^", "")
            ticker_text += f" | {sym}: <span style='color:{clr};'>₹{p:,.1f}</span> "
        except: continue
    return ticker_text

# 4. பிரீமியம் மொபைல் வடிவமைப்பு (CSS)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .metric-row { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 10px; margin-bottom: 8px; display: flex; justify-content: space-between; }
    .m-label { color: #8b949e; font-size: 11px; }
    .m-value { color: #ffd700; font-size: 15px; font-weight: bold; }
    .news-card { background: #1c2128; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# 5. மேலடுக்கு டிக்கர்
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### செட்டிங்ஸ்")
    sel_lang = st.radio("மொழியைத் தேர்ந்தெடுக்கவும்", ["Tamil", "English"], horizontal=True)

logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:65px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 6. டேட்டா சேகரிப்பு
u_input = st.text_input("பங்கின் பெயரை உள்ளிடவும் (eg: SBI, TCS, Reliance)", value="TCS").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input else u_input

try:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    if 'longName' in info:
        # நீங்கள் கேட்ட புதிய வரிசை: Overview -> Forecast -> Analysis -> Holders -> Actions -> News
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📝 Overview", "🔮 Forecast", "📊 Analysis", "🤝 Holders", "📅 Actions", "🗞️ News"])

        with tab1:
            st.markdown(f"### 📝 {info.get('longName', ticker)}")
            raw_desc = info.get('longBusinessSummary', 'தகவல் இல்லை.')
            
            if sel_lang == "Tamil":
                with st.spinner("தமிழில் மொழிபெயர்க்கிறேன்..."):
                    tamil_desc = safe_translate(raw_desc)
                    st.write(tamil_desc)
            else:
                st.write(raw_desc)
            
            st.divider()
            c1, c2 = st.columns(2)
            c1.metric("Market Cap", f"₹{info.get('marketCap', 0)//10**7:,.0f} கோடி")
            c2.metric("Sector", info.get('sector', 'N/A'))

        with tab2:
            st.markdown("### 🔮 Forecast (எதிர்காலக் கணிப்பு)")
            roe = info.get('returnOnEquity', 0)
            if roe > 0.15:
                st.success("Strong Fundamental 🚀 (சிறப்பான எதிர்காலம்)")
            else:
                st.warning("Neutral / Watch Carefully ⚖️ (கவனிக்கவும்)")
            st.write(f"ROE (லாபத்திறன்): {roe*100:.2f}%")

        with tab3:
            st.markdown("### 📊 Analysis (ஆய்வு)")
            price = info.get('currentPrice', 0) or info.get('regularMarketPrice', 0)
            prev_close = info.get('regularMarketPreviousClose', price)
            
            # காம்பாக்ட் மெட்ரிக்ஸ்
            st.markdown(f"""
                <div class="metric-row">
                    <div><span class="m-label">விலை (LTP)</span><br><span class="m-value">₹{price:,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get('trailingPE', 'N/A')}</span></div>
                </div>
                <div class="metric-row">
                    <div><span class="m-label">52 வாரத் தாழ்வு</span><br><span class="m-value">₹{info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">52 வார உயர்வு</span><br><span class="m-value">₹{info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
                </div>
            """, unsafe_allow_html=True)

            pd_sel = st.radio("Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
            hist = stock.history(period=pd_sel, interval="1m" if pd_sel=="1d" else "1d")
            
            if not hist.empty:
                # கேண்டில் ஸ்டிக் கலர் லாஜிக்
                is_up = price >= prev_close
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index, open=hist['Open'], high=hist['High'],
                    low=hist['Low'], close=hist['Close'],
                    increasing_line_color='#2ea043', decreasing_line_color='#f85149'
                )])
                fig.update_layout(height=320, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
                st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

        with tab4:
            st.markdown("### 🤝 Holders (பங்குதாரர்கள்)")
            p = info.get('heldPercentInsiders', 0.5) * 100
            inst = info.get('heldPercentInstitutions', 0.3) * 100
            fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[p, inst, 100-(p+inst)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
            fig_pie.update_layout(height=300, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)

        with tab5:
            st.markdown("### 📅 Actions (நிகழ்வுகள்)")
            acts = stock.actions.tail(10).sort_index(ascending=False)
            if not acts.empty:
                for date, row in acts.iterrows():
                    d_val = row.get('Dividends', 0)
                    s_val = row.get('Stock Splits', 0)
                    if d_val > 0: st.info(f"📅 {date.strftime('%d %b %Y')} - Dividend: ₹{d_val}")
                    if s_val > 0: st.success(f"📅 {date.strftime('%d %b %Y')} - Split: {s_val}")
            else: st.write("தகவல்கள் இல்லை.")

        with tab6:
            st.markdown("### 🗞️ News (நேரலைச் செய்திகள்)")
            try:
                news_data = stock.news
                if news_data:
                    for n in news_data[:10]:
                        ptime = n.get('providerPublishTime', 0)
                        dt_str = datetime.fromtimestamp(ptime).strftime('%d %b, %H:%M') if ptime else ""
                        st.markdown(f"""
                            <div class="news-card">
                                <a href="{n.get('link','#')}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">{n.get('title','No Title')}</a><br>
                                <small style="color:#8b949e;">{n.get('publisher','Market News')} • {dt_str}</small>
                            </div>
                        """, unsafe_allow_html=True)
                else: st.info("செய்திகள் எதுவும் கிடைக்கவில்லை.")
            except: st.write("செய்திகளை லோடு செய்ய முடியவில்லை.")

    else: st.warning("சரியான பெயரை உள்ளிடவும் (eg: SBI, TCS).")
except Exception as e:
    st.info("காத்திருக்கவும்... தரவுகள் லோடு ஆகின்றன.")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
