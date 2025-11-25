import pandas as pd
import numpy as np
from agents.base_agent import BaseAgent

class RiskAssessmentAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="RiskAssessment",
            role="Risk Manager",
            goal="Evaluate investment risks and volatility.",
            backstory="Conservative risk analyst focused on capital preservation."
        )

    def analyze(self, ticker: str) -> dict:
        self.log(f"Starting risk assessment for {ticker}...")
        
        data_key = f"data_{ticker}"
        raw_data = self.read_from_memory(data_key)
        if not raw_data:
            return {"error": f"No data found for {ticker}"}

        try:
            history_json = raw_data.get("history_daily")
            df = pd.read_json(history_json)
            df.sort_index(inplace=True)
            
            # Calculate Returns
            df['Returns'] = df['Close'].pct_change()
            
            # 1. Volatility (Annualized)
            daily_volatility = df['Returns'].std()
            annualized_volatility = daily_volatility * np.sqrt(252)
            
            # 2. Max Drawdown
            cumulative_returns = (1 + df['Returns']).cumprod()
            peak = cumulative_returns.expanding(min_periods=1).max()
            drawdown = (cumulative_returns / peak) - 1
            max_drawdown = drawdown.min()
            
            # Risk Rating
            risk_level = "Low"
            if annualized_volatility > 0.30:
                risk_level = "High"
            elif annualized_volatility > 0.15:
                risk_level = "Medium"
            
            result = {
                "annualized_volatility": annualized_volatility,
                "max_drawdown": max_drawdown,
                "risk_level": risk_level
            }

            self.save_to_memory(f"risk_{ticker}", result)
            self.log(f"Risk assessment completed for {ticker}")
            return result

        except Exception as e:
            self.log(f"Error in risk assessment: {e}")
            return {"error": str(e)}

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if ticker:
            self.analyze(ticker)
            return f"Risk assessment done for {ticker}"
        return "No ticker provided"
