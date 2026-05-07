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
  },
  ta: {
    title: "ஸ்டாக்பல்ஸ் ப்ரோ",
    subtitle: "நேரடி சந்தை தகவல்",
    search: "பங்குகளை தேடுங்கள்...",
    overview: "மேலோட்டம்",
    shareholding: "பங்குடைமை",
    corporate: "நிறுவன செயல்கள்",
    rating: "மதிப்பீடு",
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
    shareholding: {
      promoter: [0, 0, 0, 0],
      fii: [53.2, 53.5, 54.1, 54.8],
      dii: [30.1, 29.8, 29.5, 29.2],
      public: [13.5, 13.5, 13.2, 12.8],
      others: [3.2, 3.2, 3.2, 3.2],
    },
    corporate: [
      { type: "dividend", date: "2025-04-20", details: "₹19.5 per share" },
    ],
    rating: { strongBuy: 22, buy: 10, hold: 4, sell: 1, strongSell: 0 },
    targetPrice: 1950,
    technicalScore: 68,
    fundamentalScore: 90,
  },
];

const tickerItems = [
  "RELIANCE ▲ 2847.35 (+1.24%)",
  "INFY ▼ 1892.60 (-0.87%)",
  "HDFCBANK ▲ 1654.90 (+0.45%)",
  "NIFTY ▲ 22,643 (+0.48%)",
  "SENSEX ▲ 74,892 (+0.56%)",
];

export default function StockApp() {

  const [lang, setLang] = useState("en");
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedStock, setSelectedStock] = useState(stocks[0]);
  const [search, setSearch] = useState("");

  const [prices, setPrices] = useState(() =>
    stocks.reduce((acc, s) => ({ ...acc, [s.ticker]: s.price }), {})
  );

  const t = translations[lang];

  useEffect(() => {
    const interval = setInterval(() => {
      setPrices((prev) => {
        const next = { ...prev };

        stocks.forEach((s) => {
          const delta = (Math.random() - 0.5) * 4;
          next[s.ticker] = Math.max(1, prev[s.ticker] + delta);
        });

        return next;
      });
    }, 1800);

    return () => clearInterval(interval);
  }, []);

  const filteredStocks = stocks.filter(
    (s) =>
      s.name.toLowerCase().includes(search.toLowerCase()) ||
      s.ticker.toLowerCase().includes(search.toLowerCase())
  );

  const livePrice = prices[selectedStock.ticker];

  const liveChange = (
    ((livePrice - selectedStock.prevClose) /
      selectedStock.prevClose) *
    100
  ).toFixed(2);

  const isPositive = parseFloat(liveChange) >= 0;

  return (
    <div style={styles.app}>

      {/* TOP TICKER */}

      <div style={styles.tickerWrap}>

        <div style={styles.tickerLabel}>
          {t.scrollingNews}
        </div>

        <div style={styles.tickerInner}>
          <div style={styles.tickerTrack}>
            {[...tickerItems, ...tickerItems].map((item, i) => (
              <span
                key={i}
                style={{
                  ...styles.tickerItem,
                  color: item.includes("▲")
                    ? "#34d399"
                    : "#f87171",
                }}
              >
                {item}
                &nbsp;&nbsp;&nbsp;•&nbsp;&nbsp;&nbsp;
              </span>
            ))}
          </div>
        </div>

      </div>

      {/* HEADER */}

      <div style={styles.header}>

        <div>
          <div style={styles.logo}>
            {t.title}
          </div>

          <div style={styles.logoSub}>
            {t.subtitle}
          </div>
        </div>

        <div style={styles.langSwitch}>

          <button
            onClick={() => setLang("en")}
            style={{
              ...styles.langBtn,
              ...(lang === "en"
                ? styles.langBtnActive
                : {}),
            }}
          >
            English
          </button>

          <button
            onClick={() => setLang("ta")}
            style={{
              ...styles.langBtn,
              ...(lang === "ta"
                ? styles.langBtnActive
                : {}),
            }}
          >
            தமிழ்
          </button>

        </div>

      </div>

      {/* SEARCH */}

      <div style={styles.searchWrap}>

        <input
          type="text"
          placeholder={t.search}
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          style={styles.searchInput}
        />

      </div>

      {/* STOCK LIST */}

      <div style={styles.stockSelector}>

        {filteredStocks.map((s) => {

          const lp = prices[s.ticker];

          const chg = (
            ((lp - s.prevClose) / s.prevClose) *
            100
          ).toFixed(2);

          const pos = parseFloat(chg) >= 0;

          return (
            <button
              key={s.ticker}
              onClick={() => setSelectedStock(s)}
              style={{
                ...styles.stockCard,
                ...(selectedStock.ticker === s.ticker
                  ? styles.stockCardActive
                  : {}),
              }}
            >

              <div style={styles.stockCardTicker}>
                {s.ticker}
              </div>

              <div style={styles.stockCardName}>
                {s.name}
              </div>

              <div style={styles.stockCardPrice}>
                ₹{lp.toFixed(2)}
              </div>

              <div
                style={{
                  ...styles.stockCardChange,
                  color: pos
                    ? "#34d399"
                    : "#f87171",
                }}
              >
                {pos ? "▲" : "▼"} {Math.abs(chg)}%
              </div>

            </button>
          );
        })}

      </div>

      {/* MAIN CARD */}

      <div style={styles.mainCard}>

        {/* HERO */}

        <div style={styles.priceHero}>

          <div>

            <div style={styles.heroName}>
              {selectedStock.name}
            </div>

            <div style={styles.heroMeta}>
              {selectedStock.ticker}
              &nbsp;•&nbsp;
              {selectedStock.sector}
            </div>

          </div>

          <div style={{ textAlign: "right" }}>

            <div
              style={{
                ...styles.heroPrice,
                color: isPositive
                  ? "#34d399"
                  : "#f87171",
              }}
            >
              ₹{livePrice.toFixed(2)}
            </div>

            <div
              style={{
                ...styles.heroChange,
                background: isPositive
                  ? "rgba(52,211,153,0.15)"
                  : "rgba(248,113,113,0.15)",
                color: isPositive
                  ? "#34d399"
                  : "#f87171",
              }}
            >
              {isPositive ? "▲" : "▼"}
              {" "}
              {Math.abs(liveChange)}%
            </div>

          </div>

        </div>

        {/* METRICS */}

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

              <div style={styles.metricLabel}>
                {m.label}
              </div>

              <div style={styles.metricValue}>
                {m.value}
              </div>

            </div>

          ))}

        </div>

      </div>

      <style>{`

        @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Noto+Sans+Tamil:wght@400;600;700&display=swap');

        @keyframes ticker {
          0% {
            transform: translateX(0);
          }

          100% {
            transform: translateX(-50%);
          }
        }

        *{
          box-sizing:border-box;
          margin:0;
          padding:0;
        }

        body{
          background:#0a0f1e;
        }

        ::-webkit-scrollbar{
          width:4px;
          height:4px;
        }

        ::-webkit-scrollbar-thumb{
          background:#334155;
          border-radius:4px;
        }

        @media(max-width:768px){

          .mobile-grid{
            grid-template-columns:1fr !important;
          }

        }

      `}</style>

    </div>
  );
}

