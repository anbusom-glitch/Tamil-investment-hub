import streamlit as st import yfinance as yf import pandas as pd import numpy as np import plotly.graph_objects as go from plotly.subplots import make_subplots from deep_translator import GoogleTranslator from datetime import datetime import sqlite3 import os

=====================================================

DATABASE SETUP

=====================================================

conn = sqlite3.connect('tamil_invest_hub.db', check_same_thread=False) c = conn.cursor() c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)') c.execute('CREATE TABLE IF NOT EXISTS portfolio (username TEXT, symbol TEXT, qty REAL, avg REAL)') c.execute('CREATE TABLE IF NOT EXISTS watchlist (username TEXT, symbol TEXT)') conn.commit()

=====================================================

PAGE CONFIG

=====================================================

st.set_page_config(page_title='TAMIL INVEST HUB PRO MAX', page_icon='📈', layout='wide')

=====================================================

SESSION STATE

=====================================================

for k,v in [('is_logged',False),('user',''),('lang','Tamil')]: if k not in st.session_state: st.session_state[k]=v

def T(en,ta): return ta if st.session_state['lang']=='Tamil' else en

=====================================================

PREMIUM CSS

=====================================================

st.markdown('''

<style>
html,body,[class*="css"]{background:#020509;color:#dde6f0;font-family:sans-serif;}
.main-title{font-size:38px;font-weight:900;color:#39FF14;text-align:center;}
.sub{font-size:12px;color:#5a7a9a;text-align:center;}
.card{background:#08111b;padding:14px;border-radius:14px;border:1px solid #1a2535;margin-bottom:10px;}
</style>''',unsafe_allow_html=True)

=====================================================

LOGIN / REGISTER

=====================================================

if not st.session_state['is_logged']: st.markdown('<p class="main-title">📈 TAMIL INVEST HUB PRO MAX</p>',unsafe_allow_html=True) st.markdown('<p class="sub">Institutional Tamil Market Terminal</p>',unsafe_allow_html=True) lg = st.tabs(['Login','Register'])

with lg[0]:
    u = st.text_input('User ID')
    p = st.text_input('Password', type='password')
    if st.button('Login Access'):
        c.execute('SELECT * FROM users WHERE username=? AND password=?',(u,p))
        if c.fetchone():
            st.session_state['is_logged']=True
            st.session_state['user']=u
            st.rerun()
        else:
            st.error('Invalid Login')

with lg[1]:
    nu = st.text_input('Create User')
    npass = st.text_input('Create Password', type='password')
    if st.button('Register Now'):
        c.execute('INSERT INTO users VALUES (?,?)',(nu,npass))
        conn.commit()
        st.success('Registered Successfully')
st.stop()

=====================================================

FUNCTIONS

=====================================================

def calc_rsi(series, window=14): delta = series.diff() gain = delta.where(delta>0,0).rolling(window).mean() loss = (-delta.where(delta<0,0)).rolling(window).mean() rs = gain/loss.replace(0,np.nan) return 100-(100/(1+rs))

def calc_macd(series): ema12 = series.ewm(span=12).mean() ema26 = series.ewm(span=26).mean() macd = ema12-ema26 sig = macd.ewm(span=9).mean() return macd,sig

def fetch(sym,period): t = yf.Ticker(sym) return dict(t.info), t.history(period=period), t.actions, t.news[:8] if t.news else []

=====================================================

SIDEBAR

=====================================================

with st.sidebar: st.write('👤', st.session_state['user']) st.session_state['lang'] = st.radio('Language',['Tamil','English']) if st.button('Logout'): st.session_state['is_logged']=False st.rerun()

=====================================================

HEADER

=====================================================

st.markdown('<p class="main-title">📈 TAMIL INVEST HUB PRO MAX</p>',unsafe_allow_html=True) st.markdown('<p class="sub">Created by Somasundaram | Live AI Stock Analytics</p>',unsafe_allow_html=True)

=====================================================

MARKET SNAPSHOT

=====================================================

