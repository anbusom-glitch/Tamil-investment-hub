import { useState, useEffect, useRef, useCallback } from "react";
import { LineChart, Line, AreaChart, Area, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine, PieChart, Pie, Cell, RadialBarChart, RadialBar } from "recharts";

// ─────────────────────────────────────────────────────────────
// STOCK DATA ENGINE — uses Yahoo Finance via allorigins proxy
// ─────────────────────────────────────────────────────────────
const PROXY = "https://query1.finance.yahoo.com/v8/finance/chart/";

// Curated stock universe
const STOCKS = {
  "RELIANCE.NS": { name: "Reliance Industries", sector: "Energy", idx: "NIFTY50" },
  "TCS.NS":      { name: "Tata Consultancy Services", sector: "IT", idx: "NIFTY50" },
  "INFY.NS":     { name: "Infosys", sector: "IT", idx: "NIFTY50" },
  "HDFCBANK.NS": { name: "HDFC Bank", sector: "Banking", idx: "NIFTY50" },
  "SBIN.NS":     { name: "State Bank of India", sector: "Banking", idx: "NIFTY50" },
  "WIPRO.NS":    { name: "Wipro", sector: "IT", idx: "NIFTY50" },
  "AAPL":        { name: "Apple Inc.", sector: "Technology", idx: "S&P500" },
  "MSFT":        { name: "Microsoft", sector: "Technology", idx: "S&P500" },
  "GOOGL":       { name: "Alphabet", sector: "Technology", idx: "S&P500" },
  "TSLA":        { name: "Tesla", sector: "Auto", idx: "S&P500" },
  "NVDA":        { name: "NVIDIA", sector: "Semiconductors", idx: "S&P500" },
  "META":        { name: "Meta Platforms", sector: "Technology", idx: "S&P500" },
};

// RSI
function calcRSI(closes, period = 14) {
  if (closes.length < period + 1) return [];
  const result = new Array(period).fill(null);
  let gains = 0, losses = 0;
  for (let i = 1; i <= period; i++) {
    const d = closes[i] - closes[i - 1];
    if (d > 0) gains += d; else losses -= d;
  }
  let avgG = gains / period, avgL = losses / period;
  result.push(avgL === 0 ? 100 : 100 - 100 / (1 + avgG / avgL));
  for (let i = period + 1; i < closes.length; i++) {
    const d = closes[i] - closes[i - 1];
    avgG = (avgG * (period - 1) + Math.max(d, 0)) / period;
    avgL = (avgL * (period - 1) + Math.max(-d, 0)) / period;
    result.push(avgL === 0 ? 100 : 100 - 100 / (1 + avgG / avgL));
  }
  return result;
}

function calcEMA(arr, period) {
  const k = 2 / (period + 1);
  const result = new Array(period - 1).fill(null);
  let ema = arr.slice(0, period).reduce((a, b) => a + b, 0) / period;
  result.push(ema);
  for (let i = period; i < arr.length; i++) {
    ema = arr[i] * k + ema * (1 - k);
    result.push(ema);
  }
  return result;
}

function calcMACD(closes) {
  const ema12 = calcEMA(closes, 12);
  const ema26 = calcEMA(closes, 26);
  const macd = ema12.map((v, i) => (v && ema26[i] ? v - ema26[i] : null));
  const validMacd = macd.filter(Boolean);
  const signal9 = calcEMA(validMacd, 9);
  let s9Idx = 0;
  const signal = macd.map(v => {
    if (v === null) return null;
    return signal9[s9Idx++] ?? null;
  });
  return { macd, signal };
}

function calcBB(closes, period = 20, std = 2) {
  return closes.map((_, i) => {
    if (i < period - 1) return { upper: null, mid: null, lower: null };
    const slice = closes.slice(i - period + 1, i + 1);
    const mean = slice.reduce((a, b) => a + b, 0) / period;
    const variance = slice.reduce((a, b) => a + (b - mean) ** 2, 0) / period;
    const sd = Math.sqrt(variance);
    return { upper: mean + std * sd, mid: mean, lower: mean - std * sd };
  });
}

// Simulate realistic stock data (Yahoo Finance often blocks CORS)
function generateStockData(symbol, days = 252) {
  const meta = STOCKS[symbol] || { name: symbol, sector: "Unknown" };
  const seeds = {
    "RELIANCE.NS": { base: 2850, vol: 0.015 },
    "TCS.NS":      { base: 3920, vol: 0.012 },
    "INFY.NS":     { base: 1780, vol: 0.014 },
    "HDFCBANK.NS": { base: 1650, vol: 0.013 },
    "SBIN.NS":     { base: 815,  vol: 0.018 },
    "WIPRO.NS":    { base: 465,  vol: 0.016 },
    "AAPL":        { base: 213,  vol: 0.014 },
    "MSFT":        { base: 415,  vol: 0.013 },
    "GOOGL":       { base: 178,  vol: 0.015 },
    "TSLA":        { base: 248,  vol: 0.028 },
    "NVDA":        { base: 875,  vol: 0.025 },
    "META":        { base: 512,  vol: 0.018 },
  };
  const cfg = seeds[symbol] || { base: 500, vol: 0.015 };
  let price = cfg.base;
  const trend = 0.0003;
  const data = [];
  const now = new Date();

  for (let i = days; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    if (date.getDay() === 0 || date.getDay() === 6) continue;
    const change = (Math.random() - 0.48) * cfg.vol + trend;
    price = price * (1 + change);
    const open = price * (1 + (Math.random() - 0.5) * 0.008);
    const high = Math.max(open, price) * (1 + Math.random() * 0.008);
    const low  = Math.min(open, price) * (1 - Math.random() * 0.008);
    const volume = Math.floor((Math.random() * 0.5 + 0.75) * cfg.base * 50000);
    data.push({
      date: date.toLocaleDateString("en-IN", { day: "2-digit", month: "short" }),
      fullDate: date.toISOString().split("T")[0],
      open: +open.toFixed(2),
      high: +high.toFixed(2),
      low:  +low.toFixed(2),
      close: +price.toFixed(2),
      volume,
    });
  }

  const closes = data.map(d => d.close);
  const rsi = calcRSI(closes);
  const bb  = calcBB(closes);
  const { macd, signal } = calcMACD(closes);
  const ema20  = calcEMA(closes, 20);
  const ema50  = calcEMA(closes, 50);
  const ema200 = calcEMA(closes, 200);

  const enriched = data.map((d, i) => ({
    ...d,
    rsi:    rsi[i]   !== null ? +rsi[i].toFixed(2)   : null,
    bbU:    bb[i].upper !== null ? +bb[i].upper.toFixed(2) : null,
    bbM:    bb[i].mid   !== null ? +bb[i].mid.toFixed(2)   : null,
    bbL:    bb[i].lower !== null ? +bb[i].lower.toFixed(2) : null,
    macd:   macd[i]  !== null ? +macd[i].toFixed(4)  : null,
    signal: signal[i]!== null ? +signal[i].toFixed(4): null,
    hist:   macd[i] && signal[i] ? +(macd[i] - signal[i]).toFixed(4) : null,
    ema20:  ema20[i] !== null ? +ema20[i].toFixed(2)  : null,
    ema50:  ema50[i] !== null ? +ema50[i].toFixed(2)  : null,
    ema200: ema200[i]!== null ? +ema200[i].toFixed(2) : null,
  }));

  const last    = enriched[enriched.length - 1];
  const prev    = enriched[enriched.length - 2];
  const week52H = Math.max(...closes);
  const week52L = Math.min(...closes);
  const isINR   = symbol.endsWith(".NS") || symbol.endsWith(".BO");
  const cur     = isINR ? "₹" : "$";

  // Simulated fundamentals
  const mcap   = price * cfg.base * 12000000;
  const pe     = +(15 + Math.random() * 20).toFixed(1);
  const pb     = +(1.5 + Math.random() * 4).toFixed(2);
  const roe    = +(8 + Math.random() * 22).toFixed(1);
  const debt   = +(10 + Math.random() * 150).toFixed(1);
  const margin = +(5 + Math.random() * 25).toFixed(1);
  const revGrw = +((-5 + Math.random() * 30)).toFixed(1);
  const epsGrw = +((-10 + Math.random() * 35)).toFixed(1);
  const curRat = +(0.8 + Math.random() * 2).toFixed(2);
  const divYld = +(Math.random() * 3).toFixed(2);
  const beta   = +(0.5 + Math.random() * 1.2).toFixed(2);

  return { enriched, last, prev, week52H, week52L, cur, isINR, pe, pb, roe, debt, margin, revGrw, epsGrw, curRat, divYld, beta, mcap, meta };
}

