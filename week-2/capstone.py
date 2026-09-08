import csv
import datetime
import os
import random

# Investment & Business Dashboard v1.0
# Logs business ideas and stock positions to CSV
# View, analyze, and project growth

IDEAS_FILE = "ideas.csv"
PORTFOLIO_FILE = "portfolio.csv"

def setup_files():
    if not os.path.exists(IDEAS_FILE):
        with open(IDEAS_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "name", "problem", "customer", "revenue", "market_size", "personal_edge", "ease", "avg_score"])
    
    if not os.path.exists(PORTFOLIO_FILE):
        with open(PORTFOLIO_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["date", "ticker", "shares", "buy_price"])

def log_business_idea():
    print("\n--- Log Business Idea ---")
    name = input("Idea name: ")
    problem = input("Problem it solves: ")
    customer = input("Target customer: ")
    revenue = input("Revenue model: ")
    
    while True:
        try:
            market_size = int(input("Market size (1-5): "))
            if 1 <= market_size <= 5:
                break
            print("Must be between 1 and 5. Try again.")
        except ValueError:
            print("Please enter a whole number. Try again.")
    
    while True:
        try:
            personal_edge = int(input("Personal edge (1-5): "))
            if 1 <= personal_edge <= 5:
                break
            print("Must be between 1 and 5. Try again.")
        except ValueError:
            print("Please enter a whole number. Try again.")
    
    while True:
        try:
            ease = int(input("Ease of starting (1-5): "))
            if 1 <= ease <= 5:
                break
            print("Must be between 1 and 5. Try again.")
        except ValueError:
            print("Please enter a whole number. Try again.")
    
    avg_score = round((market_size + personal_edge + ease) / 3, 2)
    date = datetime.date.today()
    
    with open(IDEAS_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, name, problem, customer, revenue, market_size, personal_edge, ease, avg_score])
    
    print(f"\nIdea logged! Score: {avg_score}/5")

def log_stock_position():
    print("\n--- Log Stock Position ---")
    ticker = input("Enter ticker symbol: ").upper()
    
    while True:
        try:
            shares = float(input(f"Number of shares of {ticker}: "))
            if shares > 0:
                break
            print("Shares must be greater than zero. Try again.")
        except ValueError:
            print("Please enter a number. Try again.")
    
    while True:
        try:
            buy_price = float(input(f"Buy price per share ($): "))
            if buy_price > 0:
                break
            print("Price must be greater than zero. Try again.")
        except ValueError:
            print("Please enter a number. Try again.")
    
    date = datetime.date.today()
    cost_basis = shares * buy_price
    
    with open(PORTFOLIO_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, ticker, shares, buy_price])
    
    print(f"\nPosition logged!")
    print(f"{ticker}: {shares} shares at ${buy_price:,.2f}")
    print(f"Cost basis: ${cost_basis:,.2f}")

def view_business_ideas():
    if not os.path.exists(IDEAS_FILE):
        print("\nNo ideas logged yet.")
        return
    
    with open(IDEAS_FILE, "r") as f:
        reader = csv.DictReader(f)
        ideas = list(reader)
    
    if len(ideas) == 0:
        print("\nNo ideas logged yet.")
        return
    
    ideas.sort(key=lambda x: float(x["avg_score"]), reverse=True)
    
    print(f"\n{'Rank':<5} | {'Idea':<20} | {'Score':<6} | {'Date':<12}")
    print("-" * 50)
    
    for i, idea in enumerate(ideas, start=1):
        print(f"{i:<5} | {idea['name']:<20} | {float(idea['avg_score']):<6.2f} | {idea['date']:<12}")
    
    print(f"\nTop Idea: {ideas[0]['name']}")
    print(f"Problem:  {ideas[0]['problem']}")
    print(f"Customer: {ideas[0]['customer']}")
    print(f"Revenue:  {ideas[0]['revenue']}")