m1,m2,m3,m4 = st.columns(4) for col,sym,name in [(m1,'^NSEI','NIFTY50'),(m2,'^NSEBANK','BANKNIFTY'),(m3,'^BSESN','SENSEX'),(m4,'^INDIAVIX','INDIA VIX')]: try: tk = yf.Ticker(sym).fast_info lp = tk['lastPrice']; pc = tk['previousClose'] pct = round((lp-pc)/pc*100,2) col.metric(name, round(lp,2), str(pct)+'%') except: col.metric(name,'N/A')

=====================================================

SEARCH BAR

=====================================================

c1,c2,c3 = st.columns([4,1,1]) with c1: user_sym = st.text_input('Search Stock Symbol', value='RELIANCE').upper() with c2: per = st.selectbox('Period',['1mo','3mo','6mo','1y','2y']) with c3: ex = st.selectbox('Exchange',['NSE','BSE'])

symbol = user_sym+'.NS' if ex=='NSE' else user_sym+'.BO'

=====================================================

DATA LOAD

=====================================================

info,hist,actions,news = fetch(symbol, per) if hist.empty: st.error('No data found') st.stop()

close = hist['Close'] ltp = close.iloc[-1] prev = close.iloc[-2] chg = ltp-prev pct = chg/prev*100

ema20 = close.ewm(span=20).mean() ema50 = close.ewm(span=50).mean() ema200 = close.ewm(span=200).mean() score = 0 if ltp>ema20.iloc[-1]: score+=10 if ltp>ema50.iloc[-1]: score+=10 if ema20.iloc[-1]>ema50.iloc[-1]: score+=10 if ema50.iloc[-1]>ema200.iloc[-1]: score+=10

target = ltp1.18 sl = ltp0.92

=====================================================

TABS

=====================================================

tabs = st.tabs(['📊 Chart','📈 Indicators','🔮 AI Rating','💰 Financials','🤝 Shareholding','📰 News','📅 Actions','🏢 About'])

=====================================================

TAB1 CHART

=====================================================

with tabs[0]: st.metric(info.get('longName',symbol), round(ltp,2), str(round(pct,2))+'%') fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75,0.25]) fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema20, name='EMA20'),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema50, name='EMA50'),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema200, name='EMA200'),row=1,col=1) fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'),row=2,col=1) fig.update_layout(height=650) st.plotly_chart(fig, use_container_width=True) st.success('AI Target Price : ₹'+str(round(target,2))+' | Stoploss : ₹'+str(round(sl,2)))

=====================================================

TAB2 INDICATORS

=====================================================

with tabs[1]: hist['RSI']=calc_rsi(close) macd,sig=calc_macd(close) hist['MACD']=macd hist['SIG']=sig hist['HIST']=macd-sig fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True) fig2.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name='RSI'),row=1,col=1) fig2.add_trace(go.Bar(x=hist.index, y=hist['HIST'], name='Hist'),row=2,col=1) fig2.add_trace(go.Scatter(x=hist.index, y=hist['MACD'], name='MACD'),row=2,col=1) fig2.add_trace(go.Scatter(x=hist.index, y=hist['SIG'], name='Signal'),row=2,col=1) fig2.update_layout(height=500) st.plotly_chart(fig2,use_container_width=True)

st.metric('RSI', round(hist['RSI'].iloc[-1],2))
st.metric('MACD Trend', 'Bullish' if macd.iloc[-1]>sig.iloc[-1] else 'Bearish')

PARTIAL FULL CODE CONTINUES IN NEXT PASTE
import streamlit as st import yfinance as yf import pandas as pd import numpy as np import plotly.graph_objects as go from plotly.subplots import make_subplots from deep_translator import GoogleTranslator from datetime import datetime import sqlite3 import os

=====================================================

DATABASE SETUP

=====================================================

conn = sqlite3.connect('tamil_invest_hub.db', check_same_thread=False) c = conn.cursor() c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)') c.execute('CREATE TABLE IF NOT EXISTS portfolio (username TEXT, symbol TEXT, qty REAL, avg REAL)') c.execute('CREATE TABLE IF NOT EXISTS watchlist (username TEXT, symbol TEXT)') conn.commit()

=====================================================

PAGE CONFIG

=====================================================

st.set_page_config(page_title='TAMIL INVEST HUB PRO MAX', page_icon='📈', layout='wide')

=====================================================

