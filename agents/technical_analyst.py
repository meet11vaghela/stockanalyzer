import talib
import pandas as pd
import numpy as np
from agents.base_agent import BaseAgent
import json

class TechnicalAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="TechnicalAnalyst",
            role="Technical Analysis Expert",
            goal="Analyze price patterns, calculate indicators, and generate trading signals.",
            backstory="Seasoned chartist with expertise in algorithmic trading signals."
        )

    def analyze(self, ticker: str) -> dict:
        self.log(f"Starting technical analysis for {ticker}...")
        
        # Retrieve data
        data_key = f"data_{ticker}"
        raw_data = self.read_from_memory(data_key)
        if not raw_data:
            return {"error": f"No data found for {ticker}"}

        try:
            # Parse historical data
            history_json = raw_data.get("history_daily")
            df = pd.read_json(history_json)
            df.sort_index(inplace=True)
            
            close_prices = df['Close'].values
            high_prices = df['High'].values
            low_prices = df['Low'].values

            # Calculate Indicators
            # 1. RSI
            rsi = talib.RSI(close_prices, timeperiod=14)
            current_rsi = rsi[-1]

            # 2. MACD
            macd, macdsignal, macdhist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)
            
            # 3. Moving Averages
            sma_50 = talib.SMA(close_prices, timeperiod=50)
            sma_200 = talib.SMA(close_prices, timeperiod=200)
            
            # 4. Bollinger Bands
            upper, middle, lower = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

            # Signals
            signals = []
            if current_rsi < 30:
                signals.append("RSI Oversold (Buy Signal)")
            elif current_rsi > 70:
                signals.append("RSI Overbought (Sell Signal)")

            if close_prices[-1] > sma_200[-1]:
                signals.append("Price above 200 SMA (Bullish Trend)")
            else:
                signals.append("Price below 200 SMA (Bearish Trend)")

            if macd[-1] > macdsignal[-1]:
                signals.append("MACD Bullish Crossover")
            
            # Pattern Recognition (Simple example: Engulfing)
            engulfing = talib.CDLENGULFING(df['Open'].values, high_prices, low_prices, close_prices)
            if engulfing[-1] != 0:
                pattern_type = "Bullish" if engulfing[-1] > 0 else "Bearish"
                signals.append(f"{pattern_type} Engulfing Pattern Detected")

            analysis_result = {
                "rsi": float(current_rsi),
                "macd": float(macd[-1]),
                "sma_50": float(sma_50[-1]),
                "sma_200": float(sma_200[-1]),
                "bb_upper": float(upper[-1]),
                "bb_lower": float(lower[-1]),
                "signals": signals,
                "score": self._calculate_technical_score(current_rsi, close_prices[-1], sma_200[-1], macd[-1], macdsignal[-1])
            }

            self.save_to_memory(f"technical_{ticker}", analysis_result)
            self.log(f"Technical analysis completed for {ticker}")
            return analysis_result

        except Exception as e:
            self.log(f"Error in technical analysis: {e}")
            return {"error": str(e)}

    def _calculate_technical_score(self, rsi, price, sma200, macd, macd_signal):
        score = 50
        # RSI contribution
        if 30 <= rsi <= 70: score += 10
        if rsi < 30: score += 20 # Oversold bounce potential
        if rsi > 70: score -= 10 # Overbought risk
        
        # Trend contribution
        if price > sma200: score += 20
        else: score -= 20
        
        # Momentum contribution
        if macd > macd_signal: score += 10
        
        return max(0, min(100, score))

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if ticker:
            self.analyze(ticker)
            return f"Technical analysis done for {ticker}"
        return "No ticker provided"