def view_portfolio():
    if not os.path.exists(PORTFOLIO_FILE):
        print("\nNo positions logged yet.")
        return
    
    with open(PORTFOLIO_FILE, "r") as f:
        reader = csv.DictReader(f)
        positions = list(reader)
    
    if len(positions) == 0:
        print("\nNo positions logged yet.")
        return
    
    print(f"\n{'Ticker':<8} | {'Shares':<8} | {'Buy Price':<12} | {'Cost Basis':<12} | {'Date':<12}")
    print("-" * 65)
    
    total_cost = 0
    
    for position in positions:
        ticker = position["ticker"]
        shares = float(position["shares"])
        buy_price = float(position["buy_price"])
        cost_basis = shares * buy_price
        total_cost += cost_basis
        date = position["date"]
        
        print(f"{ticker:<8} | {shares:<8.2f} | ${buy_price:<11,.2f} | ${cost_basis:<11,.2f} | {date:<12}")
    
    print("-" * 65)
    print(f"Total Portfolio Cost Basis: ${total_cost:,.2f}")

def compound_growth_projection():
    print("\n--- Compound Growth Projection ---")
    
    while True:
        try:
            monthly_savings = float(input("Monthly savings amount ($): "))
            if monthly_savings > 0:
                break
            print("Must be greater than zero. Try again.")
        except ValueError:
            print("Please enter a number. Try again.")
    
    while True:
        try:
            annual_return = float(input("Expected annual return (%): "))
            if annual_return > 0:
                break
            print("Must be greater than zero. Try again.")
        except ValueError:
            print("Please enter a number. Try again.")
    
    monthly_return = annual_return / 100 / 12
    
    print(f"\nCompound Growth Projection (${monthly_savings:,.2f}/month at {annual_return}%):")
    print(f"{'Years':<10} | {'Final Value':>15}")
    print("-" * 30)
    
    for years in [5, 10, 20, 30]:
        months = years * 12
        future_value = monthly_savings * (((1 + monthly_return) ** months - 1) / monthly_return)
        print(f"{years:<10} | ${future_value:>14,.2f}")

def random_prompt():
    prompts = [
        "FinTech: How do college students manage debt without financial literacy?",
        "HealthTech: How do busy professionals track nutrition without meal prepping?",
        "EdTech: How do first-generation students navigate college applications?",
        "PropTech: How do tenants find reliable maintenance contractors?",
        "LegalTech: How do small businesses handle contracts without lawyers?",
        "InsurTech: How do young people understand what insurance they actually need?",
        "AgTech: How do small farms compete with large agricultural corporations?",
        "CleanTech: How do households reduce energy costs without solar panels?",
        "LogTech: How do small retailers manage inventory without expensive software?",
        "HRTech: How do startups hire and retain talent without HR departments?",
        "RetailTech: How do local stores compete with Amazon on convenience?",
        "MedTech: How do patients manage chronic conditions between doctor visits?",
        "TravelTech: How do budget travelers find authentic local experiences?",
        "SportsTech: How do amateur athletes get professional-level performance data?",
        "FoodTech: How do restaurants reduce food waste without cutting menu items?",
        "SecTech: How do small businesses protect against cybersecurity threats?",
        "ConsTech: How do homeowners manage renovation projects without overpaying?",
        "EduTech: How do working adults upskill without quitting their jobs?",
        "SocTech: How do nonprofits measure the real impact of their programs?",
        "BioTech: How do elderly patients manage multiple medications safely?"
    ]
    
    prompt = random.choice(prompts)
    print(f"\nRandom Idea Prompt:\n{prompt}")

# Main Menu
def main():
    setup_files()
    
    print("=" * 50)
    print("INVESTMENT & BUSINESS DASHBOARD v1.0")
    print("=" * 50)
    
    while True:
        print("\n1. Log a business idea")
        print("2. Log a stock position")
        print("3. View business ideas")
        print("4. View portfolio")
        print("5. Run compound growth projection")
        print("6. Random idea prompt")
        print("7. Exit")
        
        choice = input("\nSelect an option (1-6): ")
        
        if choice == "1":
            log_business_idea()
        elif choice == "2":
            log_stock_position()
        elif choice == "3":
            view_business_ideas()
        elif choice == "4":
            view_portfolio()
        elif choice == "5":
            compound_growth_projection()
        elif choice == "6":
            random_prompt()
        elif choice == "7":
            print("\nGoodbye.")
            break
        else:
            print("Invalid option. Please enter 1-7.")

if __name__ == "__main__":
    main()