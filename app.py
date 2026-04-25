import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import base64
from deep_translator import GoogleTranslator

# 1. பக்க அமைப்பு மற்றும் கான்ஃபிக்
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

if 'watchlist' not in st.session_state:
    st.session_state['watchlist'] = []

# அதிவேக மொழிபெயர்ப்பு
@st.cache_data(show_spinner=False)
def translate_to_tamil(text):
    if not text or len(str(text)) < 2: return "தகவல் இல்லை."
    try:
        return GoogleTranslator(source='en', target='ta').translate(str(text)[:1000])
    except: return str(text)

# 2. பிரீமியம் CSS (Small Font & High-Quality UI)
st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 11px !important; background-color: #0d1117; color: #c9d1d9; }
    .ticker-wrap { width: 100%; overflow: hidden; background: #161b22; border-bottom: 1px solid #f85149; padding: 6px 0; position: sticky; top: 0; z-index: 999; }
    .ticker-move { display: inline-block; white-space: nowrap; animation: ticker 40s linear infinite; font-size: 11px; font-weight: bold; }
    @keyframes ticker { 0% { transform: translateX(100%); } 100% { transform: translateX(-100%); } }
    .main-title { 
        text-align: center; font-size: 26px !important; font-weight: 900; 
        background: linear-gradient(90deg, #2ea043, #f85149);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0px;
    }
    .metric-row { background: #1c2128; border: 1px solid #30363d; border-radius: 6px; padding: 6px 10px; margin-bottom: 6px; display: flex; justify-content: space-between; align-items: center; }
    .m-label { color: #ffffff !important; font-size: 8.5px; text-transform: uppercase; font-weight: 500; }
    .m-value { color: #ffffff !important; font-size: 12px; font-weight: bold; }
    .news-card { background: #161b22; border-radius: 6px; padding: 10px; margin-bottom: 8px; border-left: 3px solid #f85149; }
    .rating-box { padding: 10px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 14px; margin: 10px 0; border: 1px solid rgba(255,255,255,0.1); }
    [data-testid="stHeader"] { height: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. லைவ் டிக்கர்
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

st.markdown(f'<div class="ticker-wrap"><div class="ticker-move">{get_ticker_text()}</div></div>', unsafe_allow_html=True)

# தலைப்பு
st.markdown('<p class="main-title">TAMIL INVEST HUB</p>', unsafe_allow_html=True)
st.markdown('<p style="text-align:center; font-size:10px; color:#8b949e; margin-top:-5px;">created by somasundaram</p>', unsafe_allow_html=True)

# 4. சர்ச் மற்றும் டேட்டா
u_input = st.text_input("Search Symbol", value="RELIANCE", label_visibility="collapsed").upper()
ticker = f"{u_input}.NS" if ".NS" not in u_input and "^" not in u_input else u_input

try:
    stock_obj = yf.Ticker(ticker)
    info = stock_obj.info
    hist = stock_obj.history(period="1y")

    if 'symbol' in info:
        # டேப்கள் - விரிவான பகுப்பாய்வு
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Analysis", "⭐ Ratings", "🔮 Forecast", "📅 Action", "🗞️ News", "📌 Watchlist"
        ])

        with tab1:
            st.markdown(f"<p style='font-size:14px; font-weight:bold;'>{info.get('longName')} Analysis</p>", unsafe_allow_html=True)
            ltp = info.get('currentPrice') or info.get('regularMarketPrice') or 0
            
            # மெட்ரிக்ஸ்
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                st.markdown(f'<div class="metric-row"><div><span class="m-label">LTP</span><br><span class="m-value">₹{ltp:,.2f}</span></div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><div><span class="m-label">P/E Ratio</span><br><span class="m-value">{info.get("trailingPE", "N/A")}</span></div></div>', unsafe_allow_html=True)
            with col_m2:
                st.markdown(f'<div class="metric-row"><div><span class="m-label">Market Cap</span><br><span class="m-value">₹{info.get("marketCap", 0)//10**7:,.0f} Cr</span></div></div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-row"><div><span class="m-label">ROE</span><br><span class="m-value">{info.get("returnOnEquity", 0)*100:.2f}%</span></div></div>', unsafe_allow_html=True)
            
            # சார்ட்
            fig = go.Figure(data=[go.Candlestick(x=hist.index[-60:], open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'])])
            fig.update_layout(height=280, template="plotly_dark", xaxis_rangeslider_visible=False, margin=dict(l=0,r=0,t=0,b=0))
            st.plotly_chart(fig, use_container_width=True)

        with tab2:
            st.markdown("### Stock Ratings & AI Verdict")
            score = 0
            pe = info.get('trailingPE', 100)
            roe = info.get('returnOnEquity', 0)
            debt = info.get('debtToEquity', 100)

            if pe < 25: score += 1
            if roe > 0.18: score += 1
            if debt < 100: score += 1

            if score == 3: st.markdown('<div class="rating-box" style="background:#2ea043;">EXCELLENT (Strong Buy) 🚀</div>', unsafe_allow_html=True)
            elif score == 2: st.markdown('<div class="rating-box" style="background:#ffd700; color:black;">GOOD (Hold) ⚖️</div>', unsafe_allow_html=True)
            else: st.markdown('<div class="rating-box" style="background:#f85149;">AVOID (Risky) ⚠️</div>', unsafe_allow_html=True)
            
            # 3D Effect Shareholding Pattern
            st.markdown("---")
            st.write("Shareholding (3D Visual)")
            p = info.get('heldPercentInsiders', 0) * 100
            i = info.get('heldPercentInstitutions', 0) * 100
            fig_3d = go.Figure(data=[go.Pie(labels=['Promoters', 'Institutions', 'Public'], values=[p, i, 100-(p+i)], hole=.6, pull=[0.1, 0, 0])])
            fig_3d.update_layout(height=250, margin=dict(l=0,r=0,t=0,b=0), showlegend=True)
            st.plotly_chart(fig_3d, use_container_width=True)

        with tab3:
            st.markdown("### Forecast (எதிர்காலக் கணிப்பு)")
            target = info.get('targetMeanPrice')
            if target:
                upside = ((target - ltp) / ltp) * 100
                st.write(f"சராசரி இலக்கு விலை (Target): ₹{target:,.2f}")
                st.metric("எதிர்பார்க்கப்படும் உயர்வு (Potential Upside)", f"{upside:.2f}%")
            else:
                st.info("தற்போது கணிப்பு விவரங்கள் கிடைக்கவில்லை.")
            
            st.markdown("---")
            st.write("Financial Estimates (அடுத்த காலாண்டு)")
            st.write(f"EPS Estimate: {info.get('earningsQuarterlyGrowth', 'N/A')}")
            st.write(f"Revenue Growth: {info.get('revenueGrowth', 0)*100:.2f}%")

        with tab4:
            st.markdown("### Corporate Action (நிகழ்வுகள்)")
            actions = stock_obj.actions.tail(10).sort_index(ascending=False)
            if not actions.empty:
                st.dataframe(actions, use_container_width=True)
            else:
                st.write("சமீபத்திய நிகழ்வுகள் ஏதுமில்லை.")

        with tab5:
            st.markdown("### Live News Feed")
            news = stock_obj.news
            if news:
                for n in news[:8]:
                    st.markdown(f"""
                        <div class="news-card">
                            <a href="{n.get('link')}" target="_blank" style="color:#f85149; text-decoration:none; font-weight:bold; font-size:13px;">{n.get('title')}</a><br>
                            <small style="color:#8b949e;">{n.get('publisher')} • {datetime.fromtimestamp(n.get('providerPublishTime')).strftime('%d %b %H:%M')}</small>
                        </div>
                    """, unsafe_allow_html=True)
            else:
                st.write("செய்திகள் இல்லை.")

        with tab6:
            st.markdown("### My Watchlist")
            if st.button(f"➕ Add {u_input}"):
                if u_input not in st.session_state['watchlist']:
                    st.session_state['watchlist'].append(u_input)
                    st.rerun()
            for item in st.session_state['watchlist']:
                c1, c2 = st.columns([5, 1])
                c1.write(f"📌 {item}")
                if c2.button("Remove", key=f"del_{item}"):
                    st.session_state['watchlist'].remove(item)
                    st.rerun()

except Exception as e:
    st.info("பங்கு விவரங்களை லோடு செய்கிறது... சரியான குறியீட்டை உள்ளிடவும்.")

st.markdown("<div style='text-align:center;color:#444;font-size:9px;margin-top:30px;'>© 2026 TAMIL INVEST HUB PRO</div>", unsafe_allow_html=True)
