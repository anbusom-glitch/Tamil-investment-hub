function App() {
  return (
    <div style={{ padding: '20px', fontFamily: 'Arial', textAlign: 'center' }}>
      <h1>Tamil Invest Hub Pro</h1>
      <p>பங்குச்சந்தை ஆய்வு தளம் - விரைவில் வரும்!</p>
      <div style={{ border: '1px solid #ccc', padding: '10px', marginTop: '20px' }}>
        <h3>முக்கிய விவரங்கள்:</h3>
        <ul style={{ listStyle: 'none' }}>
          <li>LTP: காத்திருங்கள்...</li>
          <li>52-Week Range: ஆய்வு செய்யப்படுகிறது...</li>
        </ul>
      </div>
    </div>
  )
}

export default App

import { useState, useEffect, useRef } from "react";

const translations = {
  en: {
    title: "StockPulse Pro",
    subtitle: "Live Market Intelligence",
    search: "Search stocks...",
    overview: "Overview",
    shareholding: "Shareholding",
    corporate: "Corporate Actions",
    rating: "Rating",
    searchTab: "Search",
    futures: "Futures",
    livePrice: "Live Price",
    change: "Change",
    volume: "Volume",
    marketCap: "Market Cap",
    pe: "P/E Ratio",
    eps: "EPS",
    high52: "52W High",
    low52: "52W Low",
    promoter: "Promoter",
    fii: "FII",
    dii: "DII",
    public: "Public",
    others: "Others",
    shareholdingPattern: "Shareholding Pattern",
    quarterlyTrend: "Quarterly Trend",
    dividend: "Dividend",
    bonus: "Bonus",
    split: "Stock Split",
    rights: "Rights Issue",
    buyback: "Buyback",
    date: "Date",
    details: "Details",
    analystRating: "Analyst Rating",
    strongBuy: "Strong Buy",
    buy: "Buy",
    hold: "Hold",
    sell: "Sell",
    strongSell: "Strong Sell",
    targetPrice: "Target Price",
    upside: "Upside",
    technicalScore: "Technical Score",
    fundamentalScore: "Fundamental Score",
    ticker: "Ticker",
    sector: "Sector",
    industry: "Industry",
    prevClose: "Prev Close",
    open: "Open",
    dayHigh: "Day High",
    dayLow: "Day Low",
    language: "Language",
    scrollingNews: "LIVE MARKET",
    searchPlaceholder: "Search by name or ticker...",
    noResults: "No stocks found",
    selectStock: "Select a stock to view details",
    aiInsights: "AI Insights",
    askAI: "Ask AI about this stock...",
    analyzing: "Analyzing...",
    futuresTitle: "Futures & Derivatives",
    contract: "Contract",
    lotSize: "Lot Size",
    oi: "Open Interest",
    basis: "Basis",
    expiry: "Expiry",
    nearMonth: "Near Month",
    midMonth: "Mid Month",
    farMonth: "Far Month",
    indexFutures: "Index Futures",
    stockFutures: "Stock Futures",
    pcr: "PCR",
    iv: "Implied Vol",
    maxPain: "Max Pain",
    supportLevel: "Support",
    resistanceLevel: "Resistance",
    optionChain: "Option Chain Snapshot",
    callOI: "Call OI",
    putOI: "Put OI",
    strike: "Strike",
  },
  ta: {
    title: "ஸ்டாக்பல்ஸ் ப்ரோ",
    subtitle: "நேரடி சந்தை தகவல்",
    search: "பங்குகளை தேடுங்கள்...",
    overview: "மேலோட்டம்",
    shareholding: "பங்குடைமை",
    corporate: "நிறுவன செயல்கள்",
    rating: "மதிப்பீடு",
    searchTab: "தேடல்",
    futures: "எதிர்கால",
    livePrice: "நேரடி விலை",
    change: "மாற்றம்",
    volume: "அளவு",
    marketCap: "சந்தை மூலதனம்",
    pe: "P/E விகிதம்",
    eps: "EPS",
    high52: "52வாரம் உச்சம்",
    low52: "52வாரம் தாழ்வு",
    promoter: "ஊக்குவிப்பாளர்",
    fii: "FII",
    dii: "DII",
    public: "பொது",
    others: "மற்றவை",
    shareholdingPattern: "பங்குடைமை முறை",
    quarterlyTrend: "காலாண்டு போக்கு",
    dividend: "ஈவுத்தொகை",
    bonus: "போனஸ்",
    split: "பங்கு பிரிப்பு",
    rights: "உரிமை வெளியீடு",
    buyback: "திரும்பக் கொள்முதல்",
    date: "தேதி",
    details: "விவரங்கள்",
    analystRating: "ஆய்வாளர் மதிப்பீடு",
    strongBuy: "வலுவாக வாங்கு",
    buy: "வாங்கு",
    hold: "தடுத்துவை",
    sell: "விற்கு",
    strongSell: "வலுவாக விற்கு",
    targetPrice: "இலக்கு விலை",
    upside: "ஏற்றம்",
    technicalScore: "தொழில்நுட்ப மதிப்பெண்",
    fundamentalScore: "அடிப்படை மதிப்பெண்",
    ticker: "டிக்கர்",
    sector: "துறை",
    industry: "தொழில்",
    prevClose: "முந்தைய மூடல்",
    open: "திறப்பு",
    dayHigh: "நாள் உச்சம்",
    dayLow: "நாள் தாழ்வு",
    language: "மொழி",
    scrollingNews: "நேரடி சந்தை",
    searchPlaceholder: "பெயர் அல்லது டிக்கர் மூலம் தேடுங்கள்...",
    noResults: "பங்குகள் எதுவும் இல்லை",
    selectStock: "விவரங்களை காண ஒரு பங்கை தேர்ந்தெடுக்கவும்",
    aiInsights: "AI பகுப்பாய்வு",
    askAI: "இந்த பங்கு பற்றி AI-யிடம் கேளுங்கள்...",
    analyzing: "பகுப்பாய்வு...",
    futuresTitle: "எதிர்கால & வழித்தோன்றல்கள்",
    contract: "ஒப்பந்தம்",
    lotSize: "லாட் அளவு",
    oi: "திறந்த வட்டி",
    basis: "அடிப்படை",
    expiry: "காலாவதி",
    nearMonth: "அருகில் மாதம்",
    midMonth: "நடு மாதம்",
    farMonth: "தொலைவு மாதம்",
    indexFutures: "குறியீட்டு எதிர்கால",
    stockFutures: "பங்கு எதிர்கால",
    pcr: "PCR",
    iv: "உள்ளார்ந்த வோல்",
    maxPain: "அதிகபட்ச வலி",
    supportLevel: "ஆதரவு",
    resistanceLevel: "எதிர்ப்பு",
    optionChain: "விருப்ப சங்கிலி",
    callOI: "கால் OI",
    putOI: "புட் OI",
    strike: "ஸ்ட்ரைக்",
  },
};

const stocks = [
  {
    name: "Reliance Industries",
    ticker: "RELIANCE",
    price: 2847.35,
    change: 1.24,
    volume: "12.4M",
    marketCap: "₹19.27L Cr",
    pe: 28.4,
    eps: 100.2,
    high52: 3024.9,
    low52: 2185.1,
    sector: "Energy",
    industry: "Oil & Gas",
    prevClose: 2812.5,
    open: 2830.0,
    dayHigh: 2860.0,
    dayLow: 2820.5,
    lotSize: 250,
    futures: {
      near: { expiry: "29 May 2025", price: 2851.2, oi: "4.12M", basis: 3.85 },
      mid: { expiry: "26 Jun 2025", price: 2858.9, oi: "1.87M", basis: 11.55 },
      far: { expiry: "31 Jul 2025", price: 2864.5, oi: "0.43M", basis: 17.15 },
    },
    optionChain: [
      { strike: 2800, callOI: 124500, putOI: 87200 },
      { strike: 2850, callOI: 198300, putOI: 145600 },
      { strike: 2900, callOI: 231000, putOI: 64300 },
      { strike: 2950, callOI: 87400, putOI: 32100 },
    ],
    pcr: 0.74,
    iv: 22.4,
    maxPain: 2850,
    support: 2780,
    resistance: 2920,
    shareholding: {
      promoter: [74.4, 74.4, 74.3, 74.3],
      fii: [8.2, 8.5, 8.7, 9.1],
      dii: [11.3, 11.2, 11.1, 10.8],
      public: [4.8, 4.6, 4.6, 4.5],
      others: [1.3, 1.3, 1.3, 1.3],
    },
    corporate: [
      { type: "dividend", date: "2024-08-12", details: "₹9.5 per share" },
      { type: "bonus", date: "2017-09-20", details: "1:1 Bonus" },
      { type: "split", date: "2017-07-18", details: "1:2 Split" },
    ],
    rating: { strongBuy: 18, buy: 12, hold: 5, sell: 2, strongSell: 0 },
    targetPrice: 3150,
    technicalScore: 72,
    fundamentalScore: 85,
  },
  {
    name: "Infosys Ltd",
    ticker: "INFY",
    price: 1892.6,
    change: -0.87,
    volume: "8.1M",
    marketCap: "₹7.89L Cr",
    pe: 24.1,
    eps: 78.5,
    high52: 2045.6,
    low52: 1358.35,
    sector: "Technology",
    industry: "IT Services",
    prevClose: 1909.2,
    open: 1905.0,
    dayHigh: 1915.3,
    dayLow: 1882.1,
    lotSize: 400,
    futures: {
      near: { expiry: "29 May 2025", price: 1895.4, oi: "3.21M", basis: 2.8 },
      mid: { expiry: "26 Jun 2025", price: 1901.1, oi: "1.14M", basis: 8.5 },
      far: { expiry: "31 Jul 2025", price: 1907.8, oi: "0.31M", basis: 15.2 },
    },
    optionChain: [
      { strike: 1850, callOI: 98700, putOI: 134500 },
      { strike: 1900, callOI: 187400, putOI: 167800 },
      { strike: 1950, callOI: 143200, putOI: 45600 },
      { strike: 2000, callOI: 67800, putOI: 18900 },
    ],
    pcr: 1.12,
    iv: 19.8,
    maxPain: 1900,
    support: 1850,
    resistance: 1960,
    shareholding: {
      promoter: [14.8, 14.9, 15.1, 15.2],
      fii: [33.1, 32.8, 32.5, 32.1],
      dii: [34.2, 34.5, 34.7, 35.0],
      public: [14.6, 14.5, 14.4, 14.3],
      others: [3.3, 3.3, 3.3, 3.4],
    },
    corporate: [
      { type: "dividend", date: "2025-01-15", details: "₹21 per share" },
      { type: "buyback", date: "2023-06-25", details: "₹1,500 Cr buyback" },
      { type: "split", date: "2018-06-01", details: "1:2 Split" },
    ],
    rating: { strongBuy: 10, buy: 15, hold: 8, sell: 3, strongSell: 1 },
    targetPrice: 2100,
    technicalScore: 60,
    fundamentalScore: 78,
  },
  {
    name: "HDFC Bank",
    ticker: "HDFCBANK",
    price: 1654.9,
    change: 0.45,
    volume: "10.2M",
    marketCap: "₹12.56L Cr",
    pe: 18.7,
    eps: 88.5,
    high52: 1880.0,
    low52: 1363.55,
    sector: "Finance",
    industry: "Private Bank",
    prevClose: 1647.5,
    open: 1650.0,
    dayHigh: 1663.4,
    dayLow: 1645.2,
    lotSize: 550,
    futures: {
      near: { expiry: "29 May 2025", price: 1657.3, oi: "5.88M", basis: 2.4 },
      mid: { expiry: "26 Jun 2025", price: 1663.7, oi: "2.01M", basis: 8.8 },
      far: { expiry: "31 Jul 2025", price: 1669.2, oi: "0.52M", basis: 14.3 },
    },
    optionChain: [
      { strike: 1620, callOI: 87300, putOI: 212400 },
      { strike: 1650, callOI: 234100, putOI: 189700 },
      { strike: 1680, callOI: 198500, putOI: 67800 },
      { strike: 1720, callOI: 112300, putOI: 23400 },
    ],
    pcr: 0.89,
    iv: 16.2,
    maxPain: 1650,
    support: 1610,
    resistance: 1720,
    shareholding: {
      promoter: [0, 0, 0, 0],
      fii: [53.2, 53.5, 54.1, 54.8],
      dii: [30.1, 29.8, 29.5, 29.2],
      public: [13.5, 13.5, 13.2, 12.8],
      others: [3.2, 3.2, 3.2, 3.2],
    },
    corporate: [
      { type: "dividend", date: "2025-04-20", details: "₹19.5 per share" },
      { type: "rights", date: "2023-03-10", details: "1:4 Rights @ ₹1400" },
    ],
    rating: { strongBuy: 22, buy: 10, hold: 4, sell: 1, strongSell: 0 },
    targetPrice: 1950,
    technicalScore: 68,
    fundamentalScore: 90,
  },
];

