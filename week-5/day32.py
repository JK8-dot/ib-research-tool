import os
import yfinance as yf
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent

load_dotenv()

llm = ChatAnthropic(
    model="claude-sonnet-4-6",
    temperature=0
)

@tool
def get_stock_data(ticker: str) -> str:
    """
    Fetches current financial data for a given stock ticker symbol.
    Returns current price, 52-week high and low, market cap, P/E ratio,
    daily percent change, volume, and average volume.
    Use this when you need live financial data or valuation metrics for a company.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info

        current_price = info.get("currentPrice", "N/A")
        week_high = info.get("fiftyTwoWeekHigh", "N/A")
        week_low = info.get("fiftyTwoWeekLow", "N/A")
        market_cap = info.get("marketCap", "N/A")
        pe_ratio = info.get("trailingPE", "N/A")
        volume = info.get("volume", "N/A")
        avg_volume = info.get("averageVolume", "N/A")
        daily_change = info.get("regularMarketChangePercent", "N/A")

        if market_cap != "N/A":
            market_cap = f"${market_cap / 1e9:.1f}B"

        return f"""
Stock: {ticker.upper()}
Current Price: ${current_price}
52-Week High: ${week_high}
52-Week Low: ${week_low}
Market Cap: {market_cap}
P/E Ratio: {pe_ratio}
Daily Change: {daily_change}%
Volume: {volume:,}
Avg Volume: {avg_volume:,}
        """
    except Exception as e:
        return f"Could not fetch data for {ticker}: {str(e)}"

search_tool = DuckDuckGoSearchRun()

tools = [search_tool, get_stock_data]

agent_executor = create_react_agent(llm, tools)

print("="*60)
print("COMPETITIVE ANALYSIS AGENT")
print("="*60)

target = input("\nEnter your target company ticker: ")
competitors = input("Enter up to 3 competitor tickers (comma-separated): ")

print(f"\nRunning competitive analysis...")
print("-"*60)

result = agent_executor.invoke({
    "messages": [("human", f"""Run a full competitive analysis.

Target company: {target}
Competitors: {competitors}

For each company (target and every competitor):
1. Use get_stock_data to pull live financial data
2. Search for recent news and business developments

Then synthesize everything into a structured competitive analysis:
- Market position overview
- Financial comparison table (price, market cap, P/E for each)
- Key competitive advantages per company
- Biggest threats to {target}
- Investment implication: which company looks most attractive and why""")]
})

print("-"*60)
print("\nCOMPETITIVE ANALYSIS:")
print("="*60)
print(result["messages"][-1].content)