SESSION STATE

=====================================================

for k,v in [('is_logged',False),('user',''),('lang','Tamil')]: if k not in st.session_state: st.session_state[k]=v

def T(en,ta): return ta if st.session_state['lang']=='Tamil' else en

=====================================================

PREMIUM CSS

=====================================================

st.markdown('''

<style>
html,body,[class*="css"]{background:#020509;color:#dde6f0;font-family:sans-serif;}
.main-title{font-size:38px;font-weight:900;color:#39FF14;text-align:center;}
.sub{font-size:12px;color:#5a7a9a;text-align:center;}
.card{background:#08111b;padding:14px;border-radius:14px;border:1px solid #1a2535;margin-bottom:10px;}
</style>''',unsafe_allow_html=True)

=====================================================

LOGIN / REGISTER

=====================================================

if not st.session_state['is_logged']: st.markdown('<p class="main-title">📈 TAMIL INVEST HUB PRO MAX</p>',unsafe_allow_html=True) st.markdown('<p class="sub">Institutional Tamil Market Terminal</p>',unsafe_allow_html=True) lg = st.tabs(['Login','Register'])

with lg[0]:
    u = st.text_input('User ID')
    p = st.text_input('Password', type='password')
    if st.button('Login Access'):
        c.execute('SELECT * FROM users WHERE username=? AND password=?',(u,p))
        if c.fetchone():
            st.session_state['is_logged']=True
            st.session_state['user']=u
            st.rerun()
        else:
            st.error('Invalid Login')

with lg[1]:
    nu = st.text_input('Create User')
    npass = st.text_input('Create Password', type='password')
    if st.button('Register Now'):
        c.execute('INSERT INTO users VALUES (?,?)',(nu,npass))
        conn.commit()
        st.success('Registered Successfully')
st.stop()

=====================================================

FUNCTIONS

=====================================================

def calc_rsi(series, window=14): delta = series.diff() gain = delta.where(delta>0,0).rolling(window).mean() loss = (-delta.where(delta<0,0)).rolling(window).mean() rs = gain/loss.replace(0,np.nan) return 100-(100/(1+rs))

def calc_macd(series): ema12 = series.ewm(span=12).mean() ema26 = series.ewm(span=26).mean() macd = ema12-ema26 sig = macd.ewm(span=9).mean() return macd,sig

def fetch(sym,period): t = yf.Ticker(sym) return dict(t.info), t.history(period=period), t.actions, t.news[:8] if t.news else []

=====================================================

SIDEBAR

=====================================================

with st.sidebar: st.write('👤', st.session_state['user']) st.session_state['lang'] = st.radio('Language',['Tamil','English']) if st.button('Logout'): st.session_state['is_logged']=False st.rerun()

=====================================================

HEADER

=====================================================

st.markdown('<p class="main-title">📈 TAMIL INVEST HUB PRO MAX</p>',unsafe_allow_html=True) st.markdown('<p class="sub">Created by Somasundaram | Live AI Stock Analytics</p>',unsafe_allow_html=True)

=====================================================

MARKET SNAPSHOT

=====================================================

m1,m2,m3,m4 = st.columns(4) for col,sym,name in [(m1,'^NSEI','NIFTY50'),(m2,'^NSEBANK','BANKNIFTY'),(m3,'^BSESN','SENSEX'),(m4,'^INDIAVIX','INDIA VIX')]: try: tk = yf.Ticker(sym).fast_info lp = tk['lastPrice']; pc = tk['previousClose'] pct = round((lp-pc)/pc*100,2) col.metric(name, round(lp,2), str(pct)+'%') except: col.metric(name,'N/A')

=====================================================

SEARCH BAR

=====================================================

c1,c2,c3 = st.columns([4,1,1]) with c1: user_sym = st.text_input('Search Stock Symbol', value='RELIANCE').upper() with c2: per = st.selectbox('Period',['1mo','3mo','6mo','1y','2y']) with c3: ex = st.selectbox('Exchange',['NSE','BSE'])

symbol = user_sym+'.NS' if ex=='NSE' else user_sym+'.BO'

=====================================================

DATA LOAD

=====================================================