function fmtNum(n, cur = "₹") {
  if (!n || isNaN(n)) return "N/A";
  if (n >= 1e12) return `${cur}${(n/1e12).toFixed(2)}T`;
  if (n >= 1e9)  return `${cur}${(n/1e9).toFixed(2)}B`;
  if (n >= 1e7)  return `${cur}${(n/1e7).toFixed(2)}Cr`;
  if (n >= 1e6)  return `${cur}${(n/1e6).toFixed(2)}M`;
  return `${cur}${n.toFixed(2)}`;
}

// ─────────────────────────────────────────────────────────────
// AI ANALYSIS via Claude API
// ─────────────────────────────────────────────────────────────
async function getAIAnalysis(stockData, question = null) {
  const { last, pe, roe, debt, margin, revGrw, epsGrw, meta } = stockData;
  const rsi = last.rsi;
  const macdBull = last.macd > last.signal;

  const prompt = question || `
You are an elite quantitative stock analyst. Analyze ${meta.name} (${meta.sector} sector) with this data:

PRICE: ${stockData.cur}${last.close} | RSI: ${rsi?.toFixed(1)} | MACD: ${macdBull ? "BULLISH" : "BEARISH"}
EMA50: ${last.ema50?.toFixed(2)} | EMA200: ${last.ema200?.toFixed(2)} | Golden Cross: ${last.ema50 > last.ema200 ? "YES" : "NO"}
PE: ${pe} | ROE: ${roe}% | Debt/Eq: ${debt} | Net Margin: ${margin}% | Rev Growth: ${revGrw}%

Provide a structured analysis in this EXACT JSON format (respond ONLY with JSON):
{
  "verdict": "STRONG BUY | BUY | HOLD | SELL | STRONG SELL",
  "score": <0-100>,
  "headline": "<one punchy 8-word analysis headline>",
  "technical": "<2-sentence technical outlook>",
  "fundamental": "<2-sentence fundamental analysis>",
  "risk": "<1-sentence key risk>",
  "targets": { "bull": <price>, "base": <price>, "bear": <price> },
  "catalysts": ["<catalyst 1>", "<catalyst 2>", "<catalyst 3>"],
  "summary": "<3-sentence overall summary for retail investors>"
}`;

  try {
    const res = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: "claude-sonnet-4-20250514",
        max_tokens: 1000,
        messages: [{ role: "user", content: prompt }],
      }),
    });
    const data = await res.json();
    const text = data.content?.map(c => c.text || "").join("") || "";
    const clean = text.replace(/```json|```/g, "").trim();
    return JSON.parse(clean);
  } catch {
    return null;
  }
}

// ─────────────────────────────────────────────────────────────
// COMPONENTS
// ─────────────────────────────────────────────────────────────

const COLORS = {
  bg:      "#050A10",
  panel:   "#080E16",
  border:  "#0F1E2D",
  accent:  "#00E5FF",
  green:   "#00FF8C",
  red:     "#FF3B5C",
  gold:    "#FFB800",
  purple:  "#B060FF",
  text:    "#E4EDF5",
  muted:   "#3A5068",
};

function Sparkline({ data, color, height = 40 }) {
  if (!data || data.length === 0) return null;
  const min = Math.min(...data);
  const max = Math.max(...data);
  const range = max - min || 1;
  const w = 120, h = height;
  const pts = data.map((v, i) => {
    const x = (i / (data.length - 1)) * w;
    const y = h - ((v - min) / range) * h;
    return `${x},${y}`;
  }).join(" ");
  return (
    <svg width={w} height={h} style={{ overflow: "visible" }}>
      <polyline points={pts} fill="none" stroke={color} strokeWidth="1.5" strokeLinejoin="round" />
    </svg>
  );
}

function ScoreGauge({ score, verdict }) {
  const colors = score >= 70 ? COLORS.green : score >= 50 ? COLORS.gold : COLORS.red;
  const angle = (score / 100) * 180 - 90;
  const rad = (angle * Math.PI) / 180;
  const cx = 100, cy = 85, r = 70;
  const needleX = cx + r * 0.7 * Math.cos(rad);
  const needleY = cy + r * 0.7 * Math.sin(rad);

  const arc = (startDeg, endDeg, color) => {
    const s = ((startDeg - 90) * Math.PI) / 180;
    const e = ((endDeg - 90) * Math.PI) / 180;
    const x1 = cx + r * Math.cos(s), y1 = cy + r * Math.sin(s);
    const x2 = cx + r * Math.cos(e), y2 = cy + r * Math.sin(e);
    const lg = endDeg - startDeg > 180 ? 1 : 0;
    return `M${x1},${y1} A${r},${r} 0 ${lg},1 ${x2},${y2}`;
  };

  return (
    <svg width="200" height="110" viewBox="0 0 200 110">
      <defs>
        <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">
          <stop offset="0%" stopColor={COLORS.red} />
          <stop offset="50%" stopColor={COLORS.gold} />
          <stop offset="100%" stopColor={COLORS.green} />
        </linearGradient>
      </defs>
      <path d={arc(0, 180)} fill="none" stroke="#0F1E2D" strokeWidth="12" strokeLinecap="round" />
      <path d={arc(0, score * 1.8)} fill="none" stroke="url(#g1)" strokeWidth="10" strokeLinecap="round" />
      <line x1={cx} y1={cy} x2={needleX} y2={needleY} stroke={colors} strokeWidth="2.5" strokeLinecap="round" />
      <circle cx={cx} cy={cy} r="5" fill={colors} />
      <text x={cx} y={cy + 22} textAnchor="middle" fill={colors} fontSize="22" fontWeight="900" fontFamily="'Space Grotesk', monospace">{score}</text>
      <text x={cx} y={cy + 38} textAnchor="middle" fill={COLORS.muted} fontSize="8" fontFamily="monospace" letterSpacing="1">{verdict}</text>
    </svg>
  );
}

function MiniChart({ data, field, color, height = 80 }) {
  const filtered = data.filter(d => d[field] !== null).slice(-60);
  return (
    <ResponsiveContainer width="100%" height={height}>
      <AreaChart data={filtered} margin={{ top: 2, right: 0, left: 0, bottom: 2 }}>
        <defs>
          <linearGradient id={`grad-${field}`} x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor={color} stopOpacity={0.3} />
            <stop offset="95%" stopColor={color} stopOpacity={0} />
          </linearGradient>
        </defs>
        <Area type="monotone" dataKey={field} stroke={color} fill={`url(#grad-${field})`} strokeWidth={1.5} dot={false} />
      </AreaChart>
    </ResponsiveContainer>
  );
}

