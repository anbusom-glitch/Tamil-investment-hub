import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from translate import Translator

# 1. Page Configuration
st.set_page_config(page_title="TAMIL INVEST HUB", page_icon="🏦", layout="wide")

# Helper to load logo
def get_base64_logo(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except: return None

# Safe Translation Function
def safe_translate(text):
    if not text or len(text) < 5: return "தகவல் இல்லை."
    try:
        translator = Translator(to_lang="ta", from_lang="en")
        # Translating first 450 characters for stability
        return translator.translate(text[:450])
    except:
        return text

# 2. Live Ticker Data
def get_ticker_text():
    indices = ["^NSEI", "^BSESN", "RELIANCE.NS", "SBIN.NS"]
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

# 3. Premium CSS Styling
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 12.5px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #ffd700; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 35s linear infinite; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .header-text { background: linear-gradient(90deg, #ffd700, #b8860b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 10px; padding: 12px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #8b949e; font-size: 11px; text-transform: uppercase; }
    .m-value { color: #ffd700; font-size: 15px; font-weight: bold; }
    .news-card { background: #161b22; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 4px solid #ffd700; }
    </style>
    """, unsafe_allow_html=True)

# Top Marquee Ticker
st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("### ⚙️ Settings")
    sel_lang = st.radio("Choose Language / மொழி", ["Tamil", "English"], horizontal=True)

# Logo & Header
logo_b = get_base64_logo("logo.png")
if logo_b:
    st.markdown(f'<div style="text-align:center;"><img src="data:image/png;base64,{logo_b}" style="width:60px; border-radius:12px;"></div>', unsafe_allow_html=True)
st.markdown('<p class="header-text">TAMIL INVEST HUB</p>', unsafe_allow_html=True)

# 4. Search & Data Fetch
u_input = st.text_input("Enter Stock Name (eg: Reliance, SBI, TCS)", value="TCS").upper()
ticker_sym = f"{u_input}.NS" if ".NS" not in u_input else u_input

try:
    stock_obj = yf.Ticker(ticker_sym)
    s_info = stock_obj.info
    
    if 'longName' in s_info:
        # User Requested Tab Order: 1.Analysis, 2.Overview, 3.Shareholding, 4.Forecast, 5.Action, 6.News
        t1, t2, t3, t4, t5, t6 = st.tabs(["📊 Analysis", "📝 Overview", "🤝 Shareholding", "🔮 Forecast", "📅 Action", "🗞️ News"])

        with t1:
            st.markdown(f"### {s_info.get('longName', ticker_sym)}")
            ltp = s_info.get('currentPrice', 0) or s_info.get('regularMarketPrice', 0)
            
            # Fundamentals Row 1
            st.markdown(f"""
                <div class="metric-row">
                    <div><span class="m-label">LTP (விலை)</span><br><span class="m-value">₹{ltp:,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">P/E Ratio</span><br><span class="m-value">{s_info.get('trailingPE', 'N/A')}</span></div>
                </div>
            """, unsafe_allow_html=True)
            
            # Fundamentals Row 2 (Missing items added)
            st.markdown(f"""
                <div class="metric-row">
                    <div><span class="m-label">P/B Ratio</span><br><span class="m-value">{s_info.get('priceToBook', 'N/A')}</span></div>
                    <div style="text-align:right;"><span class="m-label">PEG Ratio</span><br><span class="m-value">{s_info.get('pegRatio', 'N/A')}</span></div>
                </div>
            """, unsafe_allow_html=True)

            # Fundamentals Row 3
            st.markdown(f"""
                <div class="metric-row">
                    <div><span class="m-label">52W Low</span><br><span class="m-value">₹{s_info.get('fiftyTwoWeekLow', 0):,.1f}</span></div>
                    <div style="text-align:right;"><span class="m-label">52W High</span><br><span class="m-value">₹{s_info.get('fiftyTwoWeekHigh', 0):,.1f}</span></div>
                </div>
            """, unsafe_allow_html=True)

            # Candlestick Chart
            p_sel = st.radio("Select Period", ["1d", "5d", "1mo", "1y"], horizontal=True, label_visibility="collapsed")
            hist_data = stock_obj.history(period=p_sel, interval="1m" if p_sel=="1d" else "1d")
            
            if not hist_data.empty:
                fig_chart = go.Figure(data=[go.Candlestick(
                    x=hist_data.index, open=hist_data['Open'], high=hist_data['High'],
                    low=hist_data['Low'], close=hist_data['Close'],
                    increasing_line_color='#2ea043', decreasing_line_color='#f85149'
                )])
                fig_chart.update_layout(height=350, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_rangeslider_visible=False)
                st.plotly_chart(fig_chart, use_container_width=True, config={'displayModeBar': False})
                st.markdown("<p style='text-align:center; font-size:10px; color:#8b949e;'>நன்றி - TAMIL INVEST HUB</p>", unsafe_allow_html=True)

        with t2:
            st.markdown("### 📝 Overview (நிறுவனத் தகவல்)")
            b_desc = s_info.get('longBusinessSummary', 'No description.')
            if sel_lang == "Tamil":
                with st.spinner("தமிழில் மாற்றுகிறேன்..."):
                    st.write(safe_translate(b_desc))
            else:
                st.write(b_desc)
            
            st.divider()
            ca, cb = st.columns(2)
            ca.metric("Market Cap", f"₹{s_info.get('marketCap', 0)//10**7:,.0f} Cr")
            cb.metric("Sector", s_info.get('sector', 'N/A'))

        with t3:
            st.markdown("### 🤝 Shareholding Pattern")
            promoter_val = s_info.get('heldPercentInsiders', 0.5) * 100
            inst_val = s_info.get('heldPercentInstitutions', 0.3) * 100
            fig_pie = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Others'], values=[promoter_val, inst_val, 100-(promoter_val+inst_val)], hole=.5, marker=dict(colors=['#ffd700', '#58a6ff', '#2ea043']))])
            fig_pie.update_layout(height=350, margin=dict(l=0,r=0,t=20,b=0), legend=dict(orientation="h", y=-0.1))
            st.plotly_chart(fig_pie, use_container_width=True)

        with t4:
            st.markdown("### 🔮 Forecast (கணிப்பு)")
            roe_val = s_info.get('returnOnEquity', 0)
            if roe_val > 0.15: st.success("Strong Fundamental Strength 🚀")
            else: st.warning("Neutral Growth Outlook ⚖️")
            st.write(f"ROE: {roe_val*100:.2f}%")

        with t5:
            st.markdown("### 📅 Action (நிகழ்வுகள்)")
            all_actions = stock_obj.actions.tail(10).sort_index(ascending=False)
            if not all_actions.empty:
                for d_idx, row_val in all_actions.iterrows():
                    # Fixed potential KeyError
                    div_amt = row_val.get('Dividends', 0)
                    spl_amt = row_val.get('Stock Splits', 0)
                    if div_amt > 0: st.info(f"📅 {d_idx.strftime('%d %b %Y')} - Dividend: ₹{div_amt}")
                    if spl_amt > 0: st.success(f"📅 {d_idx.strftime('%d %b %Y')} - Split: {spl_amt}")
            else: st.write("No recent actions found.")

        with t6:
            st.markdown("### 🗞️ News (நேரலைச் செய்திகள்)")
            try:
                news_feed = stock_obj.news
                if news_feed:
                    for n_item in news_feed[:10]:
                        # Fixed potential KeyError for timestamp
                        t_stamp = n_item.get('providerPublishTime', 0)
                        d_str = datetime.fromtimestamp(t_stamp).strftime('%d %b, %H:%M') if t_stamp else ""
                        st.markdown(f"""
                            <div class="news-card">
                                <a href="{n_item.get('link','#')}" target="_blank" style="color:#ffd700; text-decoration:none; font-weight:bold;">{n_item.get('title','News Title')}</a><br>
                                <small style="color:#8b949e;">{n_item.get('publisher','Market')} • {d_str}</small>
                            </div>
                        """, unsafe_allow_html=True)
                else: st.info("சமீபத்திய செய்திகள் இல்லை.")
            except: st.write("செய்திகளைப் பெற முடியவில்லை.")

    else: st.warning("Please enter a valid stock name.")
except Exception as e:
    st.info("Loading Data...")

st.markdown("<div style='text-align:center;color:#333;font-size:10px;margin-top:30px;'>© 2026 TAMIL INVEST HUB</div>", unsafe_allow_html=True)
