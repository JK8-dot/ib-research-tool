# Stock Watchlist Tracker
# User inputs up to 10 tickers and target buy prices
# Compares against current prices and ranks by closest to target

watchlist = []

print("Enter up to 10 stock tickers and your target buy price.")
print("Type 'done' when finished.\n")

while len(watchlist) < 10:
    ticker = input("Enter ticker (or 'done' to finish): ").upper()
    if ticker == "DONE":
        break
    target_price = float(input(f"Enter your target buy price for {ticker}: $"))
    watchlist.append((ticker, target_price))

print("\nNow enter the current price for each ticker.")

results = []

for ticker, target_price in watchlist:
    current_price = float(input(f"Current price for {ticker}: $"))
    gap = ((current_price - target_price) / target_price) * 100
    results.append((ticker, target_price, current_price, gap))

results.sort(key=lambda x: abs(x[3]))

print(f"\n{'Rank':<5} | {'Ticker':<6} | {'Target':>10} | {'Current':>10} | {'Gap %':>8}")
print("-" * 50)

rank = 1
for ticker, target_price, current_price, gap in results:
    print(f"{rank:<5} | {ticker:<6} | ${target_price:>9,.2f} | ${current_price:>9,.2f} | {gap:>7.2f}%")
    if current_price < target_price:
        print(f"      → BUY SIGNAL: {ticker} is below your target price")
    rank += 1