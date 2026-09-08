import os
import yfinance as yf
from datetime import datetime
from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.tools import tool
from langgraph.prebuilt import create_react_agent
from fpdf import FPDF

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

def save_to_pdf(ticker, content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_margins(15, 15, 15)

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, f"IB Research Brief: {ticker.upper()}", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.cell(0, 8, f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 11)
    for line in content.split("\n"):
        clean_line = line.encode("ascii", "ignore").decode("ascii")
        clean_line = clean_line.replace("|", " ").strip()

        if not clean_line or all(c in "-=*_# " for c in clean_line):
            pdf.ln(3)
            continue

        words = []
        for word in clean_line.split():
            if len(word) > 50:
                word = word[:50]
            words.append(word)
        clean_line = " ".join(words)

        try:
            if clean_line.startswith("# "):
                pdf.set_font("Helvetica", "B", 13)
                pdf.multi_cell(0, 8, clean_line.replace("# ", ""))
                pdf.set_font("Helvetica", "", 11)
            elif clean_line.startswith("## "):
                pdf.set_font("Helvetica", "B", 12)
                pdf.multi_cell(0, 8, clean_line.replace("## ", ""))
                pdf.set_font("Helvetica", "", 11)
            else:
                pdf.multi_cell(0, 6, clean_line)
        except Exception:
            pass

    filename = f"{ticker.upper()}_Research_Brief_{datetime.now().strftime('%Y-%m-%d')}.pdf"
    pdf.output(filename)
    return filename

print("="*60)
print("IB RESEARCH AGENT — FULL PIPELINE")
print("="*60)

ticker = input("\nEnter a company ticker to research: ")

print(f"\nRunning full research pipeline for {ticker.upper()}...")
print("This will take 2-3 minutes. Stand by.")
print("-"*60)

result = agent_executor.invoke({
    "messages": [("human", f"""You are a senior equity research analyst at a bulge bracket investment bank.
    
Research {ticker} and produce a complete institutional research note with these exact sections:

1. Executive Summary (3 sentences max — what the company does, its position, your recommendation)
2. Business Overview (business model, products/services, revenue streams)
3. Financial Snapshot (use get_stock_data to pull live data — include all key metrics)
4. Competitive Positioning (search for main competitors, how {ticker} stacks up)
5. Industry Tailwinds and Headwinds (search for industry trends affecting this company)
6. Key Risks (top 3-5 specific risks with explanation)
7. Investment Thesis and Recommendation (Buy / Hold / Sell with clear reasoning and price target rationale)

Be specific. Use real numbers. This note will be read by a portfolio manager.""")]
})

research_note = result["messages"][-1].content

print("\nResearch complete. Saving to PDF...")

filename = save_to_pdf(ticker, research_note)

print(f"\nDone. File saved as: {filename}")
print("\nRESEARCH NOTE PREVIEW:")
print("="*60)
print(research_note[:500] + "...")