const indexFutures = [
  {
    name: "NIFTY 50",
    spot: 22643,
    futures: [
      { expiry: "29 May 2025", price: 22698, oi: "1.24Cr", basis: 55, change: 0.48 },
      { expiry: "26 Jun 2025", price: 22754, oi: "0.41Cr", basis: 111, change: 0.51 },
      { expiry: "31 Jul 2025", price: 22809, oi: "0.09Cr", basis: 166, change: 0.54 },
    ],
    pcr: 0.91,
    iv: 13.4,
    maxPain: 22600,
  },
  {
    name: "SENSEX",
    spot: 74892,
    futures: [
      { expiry: "30 May 2025", price: 75072, oi: "0.31Cr", basis: 180, change: 0.56 },
      { expiry: "27 Jun 2025", price: 75248, oi: "0.12Cr", basis: 356, change: 0.58 },
    ],
    pcr: 0.87,
    iv: 12.8,
    maxPain: 74800,
  },
  {
    name: "BANKNIFTY",
    spot: 48920,
    futures: [
      { expiry: "29 May 2025", price: 49018, oi: "0.88Cr", basis: 98, change: 0.21 },
      { expiry: "26 Jun 2025", price: 49112, oi: "0.24Cr", basis: 192, change: 0.24 },
    ],
    pcr: 0.78,
    iv: 17.1,
    maxPain: 48500,
  },
];

const tickerItems = [
  "RELIANCE ▲ 2847.35 (+1.24%)",
  "INFY ▼ 1892.60 (-0.87%)",
  "HDFCBANK ▲ 1654.90 (+0.45%)",
  "TCS ▲ 3512.45 (+0.92%)",
  "WIPRO ▼ 478.20 (-0.34%)",
  "BAJFINANCE ▲ 7234.10 (+1.87%)",
  "ICICIBANK ▲ 1102.35 (+0.63%)",
  "TATAMOTORS ▼ 812.50 (-1.12%)",
  "AXISBANK ▲ 1087.75 (+0.78%)",
  "SBIN ▼ 764.30 (-0.21%)",
  "SENSEX ▲ 74,892 (+0.56%)",
  "NIFTY ▲ 22,643 (+0.48%)",
  "GOLD ▲ ₹71,245 (+0.31%)",
  "USD/INR ▼ 83.42 (-0.08%)",
];

const quarters = ["Q1 FY24", "Q2 FY24", "Q3 FY24", "Q4 FY24"];
const corporateTypeColors = {
  dividend: "#10b981",
  bonus: "#f59e0b",
  split: "#6366f1",
  rights: "#3b82f6",
  buyback: "#ec4899",
};
const corporateIcons = {
  dividend: "💰",
  bonus: "🎁",
  split: "✂️",
  rights: "📜",
  buyback: "🔄",
};

function formatOI(oi) {
  const n = parseFloat(oi);
  if (n >= 10000000) return (n / 10000000).toFixed(2) + "Cr";
  if (n >= 100000) return (n / 100000).toFixed(1) + "L";
  return n.toLocaleString("en-IN");
}

