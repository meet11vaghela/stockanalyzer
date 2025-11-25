#!/usr/bin/env python3
"""
Indian Stock Market Analysis
Analyzes major Indian stocks from NSE (National Stock Exchange)
"""

import sys
import json
from agents.orchestrator import OrchestratorAgent
from core.state_manager import StateManager

# Major Indian stocks (NSE symbols with .NS suffix for Yahoo Finance)
INDIAN_STOCKS = {
    "RELIANCE.NS": "Reliance Industries",
    "TCS.NS": "Tata Consultancy Services",
    "HDFCBANK.NS": "HDFC Bank",
    "INFY.NS": "Infosys",
    "ICICIBANK.NS": "ICICI Bank",
    "HINDUNILVR.NS": "Hindustan Unilever",
    "ITC.NS": "ITC Limited",
    "SBIN.NS": "State Bank of India",
    "BHARTIARTL.NS": "Bharti Airtel",
    "KOTAKBANK.NS": "Kotak Mahindra Bank",
    "LT.NS": "Larsen & Toubro",
    "AXISBANK.NS": "Axis Bank",
    "BAJFINANCE.NS": "Bajaj Finance",
    "ASIANPAINT.NS": "Asian Paints",
    "MARUTI.NS": "Maruti Suzuki",
    "TITAN.NS": "Titan Company",
    "WIPRO.NS": "Wipro",
    "HCLTECH.NS": "HCL Technologies",
    "ULTRACEMCO.NS": "UltraTech Cement",
    "NESTLEIND.NS": "Nestle India"
}

def analyze_indian_stock(ticker: str, company_name: str):
    """Analyze a single Indian stock"""
    print(f"\n{'='*70}")
    print(f"🇮🇳 Analyzing {company_name} ({ticker})")
    print(f"{'='*70}\n")
    
    orchestrator = OrchestratorAgent()
    result = orchestrator.run_analysis(ticker)
    
    if "error" in result:
        print(f"❌ Error: {result['error']}")
        return None
    
    # Display results
    print(f"\n📊 ANALYSIS RESULTS FOR {company_name}")
    print(f"{'─'*70}")
    print(f"🎯 Recommendation: {result['overall_rating']}")
    print(f"📈 Overall Score: {result['overall_score']}/100")
    print(f"⚠️  Risk Level: {result['risk_assessment']['risk_level']}")
    
    print(f"\n📉 Technical Analysis:")
    print(f"   RSI: {result['technical_analysis']['rsi']:.2f}")
    print(f"   Score: {result['technical_analysis']['score']}/100")
    print(f"   Signals: {', '.join(result['technical_analysis']['signals'][:2])}")
    
    print(f"\n💰 Fundamental Analysis:")
    pe = result['fundamental_analysis']['pe_ratio']
    print(f"   P/E Ratio: {pe if pe else 'N/A'}")
    print(f"   Score: {result['fundamental_analysis']['score']}/100")
    
    print(f"\n⚡ Risk Metrics:")
    print(f"   Volatility: {result['risk_assessment']['annualized_volatility']:.2%}")
    print(f"   Max Drawdown: {result['risk_assessment']['max_drawdown']:.2%}")
    
    print(f"\n{'─'*70}\n")
    
    return result

def main():
    print("🇮🇳 INDIAN STOCK MARKET ANALYSIS")
    print("=" * 70)
    print(f"Analyzing {len(INDIAN_STOCKS)} major Indian stocks from NSE")
    print("=" * 70)
    
    results = {}
    successful = 0
    failed = 0
    
    for ticker, company_name in INDIAN_STOCKS.items():
        try:
            result = analyze_indian_stock(ticker, company_name)
            if result:
                results[ticker] = {
                    "company": company_name,
                    "analysis": result
                }
                successful += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Failed to analyze {company_name}: {e}\n")
            failed += 1
    
    # Summary
    print(f"\n{'='*70}")
    print("📊 INDIAN MARKET SUMMARY")
    print(f"{'='*70}\n")
    
    # Sort by score
    sorted_stocks = sorted(
        results.items(), 
        key=lambda x: x[1]['analysis']['overall_score'], 
        reverse=True
    )
    
    print(f"{'Rank':<6} {'Company':<30} {'Rating':<12} {'Score':<10} {'Risk':<10}")
    print(f"{'-'*70}")
    
    for idx, (ticker, data) in enumerate(sorted_stocks, 1):
        analysis = data['analysis']
        company = data['company'][:28]
        print(f"{idx:<6} {company:<30} {analysis['overall_rating']:<12} "
              f"{analysis['overall_score']:<10.1f} {analysis['risk_assessment']['risk_level']:<10}")
    
    # Top recommendations
    print(f"\n{'='*70}")
    print("🏆 TOP 5 RECOMMENDATIONS")
    print(f"{'='*70}\n")
    
    for idx, (ticker, data) in enumerate(sorted_stocks[:5], 1):
        analysis = data['analysis']
        print(f"{idx}. {data['company']} ({ticker.replace('.NS', '')})")
        print(f"   Rating: {analysis['overall_rating']} | Score: {analysis['overall_score']}/100")
        print(f"   RSI: {analysis['technical_analysis']['rsi']:.2f} | "
              f"P/E: {analysis['fundamental_analysis']['pe_ratio'] or 'N/A'}")
        print()
    
    # Save report
    with open('indian_stocks_report.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"✅ Detailed report saved to: indian_stocks_report.json")
    print(f"📊 Successfully analyzed: {successful} stocks")
    print(f"❌ Failed: {failed} stocks")
    print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
