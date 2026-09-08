import yfinance as yf
import pandas as pd
import numpy as np

tickers_input = input("Enter up to 10 ticker symbols separated by commas: ")
tickers = [t.strip().upper() for t in tickers_input.split(",")][:10]

print("\nPulling 1 year of price data...")
raw = yf.download(tickers, period="1y", auto_adjust=True, progress=False)
df = raw["Close"]

print(df.tail())

returns = df.pct_change().dropna()

avg_return = returns.mean()
volatility = returns.std() * np.sqrt(252)
total_return = (df.iloc[-1] / df.iloc[0] - 1)
sharpe = (avg_return / returns.std()) * np.sqrt(252)

max_drawdown = {}
for ticker in df.columns:
    rolling_max = df[ticker].cummax()
    drawdown = (df[ticker] - rolling_max) / rolling_max
    max_drawdown[ticker] = drawdown.min()

max_drawdown = pd.Series(max_drawdown)

results = pd.DataFrame({
    "avg_daily_return": avg_return.round(4),
    "annualized_volatility": volatility.round(4),
    "total_return": total_return.round(4),
    "sharpe_ratio": sharpe.round(4),
    "max_drawdown": max_drawdown.round(4)
}).sort_values("sharpe_ratio", ascending=False)

print("\n--- Quantitative Market Dashboard ---")
print(results)

print("\n--- Top 3 by Sharpe Ratio ---")
print(results.head(3))

print("\n--- Correlation Matrix ---")
print(returns.corr().round(2))

results.to_csv("week-3/market_dashboard.csv")
print("\n✅ Exported to week-3/market_dashboard.csv")