export default function StockApp() {
  const [lang, setLang] = useState("en");
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedStock, setSelectedStock] = useState(stocks[0]);
  const [prices, setPrices] = useState(() =>
    stocks.reduce((acc, s) => ({ ...acc, [s.ticker]: s.price }), {})
  );
  const [futurePrices, setFuturePrices] = useState(() => {
    const fp = {};
    stocks.forEach((s) => {
      fp[s.ticker] = {
        near: s.futures.near.price,
        mid: s.futures.mid.price,
        far: s.futures.far.price,
      };
    });
    const idx = {};
    indexFutures.forEach((ix) => {
      idx[ix.name] = ix.futures.map((f) => f.price);
    });
    return { stocks: fp, indices: idx };
  });
  const [indexSpots, setIndexSpots] = useState(() =>
    indexFutures.reduce((acc, ix) => ({ ...acc, [ix.name]: ix.spot }), {})
  );
  const [flashTicker, setFlashTicker] = useState({});
  const [futureFlash, setFutureFlash] = useState({});

  // Search tab state
  const [searchQuery, setSearchQuery] = useState("");
  const [searchSelected, setSearchSelected] = useState(null);
  const searchInputRef = useRef(null);

  // AI state
  const [aiQuery, setAiQuery] = useState("");
  const [aiResponse, setAiResponse] = useState("");
  const [aiLoading, setAiLoading] = useState(false);
  const [aiError, setAiError] = useState("");
  const aiInputRef = useRef(null);

  const t = translations[lang];
  const tickerRef = useRef(null);

  // Live price updates
  useEffect(() => {
    const interval = setInterval(() => {
      setPrices((prev) => {
        const next = { ...prev };
        const flashes = {};
        stocks.forEach((s) => {
          const delta = (Math.random() - 0.49) * 3;
          next[s.ticker] = Math.max(1, prev[s.ticker] + delta);
          flashes[s.ticker] = delta >= 0 ? "up" : "down";
        });
        setFlashTicker(flashes);
        setTimeout(() => setFlashTicker({}), 400);
        return next;
      });

      setFuturePrices((prev) => {
        const nextStocks = { ...prev.stocks };
        const ff = {};
        stocks.forEach((s) => {
          const near = Math.max(1, prev.stocks[s.ticker].near + (Math.random() - 0.49) * 3.2);
          const mid = Math.max(1, prev.stocks[s.ticker].mid + (Math.random() - 0.49) * 3.4);
          const far = Math.max(1, prev.stocks[s.ticker].far + (Math.random() - 0.49) * 3.6);
          nextStocks[s.ticker] = { near, mid, far };
          ff[s.ticker + "_near"] = near > prev.stocks[s.ticker].near ? "up" : "down";
        });
        const nextIndices = { ...prev.indices };
        indexFutures.forEach((ix) => {
          nextIndices[ix.name] = prev.indices[ix.name].map(
            (p) => Math.max(1, p + (Math.random() - 0.49) * 20)
          );
          ff[ix.name] = nextIndices[ix.name][0] > prev.indices[ix.name][0] ? "up" : "down";
        });
        setFutureFlash(ff);
        setTimeout(() => setFutureFlash({}), 400);
        return { stocks: nextStocks, indices: nextIndices };
      });

      setIndexSpots((prev) => {
        const next = { ...prev };
        indexFutures.forEach((ix) => {
          next[ix.name] = Math.max(1, prev[ix.name] + (Math.random() - 0.49) * 15);
        });
        return next;
      });
    }, 1800);
    return () => clearInterval(interval);
  }, []);

  // Search logic
  const searchResults =
    searchQuery.trim() === ""
      ? []
      : stocks.filter((s) => {
          const q = searchQuery.toLowerCase();
          return (
            s.name.toLowerCase().includes(q) ||
            s.ticker.toLowerCase().includes(q) ||
            s.sector.toLowerCase().includes(q) ||
            s.industry.toLowerCase().includes(q)
          );
        });

  useEffect(() => {
    if (activeTab === "search" && searchInputRef.current) {
      setTimeout(() => searchInputRef.current && searchInputRef.current.focus(), 100);
    }
  }, [activeTab]);

  const livePrice = prices[selectedStock.ticker];
  const liveChange = (
    ((livePrice - selectedStock.prevClose) / selectedStock.prevClose) *
    100
  ).toFixed(2);
  const isPositive = parseFloat(liveChange) >= 0;

  const ratingData = selectedStock.rating;
  const totalRatings = Object.values(ratingData).reduce((a, b) => a + b, 0);
  const ratingColors = {
    strongBuy: "#10b981",
    buy: "#34d399",
    hold: "#f59e0b",
    sell: "#f87171",
    strongSell: "#ef4444",
  };

  const latestShareholding = {
    promoter: selectedStock.shareholding.promoter[3],
    fii: selectedStock.shareholding.fii[3],
    dii: selectedStock.shareholding.dii[3],
    public: selectedStock.shareholding.public[3],
    others: selectedStock.shareholding.others[3],
  };

  const donutSegments = (() => {
    const items = [
      { key: "promoter", color: "#6366f1" },
      { key: "fii", color: "#f59e0b" },
      { key: "dii", color: "#10b981" },
      { key: "public", color: "#3b82f6" },
      { key: "others", color: "#ec4899" },
    ];
    let cumulative = 0;
    return items.map((item) => {
      const pct = latestShareholding[item.key];
      const start = cumulative;
      cumulative += pct;
      return { ...item, pct, start };
    });
  })();

  function polarToCartesian(cx, cy, r, angleDeg) {
    const rad = ((angleDeg - 90) * Math.PI) / 180;
    return { x: cx + r * Math.cos(rad), y: cy + r * Math.sin(rad) };
  }

  function arcPath(cx, cy, r, startAngle, endAngle) {
    const s = polarToCartesian(cx, cy, r, startAngle);
    const e = polarToCartesian(cx, cy, r, endAngle);
    const large = endAngle - startAngle > 180 ? 1 : 0;
    return `M ${s.x} ${s.y} A ${r} ${r} 0 ${large} 1 ${e.x} ${e.y}`;
  }

  const tabs = ["overview", "shareholding", "corporate", "rating", "futures", "search"];

  const handleSearchSelect = (stock) => {
    setSearchSelected(stock);
    setSelectedStock(stock);
    setAiQuery("");
    setAiResponse("");
    setAiError("");
  };

  const searchLivePrice = searchSelected ? prices[searchSelected.ticker] : null;
  const searchLiveChange = searchSelected
    ? (
        ((searchLivePrice - searchSelected.prevClose) / searchSelected.prevClose) *
        100
      ).toFixed(2)
    : null;
  const searchIsPositive = searchSelected ? parseFloat(searchLiveChange) >= 0 : false;

  // AI Query function
  const handleAIQuery = async (stockForQuery) => {
    const s = stockForQuery || selectedStock;
    if (!aiQuery.trim()) return;
    setAiLoading(true);
    setAiResponse("");
    setAiError("");
    const lp = prices[s.ticker];
    const chg = (((lp - s.prevClose) / s.prevClose) * 100).toFixed(2);
    const fp = futurePrices.stocks[s.ticker];

    const context = `
Stock: ${s.name} (${s.ticker})
Sector: ${s.sector} | Industry: ${s.industry}
Live Price: ₹${lp.toFixed(2)} (${chg > 0 ? "+" : ""}${chg}%)
Prev Close: ₹${s.prevClose} | Open: ₹${s.open}
Day High: ₹${s.dayHigh} | Day Low: ₹${s.dayLow}
52W High: ₹${s.high52} | 52W Low: ₹${s.low52}
Market Cap: ${s.marketCap} | P/E: ${s.pe} | EPS: ₹${s.eps}
Volume: ${s.volume}
Near Month Futures: ₹${fp.near.toFixed(2)} (Expiry: ${s.futures.near.expiry})
Mid Month Futures: ₹${fp.mid.toFixed(2)} (Expiry: ${s.futures.mid.expiry})
PCR: ${s.pcr} | IV: ${s.iv}% | Max Pain: ₹${s.maxPain}
Support: ₹${s.support} | Resistance: ₹${s.resistance}
Technical Score: ${s.technicalScore}/100 | Fundamental Score: ${s.fundamentalScore}/100
Target Price: ₹${s.targetPrice}
Promoter Holding: ${s.shareholding.promoter[3]}% | FII: ${s.shareholding.fii[3]}% | DII: ${s.shareholding.dii[3]}%
`;

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 1000,
          system: `You are an expert Indian stock market analyst with deep knowledge of NSE/BSE listed companies, derivatives, and market dynamics. You provide concise, insightful analysis based on the provided stock data. Keep responses focused, under 200 words, use ₹ for prices. Be direct and actionable. Format with short paragraphs or bullet points. IMPORTANT: This is for educational/informational purposes only — always add a brief disclaimer.`,
          messages: [
            {
              role: "user",
              content: `Here is the current data for ${s.name}:\n${context}\n\nUser question: ${aiQuery}`,
            },
          ],
        }),
      });
      const data = await res.json();
      if (data.error) throw new Error(data.error.message);
      const text = data.content.map((c) => c.text || "").join("\n");
      setAiResponse(text);
    } catch (err) {
      setAiError("Unable to fetch AI insights. Please try again.");
    } finally {
      setAiLoading(false);
    }
  };

  const liveFutNear = futurePrices.stocks[selectedStock.ticker]?.near;
  const liveFutMid = futurePrices.stocks[selectedStock.ticker]?.mid;
  const liveFutFar = futurePrices.stocks[selectedStock.ticker]?.far;

  return (
    <div style={styles.app}>
      {/* Ticker Tape */}
      <div style={styles.tickerWrap}>
        <span style={styles.tickerLabel}>{t.scrollingNews}</span>
        <div style={styles.tickerInner}>
          <div ref={tickerRef} style={styles.tickerTrack}>
            {[...tickerItems, ...tickerItems].map((item, i) => {
              const isUp = item.includes("▲");
              return (
                <span
                  key={i}
                  style={{ ...styles.tickerItem, color: isUp ? "#34d399" : "#f87171" }}
                >
                  {item}&nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;
                </span>
              );
            })}
          </div>
        </div>
      </div>

      {/* Header */}
      <div style={styles.header}>
        <div>
          <div style={styles.logo}>{t.title}</div>
          <div style={styles.logoSub}>{t.subtitle}</div>
        </div>
        <div style={styles.langSwitch}>
          <span style={styles.langLabel}>{t.language}:</span>
          {["en", "ta"].map((l) => (
            <button
              key={l}
              onClick={() => setLang(l)}
              style={{ ...styles.langBtn, ...(lang === l ? styles.langBtnActive : {}) }}
            >
              {l === "en" ? "English" : "தமிழ்"}
            </button>
          ))}
        </div>
      </div>

      {/* Stock Selector */}
      <div style={styles.stockSelector}>
        {stocks.map((s) => {
          const lp = prices[s.ticker];
          const chg = (((lp - s.prevClose) / s.prevClose) * 100).toFixed(2);
          const pos = parseFloat(chg) >= 0;
          const flash = flashTicker[s.ticker];
          return (
            <button
              key={s.ticker}
              onClick={() => {
                setSelectedStock(s);
                setAiQuery("");
                setAiResponse("");
                setAiError("");
              }}
              style={{
                ...styles.stockCard,
                ...(selectedStock.ticker === s.ticker ? styles.stockCardActive : {}),
                ...(flash === "up" ? styles.flashUp : flash === "down" ? styles.flashDown : {}),
              }}
            >
              <div style={styles.stockCardTicker}>{s.ticker}</div>
              <div style={styles.stockCardName}>{s.name}</div>
              <div style={styles.stockCardPrice}>₹{lp.toFixed(2)}</div>
              <div style={{ ...styles.stockCardChange, color: pos ? "#34d399" : "#f87171" }}>
                {pos ? "▲" : "▼"} {Math.abs(chg)}%
              </div>
            </button>
          );
        })}
      </div>

      {/* Main Card */}
      <div style={styles.mainCard}>
        {/* Price Hero */}
        <div style={styles.priceHero}>
          <div>
            <div style={styles.heroName}>{selectedStock.name}</div>
            <div style={styles.heroMeta}>
              {selectedStock.ticker} &nbsp;•&nbsp; {selectedStock.sector} &nbsp;•&nbsp;{" "}
              {selectedStock.industry}
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div style={{ ...styles.heroPrice, color: isPositive ? "#34d399" : "#f87171" }}>
              ₹{livePrice.toFixed(2)}
            </div>
            <div
              style={{
                ...styles.heroChange,
                background: isPositive ? "rgba(52,211,153,0.15)" : "rgba(248,113,113,0.15)",
                color: isPositive ? "#34d399" : "#f87171",
              }}
            >
              {isPositive ? "▲" : "▼"} {Math.abs(liveChange)}%
            </div>
          </div>
        </div>

        {/* Metric Row */}
        <div style={styles.metricRow}>
          {[
            { label: t.prevClose, value: `₹${selectedStock.prevClose}` },
            { label: t.open, value: `₹${selectedStock.open}` },
            { label: t.dayHigh, value: `₹${selectedStock.dayHigh}` },
            { label: t.dayLow, value: `₹${selectedStock.dayLow}` },
            { label: t.high52, value: `₹${selectedStock.high52}` },
            { label: t.low52, value: `₹${selectedStock.low52}` },
            { label: t.pe, value: selectedStock.pe },
            { label: t.eps, value: `₹${selectedStock.eps}` },
            { label: t.volume, value: selectedStock.volume },
            { label: t.marketCap, value: selectedStock.marketCap },
          ].map((m, i) => (
            <div key={i} style={styles.metricBox}>
              <div style={styles.metricLabel}>{m.label}</div>
              <div style={styles.metricValue}>{m.value}</div>
            </div>
          ))}
        </div>

        {/* Tabs */}
        <div style={styles.tabBar}>
          {tabs.map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{ ...styles.tabBtn, ...(activeTab === tab ? styles.tabBtnActive : {}) }}
            >
              {tab === "search" ? t.searchTab : tab === "futures" ? t.futures : t[tab]}
            </button>
          ))}
        </div>

        {/* TAB: Overview */}
        {activeTab === "overview" && (
          <div style={styles.section}>
            <div style={styles.grid2}>
              <div style={styles.infoCard}>
                <div style={styles.infoCardTitle}>{t.ticker}</div>
                <div style={styles.infoCardValue}>{selectedStock.ticker}</div>
              </div>
              <div style={styles.infoCard}>
                <div style={styles.infoCardTitle}>{t.sector}</div>
                <div style={styles.infoCardValue}>{selectedStock.sector}</div>
              </div>
              <div style={styles.infoCard}>
                <div style={styles.infoCardTitle}>{t.industry}</div>
                <div style={styles.infoCardValue}>{selectedStock.industry}</div>
              </div>
              <div style={styles.infoCard}>
                <div style={styles.infoCardTitle}>{t.marketCap}</div>
                <div style={styles.infoCardValue}>{selectedStock.marketCap}</div>
              </div>
            </div>

            {/* 52W Range */}
            <div style={styles.rangeBox}>
              <div style={styles.rangeLabel}>
                <span style={{ color: "#94a3b8" }}>
                  {t.low52}: ₹{selectedStock.low52}
                </span>
                <span style={{ color: "#f8fafc", fontWeight: 600 }}>52W Range</span>
                <span style={{ color: "#94a3b8" }}>
                  {t.high52}: ₹{selectedStock.high52}
                </span>
              </div>
              <div style={styles.rangeTrack}>
                <div
                  style={{
                    ...styles.rangeFill,
                    width: `${Math.min(
                      100,
                      ((livePrice - selectedStock.low52) /
                        (selectedStock.high52 - selectedStock.low52)) *
                        100
                    ).toFixed(1)}%`,
                  }}
                />
                <div
                  style={{
                    ...styles.rangeDot,
                    left: `${Math.min(
                      100,
                      ((livePrice - selectedStock.low52) /
                        (selectedStock.high52 - selectedStock.low52)) *
                        100
                    ).toFixed(1)}%`,
                  }}
                />
              </div>
            </div>

            {/* AI Insights Panel */}
            <div style={styles.aiPanel}>
              <div style={styles.aiPanelHeader}>
                <span style={styles.aiPanelIcon}>🤖</span>
                <span style={styles.aiPanelTitle}>{t.aiInsights}</span>
                <span style={styles.aiBadge}>Powered by Claude</span>
              </div>
              <div style={styles.aiInputRow}>
                <input
                  ref={aiInputRef}
                  type="text"
                  value={aiQuery}
                  onChange={(e) => setAiQuery(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleAIQuery()}
                  placeholder={t.askAI}
                  style={styles.aiInput}
                />
                <button
                  onClick={() => handleAIQuery()}
                  disabled={aiLoading || !aiQuery.trim()}
                  style={{
                    ...styles.aiSendBtn,
                    opacity: aiLoading || !aiQuery.trim() ? 0.5 : 1,
                    cursor: aiLoading || !aiQuery.trim() ? "not-allowed" : "pointer",
                  }}
                >
                  {aiLoading ? "..." : "→"}
                </button>
              </div>
              {/* Quick prompts */}
              <div style={styles.quickPrompts}>
                {[
                  "Is this a good buy now?",
                  "Explain the futures basis",
                  "Key risks for this stock",
                  "Shareholding analysis",
                ].map((q) => (
                  <button
                    key={q}
                    onClick={() => {
                      setAiQuery(q);
                      setTimeout(() => {
                        const queryToSend = q;
                        setAiQuery(queryToSend);
                        setAiLoading(true);
                        setAiResponse("");
                        setAiError("");
                        const s = selectedStock;
                        const lp = prices[s.ticker];
                        const chg = (((lp - s.prevClose) / s.prevClose) * 100).toFixed(2);
                        const fp = futurePrices.stocks[s.ticker];
                        const context = `Stock: ${s.name} (${s.ticker})\nSector: ${s.sector} | Industry: ${s.industry}\nLive Price: ₹${lp.toFixed(2)} (${chg > 0 ? "+" : ""}${chg}%)\nPrev Close: ₹${s.prevClose} | Open: ₹${s.open}\nDay High: ₹${s.dayHigh} | Day Low: ₹${s.dayLow}\n52W High: ₹${s.high52} | 52W Low: ₹${s.low52}\nMarket Cap: ${s.marketCap} | P/E: ${s.pe} | EPS: ₹${s.eps}\nVolume: ${s.volume}\nNear Month Futures: ₹${fp.near.toFixed(2)} (Expiry: ${s.futures.near.expiry})\nMid Month Futures: ₹${fp.mid.toFixed(2)} (Expiry: ${s.futures.mid.expiry})\nPCR: ${s.pcr} | IV: ${s.iv}% | Max Pain: ₹${s.maxPain}\nSupport: ₹${s.support} | Resistance: ₹${s.resistance}\nTechnical Score: ${s.technicalScore}/100 | Fundamental Score: ${s.fundamentalScore}/100\nTarget Price: ₹${s.targetPrice}\nPromoter Holding: ${s.shareholding.promoter[3]}% | FII: ${s.shareholding.fii[3]}% | DII: ${s.shareholding.dii[3]}%`;
                        fetch("https://api.anthropic.com/v1/messages", {
                          method: "POST",
                          headers: { "Content-Type": "application/json" },
                          body: JSON.stringify({
                            model: "claude-sonnet-4-20250514",
                            max_tokens: 1000,
                            system: `You are an expert Indian stock market analyst. Provide concise, insightful analysis based on the stock data. Keep responses under 200 words, use ₹ for prices. Be direct and actionable. Format with short paragraphs or bullet points. Add a brief disclaimer.`,
                            messages: [{ role: "user", content: `Here is the current data for ${s.name}:\n${context}\n\nUser question: ${queryToSend}` }],
                          }),
                        })
                          .then((r) => r.json())
                          .then((data) => {
                            if (data.error) throw new Error(data.error.message);
                            const text = data.content.map((c) => c.text || "").join("\n");
                            setAiResponse(text);
                          })
                          .catch(() => setAiError("Unable to fetch AI insights. Please try again."))
                          .finally(() => setAiLoading(false));
                      }, 0);
                    }}
                    style={styles.quickPromptBtn}
                  >
                    {q}
                  </button>
                ))}
              </div>
              {aiLoading && (
                <div style={styles.aiLoading}>
                  <div style={styles.aiLoadingDots}>
                    <span /><span /><span />
                  </div>
                  <span style={{ color: "#64748b", fontSize: 13 }}>{t.analyzing}</span>
                </div>
              )}
              {aiResponse && !aiLoading && (
                <div style={styles.aiResponse}>
                  <div style={styles.aiResponseText}>{aiResponse}</div>
                </div>
              )}
              {aiError && !aiLoading && (
                <div style={styles.aiError}>{aiError}</div>
              )}
            </div>
          </div>
        )}

        {/* TAB: Shareholding */}
        {activeTab === "shareholding" && (
          <div style={styles.section}>
            <div style={styles.sectionTitle}>{t.shareholdingPattern}</div>
            <div style={styles.donutRow}>
              <svg width="180" height="180" viewBox="0 0 180 180">
                <circle cx="90" cy="90" r="70" fill="none" stroke="#1e293b" strokeWidth="2" />
                {donutSegments.map((seg, i) => {
                  const startAngle = (seg.start / 100) * 360;
                  const endAngle = ((seg.start + seg.pct) / 100) * 360;
                  if (seg.pct === 0) return null;
                  return (
                    <path
                      key={i}
                      d={arcPath(90, 90, 65, startAngle, endAngle)}
                      fill="none"
                      stroke={seg.color}
                      strokeWidth="22"
                      strokeLinecap="butt"
                    />
                  );
                })}
                <circle cx="90" cy="90" r="42" fill="#0f172a" />
                <text x="90" y="86" textAnchor="middle" fill="#f8fafc" fontSize="11" fontWeight="700">
                  {latestShareholding.promoter}%
                </text>
                <text x="90" y="101" textAnchor="middle" fill="#64748b" fontSize="9">
                  Promoter
                </text>
              </svg>
              <div style={styles.legend}>
                {donutSegments.map((seg) => (
                  <div key={seg.key} style={styles.legendItem}>
                    <div style={{ ...styles.legendDot, background: seg.color }} />
                    <span style={styles.legendKey}>{t[seg.key]}</span>
                    <span style={styles.legendVal}>{seg.pct}%</span>
                  </div>
                ))}
              </div>
            </div>
            <div style={styles.sectionTitle}>{t.quarterlyTrend}</div>
            <div style={styles.trendTable}>
              <div style={styles.trendHeader}>
                <div style={styles.trendCell}></div>
                {quarters.map((q) => (
                  <div key={q} style={{ ...styles.trendCell, color: "#94a3b8" }}>{q}</div>
                ))}
              </div>
              {[
                { key: "promoter", color: "#6366f1" },
                { key: "fii", color: "#f59e0b" },
                { key: "dii", color: "#10b981" },
                { key: "public", color: "#3b82f6" },
                { key: "others", color: "#ec4899" },
              ].map((row) => (
                <div key={row.key} style={styles.trendRow}>
                  <div style={{ ...styles.trendCell, display: "flex", alignItems: "center", gap: 6 }}>
                    <div style={{ width: 8, height: 8, borderRadius: "50%", background: row.color }} />
                    <span style={{ color: "#e2e8f0", fontSize: 12 }}>{t[row.key]}</span>
                  </div>
                  {selectedStock.shareholding[row.key].map((v, i) => {
                    const prev = i > 0 ? selectedStock.shareholding[row.key][i - 1] : v;
                    const delta = v - prev;
                    return (
                      <div key={i} style={styles.trendCell}>
                        <span style={{ color: "#f8fafc", fontWeight: 600 }}>{v}%</span>
                        {i > 0 && (
                          <span
                            style={{
                              fontSize: 9,
                              color: delta > 0 ? "#34d399" : delta < 0 ? "#f87171" : "#64748b",
                              marginLeft: 3,
                            }}
                          >
                            {delta > 0 ? "▲" : delta < 0 ? "▼" : "–"}
                            {Math.abs(delta).toFixed(1)}
                          </span>
                        )}
                      </div>
                    );
                  })}
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB: Corporate Actions */}
        {activeTab === "corporate" && (
          <div style={styles.section}>
            <div style={styles.sectionTitle}>{t.corporate}</div>
            <div style={styles.corpList}>
              {selectedStock.corporate.map((action, i) => (
                <div key={i} style={styles.corpCard}>
                  <div
                    style={{
                      ...styles.corpBadge,
                      background: corporateTypeColors[action.type] + "22",
                      border: `1px solid ${corporateTypeColors[action.type]}44`,
                    }}
                  >
                    <span style={{ fontSize: 20 }}>{corporateIcons[action.type]}</span>
                    <span style={{ color: corporateTypeColors[action.type], fontWeight: 700, fontSize: 12 }}>
                      {t[action.type] || action.type}
                    </span>
                  </div>
                  <div style={styles.corpDetails}>
                    <div style={{ color: "#f8fafc", fontWeight: 600, fontSize: 14 }}>{action.details}</div>
                    <div style={{ color: "#64748b", fontSize: 12, marginTop: 2 }}>
                      {t.date}: {action.date}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* TAB: Rating */}
        {activeTab === "rating" && (
          <div style={styles.section}>
            <div style={styles.sectionTitle}>{t.analystRating}</div>
            {Object.entries(ratingData).map(([key, count]) => {
              const pct = ((count / totalRatings) * 100).toFixed(0);
              return (
                <div key={key} style={styles.ratingRow}>
                  <div style={{ ...styles.ratingLabel, color: ratingColors[key] }}>{t[key]}</div>
                  <div style={styles.ratingTrack}>
                    <div style={{ ...styles.ratingFill, width: `${pct}%`, background: ratingColors[key] }} />
                  </div>
                  <div style={styles.ratingCount}>{count}</div>
                </div>
              );
            })}
            <div style={styles.scoreGrid}>
              <div style={styles.scoreBox}>
                <div style={styles.scoreLabel}>{t.technicalScore}</div>
                <div style={styles.scorePie}>
                  <svg width="80" height="80">
                    <circle cx="40" cy="40" r="32" fill="none" stroke="#1e293b" strokeWidth="8" />
                    <circle
                      cx="40" cy="40" r="32" fill="none" stroke="#6366f1" strokeWidth="8"
                      strokeDasharray={`${(selectedStock.technicalScore / 100) * 201} 201`}
                      strokeDashoffset="50" strokeLinecap="round"
                    />
                    <text x="40" y="45" textAnchor="middle" fill="#f8fafc" fontSize="14" fontWeight="700">
                      {selectedStock.technicalScore}
                    </text>
                  </svg>
                </div>
              </div>
              <div style={styles.scoreBox}>
                <div style={styles.scoreLabel}>{t.fundamentalScore}</div>
                <div style={styles.scorePie}>
                  <svg width="80" height="80">
                    <circle cx="40" cy="40" r="32" fill="none" stroke="#1e293b" strokeWidth="8" />
                    <circle
                      cx="40" cy="40" r="32" fill="none" stroke="#10b981" strokeWidth="8"
                      strokeDasharray={`${(selectedStock.fundamentalScore / 100) * 201} 201`}
                      strokeDashoffset="50" strokeLinecap="round"
                    />
                    <text x="40" y="45" textAnchor="middle" fill="#f8fafc" fontSize="14" fontWeight="700">
                      {selectedStock.fundamentalScore}
                    </text>
                  </svg>
                </div>
              </div>
              <div style={styles.scoreBox}>
                <div style={styles.scoreLabel}>{t.targetPrice}</div>
                <div style={styles.targetPrice}>₹{selectedStock.targetPrice}</div>
                <div style={{ color: "#34d399", fontSize: 12, marginTop: 4 }}>
                  {t.upside}: +{(((selectedStock.targetPrice - livePrice) / livePrice) * 100).toFixed(1)}%
                </div>
              </div>
            </div>
          </div>
        )}

        {/* TAB: Futures */}
        {activeTab === "futures" && (
          <div style={styles.section}>
            {/* Index Futures */}
            <div style={styles.sectionTitle}>{t.indexFutures}</div>
            <div style={styles.indexFutGrid}>
              {indexFutures.map((ix) => {
                const spot = indexSpots[ix.name];
                const nearFut = futurePrices.indices[ix.name]?.[0];
                const flash = futureFlash[ix.name];
                const spotChg = ((nearFut - spot) / spot * 100).toFixed(2);
                const spotPos = parseFloat(spotChg) >= 0;
                return (
                  <div
                    key={ix.name}
                    style={{
                      ...styles.indexFutCard,
                      ...(flash === "up" ? styles.flashUpSoft : flash === "down" ? styles.flashDownSoft : {}),
                    }}
                  >
                    <div style={styles.indexFutName}>{ix.name}</div>
                    <div style={styles.indexFutSpot}>
                      <span style={styles.indexFutSpotLabel}>SPOT</span>
                      <span style={styles.indexFutSpotVal}>{spot.toFixed(0)}</span>
                    </div>
                    <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: 6 }}>
                      <div style={styles.indexFutNear}>
                        <span style={styles.indexFutNearLabel}>NEAR FUT</span>
                        <span style={{ color: spotPos ? "#34d399" : "#f87171", fontWeight: 700, fontSize: 15 }}>
                          {nearFut?.toFixed(0)}
                        </span>
                      </div>
                      <div style={{ ...styles.basisTag, color: spotPos ? "#34d399" : "#f87171", background: spotPos ? "rgba(52,211,153,0.1)" : "rgba(248,113,113,0.1)" }}>
                        {spotPos ? "+" : ""}{(nearFut - spot).toFixed(0)}
                      </div>
                    </div>
                    <div style={styles.indexFutMeta}>
                      PCR: <strong>{ix.pcr}</strong> &nbsp;|&nbsp; IV: <strong>{ix.iv}%</strong> &nbsp;|&nbsp; Max Pain: <strong>{ix.maxPain.toLocaleString("en-IN")}</strong>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Stock Futures */}
            <div style={styles.sectionTitle} style={{ marginTop: 20, fontSize: 14, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1, marginBottom: 16 }}>
              {t.stockFutures} — {selectedStock.ticker}
            </div>

            <div style={styles.futContractsGrid}>
              {[
                { label: t.nearMonth, key: "near", price: liveFutNear, data: selectedStock.futures.near },
                { label: t.midMonth, key: "mid", price: liveFutMid, data: selectedStock.futures.mid },
                { label: t.farMonth, key: "far", price: liveFutFar, data: selectedStock.futures.far },
              ].map(({ label, key, price, data }) => {
                const basis = price - livePrice;
                const basisPos = basis >= 0;
                const flash = futureFlash[selectedStock.ticker + "_near"];
                return (
                  <div
                    key={key}
                    style={{
                      ...styles.futContractCard,
                      ...(key === "near" && flash === "up" ? styles.flashUpSoft : key === "near" && flash === "down" ? styles.flashDownSoft : {}),
                    }}
                  >
                    <div style={styles.futContractLabel}>{label}</div>
                    <div style={styles.futContractExpiry}>{t.expiry}: {data.expiry}</div>
                    <div style={{ ...styles.futContractPrice, color: basisPos ? "#34d399" : "#f87171" }}>
                      ₹{price?.toFixed(2)}
                    </div>
                    <div style={styles.futContractRow}>
                      <div style={styles.futMetaItem}>
                        <span style={styles.futMetaLabel}>{t.basis}</span>
                        <span style={{ color: basisPos ? "#34d399" : "#f87171", fontWeight: 600, fontSize: 13 }}>
                          {basisPos ? "+" : ""}{basis.toFixed(2)}
                        </span>
                      </div>
                      <div style={styles.futMetaItem}>
                        <span style={styles.futMetaLabel}>{t.oi}</span>
                        <span style={{ color: "#e2e8f0", fontWeight: 600, fontSize: 13 }}>{data.oi}</span>
                      </div>
                      <div style={styles.futMetaItem}>
                        <span style={styles.futMetaLabel}>{t.lotSize}</span>
                        <span style={{ color: "#e2e8f0", fontWeight: 600, fontSize: 13 }}>{selectedStock.lotSize}</span>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Derivatives Summary */}
            <div style={styles.derivSummary}>
              <div style={styles.derivSummaryItem}>
                <div style={styles.derivLabel}>{t.pcr}</div>
                <div style={{
                  ...styles.derivVal,
                  color: selectedStock.pcr > 1 ? "#34d399" : selectedStock.pcr < 0.7 ? "#f87171" : "#f59e0b",
                }}>
                  {selectedStock.pcr}
                </div>
                <div style={styles.derivHint}>
                  {selectedStock.pcr > 1 ? "Bullish" : selectedStock.pcr < 0.7 ? "Bearish" : "Neutral"}
                </div>
              </div>
              <div style={styles.derivSummaryItem}>
                <div style={styles.derivLabel}>{t.iv}</div>
                <div style={styles.derivVal}>{selectedStock.iv}%</div>
                <div style={styles.derivHint}>Implied Vol</div>
              </div>
              <div style={styles.derivSummaryItem}>
                <div style={styles.derivLabel}>{t.maxPain}</div>
                <div style={styles.derivVal}>₹{selectedStock.maxPain}</div>
                <div style={styles.derivHint}>Options Pain</div>
              </div>
              <div style={styles.derivSummaryItem}>
                <div style={styles.derivLabel}>{t.supportLevel}</div>
                <div style={{ ...styles.derivVal, color: "#34d399" }}>₹{selectedStock.support}</div>
                <div style={styles.derivHint}>Key Support</div>
              </div>
              <div style={styles.derivSummaryItem}>
                <div style={styles.derivLabel}>{t.resistanceLevel}</div>
                <div style={{ ...styles.derivVal, color: "#f87171" }}>₹{selectedStock.resistance}</div>
                <div style={styles.derivHint}>Key Resistance</div>
              </div>
            </div>

            {/* Option Chain Snapshot */}
            <div style={{ marginTop: 20 }}>
              <div style={{ fontSize: 13, fontWeight: 700, color: "#94a3b8", textTransform: "uppercase", letterSpacing: 1, marginBottom: 12 }}>
                {t.optionChain}
              </div>
              <div style={styles.optionChainTable}>
                <div style={styles.optionChainHeader}>
                  <div style={{ ...styles.optionChainCell, textAlign: "right", color: "#34d399" }}>{t.callOI}</div>
                  <div style={{ ...styles.optionChainCell, textAlign: "center", color: "#f8fafc", fontWeight: 700 }}>{t.strike}</div>
                  <div style={{ ...styles.optionChainCell, textAlign: "left", color: "#f87171" }}>{t.putOI}</div>
                </div>
                {selectedStock.optionChain.map((row, i) => {
                  const maxOI = Math.max(...selectedStock.optionChain.map((r) => Math.max(r.callOI, r.putOI)));
                  const callPct = (row.callOI / maxOI) * 100;
                  const putPct = (row.putOI / maxOI) * 100;
                  const isATM = Math.abs(row.strike - livePrice) < 50;
                  return (
                    <div
                      key={i}
                      style={{
                        ...styles.optionChainRow,
                        ...(isATM ? styles.optionChainATM : {}),
                      }}
                    >
                      <div style={{ flex: 1, textAlign: "right", paddingRight: 8 }}>
                        <div style={{ fontSize: 11, color: "#34d399", fontWeight: 600 }}>
                          {(row.callOI / 1000).toFixed(1)}K
                        </div>
                        <div style={styles.optionBar}>
                          <div style={{ ...styles.optionBarFill, width: `${callPct}%`, background: "#34d399", marginLeft: "auto" }} />
                        </div>
                      </div>
                      <div style={styles.strikeCell}>
                        ₹{row.strike}
                        {isATM && <span style={styles.atmBadge}>ATM</span>}
                      </div>
                      <div style={{ flex: 1, textAlign: "left", paddingLeft: 8 }}>
                        <div style={{ fontSize: 11, color: "#f87171", fontWeight: 600 }}>
                          {(row.putOI / 1000).toFixed(1)}K
                        </div>
                        <div style={styles.optionBar}>
                          <div style={{ ...styles.optionBarFill, width: `${putPct}%`, background: "#f87171" }} />
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}

        {/* TAB: Search */}
        {activeTab === "search" && (
          <div style={styles.section}>
            <div style={styles.searchBox}>
              <span style={styles.searchIcon}>🔍</span>
              <input
                ref={searchInputRef}
                type="text"
                value={searchQuery}
                onChange={(e) => {
                  setSearchQuery(e.target.value);
                  setSearchSelected(null);
                  setAiResponse("");
                  setAiError("");
                }}
                placeholder={t.searchPlaceholder}
                style={styles.searchInput}
              />
              {searchQuery.length > 0 && (
                <button
                  onClick={() => {
                    setSearchQuery("");
                    setSearchSelected(null);
                    setAiResponse("");
                    setAiError("");
                  }}
                  style={styles.searchClear}
                >
                  ✕
                </button>
              )}
            </div>

            {searchQuery.trim() !== "" && (
              <div style={styles.searchResultsList}>
                {searchResults.length === 0 ? (
                  <div style={styles.noResults}>
                    <div style={{ fontSize: 32, marginBottom: 8 }}>🔎</div>
                    <div style={{ color: "#64748b", fontSize: 14 }}>{t.noResults}</div>
                  </div>
                ) : (
                  searchResults.map((stock) => {
                    const lp = prices[stock.ticker];
                    const chg = (((lp - stock.prevClose) / stock.prevClose) * 100).toFixed(2);
                    const pos = parseFloat(chg) >= 0;
                    const isActive = searchSelected && searchSelected.ticker === stock.ticker;
                    return (
                      <button
                        key={stock.ticker}
                        onClick={() => handleSearchSelect(stock)}
                        style={{ ...styles.searchResultItem, ...(isActive ? styles.searchResultItemActive : {}) }}
                      >
                        <div style={styles.searchResultLeft}>
                          <div style={styles.searchResultTicker}>{stock.ticker}</div>
                          <div style={styles.searchResultName}>{stock.name}</div>
                          <div style={styles.searchResultMeta}>{stock.sector} • {stock.industry}</div>
                        </div>
                        <div style={styles.searchResultRight}>
                          <div style={styles.searchResultPrice}>₹{lp.toFixed(2)}</div>
                          <div style={{ ...styles.searchResultChg, color: pos ? "#34d399" : "#f87171" }}>
                            {pos ? "▲" : "▼"} {Math.abs(chg)}%
                          </div>
                          <div style={styles.searchResultCap}>{stock.marketCap}</div>
                        </div>
                      </button>
                    );
                  })
                )}
              </div>
            )}

            {searchSelected && (
              <div style={styles.searchDetailCard}>
                <div style={styles.searchDetailHeader}>
                  <div>
                    <div style={styles.searchDetailName}>{searchSelected.name}</div>
                    <div style={styles.searchDetailMeta}>{searchSelected.ticker} • {searchSelected.sector} • {searchSelected.industry}</div>
                  </div>
                  <div style={{ textAlign: "right" }}>
                    <div style={{ ...styles.searchDetailPrice, color: searchIsPositive ? "#34d399" : "#f87171" }}>
                      ₹{searchLivePrice.toFixed(2)}
                    </div>
                    <div style={{
                      ...styles.searchDetailChgBadge,
                      background: searchIsPositive ? "rgba(52,211,153,0.15)" : "rgba(248,113,113,0.15)",
                      color: searchIsPositive ? "#34d399" : "#f87171",
                    }}>
                      {searchIsPositive ? "▲" : "▼"} {Math.abs(searchLiveChange)}%
                    </div>
                  </div>
                </div>

                <div style={styles.searchDetailGrid}>
                  {[
                    { label: t.prevClose, value: `₹${searchSelected.prevClose}` },
                    { label: t.open, value: `₹${searchSelected.open}` },
                    { label: t.dayHigh, value: `₹${searchSelected.dayHigh}` },
                    { label: t.dayLow, value: `₹${searchSelected.dayLow}` },
                    { label: t.high52, value: `₹${searchSelected.high52}` },
                    { label: t.low52, value: `₹${searchSelected.low52}` },
                    { label: t.pe, value: searchSelected.pe },
                    { label: t.eps, value: `₹${searchSelected.eps}` },
                    { label: t.volume, value: searchSelected.volume },
                    { label: t.marketCap, value: searchSelected.marketCap },
                  ].map((m, i) => (
                    <div key={i} style={styles.searchDetailMetric}>
                      <div style={styles.searchDetailMetricLabel}>{m.label}</div>
                      <div style={styles.searchDetailMetricValue}>{m.value}</div>
                    </div>
                  ))}
                </div>

                <div style={styles.searchScoreRow}>
                  <div style={styles.searchScoreItem}>
                    <div style={styles.searchScoreLabel}>{t.technicalScore}</div>
                    <div style={styles.searchScoreBar}>
                      <div style={{ ...styles.searchScoreFill, width: `${searchSelected.technicalScore}%`, background: "#6366f1" }} />
                    </div>
                    <div style={styles.searchScoreVal}>{searchSelected.technicalScore}</div>
                  </div>
                  <div style={styles.searchScoreItem}>
                    <div style={styles.searchScoreLabel}>{t.fundamentalScore}</div>
                    <div style={styles.searchScoreBar}>
                      <div style={{ ...styles.searchScoreFill, width: `${searchSelected.fundamentalScore}%`, background: "#10b981" }} />
                    </div>
                    <div style={styles.searchScoreVal}>{searchSelected.fundamentalScore}</div>
                  </div>
                  <div style={styles.searchScoreItem}>
                    <div style={styles.searchScoreLabel}>{t.targetPrice}</div>
                    <div style={{ color: "#f8fafc", fontWeight: 700, fontSize: 15, marginTop: 4 }}>₹{searchSelected.targetPrice}</div>
                    <div style={{ color: "#34d399", fontSize: 11 }}>
                      {t.upside}: +{(((searchSelected.targetPrice - searchLivePrice) / searchLivePrice) * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>

                {/* AI in Search */}
                <div style={{ ...styles.aiPanel, marginTop: 16, borderRadius: 12 }}>
                  <div style={styles.aiPanelHeader}>
                    <span style={styles.aiPanelIcon}>🤖</span>
                    <span style={styles.aiPanelTitle}>{t.aiInsights}</span>
                    <span style={styles.aiBadge}>Powered by Claude</span>
                  </div>
                  <div style={styles.aiInputRow}>
                    <input
                      type="text"
                      value={aiQuery}
                      onChange={(e) => setAiQuery(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && handleAIQuery(searchSelected)}
                      placeholder={t.askAI}
                      style={styles.aiInput}
                    />
                    <button
                      onClick={() => handleAIQuery(searchSelected)}
                      disabled={aiLoading || !aiQuery.trim()}
                      style={{
                        ...styles.aiSendBtn,
                        opacity: aiLoading || !aiQuery.trim() ? 0.5 : 1,
                        cursor: aiLoading || !aiQuery.trim() ? "not-allowed" : "pointer",
                      }}
                    >
                      {aiLoading ? "..." : "→"}
                    </button>
                  </div>
                  <div style={styles.quickPrompts}>
                    {["Quick analysis", "Buy or sell?", "Key risks"].map((q) => (
                      <button key={q} onClick={() => { setAiQuery(q); }} style={styles.quickPromptBtn}>{q}</button>
                    ))}
                  </div>
                  {aiLoading && (
                    <div style={styles.aiLoading}>
                      <div style={styles.aiLoadingDots}><span /><span /><span /></div>
                      <span style={{ color: "#64748b", fontSize: 13 }}>{t.analyzing}</span>
                    </div>
                  )}
                  {aiResponse && !aiLoading && (
                    <div style={styles.aiResponse}>
                      <div style={styles.aiResponseText}>{aiResponse}</div>
                    </div>
                  )}
                  {aiError && !aiLoading && <div style={styles.aiError}>{aiError}</div>}
                </div>
              </div>
            )}

            {searchQuery.trim() === "" && !searchSelected && (
              <div style={styles.searchEmpty}>
                <div style={{ fontSize: 40, marginBottom: 12 }}>📈</div>
                <div style={{ color: "#64748b", fontSize: 14 }}>{t.selectStock}</div>
                <div style={{ color: "#334155", fontSize: 12, marginTop: 6 }}>
                  {stocks.map((s) => s.ticker).join(" • ")}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Noto+Sans+Tamil:wght@400;600;700&display=swap');
        @keyframes ticker {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        @keyframes flashUp {
          0%,100% { background: transparent; }
          50% { background: rgba(52,211,153,0.2); }
        }
        @keyframes flashDown {
          0%,100% { background: transparent; }
          50% { background: rgba(248,113,113,0.2); }
        }
        @keyframes flashUpSoft {
          0%,100% { border-color: #1e293b; }
          50% { border-color: rgba(52,211,153,0.4); box-shadow: 0 0 12px rgba(52,211,153,0.15); }
        }
        @keyframes flashDownSoft {
          0%,100% { border-color: #1e293b; }
          50% { border-color: rgba(248,113,113,0.4); box-shadow: 0 0 12px rgba(248,113,113,0.15); }
        }
        @keyframes pulse {
          0%,100% { opacity:1; }
          50% { opacity:0.4; }
        }
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0a0f1e; }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 2px; }
        .ai-loading-dots span {
          display: inline-block;
          width: 6px; height: 6px;
          border-radius: 50%;
          background: #6366f1;
          margin: 0 2px;
          animation: pulse 1.2s ease-in-out infinite;
        }
        .ai-loading-dots span:nth-child(2) { animation-delay: 0.2s; }
        .ai-loading-dots span:nth-child(3) { animation-delay: 0.4s; }
      `}</style>
    </div>
  );
}

const styles = {
  app: {
    background: "linear-gradient(135deg, #0a0f1e 0%, #0d1829 50%, #0a0f1e 100%)",
    minHeight: "100vh",
    fontFamily: "'Space Grotesk', 'Noto Sans Tamil', sans-serif",
    color: "#f8fafc",
    paddingBottom: 40,
  },
  tickerWrap: {
    background: "#050a14",
    borderBottom: "1px solid #1e293b",
    display: "flex",
    alignItems: "center",
    overflow: "hidden",
    height: 36,
  },
  tickerLabel: {
    background: "#6366f1",
    color: "#fff",
    fontWeight: 700,
    fontSize: 10,
    padding: "0 12px",
    height: "100%",
    display: "flex",
    alignItems: "center",
    letterSpacing: 1.5,
    flexShrink: 0,
  },
  tickerInner: { flex: 1, overflow: "hidden", position: "relative" },
  tickerTrack: {
    display: "inline-flex",
    whiteSpace: "nowrap",
    animation: "ticker 35s linear infinite",
    paddingLeft: 16,
  },
  tickerItem: { fontSize: 12, fontWeight: 600, letterSpacing: 0.5 },
  header: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "20px 24px 16px",
    borderBottom: "1px solid #1e293b",
  },
  logo: {
    fontSize: 24,
    fontWeight: 700,
    background: "linear-gradient(90deg, #6366f1, #a78bfa)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
    letterSpacing: -0.5,
  },
  logoSub: { fontSize: 11, color: "#64748b", marginTop: 2, letterSpacing: 1, textTransform: "uppercase" },
  langSwitch: { display: "flex", alignItems: "center", gap: 8 },
  langLabel: { fontSize: 12, color: "#64748b" },
  langBtn: {
    background: "#1e293b",
    border: "1px solid #334155",
    color: "#94a3b8",
    padding: "5px 14px",
    borderRadius: 20,
    cursor: "pointer",
    fontSize: 12,
    fontWeight: 600,
    transition: "all 0.2s",
  },
  langBtnActive: { background: "#6366f1", border: "1px solid #6366f1", color: "#fff" },
  stockSelector: { display: "flex", gap: 12, padding: "16px 24px", overflowX: "auto" },
  stockCard: {
    background: "#0f172a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "12px 16px",
    cursor: "pointer",
    minWidth: 140,
    textAlign: "left",
    transition: "all 0.3s",
  },
  stockCardActive: {
    border: "1px solid #6366f1",
    background: "linear-gradient(135deg, #1e1b4b, #0f172a)",
    boxShadow: "0 0 20px rgba(99,102,241,0.2)",
  },
  flashUp: { animation: "flashUp 0.4s ease" },
  flashDown: { animation: "flashDown 0.4s ease" },
  flashUpSoft: { animation: "flashUpSoft 0.4s ease" },
  flashDownSoft: { animation: "flashDownSoft 0.4s ease" },
  stockCardTicker: { fontSize: 11, fontWeight: 700, color: "#6366f1", letterSpacing: 0.5 },
  stockCardName: {
    fontSize: 11, color: "#64748b", marginTop: 2, marginBottom: 6,
    whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis", maxWidth: 120,
  },
  stockCardPrice: { fontSize: 15, fontWeight: 700, color: "#f8fafc" },
  stockCardChange: { fontSize: 12, fontWeight: 600, marginTop: 2 },
  mainCard: {
    margin: "0 24px",
    background: "#0f172a",
    border: "1px solid #1e293b",
    borderRadius: 20,
    overflow: "hidden",
  },
  priceHero: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    padding: "20px 24px 16px",
    borderBottom: "1px solid #1e293b",
    background: "linear-gradient(135deg, #0f172a, #131e35)",
  },
  heroName: { fontSize: 20, fontWeight: 700, color: "#f8fafc" },
  heroMeta: { fontSize: 12, color: "#64748b", marginTop: 4 },
  heroPrice: { fontSize: 28, fontWeight: 700, letterSpacing: -1 },
  heroChange: {
    fontSize: 13, fontWeight: 600, padding: "3px 10px",
    borderRadius: 20, marginTop: 4, display: "inline-block",
  },
  metricRow: { display: "flex", overflowX: "auto", borderBottom: "1px solid #1e293b", background: "#080d1a" },
  metricBox: { flexShrink: 0, padding: "12px 16px", borderRight: "1px solid #1e293b", minWidth: 110 },
  metricLabel: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 },
  metricValue: { fontSize: 14, fontWeight: 600, color: "#e2e8f0" },
  tabBar: { display: "flex", borderBottom: "1px solid #1e293b", background: "#080d1a", overflowX: "auto" },
  tabBtn: {
    flex: 1,
    background: "none",
    border: "none",
    color: "#64748b",
    padding: "14px 8px",
    cursor: "pointer",
    fontSize: 12,
    fontWeight: 600,
    borderBottom: "2px solid transparent",
    transition: "all 0.2s",
    fontFamily: "inherit",
    whiteSpace: "nowrap",
    minWidth: 70,
  },
  tabBtnActive: { color: "#6366f1", borderBottom: "2px solid #6366f1", background: "rgba(99,102,241,0.05)" },
  section: { padding: "20px 24px" },
  sectionTitle: {
    fontSize: 14, fontWeight: 700, color: "#94a3b8",
    textTransform: "uppercase", letterSpacing: 1, marginBottom: 16, marginTop: 8,
  },
  grid2: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginBottom: 20 },
  infoCard: { background: "#080d1a", border: "1px solid #1e293b", borderRadius: 10, padding: "12px 14px" },
  infoCardTitle: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 },
  infoCardValue: { fontSize: 15, fontWeight: 700, color: "#f8fafc" },
  rangeBox: { background: "#080d1a", border: "1px solid #1e293b", borderRadius: 12, padding: "16px", marginBottom: 16 },
  rangeLabel: { display: "flex", justifyContent: "space-between", fontSize: 12, marginBottom: 10 },
  rangeTrack: { height: 6, background: "#1e293b", borderRadius: 3, position: "relative" },
  rangeFill: {
    height: "100%",
    background: "linear-gradient(90deg, #6366f1, #a78bfa)",
    borderRadius: 3,
    position: "absolute",
    left: 0,
    top: 0,
  },
  rangeDot: {
    width: 14, height: 14, background: "#fff", borderRadius: "50%",
    position: "absolute", top: -4, transform: "translateX(-50%)",
    border: "2px solid #6366f1", boxShadow: "0 0 8px rgba(99,102,241,0.5)",
  },

  // AI Panel
  aiPanel: {
    background: "linear-gradient(135deg, #0d1526, #111827)",
    border: "1px solid #1e3a5f",
    borderRadius: 14,
    padding: "16px",
    marginTop: 4,
  },
  aiPanelHeader: { display: "flex", alignItems: "center", gap: 8, marginBottom: 12 },
  aiPanelIcon: { fontSize: 16 },
  aiPanelTitle: { fontSize: 13, fontWeight: 700, color: "#93c5fd" },
  aiBadge: {
    fontSize: 10, color: "#6366f1", background: "rgba(99,102,241,0.1)",
    border: "1px solid rgba(99,102,241,0.3)", borderRadius: 20, padding: "2px 8px",
    marginLeft: "auto", fontWeight: 600,
  },
  aiInputRow: { display: "flex", gap: 8, marginBottom: 10 },
  aiInput: {
    flex: 1,
    background: "#080d1a",
    border: "1px solid #1e3a5f",
    borderRadius: 8,
    padding: "9px 12px",
    color: "#f8fafc",
    fontSize: 13,
    fontFamily: "'Space Grotesk', 'Noto Sans Tamil', sans-serif",
    outline: "none",
  },
  aiSendBtn: {
    background: "linear-gradient(135deg, #6366f1, #4f46e5)",
    border: "none",
    borderRadius: 8,
    color: "#fff",
    fontSize: 16,
    fontWeight: 700,
    width: 40,
    cursor: "pointer",
    transition: "all 0.2s",
  },
  quickPrompts: { display: "flex", flexWrap: "wrap", gap: 6, marginBottom: 10 },
  quickPromptBtn: {
    background: "rgba(99,102,241,0.08)",
    border: "1px solid rgba(99,102,241,0.25)",
    borderRadius: 20,
    color: "#93c5fd",
    fontSize: 11,
    padding: "4px 10px",
    cursor: "pointer",
    fontFamily: "inherit",
    transition: "all 0.2s",
  },
  aiLoading: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "12px 0 4px",
  },
  aiLoadingDots: { display: "flex", gap: 4 },
  aiResponse: {
    background: "#080d1a",
    border: "1px solid #1e3a5f",
    borderRadius: 10,
    padding: "12px 14px",
    marginTop: 4,
  },
  aiResponseText: {
    fontSize: 13,
    color: "#cbd5e1",
    lineHeight: 1.7,
    whiteSpace: "pre-wrap",
  },
  aiError: {
    color: "#f87171",
    fontSize: 12,
    padding: "8px 0",
    marginTop: 4,
  },

  // Shareholding
  donutRow: { display: "flex", alignItems: "center", gap: 24, marginBottom: 24 },
  legend: { flex: 1, display: "flex", flexDirection: "column", gap: 10 },
  legendItem: { display: "flex", alignItems: "center", gap: 8 },
  legendDot: { width: 10, height: 10, borderRadius: "50%", flexShrink: 0 },
  legendKey: { fontSize: 13, color: "#94a3b8", flex: 1 },
  legendVal: { fontSize: 13, fontWeight: 700, color: "#f8fafc" },
  trendTable: { background: "#080d1a", border: "1px solid #1e293b", borderRadius: 12, overflow: "hidden" },
  trendHeader: {
    display: "grid", gridTemplateColumns: "120px repeat(4, 1fr)",
    borderBottom: "1px solid #1e293b", padding: "8px 12px",
  },
  trendRow: {
    display: "grid", gridTemplateColumns: "120px repeat(4, 1fr)",
    padding: "8px 12px", borderBottom: "1px solid #0f172a",
  },
  trendCell: { fontSize: 12, color: "#64748b", display: "flex", alignItems: "center" },

  // Corporate
  corpList: { display: "flex", flexDirection: "column", gap: 12 },
  corpCard: {
    background: "#080d1a", border: "1px solid #1e293b", borderRadius: 12,
    padding: "14px 16px", display: "flex", alignItems: "center", gap: 14,
  },
  corpBadge: {
    padding: "8px 12px", borderRadius: 10, display: "flex",
    flexDirection: "column", alignItems: "center", gap: 4, minWidth: 70, textAlign: "center",
  },
  corpDetails: { flex: 1 },

  // Rating
  ratingRow: { display: "flex", alignItems: "center", gap: 12, marginBottom: 10 },
  ratingLabel: { width: 90, fontSize: 12, fontWeight: 600, flexShrink: 0 },
  ratingTrack: { flex: 1, height: 8, background: "#1e293b", borderRadius: 4, overflow: "hidden" },
  ratingFill: { height: "100%", borderRadius: 4, transition: "width 0.6s ease" },
  ratingCount: { width: 24, textAlign: "right", fontSize: 12, color: "#94a3b8", fontWeight: 600 },
  scoreGrid: { display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 12, marginTop: 24 },
  scoreBox: {
    background: "#080d1a", border: "1px solid #1e293b",
    borderRadius: 12, padding: "14px 12px", textAlign: "center",
  },
  scoreLabel: { fontSize: 10, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 10 },
  scorePie: { display: "flex", justifyContent: "center" },
  targetPrice: { fontSize: 22, fontWeight: 700, color: "#f8fafc", marginTop: 8 },

  // Futures Tab
  indexFutGrid: { display: "flex", flexDirection: "column", gap: 10, marginBottom: 8 },
  indexFutCard: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "14px 16px",
    transition: "all 0.3s",
  },
  indexFutName: { fontSize: 13, fontWeight: 700, color: "#6366f1", letterSpacing: 0.5, marginBottom: 6 },
  indexFutSpot: { display: "flex", alignItems: "center", gap: 8 },
  indexFutSpotLabel: {
    fontSize: 9, fontWeight: 700, color: "#64748b",
    background: "#1e293b", padding: "2px 6px", borderRadius: 4, letterSpacing: 0.5,
  },
  indexFutSpotVal: { fontSize: 18, fontWeight: 700, color: "#f8fafc" },
  indexFutNear: { display: "flex", flexDirection: "column", gap: 2 },
  indexFutNearLabel: { fontSize: 9, color: "#64748b", letterSpacing: 0.5 },
  basisTag: {
    fontSize: 11, fontWeight: 700, padding: "3px 8px",
    borderRadius: 6, marginLeft: 4,
  },
  indexFutMeta: { fontSize: 11, color: "#64748b", marginTop: 8 },
  futContractsGrid: { display: "flex", flexDirection: "column", gap: 10, marginBottom: 16 },
  futContractCard: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "14px 16px",
    transition: "all 0.3s",
  },
  futContractLabel: { fontSize: 11, fontWeight: 700, color: "#6366f1", letterSpacing: 0.5, marginBottom: 2 },
  futContractExpiry: { fontSize: 11, color: "#64748b", marginBottom: 6 },
  futContractPrice: { fontSize: 22, fontWeight: 700, marginBottom: 10 },
  futContractRow: { display: "flex", gap: 20 },
  futMetaItem: { display: "flex", flexDirection: "column", gap: 3 },
  futMetaLabel: { fontSize: 9, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5 },
  derivSummary: {
    display: "grid",
    gridTemplateColumns: "repeat(5, 1fr)",
    gap: 8,
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "14px",
    marginBottom: 8,
  },
  derivSummaryItem: { textAlign: "center" },
  derivLabel: { fontSize: 9, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 4 },
  derivVal: { fontSize: 14, fontWeight: 700, color: "#f8fafc" },
  derivHint: { fontSize: 10, color: "#475569", marginTop: 3 },
  optionChainTable: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    overflow: "hidden",
  },
  optionChainHeader: {
    display: "flex",
    alignItems: "center",
    padding: "8px 12px",
    borderBottom: "1px solid #1e293b",
    fontSize: 10,
    fontWeight: 700,
    textTransform: "uppercase",
    letterSpacing: 0.5,
  },
  optionChainCell: { flex: 1 },
  optionChainRow: {
    display: "flex",
    alignItems: "center",
    padding: "10px 12px",
    borderBottom: "1px solid #0f172a",
  },
  optionChainATM: { background: "rgba(99,102,241,0.07)" },
  optionBar: { height: 4, background: "#1e293b", borderRadius: 2, marginTop: 3, overflow: "hidden" },
  optionBarFill: { height: "100%", borderRadius: 2 },
  strikeCell: {
    width: 80,
    textAlign: "center",
    fontSize: 13,
    fontWeight: 700,
    color: "#f8fafc",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 2,
    flexShrink: 0,
  },
  atmBadge: {
    fontSize: 8,
    color: "#6366f1",
    background: "rgba(99,102,241,0.15)",
    border: "1px solid rgba(99,102,241,0.3)",
    borderRadius: 4,
    padding: "1px 5px",
    fontWeight: 700,
    letterSpacing: 0.5,
  },

  // Search
  searchBox: {
    display: "flex", alignItems: "center",
    background: "#080d1a", border: "1px solid #334155",
    borderRadius: 12, padding: "10px 14px", marginBottom: 16, gap: 10,
  },
  searchIcon: { fontSize: 16, flexShrink: 0 },
  searchInput: {
    flex: 1, background: "none", border: "none", outline: "none",
    color: "#f8fafc", fontSize: 14,
    fontFamily: "'Space Grotesk', 'Noto Sans Tamil', sans-serif", fontWeight: 500,
  },
  searchClear: {
    background: "none", border: "none", color: "#64748b",
    cursor: "pointer", fontSize: 13, padding: "0 2px", flexShrink: 0,
  },
  searchResultsList: { display: "flex", flexDirection: "column", gap: 8, marginBottom: 16 },
  searchResultItem: {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    background: "#080d1a", border: "1px solid #1e293b", borderRadius: 12,
    padding: "12px 16px", cursor: "pointer", textAlign: "left", width: "100%", transition: "all 0.2s",
  },
  searchResultItemActive: {
    border: "1px solid #6366f1",
    background: "linear-gradient(135deg, #1e1b4b22, #080d1a)",
    boxShadow: "0 0 12px rgba(99,102,241,0.15)",
  },
  searchResultLeft: { display: "flex", flexDirection: "column", gap: 2 },
  searchResultTicker: { fontSize: 12, fontWeight: 700, color: "#6366f1", letterSpacing: 0.5 },
  searchResultName: { fontSize: 14, fontWeight: 600, color: "#f8fafc" },
  searchResultMeta: { fontSize: 11, color: "#64748b" },
  searchResultRight: { textAlign: "right", display: "flex", flexDirection: "column", gap: 2 },
  searchResultPrice: { fontSize: 15, fontWeight: 700, color: "#f8fafc" },
  searchResultChg: { fontSize: 12, fontWeight: 600 },
  searchResultCap: { fontSize: 11, color: "#64748b" },
  noResults: { textAlign: "center", padding: "32px 0" },
  searchDetailCard: {
    background: "#080d1a", border: "1px solid #1e293b",
    borderRadius: 16, padding: "18px 16px", marginTop: 4,
  },
  searchDetailHeader: {
    display: "flex", justifyContent: "space-between", alignItems: "flex-start",
    marginBottom: 16, paddingBottom: 16, borderBottom: "1px solid #1e293b",
  },
  searchDetailName: { fontSize: 16, fontWeight: 700, color: "#f8fafc" },
  searchDetailMeta: { fontSize: 11, color: "#64748b", marginTop: 4 },
  searchDetailPrice: { fontSize: 22, fontWeight: 700, letterSpacing: -0.5 },
  searchDetailChgBadge: {
    fontSize: 12, fontWeight: 600, padding: "3px 10px",
    borderRadius: 20, marginTop: 4, display: "inline-block",
  },
  searchDetailGrid: { display: "grid", gridTemplateColumns: "1fr 1fr", gap: 8, marginBottom: 16 },
  searchDetailMetric: {
    background: "#0f172a", border: "1px solid #1e293b", borderRadius: 8, padding: "8px 10px",
  },
  searchDetailMetricLabel: { fontSize: 9, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5, marginBottom: 3 },
  searchDetailMetricValue: { fontSize: 13, fontWeight: 600, color: "#e2e8f0" },
  searchScoreRow: {
    display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 10,
    paddingTop: 14, borderTop: "1px solid #1e293b",
  },
  searchScoreItem: { display: "flex", flexDirection: "column", gap: 4 },
  searchScoreLabel: { fontSize: 9, color: "#64748b", textTransform: "uppercase", letterSpacing: 0.5 },
  searchScoreBar: { height: 6, background: "#1e293b", borderRadius: 3, overflow: "hidden", marginTop: 4 },
  searchScoreFill: { height: "100%", borderRadius: 3, transition: "width 0.5s ease" },
  searchScoreVal: { fontSize: 13, fontWeight: 700, color: "#f8fafc" },
  searchEmpty: { textAlign: "center", padding: "40px 0 20px" },
};