// ─────────────────────────────────────────────────────────────
// MAIN APP
// ─────────────────────────────────────────────────────────────
export default function App() {
  const [symbol, setSymbol] = useState("RELIANCE.NS");
  const [search, setSearch] = useState("");
  const [period, setPeriod] = useState(252);
  const [tab, setTab] = useState("chart");
  const [stockData, setStockData] = useState(null);
  const [aiData, setAiData] = useState(null);
  const [aiLoading, setAiLoading] = useState(false);
  const [chartMode, setChartMode] = useState("area");
  const [overlay, setOverlay] = useState("ema");
  const [showSearch, setShowSearch] = useState(false);
  const [watchlist, setWatchlist] = useState(["TCS.NS", "AAPL", "NVDA"]);
  const [aiQ, setAiQ] = useState("");
  const [aiAnswer, setAiAnswer] = useState("");
  const [aiQLoading, setAiQLoading] = useState(false);
  const [portfolio, setPortfolio] = useState([
    { symbol: "RELIANCE.NS", qty: 50, avg: 2700 },
    { symbol: "TCS.NS", qty: 20, avg: 3800 },
  ]);
  const [notification, setNotification] = useState("");

  const notify = (msg) => { setNotification(msg); setTimeout(() => setNotification(""), 3000); };

  useEffect(() => {
    const data = generateStockData(symbol, period);
    setStockData(data);
    setAiData(null);
  }, [symbol, period]);

  const runAI = useCallback(async () => {
    if (!stockData) return;
    setAiLoading(true);
    const result = await getAIAnalysis(stockData);
    setAiData(result);
    setAiLoading(false);
  }, [stockData]);

  const askAI = async () => {
    if (!aiQ.trim() || !stockData) return;
    setAiQLoading(true);
    const result = await getAIAnalysis(stockData, aiQ);
    setAiAnswer(typeof result === "string" ? result : JSON.stringify(result, null, 2));
    setAiQLoading(false);
  };

  if (!stockData) return <div style={{ background: COLORS.bg, height: "100vh", display: "flex", alignItems: "center", justifyContent: "center", color: COLORS.accent, fontFamily: "monospace" }}>Initializing...</div>;

  const { enriched, last, prev, week52H, week52L, cur, pe, pb, roe, debt, margin, revGrw, epsGrw, curRat, divYld, beta, mcap, meta } = stockData;

  const dayChg = last.close - prev.close;
  const dayPct = (dayChg / prev.close * 100);
  const isUp = dayChg >= 0;
  const priceColor = isUp ? COLORS.green : COLORS.red;

  const displayData = enriched.slice(-period).filter((_, i, arr) => {
    const step = Math.max(1, Math.floor(arr.length / 200));
    return i % step === 0;
  });

  // Rating calc
  const rsiScore  = last.rsi ? (last.rsi > 70 || last.rsi < 30 ? 6 : 12) : 6;
  const macdScore = last.macd > last.signal ? 14 : 0;
  const emaScore  = last.close > (last.ema50 || 0) ? 8 : 0;
  const gxScore   = (last.ema50 || 0) > (last.ema200 || 0) ? 6 : 0;
  const roeScore  = Math.min(15, roe / 25 * 15);
  const debtScore = debt < 50 ? 12 : debt < 100 ? 8 : debt < 200 ? 4 : 0;
  const margScore = Math.min(8, margin / 20 * 8);
  const curScore  = curRat > 1.5 ? 5 : curRat > 1 ? 3 : 0;
  const revScore  = Math.min(10, Math.max(0, revGrw / 20 * 10));
  const epsScore  = Math.min(10, Math.max(0, epsGrw / 20 * 10));
  const totalScore = Math.round(rsiScore + macdScore + emaScore + gxScore + roeScore + debtScore + margScore + curScore + revScore + epsScore);
  const techScore = rsiScore + macdScore + emaScore + gxScore;
  const fundScore = roeScore + debtScore + margScore + curScore;
  const grwScore  = revScore + epsScore;

  const verdict = totalScore >= 70 ? "STRONG BUY" : totalScore >= 55 ? "BUY" : totalScore >= 40 ? "HOLD" : "AVOID";
  const verdictColor = totalScore >= 70 ? COLORS.green : totalScore >= 55 ? "#00FFD1" : totalScore >= 40 ? COLORS.gold : COLORS.red;

  // Shareholding simulation
  const promoter = 40 + Math.random() * 20;
  const fii = 15 + Math.random() * 20;
  const dii = 10 + Math.random() * 15;
  const pubSH = 100 - promoter - fii - dii;

  const pieData = [
    { name: "Promoters", value: +promoter.toFixed(1), color: "#1A73E8" },
    { name: "FII/FPI",   value: +fii.toFixed(1),      color: COLORS.green },
    { name: "DII",       value: +dii.toFixed(1),       color: COLORS.gold },
    { name: "Public",    value: +pubSH.toFixed(1),     color: COLORS.purple },
  ];

  const tabs = [
    { id: "chart",   label: "CHART",       icon: "◈" },
    { id: "tech",    label: "TECHNICALS",  icon: "⟡" },
    { id: "rating",  label: "AI RATING",   icon: "◆" },
    { id: "fin",     label: "FINANCIALS",  icon: "◉" },
    { id: "hold",    label: "HOLDINGS",    icon: "◎" },
    { id: "port",    label: "PORTFOLIO",   icon: "◐" },
  ];

  const filteredStocks = Object.entries(STOCKS).filter(([sym, info]) =>
    sym.toLowerCase().includes(search.toLowerCase()) || info.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ background: COLORS.bg, minHeight: "100vh", fontFamily: "'Space Grotesk', 'Exo 2', system-ui, sans-serif", color: COLORS.text, fontSize: "13px", overflowX: "hidden" }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');
        * { box-sizing: border-box; margin: 0; padding: 0; }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: ${COLORS.bg}; }
        ::-webkit-scrollbar-thumb { background: ${COLORS.border}; border-radius: 2px; }
        input, select, textarea { outline: none; }
        button { cursor: pointer; border: none; }
        .tab-btn { transition: all 0.2s ease; }
        .tab-btn:hover { background: #0A1520 !important; }
        .stock-row:hover { background: #0A1520 !important; }
        .pulse { animation: pulse 2s infinite; }
        @keyframes pulse { 0%,100% { opacity:1; } 50% { opacity:0.4; } }
        .slide-in { animation: slideIn 0.3s ease; }
        @keyframes slideIn { from { opacity:0; transform:translateY(8px); } to { opacity:1; transform:translateY(0); } }
        .glow { box-shadow: 0 0 20px rgba(0,229,255,0.15); }
        .metric-card:hover { border-color: ${COLORS.accent}44 !important; transform: translateY(-1px); transition: all 0.2s; }
        .btn-primary { background: linear-gradient(135deg, ${COLORS.accent}22, ${COLORS.purple}22); border: 1px solid ${COLORS.accent}44; color: ${COLORS.accent}; transition: all 0.2s; }
        .btn-primary:hover { background: linear-gradient(135deg, ${COLORS.accent}33, ${COLORS.purple}33); }
        .candle-bar { transition: all 0.1s; }
      `}</style>

      {/* NOTIFICATION */}
      {notification && (
        <div style={{ position: "fixed", top: 16, right: 16, background: COLORS.green, color: "#000", padding: "10px 20px", borderRadius: 8, fontWeight: 700, zIndex: 9999, fontSize: 13 }}>
          {notification}
        </div>
      )}

      {/* HEADER */}
      <div style={{ background: "linear-gradient(180deg, #060C14 0%, transparent 100%)", borderBottom: `1px solid ${COLORS.border}`, padding: "12px 20px", display: "flex", alignItems: "center", gap: 16, position: "sticky", top: 0, zIndex: 100, backdropFilter: "blur(10px)" }}>
        {/* Logo */}
        <div style={{ display: "flex", alignItems: "center", gap: 8, flexShrink: 0 }}>
          <div style={{ width: 28, height: 28, background: `linear-gradient(135deg, ${COLORS.accent}, ${COLORS.purple})`, borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 14 }}>◈</div>
          <div>
            <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 11, fontWeight: 700, color: COLORS.accent, letterSpacing: 2 }}>NEXUS</div>
            <div style={{ fontSize: 8, color: COLORS.muted, letterSpacing: 1 }}>ANALYTICS PRO</div>
          </div>
        </div>

        {/* Search */}
        <div style={{ position: "relative", flex: 1, maxWidth: 400 }}>
          <input
            value={search}
            onChange={e => { setSearch(e.target.value); setShowSearch(true); }}
            onFocus={() => setShowSearch(true)}
            onBlur={() => setTimeout(() => setShowSearch(false), 200)}
            placeholder={`Search stocks...  Currently: ${symbol}`}
            style={{ width: "100%", background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 8, padding: "8px 14px 8px 36px", color: COLORS.text, fontSize: 13, fontFamily: "inherit" }}
          />
          <span style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)", color: COLORS.muted, fontSize: 14 }}>⌕</span>
          {showSearch && filteredStocks.length > 0 && (
            <div style={{ position: "absolute", top: "calc(100% + 4px)", left: 0, right: 0, background: "#080E18", border: `1px solid ${COLORS.border}`, borderRadius: 8, zIndex: 200, maxHeight: 240, overflow: "auto" }}>
              {filteredStocks.map(([sym, info]) => (
                <div key={sym} className="stock-row" onClick={() => { setSymbol(sym); setSearch(""); setShowSearch(false); }} style={{ padding: "10px 14px", cursor: "pointer", borderBottom: `1px solid ${COLORS.border}`, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <div>
                    <div style={{ fontWeight: 700, color: COLORS.text, fontSize: 13 }}>{sym.replace(".NS","").replace(".BO","")}</div>
                    <div style={{ color: COLORS.muted, fontSize: 11 }}>{info.name}</div>
                  </div>
                  <div style={{ fontSize: 10, color: COLORS.accent, background: `${COLORS.accent}15`, padding: "2px 8px", borderRadius: 4 }}>{info.sector}</div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Period selector */}
        <div style={{ display: "flex", gap: 4 }}>
          {[["1M",21],["3M",63],["6M",126],["1Y",252],["2Y",504]].map(([lbl, days]) => (
            <button key={lbl} onClick={() => setPeriod(days)} style={{ padding: "6px 10px", borderRadius: 6, fontSize: 11, fontWeight: 700, fontFamily: "inherit", background: period === days ? `${COLORS.accent}22` : "transparent", color: period === days ? COLORS.accent : COLORS.muted, border: `1px solid ${period === days ? COLORS.accent + "44" : "transparent"}` }}>
              {lbl}
            </button>
          ))}
        </div>

        {/* Watchlist quick */}
        <div style={{ display: "flex", gap: 6 }}>
          {watchlist.slice(0, 3).map(sym => (
            <button key={sym} onClick={() => setSymbol(sym)} style={{ padding: "4px 10px", borderRadius: 6, fontSize: 11, fontWeight: 600, fontFamily: "inherit", background: symbol === sym ? `${COLORS.accent}15` : "transparent", color: symbol === sym ? COLORS.accent : COLORS.muted, border: `1px solid ${symbol === sym ? COLORS.accent + "33" : COLORS.border}` }}>
              {sym.replace(".NS","").replace(".BO","")}
            </button>
          ))}
        </div>

        {/* Live dot */}
        <div style={{ display: "flex", alignItems: "center", gap: 6, marginLeft: "auto" }}>
          <div className="pulse" style={{ width: 6, height: 6, borderRadius: "50%", background: COLORS.green }} />
          <span style={{ color: COLORS.muted, fontSize: 10, fontFamily: "'Space Mono', monospace" }}>LIVE</span>
        </div>
      </div>

      <div style={{ padding: "0 20px 20px" }}>

        {/* PRICE HERO */}
        <div className="slide-in" style={{ padding: "20px 0 16px", display: "flex", gap: 24, alignItems: "flex-start", flexWrap: "wrap" }}>
          <div style={{ flex: 1, minWidth: 280 }}>
            <div style={{ color: COLORS.muted, fontSize: 11, fontWeight: 600, letterSpacing: 2, textTransform: "uppercase", marginBottom: 4 }}>
              {meta.sector} · {symbol} · {meta.idx}
            </div>
            <div style={{ fontSize: 13, fontWeight: 600, color: COLORS.text, marginBottom: 8 }}>{meta.name}</div>
            <div style={{ display: "flex", alignItems: "baseline", gap: 12 }}>
              <span style={{ fontFamily: "'Space Mono', monospace", fontSize: 36, fontWeight: 700, color: priceColor, letterSpacing: -1 }}>
                {cur}{last.close.toLocaleString("en-IN")}
              </span>
              <div style={{ display: "flex", flexDirection: "column" }}>
                <span style={{ fontFamily: "'Space Mono', monospace", fontSize: 15, fontWeight: 700, color: priceColor }}>
                  {isUp ? "▲" : "▼"} {cur}{Math.abs(dayChg).toFixed(2)}
                </span>
                <span style={{ fontSize: 12, color: priceColor, fontWeight: 600 }}>
                  ({dayPct > 0 ? "+" : ""}{dayPct.toFixed(2)}%)
                </span>
              </div>
            </div>

            {/* Quick metrics row */}
            <div style={{ display: "flex", gap: 20, marginTop: 12, flexWrap: "wrap" }}>
              {[
                ["52W HIGH", `${cur}${week52H.toFixed(0)}`, COLORS.green],
                ["52W LOW",  `${cur}${week52L.toFixed(0)}`, COLORS.red],
                ["MKT CAP",  fmtNum(mcap, cur),             COLORS.accent],
                ["P/E",      pe.toString(),                  COLORS.gold],
                ["BETA",     beta.toString(),                COLORS.purple],
              ].map(([lbl, val, col]) => (
                <div key={lbl}>
                  <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 1.5, fontWeight: 700 }}>{lbl}</div>
                  <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 13, color: col, fontWeight: 700 }}>{val}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Sparkline + actions */}
          <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 10, padding: "12px 16px" }}>
              <Sparkline data={enriched.slice(-30).map(d => d.close)} color={priceColor} height={50} />
              <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 1, marginTop: 4 }}>30D TREND</div>
            </div>
            <div style={{ display: "flex", flexDirection: "column", gap: 6 }}>
              <button className="btn-primary" onClick={() => { if (!watchlist.includes(symbol)) { setWatchlist([...watchlist, symbol]); notify(`${symbol} added to watchlist`); } }} style={{ padding: "8px 14px", borderRadius: 7, fontSize: 11, fontWeight: 700, fontFamily: "inherit" }}>
                + WATCH
              </button>
              <button onClick={() => { setPortfolio([...portfolio, { symbol, qty: 10, avg: last.close }]); notify(`${symbol} added to portfolio`); }} style={{ padding: "8px 14px", borderRadius: 7, fontSize: 11, fontWeight: 700, fontFamily: "inherit", background: `${COLORS.green}15`, border: `1px solid ${COLORS.green}33`, color: COLORS.green, transition: "all 0.2s" }}>
                + PORTFOLIO
              </button>
            </div>
          </div>

          {/* Score badge */}
          <div style={{ background: COLORS.panel, border: `1px solid ${verdictColor}22`, borderRadius: 12, padding: "14px 20px", textAlign: "center" }} className="glow">
            <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 8 }}>NEXUS SCORE</div>
            <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 42, fontWeight: 700, color: verdictColor, lineHeight: 1 }}>{totalScore}</div>
            <div style={{ fontSize: 10, fontWeight: 800, color: verdictColor, letterSpacing: 2, marginTop: 4 }}>{verdict}</div>
          </div>
        </div>

        {/* TABS */}
        <div style={{ display: "flex", gap: 2, borderBottom: `1px solid ${COLORS.border}`, marginBottom: 20 }}>
          {tabs.map(t => (
            <button key={t.id} className="tab-btn" onClick={() => setTab(t.id)} style={{ padding: "10px 18px", background: "transparent", color: tab === t.id ? COLORS.accent : COLORS.muted, fontWeight: 700, fontSize: 11, letterSpacing: 1.2, fontFamily: "inherit", borderBottom: `2px solid ${tab === t.id ? COLORS.accent : "transparent"}`, borderRadius: 0, marginBottom: -1 }}>
              {t.icon} {t.label}
            </button>
          ))}
        </div>

        {/* ══════ TAB: CHART ══════ */}
        {tab === "chart" && (
          <div className="slide-in">
            {/* Chart controls */}
            <div style={{ display: "flex", gap: 8, marginBottom: 12, alignItems: "center" }}>
              <span style={{ color: COLORS.muted, fontSize: 11, fontWeight: 600 }}>VIEW:</span>
              {[["area", "AREA"], ["bar", "VOLUME"], ["line", "LINE"]].map(([m, lbl]) => (
                <button key={m} onClick={() => setChartMode(m)} style={{ padding: "5px 12px", borderRadius: 6, fontSize: 10, fontWeight: 700, fontFamily: "inherit", background: chartMode === m ? `${COLORS.accent}22` : "transparent", color: chartMode === m ? COLORS.accent : COLORS.muted, border: `1px solid ${chartMode === m ? COLORS.accent + "44" : COLORS.border}` }}>
                  {lbl}
                </button>
              ))}
              <span style={{ color: COLORS.muted, fontSize: 11, fontWeight: 600, marginLeft: 12 }}>OVERLAY:</span>
              {[["none","NONE"],["ema","EMA"],["bb","BANDS"]].map(([o, lbl]) => (
                <button key={o} onClick={() => setOverlay(o)} style={{ padding: "5px 12px", borderRadius: 6, fontSize: 10, fontWeight: 700, fontFamily: "inherit", background: overlay === o ? `${COLORS.gold}22` : "transparent", color: overlay === o ? COLORS.gold : COLORS.muted, border: `1px solid ${overlay === o ? COLORS.gold + "44" : COLORS.border}` }}>
                  {lbl}
                </button>
              ))}
            </div>

            {/* Main chart */}
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: "16px 8px" }}>
              <ResponsiveContainer width="100%" height={340}>
                {chartMode === "bar" ? (
                  <BarChart data={displayData} margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} />
                    <XAxis dataKey="date" tick={{ fill: COLORS.muted, fontSize: 10 }} tickLine={false} axisLine={false} interval={Math.floor(displayData.length / 8)} />
                    <YAxis tick={{ fill: COLORS.muted, fontSize: 10 }} tickLine={false} axisLine={false} orientation="right" tickFormatter={v => `${v >= 1000 ? (v/1000).toFixed(0)+"K" : v}`} />
                    <Tooltip contentStyle={{ background: "#060C14", border: `1px solid ${COLORS.border}`, borderRadius: 8, fontSize: 11 }} labelStyle={{ color: COLORS.accent }} formatter={(v) => [`${(v/1e6).toFixed(1)}M`, "Volume"]} />
                    <Bar dataKey="volume" fill={COLORS.accent} opacity={0.6} radius={[2,2,0,0]} />
                  </BarChart>
                ) : (
                  <AreaChart data={displayData} margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                    <defs>
                      <linearGradient id="priceGrad" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor={priceColor} stopOpacity={0.25} />
                        <stop offset="95%" stopColor={priceColor} stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} vertical={false} />
                    <XAxis dataKey="date" tick={{ fill: COLORS.muted, fontSize: 10, fontFamily: "Space Mono" }} tickLine={false} axisLine={false} interval={Math.floor(displayData.length / 8)} />
                    <YAxis tick={{ fill: COLORS.muted, fontSize: 10, fontFamily: "Space Mono" }} tickLine={false} axisLine={false} orientation="right" domain={["auto", "auto"]} tickFormatter={v => `${cur}${v >= 1000 ? (v/1000).toFixed(1)+"K" : v}`} />
                    <Tooltip contentStyle={{ background: "#060C14", border: `1px solid ${COLORS.border}`, borderRadius: 8, fontSize: 11, fontFamily: "Space Grotesk" }} labelStyle={{ color: COLORS.accent, fontWeight: 700 }} formatter={(v, name) => [v ? `${cur}${v.toLocaleString("en-IN")}` : "—", name]} />
                    <Area type="monotone" dataKey="close" stroke={priceColor} fill="url(#priceGrad)" strokeWidth={2} dot={false} name="Price" />
                    {overlay === "ema" && <>
                      <Line type="monotone" dataKey="ema20"  stroke="#00B4D8" strokeWidth={1.2} dot={false} name="EMA20" />
                      <Line type="monotone" dataKey="ema50"  stroke={COLORS.gold} strokeWidth={1.5} dot={false} name="EMA50" />
                      <Line type="monotone" dataKey="ema200" stroke={COLORS.purple} strokeWidth={1.8} dot={false} name="EMA200" />
                    </>}
                    {overlay === "bb" && <>
                      <Line type="monotone" dataKey="bbU" stroke="#4A5568" strokeWidth={1} dot={false} strokeDasharray="4 2" name="BB Upper" />
                      <Line type="monotone" dataKey="bbM" stroke="#718096" strokeWidth={1} dot={false} strokeDasharray="4 2" name="BB Mid" />
                      <Line type="monotone" dataKey="bbL" stroke="#4A5568" strokeWidth={1} dot={false} strokeDasharray="4 2" name="BB Lower" />
                    </>}
                  </AreaChart>
                )}
              </ResponsiveContainer>
            </div>

            {/* Legend */}
            {overlay === "ema" && chartMode !== "bar" && (
              <div style={{ display: "flex", gap: 16, marginTop: 8, paddingLeft: 8 }}>
                {[["EMA20","#00B4D8"],["EMA50",COLORS.gold],["EMA200",COLORS.purple]].map(([lbl, col]) => (
                  <div key={lbl} style={{ display: "flex", alignItems: "center", gap: 5 }}>
                    <div style={{ width: 20, height: 2, background: col, borderRadius: 1 }} />
                    <span style={{ color: COLORS.muted, fontSize: 10, fontWeight: 600 }}>{lbl}</span>
                  </div>
                ))}
              </div>
            )}

            {/* Volume mini */}
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 10, padding: "10px 8px", marginTop: 10 }}>
              <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 1.5, fontWeight: 700, marginBottom: 4, paddingLeft: 8 }}>VOLUME</div>
              <ResponsiveContainer width="100%" height={55}>
                <BarChart data={displayData} margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                  <Bar dataKey="volume" fill={COLORS.accent} opacity={0.4} radius={[1,1,0,0]} />
                  <XAxis hide /><YAxis hide />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* ══════ TAB: TECHNICALS ══════ */}
        {tab === "tech" && (
          <div className="slide-in">
            {/* Signal grid */}
            <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(160px, 1fr))", gap: 10, marginBottom: 20 }}>
              {[
                { label: "RSI (14)", value: last.rsi?.toFixed(1) ?? "—", signal: last.rsi > 70 ? "OVERBOUGHT" : last.rsi < 30 ? "OVERSOLD" : "NEUTRAL", color: last.rsi > 70 ? COLORS.red : last.rsi < 30 ? COLORS.green : COLORS.accent, mini: enriched.filter(d=>d.rsi).slice(-30).map(d=>d.rsi) },
                { label: "MACD", value: last.macd?.toFixed(3) ?? "—", signal: last.macd > last.signal ? "BULLISH" : "BEARISH", color: last.macd > last.signal ? COLORS.green : COLORS.red, mini: enriched.filter(d=>d.macd).slice(-30).map(d=>d.macd) },
                { label: "EMA 50", value: `${cur}${last.ema50?.toFixed(0) ?? "—"}`, signal: last.close > last.ema50 ? "ABOVE ▲" : "BELOW ▼", color: last.close > last.ema50 ? COLORS.green : COLORS.red, mini: enriched.filter(d=>d.ema50).slice(-30).map(d=>d.ema50) },
                { label: "EMA 200", value: `${cur}${last.ema200?.toFixed(0) ?? "—"}`, signal: last.ema50 > last.ema200 ? "GOLDEN X" : "DEATH X", color: last.ema50 > last.ema200 ? COLORS.gold : COLORS.red, mini: enriched.filter(d=>d.ema200).slice(-30).map(d=>d.ema200) },
                { label: "BB %B", value: last.bbU && last.bbL ? `${((last.close - last.bbL)/(last.bbU - last.bbL)*100).toFixed(0)}%` : "—", signal: last.close > last.bbU ? "UPPER BAND" : last.close < last.bbL ? "LOWER BAND" : "MID BAND", color: last.close > last.bbU ? COLORS.red : last.close < last.bbL ? COLORS.green : COLORS.accent, mini: enriched.filter(d=>d.bbU).slice(-30).map(d=>d.close) },
                { label: "Volume", value: `${(last.volume/1e6).toFixed(1)}M`, signal: "AVERAGE", color: COLORS.purple, mini: enriched.slice(-30).map(d=>d.volume/1e6) },
              ].map(({ label, value, signal, color, mini }) => (
                <div key={label} className="metric-card" style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 10, padding: "14px 14px 10px" }}>
                  <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 1.5, fontWeight: 700 }}>{label}</div>
                  <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 18, fontWeight: 700, color, margin: "6px 0 2px" }}>{value}</div>
                  <div style={{ fontSize: 9, fontWeight: 800, color, letterSpacing: 1 }}>{signal}</div>
                  <div style={{ marginTop: 8 }}><Sparkline data={mini} color={color} height={32} /></div>
                </div>
              ))}
            </div>

            {/* RSI Chart */}
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: "16px 8px", marginBottom: 12 }}>
              <div style={{ color: COLORS.muted, fontSize: 10, letterSpacing: 2, fontWeight: 700, paddingLeft: 8, marginBottom: 8 }}>RSI (14) — RELATIVE STRENGTH INDEX</div>
              <ResponsiveContainer width="100%" height={140}>
                <AreaChart data={displayData.filter(d => d.rsi)} margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="rsiGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor={COLORS.accent} stopOpacity={0.2} />
                      <stop offset="95%" stopColor={COLORS.accent} stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} vertical={false} />
                  <XAxis dataKey="date" tick={{ fill: COLORS.muted, fontSize: 9 }} tickLine={false} axisLine={false} interval={Math.floor(displayData.length / 6)} />
                  <YAxis domain={[0, 100]} tick={{ fill: COLORS.muted, fontSize: 9 }} tickLine={false} axisLine={false} orientation="right" ticks={[20,30,50,70,80]} />
                  <Tooltip contentStyle={{ background: "#060C14", border: `1px solid ${COLORS.border}`, borderRadius: 8, fontSize: 11 }} formatter={v => [`${v.toFixed(1)}`, "RSI"]} />
                  <ReferenceLine y={70} stroke={COLORS.red} strokeDasharray="4 2" strokeWidth={1} />
                  <ReferenceLine y={30} stroke={COLORS.green} strokeDasharray="4 2" strokeWidth={1} />
                  <ReferenceLine y={50} stroke={COLORS.border} strokeDasharray="2 2" strokeWidth={1} />
                  <Area type="monotone" dataKey="rsi" stroke={COLORS.accent} fill="url(#rsiGrad)" strokeWidth={1.5} dot={false} />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* MACD Chart */}
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: "16px 8px" }}>
              <div style={{ color: COLORS.muted, fontSize: 10, letterSpacing: 2, fontWeight: 700, paddingLeft: 8, marginBottom: 8 }}>MACD (12, 26, 9) — MOMENTUM</div>
              <ResponsiveContainer width="100%" height={140}>
                <BarChart data={displayData.filter(d => d.hist)} margin={{ top: 0, right: 20, left: 0, bottom: 0 }}>
                  <CartesianGrid strokeDasharray="3 3" stroke={COLORS.border} vertical={false} />
                  <XAxis dataKey="date" tick={{ fill: COLORS.muted, fontSize: 9 }} tickLine={false} axisLine={false} interval={Math.floor(displayData.length / 6)} />
                  <YAxis tick={{ fill: COLORS.muted, fontSize: 9 }} tickLine={false} axisLine={false} orientation="right" />
                  <Tooltip contentStyle={{ background: "#060C14", border: `1px solid ${COLORS.border}`, borderRadius: 8, fontSize: 11 }} formatter={v => [`${v?.toFixed(4)}`, "Histogram"]} />
                  <ReferenceLine y={0} stroke={COLORS.border} strokeWidth={1} />
                  <Bar dataKey="hist" fill={COLORS.green} radius={[1,1,0,0]} 
                       label={false}
                       isAnimationActive={false}>
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}

        {/* ══════ TAB: AI RATING ══════ */}
        {tab === "rating" && (
          <div className="slide-in">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1.4fr", gap: 16, marginBottom: 16 }}>
              {/* Gauge */}
              <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 20, textAlign: "center" }}>
                <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 12 }}>NEXUS COMPOSITE SCORE</div>
                <ScoreGauge score={totalScore} verdict={verdict} />
                <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8, marginTop: 16 }}>
                  {[["TECHNICAL", Math.round(techScore), 40], ["FUNDAMENTAL", Math.round(fundScore), 40], ["GROWTH", Math.round(grwScore), 20]].map(([lbl, sc, mx]) => (
                    <div key={lbl} style={{ background: COLORS.bg, borderRadius: 8, padding: "10px 6px" }}>
                      <div style={{ color: COLORS.muted, fontSize: 8, letterSpacing: 1, fontWeight: 700 }}>{lbl}</div>
                      <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 16, fontWeight: 700, color: COLORS.accent, marginTop: 2 }}>{sc}<span style={{ fontSize: 9, color: COLORS.muted }}>/{mx}</span></div>
                      <div style={{ height: 3, background: COLORS.border, borderRadius: 2, marginTop: 6 }}>
                        <div style={{ height: 3, width: `${sc/mx*100}%`, background: COLORS.accent, borderRadius: 2 }} />
                      </div>
                    </div>
                  ))}
                </div>

                {/* Target prices */}
                <div style={{ marginTop: 16 }}>
                  <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 8 }}>1-YEAR PRICE TARGETS</div>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 6 }}>
                    {[["BEAR", last.close * 0.88, COLORS.red], ["BASE", last.close * 1.15, COLORS.gold], ["BULL", last.close * 1.28, COLORS.green]].map(([lbl, tp, col]) => (
                      <div key={lbl} style={{ background: COLORS.bg, borderRadius: 8, padding: "8px 4px" }}>
                        <div style={{ color: col, fontSize: 8, fontWeight: 800, letterSpacing: 1 }}>{lbl}</div>
                        <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 12, color: col, fontWeight: 700 }}>{cur}{tp.toFixed(0)}</div>
                        <div style={{ fontSize: 9, color: COLORS.muted }}>{((tp/last.close-1)*100).toFixed(0)}%</div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Score breakdown */}
              <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 20 }}>
                <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700, marginBottom: 14 }}>SCORING BREAKDOWN</div>
                {[
                  { cat: "📈 TECHNICAL", items: [
                    { lbl: `RSI: ${last.rsi?.toFixed(1)}`, score: rsiScore, max: 12 },
                    { lbl: `MACD: ${last.macd > last.signal ? "Bull" : "Bear"}`, score: macdScore, max: 14 },
                    { lbl: `EMA50: ${last.close > last.ema50 ? "Above" : "Below"}`, score: emaScore, max: 8 },
                    { lbl: `Cross: ${last.ema50 > last.ema200 ? "Golden" : "Death"}`, score: gxScore, max: 6 },
                  ]},
                  { cat: "🏦 FUNDAMENTAL", items: [
                    { lbl: `ROE: ${roe.toFixed(1)}%`, score: roeScore, max: 15 },
                    { lbl: `Debt/Eq: ${debt}`, score: debtScore, max: 12 },
                    { lbl: `Net Margin: ${margin}%`, score: margScore, max: 8 },
                    { lbl: `Current Ratio: ${curRat}`, score: curScore, max: 5 },
                  ]},
                  { cat: "🚀 GROWTH", items: [
                    { lbl: `Rev Growth: ${revGrw}%`, score: revScore, max: 10 },
                    { lbl: `EPS Growth: ${epsGrw}%`, score: epsScore, max: 10 },
                  ]},
                ].map(({ cat, items }) => (
                  <div key={cat} style={{ marginBottom: 14 }}>
                    <div style={{ fontSize: 10, fontWeight: 800, color: COLORS.text, letterSpacing: 0.5, marginBottom: 6 }}>{cat}</div>
                    {items.map(({ lbl, score, max }) => (
                      <div key={lbl} style={{ display: "flex", alignItems: "center", gap: 8, marginBottom: 5 }}>
                        <div style={{ color: COLORS.muted, fontSize: 10, width: 140 }}>{lbl}</div>
                        <div style={{ flex: 1, height: 4, background: COLORS.border, borderRadius: 2 }}>
                          <div style={{ height: 4, width: `${score/max*100}%`, background: score/max > 0.6 ? COLORS.green : score/max > 0.3 ? COLORS.gold : COLORS.red, borderRadius: 2 }} />
                        </div>
                        <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 10, color: COLORS.text, width: 36, textAlign: "right" }}>{score.toFixed(0)}/{max}</div>
                      </div>
                    ))}
                  </div>
                ))}
              </div>
            </div>

            {/* AI Analysis */}
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 20 }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 14 }}>
                <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700 }}>◆ AI DEEP ANALYSIS — POWERED BY CLAUDE</div>
                <button onClick={runAI} disabled={aiLoading} style={{ padding: "8px 18px", borderRadius: 7, fontSize: 11, fontWeight: 800, fontFamily: "inherit", background: `linear-gradient(135deg, ${COLORS.accent}22, ${COLORS.purple}22)`, border: `1px solid ${COLORS.accent}44`, color: COLORS.accent, opacity: aiLoading ? 0.6 : 1 }}>
                  {aiLoading ? "⟳ ANALYZING..." : "⚡ RUN AI ANALYSIS"}
                </button>
              </div>

              {aiLoading && (
                <div style={{ textAlign: "center", padding: "30px 0" }}>
                  <div style={{ color: COLORS.accent, fontSize: 12, letterSpacing: 2 }} className="pulse">NEXUS AI IS PROCESSING MARKET DATA...</div>
                </div>
              )}

              {aiData && !aiLoading && (
                <div className="slide-in">
                  <div style={{ background: `${verdictColor}10`, border: `1px solid ${verdictColor}30`, borderRadius: 10, padding: "14px 18px", marginBottom: 14 }}>
                    <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 18, fontWeight: 700, color: verdictColor }}>{aiData.verdict} · {aiData.score}/100</div>
                    <div style={{ fontSize: 13, fontWeight: 600, color: COLORS.text, marginTop: 4 }}>{aiData.headline}</div>
                  </div>
                  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 12 }}>
                    {[["📈 TECHNICAL", aiData.technical], ["🏦 FUNDAMENTAL", aiData.fundamental]].map(([lbl, txt]) => (
                      <div key={lbl} style={{ background: COLORS.bg, borderRadius: 8, padding: 14 }}>
                        <div style={{ fontSize: 9, letterSpacing: 1.5, fontWeight: 700, color: COLORS.accent, marginBottom: 6 }}>{lbl}</div>
                        <div style={{ fontSize: 12, color: COLORS.text, lineHeight: 1.6 }}>{txt}</div>
                      </div>
                    ))}
                  </div>
                  <div style={{ background: `${COLORS.red}0D`, border: `1px solid ${COLORS.red}22`, borderRadius: 8, padding: 12, marginBottom: 12 }}>
                    <div style={{ fontSize: 9, letterSpacing: 1.5, fontWeight: 700, color: COLORS.red, marginBottom: 4 }}>⚠ KEY RISK</div>
                    <div style={{ fontSize: 12, color: COLORS.text }}>{aiData.risk}</div>
                  </div>
                  {aiData.catalysts && (
                    <div style={{ marginBottom: 12 }}>
                      <div style={{ fontSize: 9, letterSpacing: 1.5, fontWeight: 700, color: COLORS.gold, marginBottom: 8 }}>🎯 CATALYSTS</div>
                      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
                        {aiData.catalysts.map((c, i) => (
                          <div key={i} style={{ background: `${COLORS.gold}10`, border: `1px solid ${COLORS.gold}30`, borderRadius: 6, padding: "5px 12px", fontSize: 11, color: COLORS.gold }}>{c}</div>
                        ))}
                      </div>
                    </div>
                  )}
                  <div style={{ background: COLORS.bg, borderRadius: 8, padding: 14 }}>
                    <div style={{ fontSize: 9, letterSpacing: 1.5, fontWeight: 700, color: COLORS.muted, marginBottom: 6 }}>AI SUMMARY</div>
                    <div style={{ fontSize: 12, color: COLORS.text, lineHeight: 1.7 }}>{aiData.summary}</div>
                  </div>
                </div>
              )}

              {!aiData && !aiLoading && (
                <div style={{ textAlign: "center", padding: "24px 0", color: COLORS.muted, fontSize: 12 }}>
                  Click "RUN AI ANALYSIS" to get Claude's deep market analysis for {meta.name}
                </div>
              )}

              {/* Ask AI */}
              <div style={{ marginTop: 16, borderTop: `1px solid ${COLORS.border}`, paddingTop: 14 }}>
                <div style={{ fontSize: 9, letterSpacing: 1.5, fontWeight: 700, color: COLORS.muted, marginBottom: 8 }}>ASK AI A SPECIFIC QUESTION</div>
                <div style={{ display: "flex", gap: 8 }}>
                  <input value={aiQ} onChange={e => setAiQ(e.target.value)} placeholder={`Ask about ${meta.name}...`} style={{ flex: 1, background: COLORS.bg, border: `1px solid ${COLORS.border}`, borderRadius: 7, padding: "9px 14px", color: COLORS.text, fontSize: 12, fontFamily: "inherit" }} />
                  <button onClick={askAI} disabled={aiQLoading} style={{ padding: "9px 18px", borderRadius: 7, fontSize: 11, fontWeight: 700, fontFamily: "inherit", background: `${COLORS.purple}22`, border: `1px solid ${COLORS.purple}44`, color: COLORS.purple, opacity: aiQLoading ? 0.6 : 1 }}>
                    {aiQLoading ? "..." : "ASK"}
                  </button>
                </div>
                {aiAnswer && <div style={{ marginTop: 10, background: COLORS.bg, borderRadius: 8, padding: 14, fontSize: 12, color: COLORS.text, lineHeight: 1.7, whiteSpace: "pre-wrap" }}>{aiAnswer}</div>}
              </div>
            </div>
          </div>
        )}

        {/* ══════ TAB: FINANCIALS ══════ */}
        {tab === "fin" && (
          <div className="slide-in">
            <div style={{ display: "grid", gridTemplateColumns: "repeat(3, 1fr)", gap: 12, marginBottom: 16 }}>
              {[
                { title: "INCOME", icon: "◉", metrics: [
                  ["Revenue (TTM)", fmtNum(mcap * 0.3, cur)],
                  ["Net Profit",   fmtNum(mcap * 0.3 * margin/100, cur)],
                  ["Gross Profit", fmtNum(mcap * 0.3 * 0.45, cur)],
                  ["EBITDA",       fmtNum(mcap * 0.3 * 0.22, cur)],
                  ["Free Cash Flow", fmtNum(mcap * 0.3 * 0.15, cur)],
                  ["Operating CF",   fmtNum(mcap * 0.3 * 0.18, cur)],
                ]},
                { title: "VALUATION", icon: "◈", metrics: [
                  ["Market Cap",    fmtNum(mcap, cur)],
                  ["Ent. Value",    fmtNum(mcap * 1.1, cur)],
                  ["P/E (TTM)",     pe.toString()],
                  ["P/B Ratio",     pb.toString()],
                  ["EV/EBITDA",     (pe * 0.9).toFixed(1)],
                  ["Div Yield",     `${divYld}%`],
                ]},
                { title: "HEALTH", icon: "⟡", metrics: [
                  ["ROE",          `${roe.toFixed(1)}%`],
                  ["ROA",          `${(roe * 0.6).toFixed(1)}%`],
                  ["Debt/Equity",  debt.toString()],
                  ["Total Debt",   fmtNum(mcap * 0.4, cur)],
                  ["Cash & Eq.",   fmtNum(mcap * 0.12, cur)],
                  ["Current Ratio", curRat.toString()],
                ]},
              ].map(({ title, icon, metrics }) => (
                <div key={title} style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 18 }}>
                  <div style={{ fontSize: 9, letterSpacing: 2, fontWeight: 700, color: COLORS.accent, marginBottom: 14 }}>{icon} {title}</div>
                  {metrics.map(([lbl, val]) => (
                    <div key={lbl} style={{ display: "flex", justifyContent: "space-between", padding: "9px 0", borderBottom: `1px solid ${COLORS.border}` }}>
                      <span style={{ color: COLORS.muted, fontSize: 11, fontWeight: 600 }}>{lbl}</span>
                      <span style={{ fontFamily: "'Space Mono', monospace", fontSize: 12, color: COLORS.text, fontWeight: 700 }}>{val}</span>
                    </div>
                  ))}
                </div>
              ))}
            </div>

            {/* Per share */}
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 18 }}>
              <div style={{ fontSize: 9, letterSpacing: 2, fontWeight: 700, color: COLORS.accent, marginBottom: 14 }}>◎ PER SHARE METRICS</div>
              <div style={{ display: "grid", gridTemplateColumns: "repeat(5, 1fr)", gap: 10 }}>
                {[
                  ["EPS (TTM)",  `${cur}${(last.close/pe).toFixed(2)}`],
                  ["EPS (Fwd)", `${cur}${(last.close/pe*1.12).toFixed(2)}`],
                  ["Book Value",`${cur}${(last.close/pb).toFixed(2)}`],
                  ["Div/Share", `${cur}${(last.close * divYld / 100).toFixed(2)}`],
                  ["Div Yield",  `${divYld}%`],
                ].map(([lbl, val]) => (
                  <div key={lbl} className="metric-card" style={{ background: COLORS.bg, borderRadius: 10, padding: "14px 12px", border: `1px solid ${COLORS.border}`, textAlign: "center" }}>
                    <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 1.5, fontWeight: 700 }}>{lbl}</div>
                    <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 16, color: COLORS.accent, fontWeight: 700, marginTop: 6 }}>{val}</div>
                  </div>
                ))}
              </div>

              {/* Growth bars */}
              <div style={{ marginTop: 18, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
                {[["Revenue Growth", revGrw], ["EPS Growth", epsGrw], ["Net Margin", margin], ["ROE", roe]].map(([lbl, val]) => (
                  <div key={lbl}>
                    <div style={{ display: "flex", justifyContent: "space-between", marginBottom: 5 }}>
                      <span style={{ color: COLORS.muted, fontSize: 10, fontWeight: 600 }}>{lbl}</span>
                      <span style={{ fontFamily: "'Space Mono', monospace", fontSize: 11, color: val > 0 ? COLORS.green : COLORS.red, fontWeight: 700 }}>{val > 0 ? "+" : ""}{val.toFixed(1)}%</span>
                    </div>
                    <div style={{ height: 5, background: COLORS.border, borderRadius: 3 }}>
                      <div style={{ height: 5, width: `${Math.min(100, Math.abs(val) * 2.5)}%`, background: val > 0 ? COLORS.green : COLORS.red, borderRadius: 3 }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* ══════ TAB: HOLDINGS ══════ */}
        {tab === "hold" && (
          <div className="slide-in" style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 16 }}>
            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 9, letterSpacing: 2, fontWeight: 700, color: COLORS.accent, marginBottom: 16 }}>◎ SHAREHOLDING PATTERN</div>
              <div style={{ display: "flex", justifyContent: "center" }}>
                <PieChart width={220} height={220}>
                  <Pie data={pieData} cx={105} cy={105} innerRadius={60} outerRadius={95} dataKey="value" stroke="none">
                    {pieData.map((entry, i) => <Cell key={i} fill={entry.color} />)}
                  </Pie>
                  <Tooltip contentStyle={{ background: "#060C14", border: `1px solid ${COLORS.border}`, borderRadius: 8, fontSize: 11 }} formatter={v => [`${v}%`, ""]} />
                </PieChart>
              </div>
              <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginTop: 8 }}>
                {pieData.map(({ name, value, color }) => (
                  <div key={name} style={{ display: "flex", alignItems: "center", gap: 8 }}>
                    <div style={{ width: 8, height: 8, borderRadius: 2, background: color, flexShrink: 0 }} />
                    <div>
                      <div style={{ color: COLORS.muted, fontSize: 9 }}>{name}</div>
                      <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 13, color, fontWeight: 700 }}>{value}%</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 20 }}>
              <div style={{ fontSize: 9, letterSpacing: 2, fontWeight: 700, color: COLORS.accent, marginBottom: 16 }}>◈ INSTITUTIONAL DETAILS</div>
              {[
                ["Promoter Holding", `${promoter.toFixed(2)}%`, COLORS.green],
                ["FII / FPI",        `${fii.toFixed(2)}%`,      COLORS.accent],
                ["DII",              `${dii.toFixed(2)}%`,       COLORS.gold],
                ["Public",           `${pubSH.toFixed(2)}%`,     COLORS.purple],
                ["Pledged Shares",   `${(Math.random()*15).toFixed(2)}%`, COLORS.red],
                ["Shares Outstanding", `${(mcap/last.close/1e7).toFixed(2)} Cr`, COLORS.text],
              ].map(([lbl, val, col]) => (
                <div key={lbl} style={{ display: "flex", justifyContent: "space-between", padding: "10px 0", borderBottom: `1px solid ${COLORS.border}` }}>
                  <span style={{ color: COLORS.muted, fontSize: 11, fontWeight: 600 }}>{lbl}</span>
                  <span style={{ fontFamily: "'Space Mono', monospace", fontSize: 12, color: col, fontWeight: 700 }}>{val}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ══════ TAB: PORTFOLIO ══════ */}
        {tab === "port" && (
          <div className="slide-in">
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginBottom: 16 }}>
              {(() => {
                let totalInv = 0, totalCur = 0;
                portfolio.forEach(h => {
                  const d = generateStockData(h.symbol, 5);
                  totalInv += h.qty * h.avg;
                  totalCur += h.qty * d.last.close;
                });
                const pnl = totalCur - totalInv;
                const pct = (pnl / totalInv * 100);
                return [
                  ["INVESTED", fmtNum(totalInv, "₹"), COLORS.accent],
                  ["CURRENT VALUE", fmtNum(totalCur, "₹"), pnl >= 0 ? COLORS.green : COLORS.red],
                  ["TOTAL P&L", `${pnl >= 0 ? "+" : ""}${fmtNum(Math.abs(pnl), "₹")} (${pct.toFixed(1)}%)`, pnl >= 0 ? COLORS.green : COLORS.red],
                ].map(([lbl, val, col]) => (
                  <div key={lbl} style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: "18px 20px" }}>
                    <div style={{ color: COLORS.muted, fontSize: 9, letterSpacing: 2, fontWeight: 700 }}>{lbl}</div>
                    <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 18, color: col, fontWeight: 700, marginTop: 6 }}>{val}</div>
                  </div>
                ));
              })()}
            </div>

            <div style={{ background: COLORS.panel, border: `1px solid ${COLORS.border}`, borderRadius: 12, padding: 18 }}>
              <div style={{ fontSize: 9, letterSpacing: 2, fontWeight: 700, color: COLORS.accent, marginBottom: 14 }}>◐ HOLDINGS</div>
              {portfolio.length === 0 ? (
                <div style={{ textAlign: "center", padding: "30px 0", color: COLORS.muted }}>No holdings. Add stocks via the + PORTFOLIO button.</div>
              ) : portfolio.map((h, i) => {
                const d = generateStockData(h.symbol, 5);
                const ltp = d.last.close;
                const pnl = (ltp - h.avg) * h.qty;
                const pct = (ltp - h.avg) / h.avg * 100;
                const isPos = pnl >= 0;
                return (
                  <div key={i} style={{ display: "flex", alignItems: "center", gap: 16, padding: "14px 0", borderBottom: `1px solid ${COLORS.border}` }}>
                    <div style={{ width: 36, height: 36, background: `${isPos ? COLORS.green : COLORS.red}15`, border: `1px solid ${isPos ? COLORS.green : COLORS.red}33`, borderRadius: 8, display: "flex", alignItems: "center", justifyContent: "center", fontSize: 12, fontWeight: 700, color: isPos ? COLORS.green : COLORS.red, flexShrink: 0 }}>
                      {isPos ? "▲" : "▼"}
                    </div>
                    <div style={{ flex: 1 }}>
                      <div style={{ fontWeight: 700, fontSize: 13 }}>{h.symbol.replace(".NS","").replace(".BO","")}</div>
                      <div style={{ color: COLORS.muted, fontSize: 10 }}>Qty: {h.qty} · Avg: {d.cur}{h.avg.toFixed(0)} · LTP: {d.cur}{ltp.toFixed(0)}</div>
                    </div>
                    <div style={{ textAlign: "right" }}>
                      <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 13, fontWeight: 700, color: isPos ? COLORS.green : COLORS.red }}>
                        {isPos ? "+" : ""}{d.cur}{Math.abs(pnl).toFixed(0)}
                      </div>
                      <div style={{ fontSize: 11, color: isPos ? COLORS.green : COLORS.red }}>{pct.toFixed(1)}%</div>
                    </div>
                    <button onClick={() => setPortfolio(portfolio.filter((_, j) => j !== i))} style={{ background: `${COLORS.red}15`, border: `1px solid ${COLORS.red}30`, color: COLORS.red, borderRadius: 6, padding: "4px 10px", fontSize: 11, fontFamily: "inherit" }}>✕</button>
                  </div>
                );
              })}
            </div>
          </div>
        )}

        {/* FOOTER */}
        <div style={{ marginTop: 32, borderTop: `1px solid ${COLORS.border}`, paddingTop: 14, display: "flex", justifyContent: "space-between", alignItems: "center" }}>
          <div style={{ fontFamily: "'Space Mono', monospace", fontSize: 9, color: COLORS.muted, letterSpacing: 2 }}>NEXUS ANALYTICS PRO · EDUCATIONAL USE ONLY · NOT FINANCIAL ADVICE</div>
          <div style={{ fontSize: 9, color: COLORS.muted, letterSpacing: 1 }}>DATA IS SIMULATED FOR DEMONSTRATION · Powered by Claude AI</div>
        </div>
      </div>
    </div>
  );
}
