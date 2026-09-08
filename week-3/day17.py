import pandas as pd

df = pd.read_csv("week-3/Prices.csv")
print(df.head())
print(df.columns.tolist())

df = df.set_index("Date")
returns = df.pct_change().dropna()
print(returns.head())

import numpy as np

avg_return = returns.mean()
volatility = returns.std() * np.sqrt(252)
total_return = (df.iloc[-1] / df.iloc[0] - 1)

print("\n--- Average Daily Return ---")
print(avg_return.sort_values(ascending=False))

print("\n--- Annualized Volatility ---")
print(volatility.sort_values())

print("\n--- Total Return (2015-2025) ---")
print(total_return.sort_values(ascending=False))

sharpe = (avg_return / returns.std()) * np.sqrt(252)

print("\n--- Sharpe Ratio (Risk-Adjusted Return) ---")
print(sharpe.sort_values(ascending=False))

print("\n--- Top 3 Performers ---")
print(sharpe.sort_values(ascending=False).head(3))

print("\n--- Bottom 3 Performers ---")
print(sharpe.sort_values(ascending=False).tail(3))

print("\n--- Correlation Matrix ---")
print(returns.corr().round(2))

results = pd.DataFrame({
    "avg_daily_return": avg_return,
    "annualized_volatility": volatility,
    "total_return": total_return,
    "sharpe_ratio": sharpe
}).sort_values("sharpe_ratio", ascending=False)

results.to_csv("week-3/stock_analysis.csv")
print("\n✅ Results exported to week-3/stock_analysis.csv")