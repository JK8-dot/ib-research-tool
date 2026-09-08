import anthropic
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

ANTHROPIC_KEY = os.getenv("ANTHROPIC_API_KEY")
NEWS_API_KEY = "a2ae4865b85d409e983cbb6ff093a76c"

client = anthropic.Anthropic(api_key=ANTHROPIC_KEY)

def get_financial_data(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    hist = stock.history(period="6mo")
    
    returns = hist["Close"].pct_change().dropna()
    total_return = (hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100
    volatility = returns.std() * np.sqrt(252)
    sharpe = (returns.mean() / returns.std()) * np.sqrt(252)
    rolling_max = hist["Close"].cummax()
    max_drawdown = ((hist["Close"] - rolling_max) / rolling_max).min() * 100

    return {
        "name": info.get("longName", ticker),
        "price": info.get("currentPrice", "N/A"),
        "pe_ratio": info.get("trailingPE", "N/A"),
        "market_cap": info.get("marketCap", "N/A"),
        "6mo_return": round(total_return, 2),
        "volatility": round(volatility, 4),
        "sharpe": round(sharpe, 4),
        "max_drawdown": round(max_drawdown, 2)
    }

def get_news(company_name):
    url = f"https://newsapi.org/v2/everything?q={company_name}&language=en&sortBy=publishedAt&pageSize=10&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    articles = response.json().get("articles", [])
    headlines = [article["title"] for article in articles[:5]]
    return headlines

def generate_research_note(ticker, fin_data, headlines):
    data_summary = f"""
Company: {fin_data['name']} ({ticker})
Current Price: ${fin_data['price']}
P/E Ratio: {fin_data['pe_ratio']}
Market Cap: {fin_data['market_cap']}
6-Month Return: {fin_data['6mo_return']}%
Annualized Volatility: {fin_data['volatility']}
Sharpe Ratio: {fin_data['sharpe']}
Max Drawdown: {fin_data['max_drawdown']}%

Recent Headlines:
{chr(10).join(f"- {h}" for h in headlines)}
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        system="""You are a senior equity research analyst at a bulge bracket investment bank.
Given quantitative data and recent news, write a structured 3-paragraph research note:
Paragraph 1: Valuation assessment vs sector peers
Paragraph 2: Key risks to the investment thesis
Paragraph 3: Price target rationale and recommendation (Buy / Hold / Sell)
Be specific. Use the numbers provided.""",
        messages=[
            {"role": "user", "content": data_summary}
        ]
    )
    
    return message.content[0].text

tickers_input = input("Enter up to 3 tickers separated by commas: ")
tickers = [t.strip().upper() for t in tickers_input.split(",")][:3]

for ticker in tickers:
    print(f"\n{'='*60}")
    print(f"Analyzing {ticker}...")
    
    fin_data = get_financial_data(ticker)
    headlines = get_news(fin_data["name"])
    research_note = generate_research_note(ticker, fin_data, headlines)
    
    print(f"\n{fin_data['name']} ({ticker})")
    print(f"Price: ${fin_data['price']} | P/E: {fin_data['pe_ratio']} | 6mo Return: {fin_data['6mo_return']}%")
    
    print(f"\nRecent Headlines:")
    for h in headlines:
        print(f"  • {h}")
    
    print(f"\n--- AI RESEARCH NOTE ---")
    print(research_note)