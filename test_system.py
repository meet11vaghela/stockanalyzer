#!/usr/bin/env python3
"""
Comprehensive test script for Multi-Agent Stock Analysis System
Tests multiple stocks and generates detailed reports
"""

import sys
import json
from agents.orchestrator import OrchestratorAgent
from core.state_manager import StateManager

def test_stock_analysis(ticker: str):
    """Run analysis for a single stock"""
    print(f"\n{'='*60}")
    print(f"Analyzing {ticker}...")
    print(f"{'='*60}\n")
    
    orchestrator = OrchestratorAgent()
    result = orchestrator.run_analysis(ticker)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return None
    
    # Display results
    print(f"\n📊 ANALYSIS RESULTS FOR {ticker}")
    print(f"{'─'*60}")
    print(f"🎯 Recommendation: {result['overall_rating']}")
    print(f"📈 Overall Score: {result['overall_score']}/100")
    print(f"⚠️  Risk Level: {result['risk_assessment']['risk_level']}")
    print(f"\n📉 Technical Analysis:")
    print(f"   RSI: {result['technical_analysis']['rsi']:.2f}")
    print(f"   Score: {result['technical_analysis']['score']}/100")
    print(f"   Signals: {', '.join(result['technical_analysis']['signals'][:2])}")
    
    print(f"\n💰 Fundamental Analysis:")
    print(f"   P/E Ratio: {result['fundamental_analysis']['pe_ratio']}")
    print(f"   Score: {result['fundamental_analysis']['score']}/100")
    
    print(f"\n📰 Sentiment Analysis:")
    print(f"   Sentiment Score: {result['sentiment_analysis']['sentiment_score']:.2f}/100")
    print(f"   Articles Analyzed: {result['sentiment_analysis']['article_count']}")
    
    print(f"\n⚡ Risk Metrics:")
    print(f"   Volatility: {result['risk_assessment']['annualized_volatility']:.2%}")
    print(f"   Max Drawdown: {result['risk_assessment']['max_drawdown']:.2%}")
    
    print(f"\n{'─'*60}\n")
    
    return result

def main():
    print("🚀 Multi-Agent Stock Analysis System - Comprehensive Test")
    print("=" * 60)
    
    # Test with multiple stocks
    test_tickers = ["AAPL", "MSFT", "GOOGL"]
    
    results = {}
    for ticker in test_tickers:
        result = test_stock_analysis(ticker)
        if result:
            results[ticker] = result
    
    # Summary comparison
    print(f"\n{'='*60}")
    print("📊 COMPARATIVE SUMMARY")
    print(f"{'='*60}\n")
    
    print(f"{'Ticker':<10} {'Rating':<15} {'Score':<10} {'Risk':<10}")
    print(f"{'-'*60}")
    for ticker, data in results.items():
        print(f"{ticker:<10} {data['overall_rating']:<15} {data['overall_score']:<10.1f} {data['risk_assessment']['risk_level']:<10}")
    
    # Save detailed report
    with open('analysis_report.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n✅ Detailed report saved to: analysis_report.json")
    print(f"{'='*60}\n")

if __name__ == "__main__":
    main()