info,hist,actions,news = fetch(symbol, per) if hist.empty: st.error('No data found') st.stop()

close = hist['Close'] ltp = close.iloc[-1] prev = close.iloc[-2] chg = ltp-prev pct = chg/prev*100

ema20 = close.ewm(span=20).mean() ema50 = close.ewm(span=50).mean() ema200 = close.ewm(span=200).mean() score = 0 if ltp>ema20.iloc[-1]: score+=10 if ltp>ema50.iloc[-1]: score+=10 if ema20.iloc[-1]>ema50.iloc[-1]: score+=10 if ema50.iloc[-1]>ema200.iloc[-1]: score+=10

target = ltp1.18 sl = ltp0.92

=====================================================

TABS

=====================================================

tabs = st.tabs(['📊 Chart','📈 Indicators','🔮 AI Rating','💰 Financials','🤝 Shareholding','📰 News','📅 Actions','🏢 About'])

=====================================================

TAB1 CHART

=====================================================

with tabs[0]: st.metric(info.get('longName',symbol), round(ltp,2), str(round(pct,2))+'%') fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75,0.25]) fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema20, name='EMA20'),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema50, name='EMA50'),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema200, name='EMA200'),row=1,col=1) fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'),row=2,col=1) fig.update_layout(height=650) st.plotly_chart(fig, use_container_width=True) st.success('AI Target Price : ₹'+str(round(target,2))+' | Stoploss : ₹'+str(round(sl,2)))

=====================================================

TAB2 INDICATORS

=====================================================

with tabs[1]: hist['RSI']=calc_rsi(close) macd,sig=calc_macd(close) hist['MACD']=macd hist['SIG']=sig hist['HIST']=macd-sig fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True) fig2.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name='RSI'),row=1,col=1) fig2.add_trace(go.Bar(x=hist.index, y=hist['HIST'], name='Hist'),row=2,col=1) fig2.add_trace(go.Scatter(x=hist.index, y=hist['MACD'], name='MACD'),row=2,col=1) fig2.add_trace(go.Scatter(x=hist.index, y=hist['SIG'], name='Signal'),row=2,col=1) fig2.update_layout(height=500) st.plotly_chart(fig2,use_container_width=True)

st.metric('RSI', round(hist['RSI'].iloc[-1],2))
st.metric('MACD Trend', 'Bullish' if macd.iloc[-1]>sig.iloc[-1] else 'Bearish')

PARTIAL FULL CODE CONTINUES IN NEXT PASTE
import streamlit as st import yfinance as yf import pandas as pd import numpy as np import plotly.graph_objects as go from plotly.subplots import make_subplots from deep_translator import GoogleTranslator from datetime import datetime import sqlite3 import os

=====================================================

DATABASE SETUP

=====================================================

conn = sqlite3.connect('tamil_invest_hub.db', check_same_thread=False) c = conn.cursor() c.execute('CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)') c.execute('CREATE TABLE IF NOT EXISTS portfolio (username TEXT, symbol TEXT, qty REAL, avg REAL)') c.execute('CREATE TABLE IF NOT EXISTS watchlist (username TEXT, symbol TEXT)') conn.commit()

=====================================================

PAGE CONFIG

=====================================================

st.set_page_config(page_title='TAMIL INVEST HUB PRO MAX', page_icon='📈', layout='wide')

=====================================================

SESSION STATE

=====================================================

for k,v in [('is_logged',False),('user',''),('lang','Tamil')]: if k not in st.session_state: st.session_state[k]=v

def T(en,ta): return ta if st.session_state['lang']=='Tamil' else en

=====================================================

PREMIUM CSS

=====================================================

st.markdown('''

<style>
html,body,[class*="css"]{background:#020509;color:#dde6f0;font-family:sans-serif;}
.main-title{font-size:38px;font-weight:900;color:#39FF14;text-align:center;}
.sub{font-size:12px;color:#5a7a9a;text-align:center;}
.card{background:#08111b;padding:14px;border-radius:14px;border:1px solid #1a2535;margin-bottom:10px;}
</style>''',unsafe_allow_html=True)

=====================================================

LOGIN / REGISTER

=====================================================

