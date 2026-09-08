import yfinance as yf
import pandas as pd
import numpy as np
import requests

NEWS_API_KEY = "a2ae4865b85d409e983cbb6ff093a76c"

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
    
    headlines = []
    for article in articles:
        headlines.append(article["title"])
    
    return headlines

tickers_input = input("Enter up to 5 tickers separated by commas: ")
tickers = [t.strip().upper() for t in tickers_input.split(",")][:5]

for ticker in tickers:
    print(f"\n{'='*50}")
    print(f"Pulling data for {ticker}...")
    
    fin_data = get_financial_data(ticker)
    news = get_news(fin_data["name"])
    
    print(f"\n{fin_data['name']} ({ticker})")
    print(f"Price: ${fin_data['price']}")
    print(f"P/E Ratio: {fin_data['pe_ratio']}")
    print(f"Market Cap: ${fin_data['market_cap']:,}" if isinstance(fin_data['market_cap'], int) else f"Market Cap: {fin_data['market_cap']}")
    print(f"6-Month Return: {fin_data['6mo_return']}%")
    print(f"Volatility: {fin_data['volatility']}")
    print(f"Sharpe Ratio: {fin_data['sharpe']}")
    print(f"Max Drawdown: {fin_data['max_drawdown']}%")
    
    print(f"\nRecent Headlines:")
    for i, headline in enumerate(news[:5], start=1):
        print(f"  {i}. {headline}")