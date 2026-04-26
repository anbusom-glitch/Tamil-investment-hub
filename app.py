# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# Fixed Version - No Unicode special characters
# =============================================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime

# =============================================================
# 1. PAGE CONFIG
# =============================================================
st.set_page_config(
    page_title="TAMIL INVEST HUB PRO",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =============================================================
# 2. SESSION STATE
# =============================================================
defaults = {
    'is_logged_in': False,
    'language': "Tamil",
    'portfolio': [],
    'watchlist': [],
    'username': '',
    'last_symbol': '',
    'last_data': None,
}
for key, default in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = default

def get_text(en, ta):
    return ta if st.session_state['language'] == "Tamil" else en

# =============================================================
# 3. PREMIUM STYLING
# =============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@700;900&family=Exo+2:wght@300;400;600;700;800&display=swap');

html, body, [class*="css"] {
    background-color: #020509 !important;
    color: #dde6f0;
    font-family: 'Exo 2', sans-serif;
    font-size: 15px !important;
}

.main-title {
    font-family: 'Orbitron', monospace;
    font-size: 36px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #39FF14 0%, #00FFD1 50%, #00AAFF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: 4px;
    margin: 0;
    line-height: 1.1;
}

.sub-title {
    font-size: 11px !important;
    color: #3a4a5a;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-top: 2px;
    font-family: 'Exo 2', sans-serif;
}

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 22px 28px;
    border-radius: 18px;
    border: 1px solid rgba(57,255,20,0.25);
    box-shadow: 0 0 30px rgba(57,255,20,0.08);
    margin-bottom: 18px;
    text-align: center;
}

.ltp-price {
    font-family: 'Orbitron', monospace;
    font-size: 42px !important;
    font-weight: 900;
    color: #39FF14;
    text-shadow: 0 0 20px rgba(57,255,20,0.4);
    line-height: 1;
}

.ltp-change {
    font-size: 18px !important;
    font-weight: 700;
    font-family: 'Exo 2', sans-serif;
}

.section-card {
    background: #080f18;
    padding: 20px 22px;
    border-radius: 14px;
    border: 1px solid #1a2535;
    margin-bottom: 16px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.4);
}

.metric-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 11px 0;
    border-bottom: 1px solid #111d2a;
}

.m-label {
    color: #5a7a9a;
    font-size: 12px;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.8px;
}

.m-value {
    color: #eaf2ff;
    font-family: 'Orbitron', monospace;
    font-size: 14px;
    font-weight: 700;
}