const styles = {

  app: {
    background:
      "linear-gradient(135deg,#0a0f1e 0%,#0d1829 50%,#0a0f1e 100%)",
    minHeight: "100vh",
    fontFamily:
      "'Space Grotesk','Noto Sans Tamil',sans-serif",
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

  tickerInner: {
    flex: 1,
    overflow: "hidden",
  },

  tickerTrack: {
    display: "inline-flex",
    whiteSpace: "nowrap",
    animation: "ticker 30s linear infinite",
    paddingLeft: 16,
  },

  tickerItem: {
    fontSize: 12,
    fontWeight: 600,
  },

  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "20px 24px",
    borderBottom: "1px solid #1e293b",
  },

  logo: {
    fontSize: 24,
    fontWeight: 700,
    background:
      "linear-gradient(90deg,#6366f1,#a78bfa)",
    WebkitBackgroundClip: "text",
    WebkitTextFillColor: "transparent",
  },

  logoSub: {
    fontSize: 11,
    color: "#64748b",
    marginTop: 2,
    letterSpacing: 1,
  },

  langSwitch: {
    display: "flex",
    gap: 8,
  },

  langBtn: {
    background: "#1e293b",
    border: "1px solid #334155",
    color: "#94a3b8",
    padding: "6px 12px",
    borderRadius: 20,
    cursor: "pointer",
    fontSize: 12,
    fontWeight: 600,
  },

  langBtnActive: {
    background: "#6366f1",
    color: "#fff",
    border: "1px solid #6366f1",
  },

  searchWrap: {
    padding: "16px 24px 0",
  },

  searchInput: {
    width: "100%",
    background: "#0f172a",
    border: "1px solid #1e293b",
    color: "#f8fafc",
    padding: "14px 16px",
    borderRadius: 12,
    fontSize: 14,
    outline: "none",
  },

  stockSelector: {
    display: "flex",
    gap: 12,
    padding: "16px 24px",
    overflowX: "auto",
  },

  stockCard: {
    background: "#0f172a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "12px 16px",
    cursor: "pointer",
    minWidth: 150,
    textAlign: "left",
    transition: "all .3s",
  },

  stockCardActive: {
    border: "1px solid #6366f1",
    background:
      "linear-gradient(135deg,#1e1b4b,#0f172a)",
    boxShadow:
      "0 0 20px rgba(99,102,241,0.2)",
  },

  stockCardTicker: {
    fontSize: 11,
    fontWeight: 700,
    color: "#6366f1",
  },

  stockCardName: {
    fontSize: 11,
    color: "#64748b",
    marginTop: 2,
    marginBottom: 6,
  },

  stockCardPrice: {
    fontSize: 15,
    fontWeight: 700,
    color: "#f8fafc",
  },

  stockCardChange: {
    fontSize: 12,
    fontWeight: 600,
    marginTop: 2,
  },

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
    padding: "20px 24px",
    borderBottom: "1px solid #1e293b",
    background:
      "linear-gradient(135deg,#0f172a,#131e35)",
  },

  heroName: {
    fontSize: 22,
    fontWeight: 700,
  },

  heroMeta: {
    fontSize: 12,
    color: "#64748b",
    marginTop: 4,
  },

  heroPrice: {
    fontSize: 30,
    fontWeight: 700,
  },

  heroChange: {
    fontSize: 13,
    fontWeight: 600,
    padding: "4px 10px",
    borderRadius: 20,
    marginTop: 4,
    display: "inline-block",
  },

  metricRow: {
    display: "flex",
    overflowX: "auto",
    background: "#080d1a",
  },

  metricBox: {
    minWidth: 120,
    padding: "12px 16px",
    borderRight: "1px solid #1e293b",
  },

  metricLabel: {
    fontSize: 10,
    color: "#64748b",
    marginBottom: 4,
    textTransform: "uppercase",
  },

  metricValue: {
    fontSize: 14,
    fontWeight: 600,
    color: "#e2e8f0",
  },

};
