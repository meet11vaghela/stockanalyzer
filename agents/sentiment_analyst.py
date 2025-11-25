from textblob import TextBlob
from agents.base_agent import BaseAgent

class SentimentAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="SentimentAnalyst",
            role="Market Sentiment Expert",
            goal="Analyze news and social media sentiment.",
            backstory="Behavioral finance specialist tracking market psychology."
        )

    def analyze(self, ticker: str) -> dict:
        self.log(f"Starting sentiment analysis for {ticker}...")
        
        data_key = f"data_{ticker}"
        raw_data = self.read_from_memory(data_key)
        if not raw_data:
            return {"error": f"No data found for {ticker}"}

        news_items = raw_data.get("news", [])
        
        if not news_items:
            return {"score": 50, "confidence": 0, "summary": "No news found"}

        total_polarity = 0
        count = 0
        headlines = []

        for item in news_items:
            title = item.get("title", "")
            if title:
                blob = TextBlob(title)
                polarity = blob.sentiment.polarity
                total_polarity += polarity
                count += 1
                headlines.append({"title": title, "polarity": polarity})

        avg_polarity = total_polarity / count if count > 0 else 0
        
        # Normalize polarity (-1 to 1) to score (0 to 100)
        # -1 -> 0, 0 -> 50, 1 -> 100
        sentiment_score = (avg_polarity + 1) * 50
        
        confidence = min(1.0, count * 0.1) # Simple confidence based on volume of news

        result = {
            "sentiment_score": sentiment_score,
            "confidence": confidence,
            "article_count": count,
            "top_headlines": headlines[:3]
        }

        self.save_to_memory(f"sentiment_{ticker}", result)
        self.log(f"Sentiment analysis completed for {ticker}")
        return result

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if ticker:
            self.analyze(ticker)
            return f"Sentiment analysis done for {ticker}"
        return "No ticker provided"