.stat-card {
    background: #080f18;
    border-radius: 14px;
    border: 1px solid #1a2535;
    padding: 16px 12px;
    text-align: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.stat-label {
    color: #5a7a9a;
    font-size: 11px;
    text-transform: uppercase;
    font-weight: 700;
    letter-spacing: 0.8px;
    margin-bottom: 6px;
}

.stat-value {
    font-family: 'Orbitron', monospace;
    font-size: 16px;
    font-weight: 700;
}

.green { color: #39FF14 !important; }
.red   { color: #FF4455 !important; }
.blue  { color: #00D4FF !important; }
.gold  { color: #FFD700 !important; }

button[data-baseweb="tab"] {
    font-size: 13px !important;
    font-weight: 700 !important;
    font-family: 'Exo 2', sans-serif !important;
    letter-spacing: 0.5px !important;
}

button[data-baseweb="tab"][aria-selected="true"] {
    color: #39FF14 !important;
}

.badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 99px;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 0.5px;
    font-family: 'Exo 2', sans-serif;
}

.badge-green { background: rgba(57,255,20,0.12);  color: #39FF14; border: 1px solid rgba(57,255,20,0.35); }
.badge-red   { background: rgba(255,68,85,0.12);   color: #FF4455; border: 1px solid rgba(255,68,85,0.35); }
.badge-blue  { background: rgba(0,212,255,0.12);   color: #00D4FF; border: 1px solid rgba(0,212,255,0.35); }
.badge-gold  { background: rgba(255,215,0,0.12);   color: #FFD700; border: 1px solid rgba(255,215,0,0.35); }

section[data-testid="stSidebar"] {
    background: #060c16 !important;
    border-right: 1px solid #1a2535;
}

input[type="text"], input[type="password"] {
    font-size: 15px !important;
    font-family: 'Exo 2', sans-serif !important;
}

.watch-tag {
    display: inline-block;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 8px;
    padding: 4px 10px;
    margin: 3px;
    font-size: 13px;
    color: #00D4FF;
    font-weight: 700;
}

.news-card {
    background: #080f18;
    border-left: 3px solid #39FF14;
    border-radius: 0 10px 10px 0;
    padding: 12px 16px;
    margin-bottom: 10px;
}

.news-title {
    font-size: 14px;
    font-weight: 700;
    color: #dde6f0;
    margin-bottom: 4px;
}

.news-meta {
    font-size: 11px;
    color: #5a7a9a;
}

div[data-testid="stDataFrame"] {
    border-radius: 12px;
    overflow: hidden;
}
</style>
""", unsafe_allow_html=True)

# =============================================================
# 4. AUTHENTICATION
# =============================================================
if not st.session_state['is_logged_in']:
    st.markdown("""
    <div style="text-align:center; padding: 60px 0 40px;">
        <p class="main-title">TAMIL INVEST HUB PRO</p>
        <p class="sub-title">Tamil Investment Platform - Created by Somasundaram</p>
    </div>
    """, unsafe_allow_html=True)

    col = st.columns([1, 1.5, 1])[1]
    with col:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown(
            '<p style="text-align:center; font-size:20px; font-weight:800; '
            'color:#00D4FF; margin-bottom:16px;">Login</p>',
            unsafe_allow_html=True
        )
        u = st.text_input("User ID / Email")
        p = st.text_input("Password", type="password")
        if st.button("ACCESS HUB", use_container_width=True):
            if u.strip() and p.strip():
                st.session_state['is_logged_in'] = True
                st.session_state['username'] = u.strip()
                st.rerun()
            else:
                st.error("User ID மற்றும் Password உள்ளிடவும்!")
        st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# =============================================================
# 5. HELPER FUNCTIONS
# =============================================================
def calc_rsi(series, window=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))

def calc_macd(series, fast=12, slow=26, signal=9):
    ema_f = series.ewm(span=fast, adjust=False).mean()
    ema_s = series.ewm(span=slow, adjust=False).mean()
    macd  = ema_f - ema_s
    sig   = macd.ewm(span=signal, adjust=False).mean()
    return macd, sig, macd - sig

def calc_bb(series, w=20, s=2):
    sma = series.rolling(w).mean()
    std = series.rolling(w).std()
    return sma + s * std, sma, sma - s * std

def fmt_cr(v):
    if not v:
        return "N/A"
    if abs(v) >= 1e12:
        return f"Rs.{v/1e12:.2f} L.Cr"
    return f"Rs.{v/1e7:,.2f} Cr"

def fmt_pct(v):
    return f"{v*100:.2f}%" if v else "N/A"

def safe(v, d=2):
    if v is None or (isinstance(v, float) and np.isnan(v)):
        return "N/A"
    return f"{v:,.{d}f}" if isinstance(v, float) else str(v)

@st.cache_data(ttl=180, show_spinner=False)
def fetch_data(sym, period):
    t = yf.Ticker(sym)
    info = dict(t.info)
    hist = t.history(period=period)
    try:
        actions = t.actions
    except Exception:
        actions = pd.DataFrame()
    try:
        news = t.news[:8]
    except Exception:
        news = []
    return info, hist, actions, news

# =============================================================
# 6. SIDEBAR
# =============================================================
with st.sidebar:
    st.markdown(
        f'<p style="font-family:Orbitron,monospace; font-size:15px; '
        f'color:#39FF14; font-weight:900; letter-spacing:2px;">PORTFOLIO</p>',
        unsafe_allow_html=True
    )
    st.markdown(
        f'<p style="color:#5a7a9a; font-size:12px;">User: {st.session_state["username"]}</p>',
        unsafe_allow_html=True
    )

    with st.expander("Add Holding"):
        ps = st.text_input("Symbol", value="SBIN", key="p_sym").upper().strip()
        pq = st.number_input("Qty", min_value=1, value=10, key="p_qty")
        pp = st.number_input("Avg Price (Rs.)", min_value=0.0, value=100.0, step=0.5, key="p_price")
        if st.button("Add", use_container_width=True):
            sym = ps if "." in ps else f"{ps}.NS"
            existing = [h for h in st.session_state['portfolio'] if h['symbol'] == sym]
            if existing:
                old = existing[0]
                total_qty = old['qty'] + pq
                old['avg_price'] = (old['avg_price'] * old['qty'] + pp * pq) / total_qty
                old['qty'] = total_qty
            else:
                st.session_state['portfolio'].append({
                    'symbol': sym, 'qty': pq, 'avg_price': pp
                })
            st.success(f"{ps} சேர்க்கப்பட்டது!")
            st.rerun()

    if st.session_state['portfolio']:
        total_inv = total_cur = 0.0
        for h in st.session_state['portfolio']:
            try:
                ltp = yf.Ticker(h['symbol']).fast_info.get('last_price') or 0
            except Exception:
                ltp = 0
            inv = h['avg_price'] * h['qty']
            cur = ltp * h['qty']
            pnl = cur - inv
            pct = pnl / inv * 100 if inv else 0
            total_inv += inv
            total_cur += cur
            clr = "#39FF14" if pnl >= 0 else "#FF4455"
            arr = "Up" if pnl >= 0 else "Down"
            st.markdown(f"""
            <div style="background:#080f18; border-radius:10px; padding:10px 12px;
                        margin-bottom:8px; border:1px solid #1a2535;">
                <div style="display:flex; justify-content:space-between;">
                    <span style="font-weight:800; font-size:14px; color:#dde6f0;">
                        {h['symbol'].replace('.NS','').replace('.BO','')}
                    </span>
                    <span style="color:{clr}; font-weight:800; font-size:13px;">
                        {arr} {abs(pct):.1f}%
                    </span>
                </div>
                <div style="color:#5a7a9a; font-size:11px;">
                    Qty: {h['qty']} | Avg: Rs.{h['avg_price']:.1f} | LTP: Rs.{ltp:.1f}
                </div>
                <div style="color:{clr}; font-size:12px; font-weight:700;">
                    P&amp;L: Rs.{pnl:+,.0f}
                </div>
            </div>
            """, unsafe_allow_html=True)

        total_pnl = total_cur - total_inv
        total_pct = total_pnl / total_inv * 100 if total_inv else 0
        clr = "#39FF14" if total_pnl >= 0 else "#FF4455"
        st.markdown(f"""
        <div style="background:linear-gradient(135deg,#080f18,#0d1f0d); border-radius:12px;
                    padding:14px; border:1px solid {clr}44; text-align:center; margin-top:4px;">
            <div class="m-label">Total P&amp;L</div>
            <div style="color:{clr}; font-family:Orbitron,monospace; font-size:20px; font-weight:900;">
                Rs.{total_pnl:+,.0f}
            </div>
            <div style="color:{clr}; font-size:14px;">({total_pct:+.2f}%)</div>
            <div style="color:#5a7a9a; font-size:11px; margin-top:4px;">
                Invested: Rs.{total_inv:,.0f} | Current: Rs.{total_cur:,.0f}
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Clear All Holdings", use_container_width=True):
            st.session_state['portfolio'] = []
            st.rerun()
    else:
        st.info("இன்னும் holdings சேர்க்கவில்லை.")

    st.markdown("---")

    st.markdown(
        '<p style="font-family:Orbitron,monospace; font-size:13px; '
        'color:#00D4FF; font-weight:700;">WATCHLIST</p>',
        unsafe_allow_html=True
    )
    wl_sym = st.text_input("Add to Watchlist", placeholder="INFY", key="wl_add")
    if st.button("+ Watch", use_container_width=True):
        s = wl_sym.upper().strip()
        if s and s not in st.session_state['watchlist']:
            st.session_state['watchlist'].append(s)
            st.rerun()

    if st.session_state['watchlist']:
        wl_html = "".join([
            f'<span class="watch-tag">{w}</span>'
            for w in st.session_state['watchlist']
        ])
        st.markdown(wl_html, unsafe_allow_html=True)
        if st.button("Clear Watchlist"):
            st.session_state['watchlist'] = []
            st.rerun()

    st.markdown("---")
    st.session_state['language'] = st.radio(
        "Language / Mozhi", ["Tamil", "English"], horizontal=True
    )
    if st.button("Logout", use_container_width=True):
        st.session_state['is_logged_in'] = False
        st.rerun()

# =============================================================
# 7. HEADER
# =============================================================
st.markdown("""
<div style="text-align:center; padding:12px 0 8px;">
    <p class="main-title">TAMIL INVEST HUB PRO</p>
    <p class="sub-title">Tamil Investment Platform - Created by Somasundaram - Live Market Data</p>
</div>
""", unsafe_allow_html=True)

# =============================================================
# 8. SEARCH BAR
# =============================================================
sc1, sc2, sc3 = st.columns([5, 1.5, 1.5])
with sc1:
    u_input = st.text_input(
        get_text("Search Symbol (eg: SBIN, RELIANCE, TCS, NIFTY50.NS)",
                 "Symbol தேடவும் (eg: SBIN, RELIANCE, TCS)"),
        value="RELIANCE",
        label_visibility="visible"
    ).upper().strip()

with sc2:
    period_map = {"1M": "1mo", "3M": "3mo", "6M": "6mo", "1Y": "1y", "2Y": "2y", "5Y": "5y"}
    period_label = st.selectbox(
        get_text("Period", "Kalam"),
        list(period_map.keys()),
        index=3
    )
    period = period_map[period_label]

with sc3:
    exchange = st.selectbox(
        get_text("Exchange", "Pangu Sandhai"),
        ["NSE (.NS)", "BSE (.BO)", "Manual"]
    )

if exchange == "NSE (.NS)":
    ticker_symbol = u_input if "." in u_input else f"{u_input}.NS"
elif exchange == "BSE (.BO)":
    ticker_symbol = u_input if "." in u_input else f"{u_input}.BO"
else:
    ticker_symbol = u_input

# =============================================================
# 9. TABS
# =============================================================
tabs = st.tabs([
    get_text("Chart", "Vilai Varapadam"),
    get_text("Indicators", "Thozilnutpam"),
    get_text("Rating", "Rating"),
    get_text("Financials", "Nidhinilai"),
    get_text("Shareholding", "Panguthaarar"),
    get_text("News", "Seithigal"),
    get_text("Actions", "Nigazhvugal"),
    get_text("About", "Niruvagam"),
])

# =============================================================
# 10. DATA FETCH + INDICATORS
# =============================================================
try:
    with st.spinner(get_text("Loading live data...", "Theravu Ertrugirathu...")):
        info, hist, actions, news_list = fetch_data(ticker_symbol, period)

    if hist.empty:
        st.error(
            f"'{ticker_symbol}' - theravu kidaikkavillai. "
            f"Symbol saripaaarkavum."
        )
        st.stop()

    close = hist['Close']
    hist['RSI']         = calc_rsi(close)
    hist['MACD'], hist['MACD_Sig'], hist['MACD_Hist'] = calc_macd(close)
    hist['BB_U'], hist['BB_M'], hist['BB_L'] = calc_bb(close)
    hist['EMA20']  = close.ewm(span=20).mean()
    hist['EMA50']  = close.ewm(span=50).mean()
    hist['EMA200'] = close.ewm(span=200).mean()
    hist['ATR']    = (hist['High'] - hist['Low']).rolling(14).mean()

    rsi_now    = hist['RSI'].iloc[-1]
    macd_now   = hist['MACD'].iloc[-1]
    sig_now    = hist['MACD_Sig'].iloc[-1]
    macd_bull  = macd_now > sig_now
    ltp        = (info.get('currentPrice')
                  or info.get('regularMarketPrice')
                  or float(close.iloc[-1]))
    prev_c     = (info.get('regularMarketPreviousClose')
                  or float(close.iloc[-2]))
    day_chg    = ltp - prev_c
    day_pct    = day_chg / prev_c * 100 if prev_c else 0
    ema50_val  = hist['EMA50'].iloc[-1]
    ema200_val = hist['EMA200'].iloc[-1]
    ema_bull   = ltp > ema50_val if not np.isnan(ema50_val) else False
    golden_x   = (ema50_val > ema200_val
                  if not (np.isnan(ema50_val) or np.isnan(ema200_val))
                  else False)
    atr_val    = hist['ATR'].iloc[-1]
    bb_u       = hist['BB_U'].iloc[-1]
    bb_l       = hist['BB_L'].iloc[-1]
    bb_pct     = ((ltp - bb_l) / (bb_u - bb_l) * 100
                  if (bb_u - bb_l) else 50)

    # ==========================================================
    # TAB 0 - CANDLESTICK CHART
    # ==========================================================
    with tabs[0]:
        name   = info.get('longName', ticker_symbol)
        sector = info.get('sector', '')
        st.markdown(
            f'<div style="font-size:20px; font-weight:800; color:#dde6f0; '
            f'margin-bottom:4px;">{name} '
            f'<span style="font-size:13px; color:#5a7a9a;">| {sector}</span></div>',
            unsafe_allow_html=True
        )

        chg_clr = "#39FF14" if day_chg >= 0 else "#FF4455"
        arr     = "UP" if day_chg >= 0 else "DOWN"

        st.markdown(f"""
        <div class="price-card">
            <div class="ltp-price">Rs.{ltp:,.2f}</div>
            <div class="ltp-change" style="color:{chg_clr}; margin-top:6px;">
                {arr} Rs.{abs(day_chg):.2f} ({day_pct:+.2f}%)
            </div>
            <div style="color:#5a7a9a; font-size:12px; margin-top:4px;">
                {get_text('Day Range','Inru')}: Rs.{info.get('regularMarketDayLow',0):,.2f}
                to Rs.{info.get('regularMarketDayHigh',0):,.2f}
                | Vol: {info.get('regularMarketVolume',0):,}
            </div>
        </div>
        """, unsafe_allow_html=True)

        s1, s2, s3, s4, s5 = st.columns(5)
        stats = [
            ("52W High", f"Rs.{info.get('fiftyTwoWeekHigh',0):,.2f}", "green"),
            ("52W Low",  f"Rs.{info.get('fiftyTwoWeekLow',0):,.2f}",  "red"),
            ("Mkt Cap",  fmt_cr(info.get("marketCap")),               "blue"),
            ("P/E",      safe(info.get("trailingPE")),                "gold"),
            ("ATR(14)",  f"Rs.{atr_val:.2f}",                        ""),
        ]
        for col, (lbl, val, clr) in zip([s1, s2, s3, s4, s5], stats):
            with col:
                st.markdown(
                    f'<div class="stat-card">'
                    f'<div class="stat-label">{lbl}</div>'
                    f'<div class="stat-value {clr}">{val}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

        st.markdown("")
        ov1, ov2 = st.columns([4, 1])
        with ov2:
            show_ema = st.checkbox("EMA Lines",  value=True)
            show_bb  = st.checkbox("Bollinger",  value=True)
            show_vol = st.checkbox("Volume",     value=True)

        rows_n = 2 if show_vol else 1
        row_h  = [0.73, 0.27] if show_vol else [1]

        fig = make_subplots(
            rows=rows_n, cols=1, shared_xaxes=True,
            vertical_spacing=0.02, row_heights=row_h
        )

        fig.add_trace(go.Candlestick(
            x=hist.index,
            open=hist['Open'], high=hist['High'],
            low=hist['Low'],   close=hist['Close'],
            increasing_line_color='#39FF14',
            decreasing_line_color='#FF4455',
            increasing_fillcolor='rgba(57,255,20,0.45)',
            decreasing_fillcolor='rgba(255,68,85,0.45)',
            name="Price"
        ), row=1, col=1)

        if show_ema:
            for span, clr, w in [(20,'#00D4FF',1.2),(50,'#FFD700',1.5),(200,'#FF69B4',1.8)]:
                k = f'EMA{span}'
                if k in hist.columns:
                    fig.add_trace(go.Scatter(
                        x=hist.index, y=hist[k], name=f"EMA{span}",
                        line=dict(color=clr, width=w)
                    ), row=1, col=1)

        if show_bb:
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist['BB_U'], name="BB Up",
                line=dict(color='rgba(150,150,150,0.5)', width=1, dash='dot'),
                showlegend=False
            ), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist['BB_L'], name="BB Lo",
                line=dict(color='rgba(150,150,150,0.5)', width=1, dash='dot'),
                fill='tonexty', fillcolor='rgba(150,150,150,0.04)',
                showlegend=False
            ), row=1, col=1)
            fig.add_trace(go.Scatter(
                x=hist.index, y=hist['BB_M'], name="BB Mid",
                line=dict(color='rgba(100,100,100,0.6)', width=1, dash='dash'),
                showlegend=False
            ), row=1, col=1)

        if show_vol:
            vol_clr = [
                'rgba(57,255,20,0.6)' if c >= o else 'rgba(255,68,85,0.6)'
                for c, o in zip(hist['Close'], hist['Open'])
            ]
            fig.add_trace(go.Bar(
                x=hist.index, y=hist['Volume'],
                name="Volume", marker_color=vol_clr
            ), row=2, col=1)
            fig.update_yaxes(
                title_text="Vol", row=2, col=1,
                title_font=dict(size=10)
            )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='#020509',
            plot_bgcolor='#080f18',
            height=580,
            margin=dict(t=10, b=10, l=8, r=8),
            xaxis_rangeslider_visible=False,
            legend=dict(orientation="h", yanchor="bottom", y=1.01, font=dict(size=11)),
            font=dict(family="Exo 2")
        )
        fig.update_xaxes(gridcolor='#10192a', zeroline=False)
        fig.update_yaxes(gridcolor='#10192a', zeroline=False)
        st.plotly_chart(fig, use_container_width=True)

    # ==========================================================
    # TAB 1 - TECHNICAL INDICATORS
    # ==========================================================
    with tabs[1]:
        st.markdown(
            f"### {get_text('Technical Indicators','Thozilnutpa Kurikkattingal')}"
        )

        fig2 = make_subplots(
            rows=2, cols=1, shared_xaxes=True,
            vertical_spacing=0.1, row_heights=[0.5, 0.5],
            subplot_titles=["RSI (14)", "MACD (12,26,9)"]
        )

        fig2.add_trace(go.Scatter(
            x=hist.index, y=hist['RSI'], name="RSI",
            line=dict(color='#00D4FF', width=2)
        ), row=1, col=1)
        fig2.add_hline(y=70, line_color='#FF4455', line_dash='dash', line_width=1.2, row=1, col=1)
        fig2.add_hline(y=30, line_color='#39FF14', line_dash='dash', line_width=1.2, row=1, col=1)
        fig2.add_hline(y=50, line_color='#444',    line_dash='dot',  line_width=1,   row=1, col=1)
        fig2.add_hrect(y0=30, y1=70, fillcolor='rgba(255,255,255,0.015)', line_width=0, row=1, col=1)

        hist_clr = [
            'rgba(57,255,20,0.7)' if v >= 0 else 'rgba(255,68,85,0.7)'
            for v in hist['MACD_Hist'].fillna(0)
        ]
        fig2.add_trace(go.Bar(
            x=hist.index, y=hist['MACD_Hist'],
            name="Histogram", marker_color=hist_clr, opacity=0.8
        ), row=2, col=1)
        fig2.add_trace(go.Scatter(
            x=hist.index, y=hist['MACD'], name="MACD",
            line=dict(color='#00D4FF', width=2)
        ), row=2, col=1)
        fig2.add_trace(go.Scatter(
            x=hist.index, y=hist['MACD_Sig'], name="Signal",
            line=dict(color='#FFD700', width=2)
        ), row=2, col=1)

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor='#020509', plot_bgcolor='#080f18',
            height=500, margin=dict(t=30, b=10, l=8, r=8),
            font=dict(family="Exo 2"),
            legend=dict(orientation="h", y=1.02, font=dict(size=11))
        )
        fig2.update_xaxes(gridcolor='#10192a')
        fig2.update_yaxes(gridcolor='#10192a')
        st.plotly_chart(fig2, use_container_width=True)

        st.markdown(f"#### {get_text('Live Signal Summary','Neradi Samignai Surukkam')}")

        rsi_zone = ("Overbought" if rsi_now > 70
                    else ("Oversold" if rsi_now < 30 else "Neutral"))
        rsi_bcls = ("badge-red" if rsi_now > 70
                    else ("badge-green" if rsi_now < 30 else "badge-blue"))
        bb_zone  = ("Near Upper" if bb_pct > 80
                    else ("Near Lower" if bb_pct < 20 else "Mid Band"))
        bb_bcls  = ("badge-red" if bb_pct > 80
                    else ("badge-green" if bb_pct < 20 else "badge-blue"))
        gx_txt   = "Golden Cross" if golden_x else "Death Cross"
        gx_bcls  = "badge-gold" if golden_x else "badge-red"

        ind_cards = [
            ("RSI (14)",     f"{rsi_now:.1f}",    rsi_zone,                                           rsi_bcls),
            ("MACD",         f"{macd_now:.3f}",   "Bullish" if macd_bull else "Bearish",              "badge-green" if macd_bull else "badge-red"),
            ("Bollinger %B", f"{bb_pct:.1f}%",    bb_zone,                                            bb_bcls),
            ("EMA50 Trend",  f"Rs.{ema50_val:,.1f}", "Above EMA" if ema_bull else "Below EMA",       "badge-green" if ema_bull else "badge-red"),
            ("EMA Cross",    "50 vs 200",          gx_txt,                                             gx_bcls),
            ("ATR (14)",     f"Rs.{atr_val:.2f}", "Volatility Measure",                               "badge-blue"),
        ]

        c1, c2, c3 = st.columns(3)
        for i, (nm, vl, zn, bc) in enumerate(ind_cards):
            with [c1, c2, c3][i % 3]:
                st.markdown(f"""
                <div class="section-card" style="text-align:center; margin-bottom:12px;">
                    <div class="m-label" style="font-size:13px;">{nm}</div>
                    <div style="font-family:Orbitron,monospace; font-size:22px; font-weight:900;
                                color:#dde6f0; margin:8px 0;">{vl}</div>
                    <span class="badge {bc}">{zn}</span>
                </div>
                """, unsafe_allow_html=True)

    # ==========================================================
    # TAB 2 - RATING ENGINE
    # ==========================================================
    with tabs[2]:
        st.markdown(f"### {get_text('AI Rating Engine','AI Mathipeettu Iyanthiram')}")

        roe        = (info.get('returnOnEquity') or 0) * 100
        debt       = info.get('debtToEquity') or 999
        net_margin = (info.get('profitMargins') or 0) * 100
        rev_growth = (info.get('revenueGrowth') or 0) * 100
        eps_growth = (info.get('earningsGrowth') or 0) * 100
        cur_ratio  = info.get('currentRatio') or 0

        # Fundamental (40 pts)
        f1 = min(15, max(0, roe / 25 * 15))
        f2 = 12 if debt < 50 else (8 if debt < 100 else (4 if debt < 200 else 0))
        f3 = min(8, max(0, net_margin / 20 * 8))
        f4 = 5 if cur_ratio > 1.5 else (3 if cur_ratio > 1 else 0)
        fund = f1 + f2 + f3 + f4

        # Technical (40 pts)
        t1 = 12 if 40 <= rsi_now <= 60 else (8 if 30 <= rsi_now <= 70 else 0)
        t2 = 14 if macd_bull else 0
        t3 = 8  if ema_bull  else 0
        t4 = 6  if golden_x  else 0
        tech = t1 + t2 + t3 + t4

        # Growth (20 pts)
        g1 = min(10, max(0, rev_growth / 20 * 10)) if rev_growth > 0 else 0
        g2 = min(10, max(0, eps_growth / 20 * 10)) if eps_growth > 0 else 0
        growth = g1 + g2

        total      = fund + tech + growth
        total_pct  = int(total)

        if total_pct >= 70:
            clr  = "#39FF14"
            rec  = get_text("STRONG BUY", "Valuvaga Vaangalam")
            detail = get_text(
                "Excellent fundamentals and bullish technicals.",
                "Sirantha adipppadai & Erppa Pokku."
            )
        elif total_pct >= 55:
            clr  = "#00FFD1"
            rec  = get_text("BUY", "Vaangalam")
            detail = get_text(
                "Good signals. Accumulate gradually.",
                "Nalla Samignaigal. Padippadadiyaga segarikkalaam."
            )
        elif total_pct >= 40:
            clr  = "#FFD700"
            rec  = get_text("HOLD", "Vaithirukkalaam")
            detail = get_text(
                "Mixed signals. Wait for confirmation.",
                "Kalappu Samignaigal. Uruthipaduthalukkaaga Kaathtirungal."
            )
        else:
            clr  = "#FF4455"
            rec  = get_text("AVOID", "Thavirkavum")
            detail = get_text(
                "Weak signals. High risk zone.",
                "Palaveenamana Samignaigal. Athika Aapathu."
            )

        r1, r2 = st.columns([1, 1.2])

        with r1:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=total_pct,
                number={
                    'font': {'size': 52, 'family': 'Orbitron', 'color': clr},
                    'suffix': ''
                },
                gauge={
                    'axis': {'range': [0, 100], 'tickcolor': '#5a7a9a', 'tickfont': {'size': 12}},
                    'bar': {'color': clr, 'thickness': 0.25},
                    'bgcolor': '#080f18',
                    'bordercolor': '#1a2535',
                    'steps': [
                        {'range': [0,  40],  'color': 'rgba(255,68,85,0.15)'},
                        {'range': [40, 55],  'color': 'rgba(255,215,0,0.1)'},
                        {'range': [55, 70],  'color': 'rgba(0,255,209,0.1)'},
                        {'range': [70, 100], 'color': 'rgba(57,255,20,0.15)'},
                    ],
                    'threshold': {
                        'line': {'color': clr, 'width': 4},
                        'thickness': 0.8,
                        'value': total_pct
                    }
                },
                title={
                    'text': f"<b>{rec}</b>",
                    'font': {'size': 16, 'color': clr, 'family': 'Exo 2'}
                }
            ))
            fig_g.update_layout(
                paper_bgcolor='#020509', height=300,
                margin=dict(t=30, b=10, l=20, r=20),
                font=dict(family="Exo 2")
            )
            st.plotly_chart(fig_g, use_container_width=True)
            st.markdown(
                f'<div style="text-align:center; color:#5a7a9a; font-size:13px;">{detail}</div>',
                unsafe_allow_html=True
            )

        with r2:
            st.markdown('<div class="section-card">', unsafe_allow_html=True)
            categories = [
                ("Fundamental", fund, 40, [
                    (f"ROE: {roe:.1f}%",          f"+{f1:.0f}"),
                    (f"Debt/Eq: {debt:.0f}",       f"+{f2:.0f}"),
                    (f"Net Margin: {net_margin:.1f}%", f"+{f3:.0f}"),
                    (f"Current Ratio: {cur_ratio:.1f}", f"+{f4:.0f}"),
                ]),
                ("Technical", tech, 40, [
                    (f"RSI: {rsi_now:.1f}",         f"+{t1:.0f}"),
                    (f"MACD: {'Bull' if macd_bull else 'Bear'}", f"+{t2:.0f}"),
                    (f"EMA50: {'Above' if ema_bull else 'Below'}", f"+{t3:.0f}"),
                    (f"Cross: {'Golden' if golden_x else 'Death'}", f"+{t4:.0f}"),
                ]),
                ("Growth", growth, 20, [
                    (f"Rev Growth: {rev_growth:.1f}%", f"+{g1:.0f}"),
                    (f"EPS Growth: {eps_growth:.1f}%", f"+{g2:.0f}"),
                ]),
            ]

            for cat_name, score, mx, factors in categories:
                pct2 = int(score / mx * 100)
                bclr = ("#39FF14" if pct2 >= 65
                        else ("#FFD700" if pct2 >= 40 else "#FF4455"))
                st.markdown(f"""
                <div style="margin-bottom:16px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="font-weight:800; font-size:14px;">{cat_name}</span>
                        <span style="font-family:Orbitron,monospace; color:{bclr};
                                    font-size:14px; font-weight:700;">{int(score)}/{mx}</span>
                    </div>
                    <div style="background:#10192a; border-radius:8px; height:10px; margin-bottom:6px;">
                        <div style="background:{bclr}; width:{pct2}%; height:10px; border-radius:8px;"></div>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:6px;">
                """, unsafe_allow_html=True)
                for fn, fp in factors:
                    st.markdown(
                        f'<span style="background:#10192a; border-radius:6px; padding:2px 8px; '
                        f'font-size:11px; color:#5a7a9a;">{fn} '
                        f'<span style="color:{bclr}; font-weight:700;">{fp}</span></span>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div></div>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"#### {get_text('Target Price Estimate','Ilakku Vilai Mathipeedu')}")
        tp_c1, tp_c2, tp_c3 = st.columns(3)
        conservative = ltp * 1.08
        moderate     = ltp * 1.15
        aggressive   = ltp * 1.25

        for col, (lbl, tp, clr2) in zip([tp_c1, tp_c2, tp_c3], [
            (get_text("Conservative", "Echcharikkai"),  conservative, "#FFD700"),
            (get_text("Moderate",     "Mithamana"),     moderate,     "#00D4FF"),
            (get_text("Aggressive",   "Theeviramana"),  aggressive,   "#39FF14"),
        ]):
            with col:
                st.markdown(f"""
                <div class="stat-card" style="border:1px solid {clr2}33;">
                    <div class="stat-label">{lbl} (1Y)</div>
                    <div style="font-family:Orbitron,monospace; font-size:20px;
                                color:{clr2}; font-weight:900;">Rs.{tp:,.2f}</div>
                    <div style="color:#5a7a9a; font-size:11px;">+{(tp/ltp-1)*100:.1f}% upside</div>
                </div>
                """, unsafe_allow_html=True)

    # ==========================================================
    # TAB 3 - FINANCIALS
    # ==========================================================
    with tabs[3]:
        st.markdown(f"### {get_text('Key Financial Metrics','Mukkiya Nithi Vivarangal')}")

        fin_data = {
            get_text("Income", "Varumaanam"): [
                ("Revenue (TTM)",    fmt_cr(info.get("totalRevenue"))),
                ("Net Profit (TTM)", fmt_cr(info.get("netIncomeToCommon"))),
                ("Gross Profit",     fmt_cr(info.get("grossProfits"))),
                ("EBITDA",           fmt_cr(info.get("ebitda"))),
                ("Free Cash Flow",   fmt_cr(info.get("freeCashflow"))),
                ("Operating CF",     fmt_cr(info.get("operatingCashflow"))),
            ],
            get_text("Valuation", "Mathipeedu"): [
                ("Market Cap",       fmt_cr(info.get("marketCap"))),
                ("Enterprise Value", fmt_cr(info.get("enterpriseValue"))),
                ("P/E (TTM)",        safe(info.get("trailingPE"))),
                ("P/E (Fwd)",        safe(info.get("forwardPE"))),
                ("P/B Ratio",        safe(info.get("priceToBook"))),
                ("EV/EBITDA",        safe(info.get("enterpriseToEbitda"))),
            ],
            get_text("Health", "Aarokkiyam"): [
                ("ROE",              fmt_pct(info.get("returnOnEquity"))),
                ("ROA",              fmt_pct(info.get("returnOnAssets"))),
                ("Debt/Equity",      safe(info.get("debtToEquity"))),
                ("Total Debt",       fmt_cr(info.get("totalDebt"))),
                ("Cash & Equiv.",    fmt_cr(info.get("totalCash"))),
                ("Current Ratio",    safe(info.get("currentRatio"))),
            ],
        }

        fc1, fc2, fc3 = st.columns(3)
        for col, (section, rows) in zip([fc1, fc2, fc3], fin_data.items()):
            with col:
                st.markdown(
                    f'<div class="section-card">'
                    f'<p style="font-size:15px;font-weight:800;color:#00D4FF;margin-bottom:8px;">'
                    f'{section}</p>',
                    unsafe_allow_html=True
                )
                for lbl, val in rows:
                    st.markdown(
                        f'<div class="metric-row">'
                        f'<span class="m-label">{lbl}</span>'
                        f'<span class="m-value">{val}</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
                st.markdown('</div>', unsafe_allow_html=True)

        st.markdown(f"**{get_text('Per Share & Dividend','Pangu & Eevuthogai')}**")
        ps1, ps2, ps3, ps4, ps5 = st.columns(5)
        per_share = [
            ("EPS (TTM)", f"Rs.{safe(info.get('trailingEps'))}"),
            ("EPS (Fwd)", f"Rs.{safe(info.get('forwardEps'))}"),
            ("Book Value",f"Rs.{safe(info.get('bookValue'))}"),
            ("Div/Share", f"Rs.{safe(info.get('dividendRate'))}"),
            ("Div Yield",   fmt_pct(info.get("dividendYield"))),
        ]
        for col, (lbl, val) in zip([ps1, ps2, ps3, ps4, ps5], per_share):
            with col:
                st.markdown(
                    f'<div class="stat-card">'
                    f'<div class="stat-label">{lbl}</div>'
                    f'<div class="stat-value blue">{val}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ==========================================================
    # TAB 4 - SHAREHOLDING
    # ==========================================================
    with tabs[4]:
        p_pct   = (info.get('heldPercentInsiders') or 0) * 100
        i_pct   = (info.get('heldPercentInstitutions') or 0) * 100
        pub_pct = max(0, 100 - p_pct - i_pct)

        fig3 = go.Figure(data=[go.Pie(
            labels=['Promoters', 'Institutions/FII', 'Public'],
            values=[p_pct, i_pct, pub_pct],
            hole=0.65,
            marker=dict(
                colors=['#1A73E8', '#00C853', '#FFAB00'],
                line=dict(color='#020509', width=3)
            ),
            textfont=dict(size=13, family="Exo 2"),
            textinfo='label+percent',
        )])
        fig3.add_annotation(
            text=f"<b>{info.get('longName','')[:10]}</b>",
            x=0.5, y=0.5,
            font=dict(size=12, color='#dde6f0'),
            showarrow=False
        )
        fig3.update_layout(
            template="plotly_dark",
            paper_bgcolor='#020509', height=400,
            margin=dict(t=20, b=30),
            font=dict(family="Exo 2"),
            legend=dict(orientation="h", y=-0.1, font=dict(size=13))
        )
        st.plotly_chart(fig3, use_container_width=True)

        sh1, sh2, sh3 = st.columns(3)
        for col, (lbl, val, clr2) in zip([sh1, sh2, sh3], [
            ("Promoters",        f"{p_pct:.2f}%",   "#1A73E8"),
            ("Institutions/FII", f"{i_pct:.2f}%",   "#00C853"),
            ("Public",           f"{pub_pct:.2f}%",  "#FFAB00"),
        ]):
            with col:
                st.markdown(
                    f'<div class="stat-card" style="border:1px solid {clr2}44;">'
                    f'<div class="stat-label">{lbl}</div>'
                    f'<div style="font-family:Orbitron,monospace; font-size:26px; '
                    f'color:{clr2}; font-weight:900;">{val}</div>'
                    f'</div>',
                    unsafe_allow_html=True
                )

    # ==========================================================
    # TAB 5 - NEWS
    # ==========================================================
    with tabs[5]:
        st.markdown(
            f"### {get_text('Latest News','Sameepatthiya Seithigal')} - "
            f"{info.get('longName','')}"
        )
        if news_list:
            for n in news_list:
                title     = n.get('title', 'No title')
                publisher = n.get('publisher', '')
                link      = n.get('link', '#')
                pub_time  = n.get('providerPublishTime', 0)
                try:
                    time_str = datetime.fromtimestamp(pub_time).strftime(
                        "%d %b %Y, %I:%M %p"
                    )
                except Exception:
                    time_str = ''
                st.markdown(f"""
                <div class="news-card">
                    <div class="news-title">
                        <a href="{link}" target="_blank"
                           style="color:#dde6f0; text-decoration:none;">{title}</a>
                    </div>
                    <div class="news-meta">
                        Publisher: {publisher} | Time: {time_str}
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info(get_text(
                "No news available for this stock.",
                "Inda Pangirkku Seithigal Kidaikkavillai."
            ))

    # ==========================================================
    # TAB 6 - CORPORATE ACTIONS
    # ==========================================================
    with tabs[6]:
        st.markdown(f"### {get_text('Corporate Actions','Niruvaga Nigazhvugal')}")
        if not actions.empty:
            disp = actions.sort_index(ascending=False).head(20).copy()
            disp.index = disp.index.strftime("%d %b %Y")
            st.dataframe(disp, use_container_width=True)

            if 'Dividends' in actions.columns:
                div_h = actions[actions['Dividends'] > 0]['Dividends']
                if not div_h.empty:
                    st.markdown(f"#### {get_text('Dividend History','Eevuthogai Varalaru')}")
                    fig4 = go.Figure(go.Bar(
                        x=div_h.index, y=div_h.values,
                        marker_color='#FFD700', opacity=0.9
                    ))
                    fig4.update_layout(
                        template="plotly_dark",
                        paper_bgcolor='#020509', plot_bgcolor='#080f18',
                        height=280, margin=dict(t=10, b=10),
                        yaxis_title="Rs./share",
                        font=dict(family="Exo 2")
                    )
                    fig4.update_xaxes(gridcolor='#10192a')
                    fig4.update_yaxes(gridcolor='#10192a')
                    st.plotly_chart(fig4, use_container_width=True)
        else:
            st.info(get_text(
                "No corporate actions found.",
                "Niruvaga Nigazhvugal Kidaikkavillai."
            ))

    # ==========================================================
    # TAB 7 - ABOUT
    # ==========================================================
    with tabs[7]:
        st.markdown(f"### {get_text('About Company','Niruvagam Parri')}")
        about_raw = info.get('longBusinessSummary', 'No description available.')

        # Try translation - if deep_translator not installed, show English
        try:
            from deep_translator import GoogleTranslator
            if st.session_state['language'] == "Tamil":
                with st.spinner(get_text("Translating...", "Mozhipeyarkkipathu...")):
                    try:
                        display_text = GoogleTranslator(
                            source='auto', target='ta'
                        ).translate(about_raw)
                    except Exception:
                        display_text = about_raw
            else:
                display_text = about_raw
        except ImportError:
            display_text = about_raw

        st.markdown(
            f'<div class="section-card" style="font-size:15px; line-height:1.8;">'
            f'{display_text}</div>',
            unsafe_allow_html=True
        )

        st.markdown(f"**{get_text('Company Details','Niruvaga Vivarangal')}**")
        cd1, cd2 = st.columns(2)
        left_d = [
            ("Sector",   info.get("sector",   "N/A")),
            ("Industry", info.get("industry", "N/A")),
            ("Country",  info.get("country",  "N/A")),
            ("Exchange", info.get("exchange", "N/A")),
        ]
        right_d = [
            ("Employees", f"{info.get('fullTimeEmployees', 0):,}"),
            ("Website",   info.get("website",        "N/A")),
            ("Currency",  info.get("currency",       "N/A")),
            ("Fiscal YE", info.get("lastFiscalYearEnd", "N/A")),
        ]
        with cd1:
            for l, v in left_d:
                st.markdown(
                    f'<div class="metric-row">'
                    f'<span class="m-label">{l}</span>'
                    f'<span class="m-value">{v}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )
        with cd2:
            for l, v in right_d:
                st.markdown(
                    f'<div class="metric-row">'
                    f'<span class="m-label">{l}</span>'
                    f'<span class="m-value">{v}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

except Exception as e:
    st.error(f"Pizhai (Error): {e}")
    st.info(
        "Symbol sariyaga ullidavum. "
        "Utharanam (Example): SBIN, RELIANCE, TCS, INFY"
    )

# =============================================================
# FOOTER
# =============================================================
st.markdown("""
<div style="text-align:center; margin-top:60px; padding:20px 0; border-top:1px solid #1a2535;">
    <p style="color:#1a2535; font-size:11px; font-family:Orbitron,monospace; letter-spacing:2px;">
        2026 TAMIL INVEST HUB PRO - CREATED BY SOMASUNDARAM -
        FOR EDUCATIONAL PURPOSES ONLY - NOT FINANCIAL ADVICE
    </p>
</div>
""", unsafe_allow_html=True)
