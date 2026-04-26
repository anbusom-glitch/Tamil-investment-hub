# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

# 1. PAGE CONFIG
st.set_page_config(page_title="TAMIL WEALTH CALC", page_icon="🧮", layout="wide")

# 2. CSS STYLING (Clean Fonts for Numbers)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Exo+2:wght@400;600;700;800&family=Orbitron:wght@900&display=swap');

html, body, [class*="css"] {
    background-color: #020509 !important;
    color: #dde6f0;
    font-family: 'Exo 2', sans-serif;
}

.main-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 32px !important;
    font-weight: 900;
    background: linear-gradient(90deg, #FFD700 0%, #00FFD1 50%, #39FF14 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-align: center;
    margin: 0;
}

.sub-title { text-align: center; color: #5a7a9a; font-size: 13px; letter-spacing: 3px; margin-bottom: 25px; }

.calc-card {
    background: #080f18;
    padding: 25px;
    border-radius: 18px;
    border: 1px solid #1a2535;
    margin-bottom: 20px;
}

.metric-row {
    display: flex;
    justify-content: space-between;
    padding: 15px 0;
    border-bottom: 1px solid #111d2a;
}

.m-label { color: #5a7a9a; font-size: 15px; font-weight: 600; }
.m-value { color: #39FF14; font-size: 18px; font-weight: 800; }

.result-card {
    background: linear-gradient(135deg, #0a1628 0%, #0d1f0d 100%);
    padding: 30px;
    border-radius: 18px;
    border: 1px solid rgba(57,255,20,0.3);
    text-align: center;
}

.total-value { font-size: 45px !important; font-weight: 800; color: #39FF14; }
</style>
""", unsafe_allow_html=True)

# 3. HEADER
st.markdown('<p class="main-title">TAMIL WEALTH CALC</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">CREATED BY SOMASUNDARAM - முதலீட்டுத் திட்டமிடல்</p>', unsafe_allow_html=True)

# 4. TABS FOR DIFFERENT CALCULATORS
tab1, tab2, tab3 = st.tabs(["SIP Calculator", "Lumpsum Calculator", "Goal Planner"])

# --- TAB 1: SIP CALCULATOR ---
with tab1:
    st.markdown("### மாதவாரி முதலீடு (SIP)")
    c1, c2 = st.columns([1.5, 2])
    
    with c1:
        st.markdown('<div class="calc-card">', unsafe_allow_html=True)
        monthly_investment = st.number_input("மாதாந்திர முதலீடு (Rs.)", min_value=500, value=5000, step=500)
        expected_return = st.slider("எதிர்பார்க்கும் லாபம் (%)", 1.0, 30.0, 12.0)
        years = st.slider("காலம் (ஆண்டுகள்)", 1, 40, 10)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # SIP Formula
        i = (expected_return / 100) / 12
        n = years * 12
        total_value = monthly_investment * ((((1 + i)**n) - 1) / i) * (1 + i)
        invested_amt = monthly_investment * n
        wealth_gain = total_value - invested_amt
        
    with c2:
        st.markdown(f"""
        <div class="result-card">
            <div style="color:#5a7a9a; font-size:16px;">முதிர்வுத் தொகை (Maturity Value)</div>
            <div class="total-value">Rs.{total_value:,.0f}</div>
            <div class="metric-row"><span class="m-label">முதலீடு செய்த தொகை</span><span class="m-value" style="color:#eaf2ff;">Rs.{invested_amt:,.0f}</span></div>
            <div class="metric-row"><span class="m-label">கிடைத்த லாபம்</span><span class="m-value">Rs.{wealth_gain:,.0f}</span></div>
        </div>
        """, unsafe_allow_html=True)
        
        # Pie Chart for Visualization
        fig = go.Figure(data=[go.Pie(labels=['முதலீடு', 'லாபம்'], values=[invested_amt, wealth_gain], hole=.4, marker_colors=['#00D4FF', '#39FF14'])])
        fig.update_layout(template="plotly_dark", paper_bgcolor='#020509', margin=dict(t=0,b=0,l=0,r=0))
        st.plotly_chart(fig, use_container_width=True)

# --- TAB 2: LUMPSUM CALCULATOR ---
with tab2:
    st.markdown("### மொத்த முதலீடு (Lumpsum)")
    cl1, cl2 = st.columns([1.5, 2])
    
    with cl1:
        st.markdown('<div class="calc-card">', unsafe_allow_html=True)
        lumpsum_investment = st.number_input("முதலீட்டுத் தொகை (Rs.)", min_value=1000, value=100000, step=5000)
        l_expected_return = st.slider("எதிர்பார்க்கும் லாபம் (%) ", 1.0, 30.0, 12.0)
        l_years = st.slider("காலம் (ஆண்டுகள்) ", 1, 40, 10)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Lumpsum Formula
        l_total_value = lumpsum_investment * (1 + (l_expected_return/100))**l_years
        l_wealth_gain = l_total_value - lumpsum_investment
        
    with cl2:
        st.markdown(f"""
        <div class="result-card">
            <div style="color:#5a7a9a; font-size:16px;">மொத்தத் தொகை</div>
            <div class="total-value">Rs.{l_total_value:,.0f}</div>
            <div class="metric-row"><span class="m-label">முதலீடு செய்த தொகை</span><span class="m-value" style="color:#eaf2ff;">Rs.{lumpsum_investment:,.0f}</span></div>
            <div class="metric-row"><span class="m-label">கிடைத்த லாபம்</span><span class="m-value">Rs.{l_wealth_gain:,.0f}</span></div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: GOAL PLANNER ---
with tab3:
    st.markdown("### இலக்குத் திட்டமிடல் (Goal Planner)")
    cg1, cg2 = st.columns([1.5, 2])
    
    with cg1:
        st.markdown('<div class="calc-card">', unsafe_allow_html=True)
        target_amount = st.number_input("உங்கள் இலக்குத் தொகை (Rs.)", min_value=100000, value=5000000, step=100000)
        g_years = st.slider("காலம் (எத்தனை ஆண்டுகளில்?)", 1, 40, 15)
        g_return = st.slider("எதிர்பார்க்கும் லாபம் (%)  ", 1.0, 30.0, 12.0)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Required SIP Formula
        r = (g_return / 100) / 12
        n_months = g_years * 12
        required_sip = target_amount / ((( (1 + r)**n_months ) - 1) / r * (1 + r))
        
    with cg2:
        st.markdown(f"""
        <div class="result-card">
            <div style="color:#5a7a9a; font-size:16px;">ஒவ்வொரு மாதமும் நீங்கள் சேமிக்க வேண்டியது</div>
            <div class="total-value" style="color:#00D4FF;">Rs.{required_sip:,.0f}</div>
            <p style="color:#5a7a9a; margin-top:15px;">{g_years} ஆண்டுகளில் {target_amount:,.0f} ரூபாயை அடைய மாதம் Rs.{required_sip:,.0f} முதலீடு செய்ய வேண்டும்.</p>
        </div>
        """, unsafe_allow_html=True)

# 5. FOOTER
st.markdown('<div style="text-align:center; padding:30px; border-top:1px solid #1a2535; font-size:12px; color:#5a7a9a;">2026 TAMIL WEALTH CALC - Created by Somasundaram</div>', unsafe_allow_html=True)
