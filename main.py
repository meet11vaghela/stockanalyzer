import argparse
import sys
from agents.orchestrator import OrchestratorAgent

def main():
    parser = argparse.ArgumentParser(description="Multi-Agent Stock Analysis System")
    parser.add_argument("ticker", help="Stock ticker symbol (e.g., AAPL)")
    args = parser.parse_args()

    print(f"Initializing Multi-Agent System for {args.ticker}...")
    
    orchestrator = OrchestratorAgent()
    result = orchestrator.run_analysis(args.ticker)
    
    print("\nAnalysis Complete!")
    print("-" * 50)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print(f"Recommendation: {result.get('overall_rating')}")
        print(f"Score: {result.get('overall_score')}/100")
        print(f"Summary: {result.get('summary')}")
        print("-" * 50)
        print("Full report saved to memory.")

if __name__ == "__main__":
    main()
