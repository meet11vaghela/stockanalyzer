from agents.base_agent import BaseAgent
from agents.data_fetcher import DataFetcherAgent
from agents.technical_analyst import TechnicalAnalystAgent
from agents.fundamental_analyst import FundamentalAnalystAgent
from agents.sentiment_analyst import SentimentAnalystAgent
from agents.risk_assessment import RiskAssessmentAgent
from agents.report_generator import ReportGeneratorAgent

class OrchestratorAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="Orchestrator",
            role="Team Lead",
            goal="Coordinate the analysis workflow and deliver final insights.",
            backstory="Experienced project manager ensuring seamless collaboration."
        )
        # Initialize sub-agents
        self.data_fetcher = DataFetcherAgent()
        self.technical_analyst = TechnicalAnalystAgent()
        self.fundamental_analyst = FundamentalAnalystAgent()
        self.sentiment_analyst = SentimentAnalystAgent()
        self.risk_analyst = RiskAssessmentAgent()
        self.report_generator = ReportGeneratorAgent()

    def run_analysis(self, ticker: str) -> dict:
        self.log(f"Starting analysis workflow for {ticker}")
        
        # 1. Fetch Data
        data_result = self.data_fetcher.fetch_stock_data(ticker)
        if "error" in data_result:
            return {"error": f"Data fetching failed: {data_result['error']}"}

        # 2. Parallel Analysis (Simulated here as sequential for simplicity, but could be threaded)
        self.technical_analyst.analyze(ticker)
        self.fundamental_analyst.analyze(ticker)
        self.sentiment_analyst.analyze(ticker)
        self.risk_analyst.analyze(ticker)

        # 3. Generate Report
        final_report = self.report_generator.generate_report(ticker)
        
        self.log(f"Analysis workflow completed for {ticker}")
        return final_report

    def execute_task(self, task_description: str, context: dict = None) -> str:
        ticker = context.get("ticker") if context else None
        if not ticker:
             words = task_description.split()
             for word in words:
                 if word.isupper() and len(word) <= 5:
                     ticker = word
                     break
        
        if ticker:
            result = self.run_analysis(ticker)
            return str(result)
        return "No ticker provided"