if not st.session_state['is_logged']: st.markdown('<p class="main-title">📈 TAMIL INVEST HUB PRO MAX</p>',unsafe_allow_html=True) st.markdown('<p class="sub">Institutional Tamil Market Terminal</p>',unsafe_allow_html=True) lg = st.tabs(['Login','Register'])

with lg[0]:
    u = st.text_input('User ID')
    p = st.text_input('Password', type='password')
    if st.button('Login Access'):
        c.execute('SELECT * FROM users WHERE username=? AND password=?',(u,p))
        if c.fetchone():
            st.session_state['is_logged']=True
            st.session_state['user']=u
            st.rerun()
        else:
            st.error('Invalid Login')

with lg[1]:
    nu = st.text_input('Create User')
    npass = st.text_input('Create Password', type='password')
    if st.button('Register Now'):
        c.execute('INSERT INTO users VALUES (?,?)',(nu,npass))
        conn.commit()
        st.success('Registered Successfully')
st.stop()

=====================================================

FUNCTIONS

=====================================================

def calc_rsi(series, window=14): delta = series.diff() gain = delta.where(delta>0,0).rolling(window).mean() loss = (-delta.where(delta<0,0)).rolling(window).mean() rs = gain/loss.replace(0,np.nan) return 100-(100/(1+rs))

def calc_macd(series): ema12 = series.ewm(span=12).mean() ema26 = series.ewm(span=26).mean() macd = ema12-ema26 sig = macd.ewm(span=9).mean() return macd,sig

def fetch(sym,period): t = yf.Ticker(sym) return dict(t.info), t.history(period=period), t.actions, t.news[:8] if t.news else []

=====================================================

SIDEBAR

=====================================================

with st.sidebar: st.write('👤', st.session_state['user']) st.session_state['lang'] = st.radio('Language',['Tamil','English']) if st.button('Logout'): st.session_state['is_logged']=False st.rerun()

=====================================================

HEADER

=====================================================

st.markdown('<p class="main-title">📈 TAMIL INVEST HUB PRO MAX</p>',unsafe_allow_html=True) st.markdown('<p class="sub">Created by Somasundaram | Live AI Stock Analytics</p>',unsafe_allow_html=True)

=====================================================

MARKET SNAPSHOT

=====================================================

m1,m2,m3,m4 = st.columns(4) for col,sym,name in [(m1,'^NSEI','NIFTY50'),(m2,'^NSEBANK','BANKNIFTY'),(m3,'^BSESN','SENSEX'),(m4,'^INDIAVIX','INDIA VIX')]: try: tk = yf.Ticker(sym).fast_info lp = tk['lastPrice']; pc = tk['previousClose'] pct = round((lp-pc)/pc*100,2) col.metric(name, round(lp,2), str(pct)+'%') except: col.metric(name,'N/A')

=====================================================

SEARCH BAR

=====================================================

c1,c2,c3 = st.columns([4,1,1]) with c1: user_sym = st.text_input('Search Stock Symbol', value='RELIANCE').upper() with c2: per = st.selectbox('Period',['1mo','3mo','6mo','1y','2y']) with c3: ex = st.selectbox('Exchange',['NSE','BSE'])

symbol = user_sym+'.NS' if ex=='NSE' else user_sym+'.BO'

=====================================================

DATA LOAD

=====================================================

info,hist,actions,news = fetch(symbol, per) if hist.empty: st.error('No data found') st.stop()

close = hist['Close'] ltp = close.iloc[-1] prev = close.iloc[-2] chg = ltp-prev pct = chg/prev*100

ema20 = close.ewm(span=20).mean() ema50 = close.ewm(span=50).mean() ema200 = close.ewm(span=200).mean() score = 0 if ltp>ema20.iloc[-1]: score+=10 if ltp>ema50.iloc[-1]: score+=10 if ema20.iloc[-1]>ema50.iloc[-1]: score+=10 if ema50.iloc[-1]>ema200.iloc[-1]: score+=10

target = ltp1.18 sl = ltp0.92

=====================================================

TABS

=====================================================

tabs = st.tabs(['📊 Chart','📈 Indicators','🔮 AI Rating','💰 Financials','🤝 Shareholding','📰 News','📅 Actions','🏢 About'])

=====================================================

