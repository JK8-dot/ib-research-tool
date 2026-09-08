import yfinance as yf

tickers_input = input("Enter up to 5 ticker symbols separated by commas (e.g. AAPL, MSFT, NVDA): ")
tickers = [t.strip().upper() for t in tickers_input.split(",")][:5]

for ticker in tickers:
    stock = yf.Ticker(ticker)
    info = stock.info
    
    name = info.get("longName", ticker)
    price = info.get("currentPrice", "N/A")
    week_high = info.get("fiftyTwoWeekHigh", "N/A")
    week_low = info.get("fiftyTwoWeekLow", "N/A")
    market_cap = info.get("marketCap", "N/A")
    pe_ratio = info.get("trailingPE", "N/A")
    day_change = info.get("regularMarketChangePercent", "N/A")
    volume = info.get("volume", "N/A")
    avg_volume = info.get("averageVolume", "N/A")
    
    print(f"\n{ticker} — {name}")
    print(f"Price: ${price}")
    print(f"Day Change: {round(day_change, 2)}%" if isinstance(day_change, float) else f"Day Change: {day_change}")
    print(f"52-Week High: ${week_high} | Low: ${week_low}")
    print(f"Market Cap: ${market_cap:,}" if isinstance(market_cap, int) else f"Market Cap: {market_cap}")
    print(f"P/E Ratio: {pe_ratio}")
    print(f"Volume: {volume:,} | Avg Volume: {avg_volume:,}" if isinstance(volume, int) else f"Volume: {volume}")

    flags = []
    
    if isinstance(price, float) and isinstance(week_high, float):
        if (week_high - price) / week_high <= 0.05:
            flags.append("🚀 Within 5% of 52-week high — momentum signal")
    
    if isinstance(volume, int) and isinstance(avg_volume, int):
        if volume > 2 * avg_volume:
            flags.append("⚠️ Volume over 2x average — unusual activity")
    
    if isinstance(pe_ratio, float) and pe_ratio > 40:
        flags.append("💸 P/E above 40 — expensive by traditional metrics")
    
    if flags:
        print("Flags:")
        for flag in flags:
            print(f"  {flag}")