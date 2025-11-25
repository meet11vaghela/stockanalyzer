from agents.base_agent import BaseAgent

class FundamentalAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="FundamentalAnalyst",
            role="Fundamental Analysis Expert",
            goal="Evaluate company financial health and valuation.",
            backstory="Value investor focused on long-term growth and stability."
        )

    def analyze(self, ticker: str) -> dict:
        self.log(f"Starting fundamental analysis for {ticker}...")
        
        data_key = f"data_{ticker}"
        raw_data = self.read_from_memory(data_key)
        if not raw_data:
            return {"error": f"No data found for {ticker}"}

        fundamentals = raw_data.get("fundamentals", {})
        
        pe_ratio = fundamentals.get("trailingPE")
        forward_pe = fundamentals.get("forwardPE")
        market_cap = fundamentals.get("marketCap")
        dividend_yield = fundamentals.get("dividendYield")
        
        # Scoring Logic
        score = 50
        findings = []

        # P/E Analysis
        if pe_ratio:
            if pe_ratio < 15:
                score += 15
                findings.append("Undervalued P/E ratio (< 15)")
            elif pe_ratio > 30:
                score -= 10
                findings.append("High P/E ratio (> 30)")
            else:
                score += 5
                findings.append("Moderate P/E ratio")
        
        # Growth Potential
        if pe_ratio and forward_pe and forward_pe < pe_ratio:
            score += 10
            findings.append("Forward P/E lower than Trailing P/E (Expected Growth)")

        # Dividend
        if dividend_yield and dividend_yield > 0.02:
            score += 10
            findings.append(f"Good Dividend Yield ({dividend_yield*100:.2f}%)")

        # Market Cap
        if market_cap and market_cap > 10_000_000_000: # Large Cap
            score += 5
            findings.append("Large Cap Company (Stability)")

        score = max(0, min(100, score))
        
        result = {
            "pe_ratio": pe_ratio,
            "market_cap": market_cap,
            "dividend_yield": dividend_yield,
            "score": score,
            "findings": findings
        }

        self.save_to_memory(f"fundamental_{ticker}", result)
        self.log(f"Fundamental analysis completed for {ticker}")
        return result

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if ticker:
            self.analyze(ticker)
            return f"Fundamental analysis done for {ticker}"
        return "No ticker provided"