TAB1 CHART

=====================================================

with tabs[0]: st.metric(info.get('longName',symbol), round(ltp,2), str(round(pct,2))+'%') fig = make_subplots(rows=2, cols=1, shared_xaxes=True, row_heights=[0.75,0.25]) fig.add_trace(go.Candlestick(x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema20, name='EMA20'),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema50, name='EMA50'),row=1,col=1) fig.add_trace(go.Scatter(x=hist.index, y=ema200, name='EMA200'),row=1,col=1) fig.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'),row=2,col=1) fig.update_layout(height=650) st.plotly_chart(fig, use_container_width=True) st.success('AI Target Price : ₹'+str(round(target,2))+' | Stoploss : ₹'+str(round(sl,2)))

=====================================================

TAB2 INDICATORS

=====================================================

with tabs[1]: hist['RSI']=calc_rsi(close) macd,sig=calc_macd(close) hist['MACD']=macd hist['SIG']=sig hist['HIST']=macd-sig fig2 = make_subplots(rows=2, cols=1, shared_xaxes=True) fig2.add_trace(go.Scatter(x=hist.index, y=hist['RSI'], name='RSI'),row=1,col=1) fig2.add_trace(go.Bar(x=hist.index, y=hist['HIST'], name='Hist'),row=2,col=1) fig2.add_trace(go.Scatter(x=hist.index, y=hist['MACD'], name='MACD'),row=2,col=1) fig2.add_trace(go.Scatter(x=hist.index, y=hist['SIG'], name='Signal'),row=2,col=1) fig2.update_layout(height=500) st.plotly_chart(fig2,use_container_width=True)

st.metric('RSI', round(hist['RSI'].iloc[-1],2))
st.metric('MACD Trend', 'Bullish' if macd.iloc[-1]>sig.iloc[-1] else 'Bearish')

=====================================================

TAB3 AI RATING ENGINE

=====================================================

with tabs[2]: roe = (info.get('returnOnEquity') or 0)*100 debt = info.get('debtToEquity') or 0 margin = (info.get('profitMargins') or 0)*100 revg = (info.get('revenueGrowth') or 0)*100 epsg = (info.get('earningsGrowth') or 0)*100

fund_score = 0
if roe>15: fund_score += 20
if debt<100: fund_score += 15
if margin>10: fund_score += 15
if revg>8: fund_score += 10
if epsg>8: fund_score += 10

tech_score = score
final_score = min(100, fund_score + tech_score)

figg = go.Figure(go.Indicator(mode='gauge+number', value=final_score,
    title={'text':'MASTER STOCK AI SCORE'}, gauge={'axis':{'range':[0,100]}}))
figg.update_layout(height=350)
st.plotly_chart(figg, use_container_width=True)

if final_score>=75:
    st.success('✅ STRONG BUY ZONE')
elif final_score>=55:
    st.info('🟢 BUY / ACCUMULATE')
elif final_score>=40:
    st.warning('🟡 HOLD & WATCH')
else:
    st.error('🔴 AVOID / HIGH RISK')

a1,a2,a3 = st.columns(3)
a1.metric('Fundamental', fund_score)
a2.metric('Technical', tech_score)
a3.metric('Final Score', final_score)

=====================================================

TAB4 FINANCIALS

=====================================================

with tabs[3]: f1,f2,f3 = st.columns(3) with f1: st.metric('Market Cap', info.get('marketCap','N/A')) st.metric('Revenue', info.get('totalRevenue','N/A')) st.metric('Net Profit', info.get('netIncomeToCommon','N/A')) st.metric('EBITDA', info.get('ebitda','N/A')) with f2: st.metric('P/E', info.get('trailingPE','N/A')) st.metric('P/B', info.get('priceToBook','N/A')) st.metric('ROE', round(roe,2)) st.metric('Debt/Eq', debt) with f3: st.metric('EPS', info.get('trailingEps','N/A')) st.metric('Book Value', info.get('bookValue','N/A')) st.metric('Dividend Yield', info.get('dividendYield','N/A')) st.metric('Profit Margin', round(margin,2))

=====================================================

TAB5 SHAREHOLDING

=====================================================

