# -*- coding: utf-8 -*-
# =============================================================
# TAMIL INVEST HUB PRO - Created by Somasundaram
# Integrated Full Version - 52W Range Bar & Buy/Sell %
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
}

.sub-title {
    font-size: 11px !important;
    color: #5a7a9a;
    letter-spacing: 5px;
    text-transform: uppercase;
    margin-top: 2px;
}

.price-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 22px 28px;
    border-radius: 18px;
    border: 1px solid rgba(57,255,20,0.25);
    margin-bottom: 18px;
    text-align: center;
}

.ltp-price {
    font-family: 'Orbitron', monospace;
    font-size: 42px !important;
    color: #39FF14;
    line-height: 1;
}

/* 52W Range Bar Styling */
.range-container {
    background: #111d2a;
    height: 10px;
    border-radius: 10px;
    width: 100%;
    position: relative;
    margin: 15px 0 5px 0;
    border: 1px solid #1a2535;
}
.range-bar-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #FF4455 0%, #FFD700 50%, #39FF14 100%);
}
.range-marker {
    position: absolute;
    top: -5px;
    width: 4px;
    height: 20px;
    background: white;
    border-radius: 2px;
    box-shadow: 0 0 8px #fff;
    transform: translateX(-50%);
}

.section-card {
    background: #080f18;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #1a2535;
    margin-bottom: 16px;
}

.stat-card {
    background: #080f18;
    border-radius: 14px;
    border: 1px solid #1a2535;
    padding: 16px;
    text-align: center;
}

.stat-label { color: #5a7a9a; font-size: 11px; text-transform: uppercase; font-weight: 700; margin-bottom: 6px;}
.stat-value { font-family: 'Orbitron', monospace; font-size: 16px; font-weight: 700; }
.green { color: #39FF14 !important; }
.red   { color: #FF4455 !important; }
.blue  { color: #00D4FF !important; }
.gold  { color: #FFD700 !important; }

.big-score {
    font-family: 'Orbitron', monospace;
    font-size: 64px !important;
    font-weight: 900;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #111d2a;
}
.m-label { color: #5a7a9a; font-size: 12px; }
.m-value { color: #eaf2ff; font-family: 'Orbitron'; font-size: 13px; }
</style
