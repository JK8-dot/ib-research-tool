import datetime

# Ticker + Company Formatter
# Takes a company name and stock ticker as input
# Outputs multiple formatted versions

ticker = input("Enter stock ticker: ")
company = input("Enter company name: ")

ticker = ticker.upper()
company = company.title()

print(f"\n{company} ({ticker})")
print(f"Ticker length: {len(ticker)} characters")

if len(ticker) >= 1 and len(ticker) <= 5:
    print("Ticker length: Valid (1-5 characters)")
else:
    print("Ticker length: Invalid (must be 1-5 characters)")

slug = company.lower().replace(" ", "-")
print(f"URL slug: {slug}")

print(f"\nBloomberg Header:")
print(f"{ticker} US Equity  |  {company}  |  Last updated: {datetime.date.today()}")