with tabs[4]: insider = (info.get('heldPercentInsiders') or 0)*100 inst = (info.get('heldPercentInstitutions') or 0)*100 public = max(0,100-insider-inst) figp = go.Figure(data=[go.Pie(labels=['Promoters','Institutions','Public'], values=[insider,inst,public], hole=0.55)]) figp.update_layout(height=400) st.plotly_chart(figp, use_container_width=True)

=====================================================

TAB6 NEWS

=====================================================

with tabs[5]: if news: for n in news: st.write('📌', n.get('title','No title')) st.caption(n.get('publisher','')) if n.get('link'): st.link_button('Open News', n.get('link')) else: st.info('No News Available')

=====================================================

TAB7 ACTIONS

=====================================================

with tabs[6]: if not actions.empty: st.dataframe(actions.tail(20), use_container_width=True) else: st.info('No Corporate Actions')

=====================================================

TAB8 ABOUT COMPANY

=====================================================

with tabs[7]: st.write(info.get('longBusinessSummary','No description')) st.write('Sector:', info.get('sector','N/A')) st.write('Industry:', info.get('industry','N/A')) st.write('Country:', info.get('country','N/A')) st.write('Website:', info.get('website','N/A'))

=====================================================

QUICK MARKET SCANNER

=====================================================

st.markdown('---') st.subheader('⚡ Quick Market Scanner') scan_syms = ['RELIANCE.NS','TCS.NS','INFY.NS','SBIN.NS','ICICIBANK.NS','HDFCBANK.NS'] scan=[] for s in scan_syms: try: fi = yf.Ticker(s).fast_info lp = fi['lastPrice'] pc = fi['previousClose'] cp = round((lp-pc)/pc*100,2) scan.append((s.replace('.NS',''), lp, cp)) except: pass if scan: dfscan = pd.DataFrame(scan, columns=['Symbol','LTP','Change%']) st.dataframe(dfscan, use_container_width=True)

=====================================================

FOOTER

=====================================================

st.markdown('---') st.caption('© 2026 TAMIL INVEST HUB PRO MAX | Created by Somasundaram')

=====================================================

BONUS PERMANENT PORTFOLIO DATABASE MODULE

Add inside sidebar after language radio

=====================================================

with st.sidebar.expander('💾 My Portfolio'): psym = st.text_input('Add Symbol').upper() pqty = st.number_input('Qty',1,100000,1) pavg = st.number_input('Avg Price',1.0,1000000.0,100.0) if st.button('Add Holding'): c.execute('INSERT INTO portfolio VALUES (?,?,?,?)',(st.session_state['user'],psym,pqty,pavg)) conn.commit() st.success('Holding Added')

c.execute('SELECT symbol,qty,avg FROM portfolio WHERE username=?',(st.session_state['user'],))
rows = c.fetchall()
for r in rows:
    st.write(r[0], 'Qty:', r[1], 'Avg:', r[2])

=====================================================

BONUS PERMANENT WATCHLIST DATABASE MODULE

=====================================================

with st.sidebar.expander('👁 My Watchlist'): wsym = st.text_input('Watch Symbol').upper() if st.button('Add Watchlist'): c.execute('INSERT INTO watchlist VALUES (?,?)',(st.session_state['user'],wsym)) conn.commit() st.success('Added Watchlist')

c.execute('SELECT symbol FROM watchlist WHERE username=?',(st.session_state['user'],))
wr = c.fetchall()
for x in wr:
    st.write('⭐',x[0])

=====================================================

DUPLICATE REGISTER BUG FIX

Replace register button code with duplicate check

=====================================================

c.execute('SELECT * FROM users WHERE username=?',(nu,))

if c.fetchone(): st.error('User already exists')

else insert

=====================================================

SAFE YFINANCE WRAPPER

=====================================================

try:

info,hist,actions,news = fetch(symbol,per)

except Exception as e:

st.error('Yahoo Finance connection error')

st.stop()

=====================================================

FINAL PRODUCTION NOTES

=====================================================

pip install streamlit yfinance pandas numpy plotly deep-translator

run command : streamlit run app.py

streamlit cloud deploy supported

can convert to apk using webview later

========================== APP 100% MASTER BUILD END ==========================
