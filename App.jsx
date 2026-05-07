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

export default function StockApp() {
  const [lang, setLang] = useState("en");
  const [activeTab, setActiveTab] = useState("overview");
  const [selectedStock, setSelectedStock] = useState(stocks[0]);
  const [prices, setPrices] = useState(() =>
    stocks.reduce((acc, s) => ({ ...acc, [s.ticker]: s.price }), {})
  );
  const [flashTicker, setFlashTicker] = useState({});
  const t = translations[lang];
  const tickerRef = useRef(null);

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
    }, 1800);
    return () => clearInterval(interval);
  }, []);

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

  const tabs = ["overview", "shareholding", "corporate", "rating"];

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
                  style={{
                    ...styles.tickerItem,
                    color: isUp ? "#34d399" : "#f87171",
                  }}
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
              style={{
                ...styles.langBtn,
                ...(lang === l ? styles.langBtnActive : {}),
              }}
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
              onClick={() => setSelectedStock(s)}
              style={{
                ...styles.stockCard,
                ...(selectedStock.ticker === s.ticker
                  ? styles.stockCardActive
                  : {}),
                ...(flash === "up"
                  ? styles.flashUp
                  : flash === "down"
                  ? styles.flashDown
                  : {}),
              }}
            >
              <div style={styles.stockCardTicker}>{s.ticker}</div>
              <div style={styles.stockCardName}>{s.name}</div>
              <div style={styles.stockCardPrice}>₹{lp.toFixed(2)}</div>
              <div
                style={{
                  ...styles.stockCardChange,
                  color: pos ? "#34d399" : "#f87171",
                }}
              >
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
              {selectedStock.ticker} &nbsp;•&nbsp; {selectedStock.sector}{" "}
              &nbsp;•&nbsp; {selectedStock.industry}
            </div>
          </div>
          <div style={{ textAlign: "right" }}>
            <div
              style={{
                ...styles.heroPrice,
                color: isPositive ? "#34d399" : "#f87171",
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
              style={{
                ...styles.tabBtn,
                ...(activeTab === tab ? styles.tabBtnActive : {}),
              }}
            >
              {t[tab]}
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

            {/* 52 Week Range Bar */}
            <div style={styles.rangeBox}>
              <div style={styles.rangeLabel}>
                <span style={{ color: "#94a3b8" }}>{t.low52}: ₹{selectedStock.low52}</span>
                <span style={{ color: "#f8fafc", fontWeight: 600 }}>52W Range</span>
                <span style={{ color: "#94a3b8" }}>{t.high52}: ₹{selectedStock.high52}</span>
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
          </div>
        )}

        {/* TAB: Shareholding */}
        {activeTab === "shareholding" && (
          <div style={styles.section}>
            <div style={styles.sectionTitle}>{t.shareholdingPattern}</div>

            {/* Donut + Legend */}
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

            {/* Quarterly Trend */}
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
                          <span style={{ fontSize: 9, color: delta > 0 ? "#34d399" : delta < 0 ? "#f87171" : "#64748b", marginLeft: 3 }}>
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
                  <div style={{ ...styles.corpBadge, background: corporateTypeColors[action.type] + "22", border: `1px solid ${corporateTypeColors[action.type]}44` }}>
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

            {/* Rating Bars */}
            {Object.entries(ratingData).map(([key, count]) => {
              const pct = ((count / totalRatings) * 100).toFixed(0);
              return (
                <div key={key} style={styles.ratingRow}>
                  <div style={{ ...styles.ratingLabel, color: ratingColors[key] }}>{t[key]}</div>
                  <div style={styles.ratingTrack}>
                    <div
                      style={{
                        ...styles.ratingFill,
                        width: `${pct}%`,
                        background: ratingColors[key],
                      }}
                    />
                  </div>
                  <div style={styles.ratingCount}>{count}</div>
                </div>
              );
            })}

            {/* Scores */}
            <div style={styles.scoreGrid}>
              <div style={styles.scoreBox}>
                <div style={styles.scoreLabel}>{t.technicalScore}</div>
                <div style={styles.scorePie}>
                  <svg width="80" height="80">
                    <circle cx="40" cy="40" r="32" fill="none" stroke="#1e293b" strokeWidth="8" />
                    <circle
                      cx="40" cy="40" r="32" fill="none"
                      stroke="#6366f1" strokeWidth="8"
                      strokeDasharray={`${(selectedStock.technicalScore / 100) * 201} 201`}
                      strokeDashoffset="50"
                      strokeLinecap="round"
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
                      cx="40" cy="40" r="32" fill="none"
                      stroke="#10b981" strokeWidth="8"
                      strokeDasharray={`${(selectedStock.fundamentalScore / 100) * 201} 201`}
                      strokeDashoffset="50"
                      strokeLinecap="round"
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
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0a0f1e; }
        ::-webkit-scrollbar { width: 4px; height: 4px; }
        ::-webkit-scrollbar-track { background: #0f172a; }
        ::-webkit-scrollbar-thumb { background: #334155; border-radius: 2px; }
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
  tickerInner: {
    flex: 1,
    overflow: "hidden",
    position: "relative",
  },
  tickerTrack: {
    display: "inline-flex",
    whiteSpace: "nowrap",
    animation: "ticker 35s linear infinite",
    paddingLeft: 16,
  },
  tickerItem: {
    fontSize: 12,
    fontWeight: 600,
    letterSpacing: 0.5,
  },
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
  logoSub: {
    fontSize: 11,
    color: "#64748b",
    marginTop: 2,
    letterSpacing: 1,
    textTransform: "uppercase",
  },
  langSwitch: {
    display: "flex",
    alignItems: "center",
    gap: 8,
  },
  langLabel: {
    fontSize: 12,
    color: "#64748b",
  },
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
  langBtnActive: {
    background: "#6366f1",
    border: "1px solid #6366f1",
    color: "#fff",
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
  stockCardTicker: {
    fontSize: 11,
    fontWeight: 700,
    color: "#6366f1",
    letterSpacing: 0.5,
  },
  stockCardName: {
    fontSize: 11,
    color: "#64748b",
    marginTop: 2,
    marginBottom: 6,
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    maxWidth: 120,
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
    padding: "20px 24px 16px",
    borderBottom: "1px solid #1e293b",
    background: "linear-gradient(135deg, #0f172a, #131e35)",
  },
  heroName: {
    fontSize: 20,
    fontWeight: 700,
    color: "#f8fafc",
  },
  heroMeta: {
    fontSize: 12,
    color: "#64748b",
    marginTop: 4,
  },
  heroPrice: {
    fontSize: 28,
    fontWeight: 700,
    letterSpacing: -1,
  },
  heroChange: {
    fontSize: 13,
    fontWeight: 600,
    padding: "3px 10px",
    borderRadius: 20,
    marginTop: 4,
    display: "inline-block",
  },
  metricRow: {
    display: "flex",
    overflowX: "auto",
    borderBottom: "1px solid #1e293b",
    background: "#080d1a",
  },
  metricBox: {
    flexShrink: 0,
    padding: "12px 16px",
    borderRight: "1px solid #1e293b",
    minWidth: 110,
  },
  metricLabel: {
    fontSize: 10,
    color: "#64748b",
    textTransform: "uppercase",
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  metricValue: {
    fontSize: 14,
    fontWeight: 600,
    color: "#e2e8f0",
  },
  tabBar: {
    display: "flex",
    borderBottom: "1px solid #1e293b",
    background: "#080d1a",
  },
  tabBtn: {
    flex: 1,
    background: "none",
    border: "none",
    color: "#64748b",
    padding: "14px 8px",
    cursor: "pointer",
    fontSize: 13,
    fontWeight: 600,
    borderBottom: "2px solid transparent",
    transition: "all 0.2s",
    fontFamily: "inherit",
  },
  tabBtnActive: {
    color: "#6366f1",
    borderBottom: "2px solid #6366f1",
    background: "rgba(99,102,241,0.05)",
  },
  section: {
    padding: "20px 24px",
  },
  sectionTitle: {
    fontSize: 14,
    fontWeight: 700,
    color: "#94a3b8",
    textTransform: "uppercase",
    letterSpacing: 1,
    marginBottom: 16,
    marginTop: 8,
  },
  grid2: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: 12,
    marginBottom: 20,
  },
  infoCard: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 10,
    padding: "12px 14px",
  },
  infoCardTitle: {
    fontSize: 10,
    color: "#64748b",
    textTransform: "uppercase",
    letterSpacing: 0.5,
    marginBottom: 4,
  },
  infoCardValue: {
    fontSize: 15,
    fontWeight: 700,
    color: "#f8fafc",
  },
  rangeBox: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "16px",
  },
  rangeLabel: {
    display: "flex",
    justifyContent: "space-between",
    fontSize: 12,
    marginBottom: 10,
  },
  rangeTrack: {
    height: 6,
    background: "#1e293b",
    borderRadius: 3,
    position: "relative",
  },
  rangeFill: {
    height: "100%",
    background: "linear-gradient(90deg, #6366f1, #a78bfa)",
    borderRadius: 3,
    position: "absolute",
    left: 0,
    top: 0,
  },
  rangeDot: {
    width: 14,
    height: 14,
    background: "#fff",
    borderRadius: "50%",
    position: "absolute",
    top: -4,
    transform: "translateX(-50%)",
    border: "2px solid #6366f1",
    boxShadow: "0 0 8px rgba(99,102,241,0.5)",
  },
  donutRow: {
    display: "flex",
    alignItems: "center",
    gap: 24,
    marginBottom: 24,
  },
  legend: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  legendItem: {
    display: "flex",
    alignItems: "center",
    gap: 8,
  },
  legendDot: {
    width: 10,
    height: 10,
    borderRadius: "50%",
    flexShrink: 0,
  },
  legendKey: {
    fontSize: 13,
    color: "#94a3b8",
    flex: 1,
  },
  legendVal: {
    fontSize: 13,
    fontWeight: 700,
    color: "#f8fafc",
  },
  trendTable: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    overflow: "hidden",
  },
  trendHeader: {
    display: "grid",
    gridTemplateColumns: "120px repeat(4, 1fr)",
    borderBottom: "1px solid #1e293b",
    padding: "8px 12px",
  },
  trendRow: {
    display: "grid",
    gridTemplateColumns: "120px repeat(4, 1fr)",
    padding: "8px 12px",
    borderBottom: "1px solid #0f172a",
  },
  trendCell: {
    fontSize: 12,
    color: "#64748b",
    display: "flex",
    alignItems: "center",
  },
  corpList: {
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  corpCard: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "14px 16px",
    display: "flex",
    alignItems: "center",
    gap: 14,
  },
  corpBadge: {
    padding: "8px 12px",
    borderRadius: 10,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    gap: 4,
    minWidth: 70,
    textAlign: "center",
  },
  corpDetails: {
    flex: 1,
  },
  ratingRow: {
    display: "flex",
    alignItems: "center",
    gap: 12,
    marginBottom: 10,
  },
  ratingLabel: {
    width: 90,
    fontSize: 12,
    fontWeight: 600,
    flexShrink: 0,
  },
  ratingTrack: {
    flex: 1,
    height: 8,
    background: "#1e293b",
    borderRadius: 4,
    overflow: "hidden",
  },
  ratingFill: {
    height: "100%",
    borderRadius: 4,
    transition: "width 0.6s ease",
  },
  ratingCount: {
    width: 24,
    textAlign: "right",
    fontSize: 12,
    color: "#94a3b8",
    fontWeight: 600,
  },
  scoreGrid: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr 1fr",
    gap: 12,
    marginTop: 24,
  },
  scoreBox: {
    background: "#080d1a",
    border: "1px solid #1e293b",
    borderRadius: 12,
    padding: "14px 12px",
    textAlign: "center",
  },
  scoreLabel: {
    fontSize: 10,
    color: "#64748b",
    textTransform: "uppercase",
    letterSpacing: 0.5,
    marginBottom: 10,
  },
  scorePie: {
    display: "flex",
    justifyContent: "center",
  },
  targetPrice: {
    fontSize: 22,
    fontWeight: 700,
    color: "#f8fafc",
    marginTop: 8,
  },
};
export default StockApp; // 
