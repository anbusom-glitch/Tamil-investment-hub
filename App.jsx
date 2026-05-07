import React, { useState, useEffect } from "react";

const translations = {
  ta: {
    title: "ஸ்டாக்பல்ஸ் ப்ரோ",
    subtitle: "நேரடி சந்தை தகவல்",
    livePrice: "நேரடி விலை",
    marketCap: "சந்தை மூலதனம்",
    pe: "P/E விகிதம்",
    scrollingNews: "நேரடி சந்தை",
    language: "Language",
  },
  en: {
    title: "StockPulse Pro",
    subtitle: "Live Market Intelligence",
    livePrice: "Live Price",
    marketCap: "Market Cap",
    pe: "P/E Ratio",
    scrollingNews: "LIVE MARKET",
    language: "Language",
  }
};

const stocks = [
  { name: "Reliance Industries", ticker: "RELIANCE", price: 2847.35, marketCap: "₹19.27L Cr", pe: 28.4 },
  { name: "Infosys Ltd", ticker: "INFY", price: 1892.6, marketCap: "₹7.89L Cr", pe: 24.1 },
  { name: "HDFC Bank", ticker: "HDFCBANK", price: 1654.9, marketCap: "#12.56L Cr", pe: 18.7 }
];

export default function App() {
  const [lang, setLang] = useState("ta");
  const [prices, setPrices] = useState(stocks.reduce((acc, s) => ({ ...acc, [s.ticker]: s.price }), {}));
  const t = translations[lang];

  useEffect(() => {
    const interval = setInterval(() => {
      setPrices(prev => {
        const next = { ...prev };
        stocks.forEach(s => {
          next[s.ticker] = prev[s.ticker] + (Math.random() - 0.5) * 5;
        });
        return next;
      });
    }, 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ background: "#0a0f1e", color: "white", minHeight: "100vh", padding: "20px", fontFamily: "sans-serif" }}>
      <header style={{ borderBottom: "1px solid #1e293b", paddingBottom: "10px", marginBottom: "20px" }}>
        <h1 style={{ color: "#6366f1", margin: 0 }}>{t.title}</h1>
        <p style={{ color: "#64748b", margin: 0 }}>{t.subtitle}</p>
        <button onClick={() => setLang(lang === "ta" ? "en" : "ta")} style={{ marginTop: "10px", padding: "5px 15px", borderRadius: "15px", border: "1px solid #6366f1", background: "none", color: "white", cursor: "pointer" }}>
          {lang === "ta" ? "English" : "தமிழ்"}
        </button>
      </header>

      <div style={{ display: "grid", gap: "15px" }}>
        {stocks.map(s => (
          <div key={s.ticker} style={{ background: "#0f172a", padding: "15px", borderRadius: "12px", border: "1px solid #1e293b" }}>
            <div style={{ display: "flex", justifyContent: "space-between" }}>
              <span style={{ fontWeight: "bold", color: "#6366f1" }}>{s.ticker}</span>
              <span style={{ fontSize: "1.2rem", fontWeight: "bold" }}>₹{prices[s.ticker].toFixed(2)}</span>
            </div>
            <div style={{ color: "#94a3b8", fontSize: "0.9rem", marginTop: "5px" }}>{s.name}</div>
            <div style={{ display: "flex", gap: "20px", marginTop: "10px", fontSize: "0.8rem", color: "#64748b" }}>
              <span>{t.marketCap}: {s.marketCap}</span>
              <span>{t.pe}: {s.pe}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
