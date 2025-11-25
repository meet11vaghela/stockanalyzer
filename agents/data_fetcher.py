import yfinance as yf
import pandas as pd
from agents.base_agent import BaseAgent
from core.adk_core import Task

class DataFetcherAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DataFetcher",
            role="Data Acquisition Specialist",
            goal="Fetch comprehensive stock data including real-time price, history, and fundamentals.",
            backstory="Expert in financial data retrieval with robust error handling."
        )

    def fetch_stock_data(self, ticker: str) -> dict:
        """Fetches all necessary data for a given ticker."""
        self.log(f"Fetching data for {ticker}...")
        try:
            stock = yf.Ticker(ticker)
            
            # 1. Historical Data (1 year daily, 3 months hourly)
            history_daily = stock.history(period="1y", interval="1d")
            history_hourly = stock.history(period="3mo", interval="1h")
            
            # 2. Fundamentals
            info = stock.info
            fundamentals = {
                "marketCap": info.get("marketCap"),
                "trailingPE": info.get("trailingPE"),
                "forwardPE": info.get("forwardPE"),
                "dividendYield": info.get("dividendYield"),
                "sector": info.get("sector"),
                "industry": info.get("industry"),
                "currentPrice": info.get("currentPrice")
            }

            # 3. News (for sentiment analysis)
            news = stock.news

            data = {
                "ticker": ticker,
                "history_daily": history_daily.to_json(date_format='iso'),
                "history_hourly": history_hourly.to_json(date_format='iso'),
                "fundamentals": fundamentals,
                "news": news
            }
            
            # Save to shared memory
            self.save_to_memory(f"data_{ticker}", data)
            self.log(f"Data fetched and saved for {ticker}")
            return data

        except Exception as e:
            self.log(f"Error fetching data for {ticker}: {e}")
            return {"error": str(e)}

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if not ticker:
             # Try to parse ticker from description if not in context
             words = task_description.split()
             for word in words:
                 if word.isupper() and len(word) <= 5:
                     ticker = word
                     break
        
        if ticker:
            self.fetch_stock_data(ticker)
            return f"Data fetched for {ticker}"
        else:
            return "No ticker specified."
