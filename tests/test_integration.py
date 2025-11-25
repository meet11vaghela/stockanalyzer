import unittest
from unittest.mock import MagicMock, patch
import pandas as pd
import numpy as np
from agents.orchestrator import OrchestratorAgent

class TestStockAnalysisSystem(unittest.TestCase):
    
    @patch('agents.data_fetcher.yf.Ticker')
    def test_full_pipeline(self, mock_ticker):
        # Mock yfinance data
        mock_stock = MagicMock()
        
        # Mock History
        dates = pd.date_range(start='2023-01-01', periods=100)
        data = {
            'Open': np.random.rand(100) * 100,
            'High': np.random.rand(100) * 105,
            'Low': np.random.rand(100) * 95,
            'Close': np.random.rand(100) * 100,
            'Volume': np.random.randint(1000, 10000, 100)
        }
        mock_history = pd.DataFrame(data, index=dates)
        mock_stock.history.return_value = mock_history
        
        # Mock Info
        mock_stock.info = {
            "marketCap": 2000000000000,
            "trailingPE": 25,
            "forwardPE": 20,
            "dividendYield": 0.005,
            "sector": "Technology",
            "industry": "Consumer Electronics",
            "currentPrice": 150
        }
        
        # Mock News
        mock_stock.news = [
            {"title": "Apple releases new iPhone", "publisher": "TechCrunch"},
            {"title": "Stock market hits record high", "publisher": "CNBC"}
        ]
        
        mock_ticker.return_value = mock_stock

        # Run Orchestrator
        orchestrator = OrchestratorAgent()
        result = orchestrator.run_analysis("AAPL")
        
        # Assertions
        self.assertIn("overall_rating", result)
        self.assertIn("overall_score", result)
        self.assertIn("technical_analysis", result)
        self.assertIn("fundamental_analysis", result)
        self.assertIn("sentiment_analysis", result)
        self.assertIn("risk_assessment", result)
        
        print("\nTest Result Summary:")
        print(result['summary'])

if __name__ == '__main__':
    unittest.main()
