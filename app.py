import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from deep_translator import GoogleTranslator

# ──────────────────────────────────────────────
# 1. PAGE CONFIG
# ──────────────────────────────────────────────
st.set_page_config(page_title="TAMIL INVEST HUB PRO", page_icon="📈", layout="wide")

# ──────────────────────────────────────────────
# 2. SESSION STATE INIT
# ──────────────────────────────────────────────
for key, default in [
    ('is_logged_in', False),
    ('watchlist', []),
    ('language', "Tamil"),
    ('portfolio', []),          # list of dicts: {symbol, qty, avg_price}
]:
    if key not in st.session_state:
        st.session_state[key] = default

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# ──────────────────────────────────────────────
# 3. STYLING
# ──────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    background-color: #060a0f !important;
    color: #c9d1d9;
    font-family: 'DM Sans', sans-serif;
    font-size: 13px !important;
}
.main-title {
    font-family: 'Space Mono', monospace;
    font-size: 28px !important; font-weight: 700;
    background: linear-gradient(90deg, #39FF14, #00D1FF);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    letter-spacing: 2px;
}
.sub-title { font-size: 10px !important; color: #444; letter-spacing: 3px; text-transform: uppercase; margin-top: -4px; }

.price-card {
    background: linear-gradient(135deg, #0d1117 60%, #0f1e12);
    padding: 18px 22px; border-radius: 14px;
    border: 1px solid #39FF1430; margin-bottom: 16px; text-align: center;
}
.section-card {
    background: #0d1117; padding: 18px 20px; border-radius: 12px;
    border: 1px solid #21262d; margin-bottom: 16px;
}
.metric-row {
    display: flex; justify-content: space-between; align-items: center;
    padding: 9px 0; border-bottom: 1px solid #161b22;
}
.m-label { color: #8b949e; font-size: 10px; text-transform: uppercase; font-weight: 600; letter-spacing: 0.5px; }
.m-value { color: #f0f6fc; font-family: 'Space Mono', monospace; font-size: 12px; font-weight: 700; }
.green { color: #39FF14 !important; }
.red   { color: #FF4444 !important; }
.blue  { color: #00D1FF !important; }

/* Tab tweaks */
button[data-baseweb="tab"] { font-size: 12px !important; }
div[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* Sidebar */
section[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid #21262d; }

.badge {
    display: inline-block; padding: 2px 8px; border-radius: 99px;
    font-size: 10px; font-weight: 700; letter-spacing: 0.5px;
}
.badge-green { background: #39FF1422; color: #39FF14; border: 1px solid #39FF1455; }
.badge-red   { background: #FF444422; color: #FF4444; border: 1px solid #FF444455; }
.badge-blue  { background: #00D1FF22; color: #00D1FF; border: 1px solid #00D1FF55; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────
# 4. AUTHENTICATION
# ──────────────────────────────────────────────
if not st.session_state['is_logged_in']:
    st.markdown('<div style="text-align:center; padding: 30px 0;"><p class="main-title">TAMIL INVEST HUB PRO</p><p class="sub-title">created by somasundaram</p></div>', unsafe_allow_html=True)
    col = st.columns([1, 2, 1])[1]
    with col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        u = st.text_input("User ID", value="admin")
        p = st.text_input("Password", type="password", value="1234")
        if st.button("🚀 Access Hub", use_container_width=True):
            # Any non-empty user ID and password is accepted
            if u.strip() and p.strip():
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = u.strip()
                st.rerun()
            else:
                st.error("User ID மற்றும் Password உள்ளிடவும்")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# ──────────────────────────────────────────────
# 5. SIDEBAR – Portfolio Tracker
# ──────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="main-title" style="font-size:16px!important;">📂 Portfolio</p>', unsafe_allow_html=True)
    with st.expander("➕ Add Holding", expanded=False):
        ps = st.text_input("Symbol", value="SBIN", key="p_sym").upper().strip()
        pq = st.number_input("Qty", min_value=1, value=10, key="p_qty")
        pp = st.number_input("Avg Price (₹)", min_value=0.0, value=100.0, key="p_price")
        if st.button("Add to Portfolio", use_container_width=True):
            sym = ps if any(x in ps for x in [".NS", ".BO"]) else f"{ps}.NS"
            # update if exists
            existing = [h for h in st.session_state['portfolio'] if h['symbol'] == sym]
            if existing:
                existing[0]['qty'] += pq
                existing[0]['avg_price'] = (existing[0]['avg_price'] + pp) / 2
            else:
                st.session_state['portfolio'].append({'symbol': sym, 'qty': pq, 'avg_price': pp})
            st.success(f"Added {ps}")
            st.rerun()

    if st.session_state['portfolio']:
        total_inv, total_cur = 0.0, 0.0
        rows = []
        for h in st.session_state['portfolio']:
            try:
                ltp = yf.Ticker(h['symbol']).fast_info.get('last_price', 0) or 0
            except Exception:
                ltp = 0
            inv = h['avg_price'] * h['qty']
            cur = ltp * h['qty']
            pnl = cur - inv
            pnl_pct = (pnl / inv * 100) if inv else 0
            total_inv += inv; total_cur += cur
            rows.append({
                "Symbol": h['symbol'].replace(".NS", ""),
                "Qty": h['qty'],
                "Avg": f"₹{h['avg_price']:.1f}",
                "LTP": f"₹{ltp:.1f}",
                "P&L": f"{'▲' if pnl >= 0 else '▼'} ₹{abs(pnl):,.0f} ({pnl_pct:+.1f}%)"
            })

        df_port = pd.DataFrame(rows)
        st.dataframe(df_port, use_container_width=True, hide_index=True)

        total_pnl = total_cur - total_inv
        total_pct = (total_pnl / total_inv * 100) if total_inv else 0
        clr = "#39FF14" if total_pnl >= 0 else "#FF4444"
        st.markdown(f"""
        <div style="background:#0d1117; border-radius:10px; padding:12px; border:1px solid {clr}44; margin-top:8px; text-align:center;">
            <div class="m-label">Total P&L</div>
            <div style="color:{clr}; font-family:'Space Mono',monospace; font-size:16px; font-weight:700;">
                {'▲' if total_pnl >= 0 else '▼'} ₹{abs(total_pnl):,.0f} ({total_pct:+.1f}%)
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗑 Clear Portfolio"):
            st.session_state['portfolio'] = []
            st.rerun()
    else:
        st.info("No holdings yet.")

    st.markdown("---")
    st.session_state['language'] = st.radio("Language", ["Tamil", "English"], horizontal=True)
    if st.button("Logout 🚪", use_container_width=True):
        st.session_state['is_logged_in'] = False
        st.rerun()

# ──────────────────────────────────────────────
# 6. HEADER & SEARCH
# ──────────────────────────────────────────────
st.markdown('<div style="text-align:center; padding:8px 0 4px;"><p class="main-title">TAMIL INVEST HUB PRO</p><p class="sub-title">created by somasundaram</p></div>', unsafe_allow_html=True)

col_s1, col_s2 = st.columns([5, 1])
with col_s1:
    u_input = st.text_input("🔍 " + get_text("Search Symbol (eg: SBIN, RELIANCE, TCS)", "சின்னம் தேடவும் (eg: SBIN, RELIANCE)"), value="RELIANCE").upper().strip()
with col_s2:
    period_map = {"1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "2Y": "2y", "5Y": "5y"}
    period_label = st.selectbox("Period", list(period_map.keys()), index=3)
    period = period_map[period_label]

ticker_symbol = u_input if any(x in u_input for x in [".NS", ".BO"]) else f"{u_input}.NS"

# ──────────────────────────────────────────────
# 7. HELPER FUNCTIONS
# ──────────────────────────────────────────────
def calc_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def calc_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram

def calc_bollinger(series, window=20, num_std=2):
    sma = series.rolling(window).mean()
    std = series.rolling(window).std()
    return sma + num_std * std, sma, sma - num_std * std

def fmt_cr(val):
    if val is None or val == 0: return "N/A"
    return f"₹{val/10_000_000:,.2f} Cr"

def fmt_pct(val):
    if val is None: return "N/A"
    return f"{val*100:.2f}%"

def safe(val, decimals=2):
    if val is None or (isinstance(val, float) and np.isnan(val)): return "N/A"
    if isinstance(val, float): return f"{val:,.{decimals}f}"
    return str(val)

# ──────────────────────────────────────────────
# 8. DATA FETCH
# ──────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def fetch_data(sym, period):
    stock = yf.Ticker(sym)
    info = dict(stock.info)           # plain dict — serializable
    hist = stock.history(period=period)
    try:
        actions = stock.actions
    except Exception:
        actions = pd.DataFrame()
    return info, hist, actions

try:
    with st.spinner("Fetching market data..."):
        info, hist, actions = fetch_data(ticker_symbol, period)
        stock = yf.Ticker(ticker_symbol)   # non-cached, used only for sidebar portfolio LTP

    if hist.empty:
        st.error("⚠️ No data found. Please check the symbol and try again.")
        st.stop()

    # Pre-compute indicators
    close = hist['Close']
    hist['RSI'] = calc_rsi(close)
    hist['MACD'], hist['MACD_Signal'], hist['MACD_Hist'] = calc_macd(close)
    hist['BB_Upper'], hist['BB_Mid'], hist['BB_Lower'] = calc_bollinger(close)
    hist['EMA20'] = close.ewm(span=20).mean()
    hist['EMA50'] = close.ewm(span=50).mean()
    hist['EMA200'] = close.ewm(span=200).mean()

    rsi_val = hist['RSI'].iloc[-1]
    macd_val = hist['MACD'].iloc[-1]
    macd_sig = hist['MACD_Signal'].iloc[-1]
    ltp = info.get('currentPrice') or info.get('regularMarketPrice') or float(close.iloc[-1])
    prev_close = info.get('regularMarketPreviousClose') or float(close.iloc[-2])
    day_chg = ltp - prev_close
    day_chg_pct = (day_chg / prev_close * 100) if prev_close else 0

    # ──────────────────────────────────────────────
    # 9. TABS
    # ──────────────────────────────────────────────
    tabs = st.tabs([
        f"📊 {get_text('Chart', 'விலை வரைபடம்')}",
        f"📈 {get_text('Indicators', 'தொழில்நுட்பம்')}",
        f"🔮 {get_text('Rating', 'ரேட்டிங்')}",
        f"💰 {get_text('Financials', 'நிதிநிலை')}",
        f"🤝 {get_text('Shareholding', 'பங்குதாரர்')}",
        f"📅 {get_text('Actions', 'நிகழ்வுகள்')}",
        f"🏢 {get_text('About', 'நிறுவனம்')}",
    ])

    # ══════════════════════════════════════════════
    # TAB 0 – CANDLESTICK CHART
    # ══════════════════════════════════════════════
    with tabs[0]:
        name = info.get('longName', ticker_symbol)
        st.subheader(name)

        # Price header row
        chg_clr = "#39FF14" if day_chg >= 0 else "#FF4444"
        arrow = "▲" if day_chg >= 0 else "▼"
        st.markdown(f"""
        <div class="price-card">
            <span class="m-label">LTP (விலை)</span><br>
            <span style="color:#39FF14; font-family:'Space Mono',monospace; font-size:30px; font-weight:800;">₹{ltp:,.2f}</span>
            &nbsp;<span style="color:{chg_clr}; font-size:15px;">{arrow} ₹{abs(day_chg):.2f} ({day_chg_pct:+.2f}%)</span>
        </div>
        """, unsafe_allow_html=True)

        # Quick stats row
        q1, q2, q3, q4, q5 = st.columns(5)
        metrics = [
            ("52W High", f"₹{info.get('fiftyTwoWeekHigh', 0):,.2f}", "green"),
            ("52W Low", f"₹{info.get('fiftyTwoWeekLow', 0):,.2f}", "red"),
            ("Mkt Cap", fmt_cr(info.get("marketCap")), "blue"),
            ("P/E Ratio", safe(info.get("trailingPE")), ""),
            ("Volume", f"{info.get('regularMarketVolume', 0):,}", ""),
        ]
        for col, (lbl, val, clr) in zip([q1, q2, q3, q4, q5], metrics):
            with col:
                st.markdown(f'<div class="section-card" style="text-align:center;padding:10px;"><div class="m-label">{lbl}</div><div class="m-value {clr}">{val}</div></div>', unsafe_allow_html=True)

        # Overlay toggle
        ov1, ov2 = st.columns([3, 1])
        with ov2:
            show_ema = st.checkbox("EMA Lines", value=True)
            show_bb  = st.checkbox("Bollinger Bands", value=True)
            show_vol = st.checkbox("Volume", value=True)

        # Build candlestick chart
        rows_n = 2 if show_vol else 1
        row_heights = [0.72, 0.28] if show_vol else [1]
        fig = make_subplots(rows=rows_n, cols=1, shared_xaxes=True, vertical_spacing=0.03, row_heights=row_heights)

        fig.add_trace(go.Candlestick(
            x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close'],
            increasing_line_color='#39FF14', decreasing_line_color='#FF4444',
            increasing_fillcolor='rgba(57,255,20,0.5)', decreasing_fillcolor='rgba(255,68,68,0.5)',
            name="Price"
        ), row=1, col=1)

        if show_ema:
            for span, clr, w in [(20, '#00D1FF', 1.2), (50, '#FFD700', 1.2), (200, '#FF69B4', 1.5)]:
                col_key = f'EMA{span}'
                if col_key in hist.columns:
                    fig.add_trace(go.Scatter(x=hist.index, y=hist[col_key], name=f"EMA{span}",
                                             line=dict(color=clr, width=w), opacity=0.85), row=1, col=1)

        if show_bb:
            fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Upper'], name="BB Upper",
                                     line=dict(color='#888', width=1, dash='dot'), showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Lower'], name="BB Lower",
                                     line=dict(color='#888', width=1, dash='dot'),
                                     fill='tonexty', fillcolor='rgba(136,136,136,0.05)', showlegend=False), row=1, col=1)
            fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Mid'], name="BB Mid",
                                     line=dict(color='#666', width=1, dash='dash'), showlegend=False), row=1, col=1)

        if show_vol:
            colors = ['#39FF14' if c >= o else '#FF4444' for c, o in zip(hist['Close'], hist['Open'])]
            fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name="Volume",
                                 marker_color=colors, opacity=0.6), row=2, col=1)
            fig.update_yaxes(title_text="Volume", row=2, col=1, title_font=dict(size=9))

        fig.update_layout(
            template="plotly_dark", paper_bgcolor='#060a0f', plot_bgcolor='#0d1117',
            height=560, margin=dict(t=10, b=10, l=10, r=10),
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.01, font=dict(size=10)),
            font=dict(family="DM Sans")
        )
        fig.update_xaxes(gridcolor='#161b22', zeroline=False)
        fig.update_yaxes(gridcolor='#161b22', zeroline=False)
        st.plotly_chart(fig, use_container_width=True)

    # ══════════════════════════════════════════════
    # TAB 1 – TECHNICAL INDICATORS
    # ══════════════════════════════════════════════
    with tabs[1]:
        st.markdown(f"### 📈 {get_text('Technical Indicators', 'தொழில்நுட்ப குறிகாட்டிகள்')}")

        # RSI + MACD chart
        fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                             row_heights=[0.5, 0.5],
                             subplot_titles=["RSI (14)", "MACD (12,26,9)"])

        # RSI
        fig2.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name="RSI",
                                  line=dict(color='#00D1FF', width=1.5)), row=1, col=1)
        fig2.add_hline(y=70, line_color='#FF4444', line_dash='dash', line_width=1, row=1, col=1)
        fig2.add_hline(y=30, line_color='#39FF14', line_dash='dash', line_width=1, row=1, col=1)
        fig2.add_hrect(y0=30, y1=70, fillcolor='rgba(255,255,255,0.02)', line_width=0, row=1, col=1)

        # MACD
        macd_colors = ['#39FF14' if v >= 0 else '#FF4444' for v in hist['MACD_Hist']]
        fig2.add_trace(go.Bar(x=hist.index, y=hist['MACD_Hist'], name="Histogram",
                              marker_color=macd_colors, opacity=0.7), row=2, col=1)
        fig2.add_trace(go.Scatter(x=hist.index, y=hist['MACD'], name="MACD",
                                  line=dict(color='#00D1FF', width=1.5)), row=2, col=1)
        fig2.add_trace(go.Scatter(x=hist.index, y=hist['MACD_Signal'], name="Signal",
                                  line=dict(color='#FFD700', width=1.5)), row=2, col=1)

        fig2.update_layout(template="plotly_dark", paper_bgcolor='#060a0f', plot_bgcolor='#0d1117',
                           height=480, margin=dict(t=30, b=10, l=10, r=10),
                           font=dict(family="DM Sans"),
                           legend=dict(orientation="h", yanchor="bottom", y=1.01, font=dict(size=10)))
        fig2.update_xaxes(gridcolor='#161b22'); fig2.update_yaxes(gridcolor='#161b22')
        st.plotly_chart(fig2, use_container_width=True)

        # Indicator Summary Cards
        st.markdown(f"#### {get_text('Signal Summary', 'சமிக்ஞை சுருக்கம்')}")
        macd_bull = macd_val > macd_sig
        rsi_zone = "Overbought (அதிக வாங்கல்)" if rsi_val > 70 else ("Oversold (அதிக விற்பனை)" if rsi_val < 30 else "Neutral (சமநிலை)")
        rsi_clr = "red" if rsi_val > 70 else ("green" if rsi_val < 30 else "blue")

        bb_upper = hist['BB_Upper'].iloc[-1]
        bb_lower = hist['BB_Lower'].iloc[-1]
        bb_pct = ((ltp - bb_lower) / (bb_upper - bb_lower) * 100) if (bb_upper - bb_lower) else 50
        bb_zone = "Near Upper Band" if bb_pct > 80 else ("Near Lower Band" if bb_pct < 20 else "Mid Band")

        ema_bull = ltp > hist['EMA50'].iloc[-1] if not hist['EMA50'].isna().iloc[-1] else False

        ind_data = [
            ("RSI (14)", f"{rsi_val:.1f}", rsi_zone, rsi_clr),
            ("MACD Signal", f"{macd_val:.3f}", "Bullish Cross ▲" if macd_bull else "Bearish Cross ▼", "green" if macd_bull else "red"),
            ("Bollinger %B", f"{bb_pct:.1f}%", bb_zone, "green" if 20 < bb_pct < 80 else "red"),
            ("EMA50 Trend", f"₹{hist['EMA50'].iloc[-1]:,.2f}", "Price Above EMA ▲" if ema_bull else "Price Below EMA ▼", "green" if ema_bull else "red"),
        ]
        c1, c2, c3, c4 = st.columns(4)
        for col, (name_i, val_i, zone_i, clr_i) in zip([c1, c2, c3, c4], ind_data):
            badge_cls = f"badge-{clr_i}" if clr_i in ("green", "red", "blue") else "badge-blue"
            with col:
                st.markdown(f"""
                <div class="section-card" style="text-align:center;">
                    <div class="m-label">{name_i}</div>
                    <div class="m-value" style="font-size:18px; margin:6px 0;">{val_i}</div>
                    <span class="badge {badge_cls}">{zone_i}</span>
                </div>
                """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # TAB 2 – IMPROVED RATING
    # ══════════════════════════════════════════════
    with tabs[2]:
        st.markdown(f"### 🔮 {get_text('Investment Rating Engine', 'முதலீட்டு மதிப்பீட்டு இயந்திரம்')}")

        scores = {}

        # ── Fundamental Score (40 pts max) ──
        roe = (info.get('returnOnEquity') or 0) * 100
        debt = (info.get('debtToEquity') or 999)
        pe = info.get('trailingPE') or 999
        net_margin = (info.get('profitMargins') or 0) * 100
        rev_growth = (info.get('revenueGrowth') or 0) * 100

        f1 = min(20, max(0, roe / 25 * 20))        # ROE → max 20 pts
        f2 = 15 if debt < 50 else (10 if debt < 100 else (5 if debt < 200 else 0))  # Debt/Equity
        f3 = min(10, max(0, net_margin / 20 * 10))  # Net Margin → max 10 pts
        fund_score = f1 + f2 + f3
        scores['Fundamental'] = (fund_score, 45)

        # ── Technical Score (35 pts max) ──
        t1 = 15 if 40 <= rsi_val <= 60 else (10 if 30 <= rsi_val <= 70 else 0)
        t2 = 12 if macd_bull else 0
        t3 = 8 if ema_bull else 0
        tech_score = t1 + t2 + t3
        scores['Technical'] = (tech_score, 35)

        # ── Growth Score (20 pts max) ──
        g1 = min(10, max(0, rev_growth / 20 * 10)) if rev_growth > 0 else 0
        eps_growth = (info.get('earningsGrowth') or 0) * 100
        g2 = min(10, max(0, eps_growth / 20 * 10)) if eps_growth > 0 else 0
        growth_score = g1 + g2
        scores['Growth'] = (growth_score, 20)

        total_raw = fund_score + tech_score + growth_score
        total_max = 100
        total_pct = int(total_raw / total_max * 100)

        clr = "#39FF14" if total_pct >= 65 else ("#FFD700" if total_pct >= 40 else "#FF4444")
        if total_pct >= 65:
            rec = get_text("STRONG BUY ✅", "வலுவாக வாங்கலாம் ✅")
            rec_detail = get_text("Fundamentals & technicals align. Good entry opportunity.", "அடிப்படை மற்றும் தொழில்நுட்பம் சாதகமாக உள்ளது.")
        elif total_pct >= 50:
            rec = get_text("BUY 🟢", "வாங்கலாம் 🟢")
            rec_detail = get_text("Positive signals. Consider accumulating.", "நேர்மறையான சமிக்ஞைகள். சேகரிக்கலாம்.")
        elif total_pct >= 35:
            rec = get_text("HOLD 🔵", "வைத்திருக்கலாம் 🔵")
            rec_detail = get_text("Mixed signals. Wait for clearer trend.", "கலப்பு சமிக்ஞைகள். தெளிவான போக்கை காத்திருங்கள்.")
        else:
            rec = get_text("AVOID / SELL 🔴", "தவிர்க்கவும் 🔴")
            rec_detail = get_text("Weak fundamentals or bearish technicals.", "பலவீனமான அடிப்படை அல்லது மந்தமான நிலை.")

        # Rating card
        r1, r2 = st.columns([1, 1])
        with r1:
            st.markdown(f"""
            <div style="border:2px solid {clr}; padding:30px 20px; border-radius:16px; text-align:center; background:{clr}08;">
                <p class="m-label">Overall Score</p>
                <h1 style="color:{clr}; font-family:'Space Mono',monospace; font-size:58px; margin:4px 0;">{total_pct}</h1>
                <p class="m-label">/ 100</p>
                <h2 style="color:{clr}; font-size:18px; margin:12px 0;">{rec}</h2>
                <p style="color:#8b949e; font-size:11px;">{rec_detail}</p>
            </div>
            """, unsafe_allow_html=True)

        with r2:
            st.markdown("<div class='section-card'>", unsafe_allow_html=True)
            for cat, (s, mx) in scores.items():
                pct = int(s / mx * 100)
                bar_clr = "#39FF14" if pct >= 65 else ("#FFD700" if pct >= 40 else "#FF4444")
                st.markdown(f"""
                <div style="margin-bottom:14px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
                        <span class="m-label">{cat}</span>
                        <span class="m-value">{int(s)}/{mx} ({pct}%)</span>
                    </div>
                    <div style="background:#21262d; border-radius:6px; height:8px;">
                        <div style="background:{bar_clr}; width:{pct}%; height:8px; border-radius:6px; transition:width 0.5s;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="margin-top:16px; font-size:10px; color:#555; border-top:1px solid #21262d; padding-top:10px;">
                📌 {get_text('Based on ROE, Debt/Equity, Net Margin, RSI, MACD, EMA Trend & Revenue/EPS Growth.', 'ROE, கடன்/சொத்து, நிகர லாப விகிதம், RSI, MACD, EMA போக்கு & வருவாய் வளர்ச்சி ஆகியவற்றின் அடிப்படையில்.')}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        # Input factors breakdown
        st.markdown(f"#### {get_text('Score Inputs', 'மதிப்பீட்டு காரணிகள்')}")
        factor_cols = st.columns(3)
        factors = [
            ("ROE", f"{roe:.1f}%", f"+{f1:.0f} pts"),
            ("Debt/Equity", f"{debt:.1f}", f"+{f2:.0f} pts"),
            ("Net Margin", f"{net_margin:.1f}%", f"+{f3:.0f} pts"),
            ("RSI Signal", f"{rsi_val:.1f}", f"+{t1:.0f} pts"),
            ("MACD Signal", "Bull" if macd_bull else "Bear", f"+{t2:.0f} pts"),
            ("EMA Trend", "Above" if ema_bull else "Below", f"+{t3:.0f} pts"),
            ("Rev Growth", f"{rev_growth:.1f}%", f"+{g1:.0f} pts"),
            ("EPS Growth", f"{eps_growth:.1f}%", f"+{g2:.0f} pts"),
        ]
        for i, (fn, fv, fp) in enumerate(factors):
            with factor_cols[i % 3]:
                st.markdown(f'<div class="metric-row"><span class="m-label">{fn}: {fv}</span><span class="m-value green">{fp}</span></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # TAB 3 – FINANCIALS
    # ══════════════════════════════════════════════
    with tabs[3]:
        st.markdown(f"### 💰 {get_text('Key Financial Metrics', 'முக்கிய நிதி விவரங்கள்')}")

        f_c1, f_c2 = st.columns(2)
        fin_left = [
            ("Market Cap", fmt_cr(info.get("marketCap"))),
            ("Revenue (TTM)", fmt_cr(info.get("totalRevenue"))),
            ("Net Profit (TTM)", fmt_cr(info.get("netIncomeToCommon"))),
            ("Gross Profit", fmt_cr(info.get("grossProfits"))),
            ("EBITDA", fmt_cr(info.get("ebitda"))),
            ("Free Cash Flow", fmt_cr(info.get("freeCashflow"))),
        ]
        fin_right = [
            ("P/E Ratio (TTM)", safe(info.get("trailingPE"))),
            ("P/E Ratio (Fwd)", safe(info.get("forwardPE"))),
            ("P/B Ratio", safe(info.get("priceToBook"))),
            ("EV/EBITDA", safe(info.get("enterpriseToEbitda"))),
            ("P/S Ratio", safe(info.get("priceToSalesTrailing12Months"))),
            ("Book Value/Share", f"₹{safe(info.get('bookValue'))}"),
        ]
        fin_right2 = [
            ("ROE", fmt_pct(info.get("returnOnEquity"))),
            ("ROA", fmt_pct(info.get("returnOnAssets"))),
            ("Debt/Equity", safe(info.get("debtToEquity"))),
            ("Total Debt", fmt_cr(info.get("totalDebt"))),
            ("Cash & Equiv.", fmt_cr(info.get("totalCash"))),
            ("Current Ratio", safe(info.get("currentRatio"))),
        ]

        with f_c1:
            st.markdown(f"**{get_text('Valuation & Income', 'மதிப்பீடு & வருமானம்')}**")
            for lbl, val in fin_left:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
        with f_c2:
            st.markdown(f"**{get_text('Valuation Ratios', 'மதிப்பீட்டு விகிதங்கள்')}**")
            for lbl, val in fin_right:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

        st.markdown(f"**{get_text('Health & Efficiency', 'நிதி ஆரோக்கியம்')}**")
        f_c3, f_c4 = st.columns(2)
        half = len(fin_right2) // 2
        with f_c3:
            for lbl, val in fin_right2[:half]:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
        with f_c4:
            for lbl, val in fin_right2[half:]:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

        # Per share metrics
        st.markdown(f"**{get_text('Per Share Data', 'பங்கு விவரங்கள்')}**")
        ps_c1, ps_c2, ps_c3, ps_c4 = st.columns(4)
        per_share = [
            ("EPS (TTM)", f"₹{safe(info.get('trailingEps'))}"),
            ("EPS (Fwd)", f"₹{safe(info.get('forwardEps'))}"),
            ("Dividend/Share", f"₹{safe(info.get('dividendRate'))}"),
            ("Dividend Yield", fmt_pct(info.get("dividendYield"))),
        ]
        for col, (lbl, val) in zip([ps_c1, ps_c2, ps_c3, ps_c4], per_share):
            with col:
                st.markdown(f'<div class="section-card" style="text-align:center;padding:10px;"><div class="m-label">{lbl}</div><div class="m-value blue">{val}</div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # TAB 4 – SHAREHOLDING
    # ══════════════════════════════════════════════
    with tabs[4]:
        p_pct = (info.get('heldPercentInsiders') or 0) * 100
        i_pct = (info.get('heldPercentInstitutions') or 0) * 100
        pub_pct = max(0, 100 - p_pct - i_pct)

        fig3 = go.Figure(data=[go.Pie(
            labels=['Promoters / Insiders', 'Institutions / FII', 'Public / Others'],
            values=[p_pct, i_pct, pub_pct],
            hole=0.62,
            marker=dict(colors=['#1A73E8', '#00C853', '#FFAB00'], line=dict(color='#060a0f', width=3)),
            textfont=dict(size=11)
        )])
        fig3.add_annotation(text=f"<b>{info.get('longName','')[:12]}</b>", x=0.5, y=0.5,
                            font=dict(size=11, color='#c9d1d9'), showarrow=False)
        fig3.update_layout(template="plotly_dark", paper_bgcolor='#060a0f', height=380,
                           margin=dict(t=20, b=20), font=dict(family="DM Sans"),
                           legend=dict(orientation="h", yanchor="bottom", y=-0.15))
        st.plotly_chart(fig3, use_container_width=True)

        sh_c1, sh_c2, sh_c3 = st.columns(3)
        for col, (lbl, val, clr) in zip([sh_c1, sh_c2, sh_c3], [
            ("Promoters / Insiders", f"{p_pct:.2f}%", "#1A73E8"),
            ("Institutions / FII",  f"{i_pct:.2f}%", "#00C853"),
            ("Public / Others",     f"{pub_pct:.2f}%","#FFAB00"),
        ]):
            with col:
                st.markdown(f'<div class="section-card" style="text-align:center; border-color:{clr}44;"><div class="m-label">{lbl}</div><div style="color:{clr}; font-family:Space Mono,monospace; font-size:22px; font-weight:700;">{val}</div></div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════
    # TAB 5 – CORPORATE ACTIONS
    # ══════════════════════════════════════════════
    with tabs[5]:
        st.markdown(f"### 📅 {get_text('Corporate Actions', 'நிறுவன நிகழ்வுகள்')}")
        if not actions.empty:
            display_actions = actions.sort_index(ascending=False).head(20).copy()
            display_actions.index = display_actions.index.strftime("%d %b %Y")
            st.dataframe(display_actions.style.format({"Dividends": "₹{:.2f}", "Stock Splits": "{:.2f}x"}),
                         use_container_width=True)
        else:
            st.info("No corporate actions found for this symbol.")

        # Upcoming dividends
        st.markdown(f"#### {get_text('Dividend History Chart', 'ஈவுத்தொகை வரலாறு')}")
        if not actions.empty and 'Dividends' in actions.columns:
            div_hist = actions[actions['Dividends'] > 0]['Dividends']
            if not div_hist.empty:
                fig4 = go.Figure(go.Bar(x=div_hist.index, y=div_hist.values,
                                        marker_color='#FFD700', opacity=0.85, name="Dividend"))
                fig4.update_layout(template="plotly_dark", paper_bgcolor='#060a0f', plot_bgcolor='#0d1117',
                                   height=260, margin=dict(t=10, b=10), yaxis_title="₹ per share",
                                   font=dict(family="DM Sans"))
                st.plotly_chart(fig4, use_container_width=True)
            else:
                st.info("No dividend data available.")

    # ══════════════════════════════════════════════
    # TAB 6 – ABOUT COMPANY
    # ══════════════════════════════════════════════
    with tabs[6]:
        st.markdown(f"### 🏢 {get_text('About Company', 'நிறுவனம் பற்றி')}")
        about_raw = info.get('longBusinessSummary', 'No description available.')
        with st.spinner("Translating..."):
            try:
                display_text = GoogleTranslator(source='auto', target='ta').translate(about_raw) if st.session_state['language'] == "Tamil" else about_raw
            except Exception:
                display_text = about_raw
        st.markdown(f'<div class="section-card">{display_text}</div>', unsafe_allow_html=True)

        # Company info table
        st.markdown(f"**{get_text('Company Details', 'நிறுவன விவரங்கள்')}**")
        co_c1, co_c2 = st.columns(2)
        co_details_l = [
            ("Sector", info.get("sector", "N/A")),
            ("Industry", info.get("industry", "N/A")),
            ("Country", info.get("country", "N/A")),
            ("Exchange", info.get("exchange", "N/A")),
        ]
        co_details_r = [
            ("Employees", f"{info.get('fullTimeEmployees', 0):,}"),
            ("Website", info.get("website", "N/A")),
            ("Currency", info.get("currency", "N/A")),
            ("Fiscal Year End", info.get("lastFiscalYearEnd", "N/A")),
        ]
        with co_c1:
            for lbl, val in co_details_l:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)
        with co_c2:
            for lbl, val in co_details_r:
                st.markdown(f'<div class="metric-row"><span class="m-label">{lbl}</span><span class="m-value">{val}</span></div>', unsafe_allow_html=True)

except Exception as e:
    st.error(f"⚠️ Error fetching data: {e}")
    st.info("Please check the stock symbol and try again. Example: SBIN, RELIANCE, TCS, INFY")

# ──────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────
st.markdown("<p style='text-align:center; color:#2a2a2a; font-size:9px; margin-top:50px; font-family:Space Mono,monospace;'>© 2026 TAMIL INVEST HUB PRO | Created by Somasundaram | For educational purposes only. Not financial advice.</p>", unsafe_allow_html=True)
