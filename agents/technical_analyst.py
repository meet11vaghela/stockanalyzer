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

            # Calculate Indicators (without TA-Lib)
            # 1. RSI (Simple implementation)
            current_rsi = self._calculate_rsi(close_prices)

            # 2. MACD (Simple implementation)
            macd, macdsignal = self._calculate_macd(close_prices)
            
            # 3. Moving Averages
            sma_50 = np.mean(close_prices[-50:]) if len(close_prices) >= 50 else np.mean(close_prices)
            sma_200 = np.mean(close_prices[-200:]) if len(close_prices) >= 200 else np.mean(close_prices)
            
            # 4. Bollinger Bands
            bb_period = 20
            if len(close_prices) >= bb_period:
                sma = np.mean(close_prices[-bb_period:])
                std = np.std(close_prices[-bb_period:])
                upper = sma + (2 * std)
                lower = sma - (2 * std)
            else:
                upper = lower = np.mean(close_prices)

            # Signals
            signals = []
            if current_rsi < 30:
                signals.append("RSI Oversold (Buy Signal)")
            elif current_rsi > 70:
                signals.append("RSI Overbought (Sell Signal)")
            else:
                signals.append("RSI Neutral")

            if close_prices[-1] > sma_200:
                signals.append("Price above 200 SMA (Bullish Trend)")
            else:
                signals.append("Price below 200 SMA (Bearish Trend)")

            if macd > macdsignal:
                signals.append("MACD Bullish Crossover")
            else:
                signals.append("MACD Bearish")

            analysis_result = {
                "rsi": float(current_rsi),
                "macd": float(macd),
                "sma_50": float(sma_50),
                "sma_200": float(sma_200),
                "bb_upper": float(upper),
                "bb_lower": float(lower),
                "signals": signals,
                "score": self._calculate_technical_score(current_rsi, close_prices[-1], sma_200, macd, macdsignal)
            }

            self.save_to_memory(f"technical_{ticker}", analysis_result)
            self.log(f"Technical analysis completed for {ticker}")
            return analysis_result

        except Exception as e:
            self.log(f"Error in technical analysis: {e}")
            return {"error": str(e)}

    def _calculate_rsi(self, prices, period=14):
        """Simple RSI calculation"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        gains = np.where(deltas > 0, deltas, 0)
        losses = np.where(deltas < 0, -deltas, 0)
        
        avg_gain = np.mean(gains[-period:])
        avg_loss = np.mean(losses[-period:])
        
        if avg_loss == 0:
            return 100.0
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    def _calculate_macd(self, prices):
        """Simple MACD calculation"""
        if len(prices) < 26:
            return 0.0, 0.0
        
        ema_12 = self._ema(prices, 12)
        ema_26 = self._ema(prices, 26)
        macd = ema_12 - ema_26
        signal = self._ema(np.array([macd]), 9)
        
        return macd, signal

    def _ema(self, prices, period):
        """Exponential Moving Average"""
        if len(prices) < period:
            return np.mean(prices)
        
        multiplier = 2 / (period + 1)
        ema = np.mean(prices[:period])
        
        for price in prices[period:]:
            ema = (price * multiplier) + (ema * (1 - multiplier))
        
        return ema

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
