import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime

# 1. ராயல் தீம் மற்றும் பக்க அமைப்பு
st.set_page_config(
    page_title="Tamil Invest Hub | Professional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. பிரத்யேக ராயல் டிசைன் (Advanced Compact CSS)
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] { font-family: 'Poppins', sans-serif; background-color: #050a0f; color: #e0e0e0; }
    
    /* ராயல் கோல்டு ஹெடர் */
    .royal-header {
        background: linear-gradient(90deg, #b8860b, #ffd700, #b8860b);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 22px !important; font-weight: 800; text-align: center;
        margin-bottom: 2px; letter-spacing: 1px;
    }
    
    /* கச்சிதமான கிரெடிட்ஸ் */
    .footer-credits {
        font-size: 10px; color: #555; text-align: center; 
        border-top: 1px solid #1e2630; padding-top: 10px; margin-top: 30px;
    }
    
    /* மெட்ரிக் கார்டுகள் */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.02);
        border: 1px solid #1e2630; border-radius: 8px;
        padding: 8px !important;
    }
    
    /* எழுத்து அளவுகள் */
    div[data-testid="stMetricValue"] { font-size: 18px !important; color: #ffd700 !important; }
    div[data-testid="stMetricLabel"] { font-size: 11px !important; color: #aaa !important; }
    
    /* சிறிய செய்தி எழுத்துக்கள் */
    .news-link { font-size: 12px; text-decoration:none; color:#e0e0e0; }
    </style>
    """, unsafe_allow_html=True)

# 3. மொழி மற்றும் செட்டிங்ஸ் (Sidebar)
with st.sidebar:
    st.markdown("<h3 style='color:#ffd700;'>Settings</h3>", unsafe_allow_html=True)
    lang = st.radio("Language / மொழி", ["தமிழ்", "English"])
    ticker = st.text_input("Stock Symbol", value="RELIANCE.NS").upper()
    period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=0)

t = {
    "தமிழ்": {
        "title": "TAMIL INVEST HUB",
        "subtitle": "உங்கள் நிதிச் சுதந்திரத்தின் நுழைவாயில்",
        "price": "தற்போதைய விலை", "change": "மாற்றம்", "mcap": "சந்தை மதிப்பு",
        "low": "Day Low", "high": "Day High", "news": "சமீபத்திய செய்திகள்",
        "loading": "தரவுகள் சேகரிக்கப்படுகின்றன...", "error": "சரியான குறியீட்டை இடவும்.",
        "lakh_cr": "இலட்சம் கோடி"
    },
    "English": {
        "title": "TAMIL INVEST HUB",
        "subtitle": "Your Gateway to Financial Freedom",
        "price": "Current Price", "change": "Day Change", "mcap": "Market Cap",
        "low": "Day Low", "high": "Day High", "news": "Latest Insights",
        "loading": "Architecting Data...", "error": "Invalid Symbol Provided.",
        "lakh_cr": "L Cr"
    }
}[lang]

# 4. மெயின் டைட்டில்
st.markdown(f'<p class="royal-header">{t["title"]}</p>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; font-size:10px; color:#ffd700; margin-top:-15px; margin-bottom:10px;">{t["subtitle"]}</p>', unsafe_allow_html=True)

# 5. டேட்டா மேனேஜ்மென்ட்
try:
    with st.spinner(t['loading']):
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        info = stock.info
        
        if not hist.empty:
            # அ) பிரீமியம் கேண்டில் ஸ்டிக் சார்ட்
            fig = go.Figure(data=[go.Candlestick(
                x=hist.index, open=hist['Open'], high=hist['High'],
                low=hist['Low'], close=hist['Close'],
                increasing_line_color='#00ff88', decreasing_line_color='#ff3131'
            )])
            fig.update_layout(
                template="plotly_dark", xaxis_rangeslider_visible=False,
                height=380, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=5, r=5, t=5, b=5)
            )
            st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

            # ஆ) மெட்ரிக்ஸ் கிரிட்
            curr = info.get('currentPrice', hist['Close'].iloc[-1])
            prev = info.get('previousClose', curr)
            chg_pct = ((curr - prev) / prev) * 100
            
            c1, c2, c3 = st.columns(3)
            c1.metric(t['price'], f"₹{curr:,.2f}")
            c2.metric(t['change'], f"{chg_pct:+.2f}%")
            
            mcap = info.get('marketCap', 0)
            mcap_val = f"₹{mcap/10**11:,.2f} {t['lakh_cr']}" if mcap > 10**11 else f"₹{mcap/10**7:,.2f} Cr"
            c3.metric(t['mcap'], mcap_val)

            # இ) செய்திகள்
            st.markdown(f"<h5 style='color:#ffd700; margin-top:15px; margin-bottom:5px; font-size:14px;'>📰 {t['news']}</h5>", unsafe_allow_html=True)
            for item in stock.news[:3]:
                st.markdown(f"""
                    <div style='background:rgba(255,255,255,0.01); padding:5px; border-radius:5px; margin-bottom:3px; border-left:2px solid #ffd700;'>
                        <a href='{item.get('link', '#')}' class='news-link'>{item.get('title', 'No Title')}</a>
                        <div style='font-size:9px; color:#555;'>{item.get('publisher', 'N/A')}</div>
                    </div>
                """, unsafe_allow_html=True)

        else:
            st.error(t['error'])
except Exception as e:
    st.error(t['error'])

# 6. பொதுவான அடிக்குறிப்பு (Footer Without Names)
st.markdown(f"""
    <div class="footer-credits">
        © {datetime.now().year} Tamil Invest Hub - Premium Financial Analytics<br>
        Focus on Action, Driven by Results.
    </div>
""", unsafe_allow_html=True)
