import json
from agents.base_agent import BaseAgent
from datetime import datetime

class ReportGeneratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="ReportGenerator",
            role="Investment Strategist",
            goal="Synthesize all analysis into a comprehensive actionable report.",
            backstory="Senior portfolio manager known for clear, data-driven insights."
        )

    def generate_report(self, ticker: str) -> dict:
        self.log(f"Generating report for {ticker}...")
        
        # Gather all data
        technical = self.read_from_memory(f"technical_{ticker}")
        fundamental = self.read_from_memory(f"fundamental_{ticker}")
        sentiment = self.read_from_memory(f"sentiment_{ticker}")
        risk = self.read_from_memory(f"risk_{ticker}")
        
        if not all([technical, fundamental, sentiment, risk]):
            return {"error": "Incomplete analysis data"}

        # Calculate Overall Score (Weighted)
        # Weights: Tech 30%, Fund 40%, Sent 15%, Risk 15% (Risk is negative factor usually, but here we treat score as quality)
        # For risk, let's invert: Low risk = high score.
        risk_score = 100
        if risk['risk_level'] == "Medium": risk_score = 60
        if risk['risk_level'] == "High": risk_score = 30
        
        overall_score = (
            technical['score'] * 0.30 +
            fundamental['score'] * 0.40 +
            sentiment['sentiment_score'] * 0.15 +
            risk_score * 0.15
        )
        
        recommendation = "HOLD"
        if overall_score > 70: recommendation = "BUY"
        if overall_score > 85: recommendation = "STRONG BUY"
        if overall_score < 40: recommendation = "SELL"
        if overall_score < 25: recommendation = "STRONG SELL"

        report = {
            "ticker": ticker,
            "timestamp": datetime.now().isoformat(),
            "overall_rating": recommendation,
            "overall_score": round(overall_score, 2),
            "technical_analysis": technical,
            "fundamental_analysis": fundamental,
            "sentiment_analysis": sentiment,
            "risk_assessment": risk,
            "summary": self._create_summary(ticker, recommendation, overall_score, technical, fundamental, sentiment, risk)
        }
        
        self.save_to_memory(f"report_{ticker}", report)
        self.log(f"Report generated for {ticker}")
        return report

    def _create_summary(self, ticker, recommendation, score, tech, fund, sent, risk):
        return (
            f"Investment Report for {ticker}:\n"
            f"Recommendation: {recommendation} (Score: {score:.2f}/100)\n"
            f"Risk Level: {risk['risk_level']}\n"
            f"Technical Outlook: RSI at {tech['rsi']:.2f}, {tech['signals'][0] if tech['signals'] else ''}\n"
            f"Fundamental: P/E {fund['pe_ratio']}, {fund['findings'][0] if fund['findings'] else ''}\n"
            f"Sentiment: Score {sent['sentiment_score']:.2f} based on {sent['article_count']} articles."
        )

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if ticker:
            report = self.generate_report(ticker)
            return json.dumps(report, indent=2)
        return "No ticker provided"
