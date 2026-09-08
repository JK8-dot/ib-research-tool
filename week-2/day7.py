import datetime

# Personal Finance Dashboard v2
# Refactored version of Week 1 capstone
# Every logical block is now its own function

def get_income():
    while True:
        try:
            income = float(input("Enter your monthly take-home income ($): "))
            if income <= 0:
                print("Income must be greater than zero. Try again.")
                continue
            return income
        except ValueError:
            print("Invalid input. Please enter a number. Try again.")

def get_expenses():
    expenses = {}
    print("\nEnter your expense categories and amounts.")
    print("Type 'done' when finished.\n")
    
    while True:
        category = input("Enter expense category (or 'done' to finish): ")
        if category.lower() == "done":
            break
        if category.strip() == "":
            print("Category name cannot be empty. Try again.")
            continue
        while True:
            try:
                amount = float(input(f"Enter amount for {category}: $"))
                if amount < 0:
                    print("Amount cannot be negative. Try again.")
                    continue
                break
            except ValueError:
                print("Invalid input. Please enter a number. Try again.")
        expenses[category] = amount
    
    return expenses

def calculate_savings(income, expenses):
    total_expenses = sum(expenses.values())
    savings = income - total_expenses
    savings_rate = (savings / income) * 100
    return savings, total_expenses, savings_rate

def categorize_savings_rate(savings_rate):
    if savings_rate < 10:
        return "Critical -- below survival threshold"
    elif savings_rate < 20:
        return "Minimal -- reduce expenses or increase income"
    elif savings_rate < 35:
        return "Healthy -- on track"
    else:
        return "Strong -- wealth-building pace"

def project_growth(savings, annual_return):
    monthly_return = annual_return / 100 / 12
    
    print("\nCompound Growth Projection:")
    print(f"{'Years':<10} | {'Final Value':>15}")
    print("-" * 30)
    
    for years in [5, 10, 20, 30]:
        months = years * 12
        future_value = savings * (((1 + monthly_return) ** months - 1) / monthly_return)
        print(f"{years:<10} | ${future_value:>14,.2f}")

def print_dashboard(income, expenses, savings, total_expenses, savings_rate, category):
    print("\n" + "=" * 50)
    print("PERSONAL FINANCE DASHBOARD")
    print("=" * 50)
    print(f"Date: {datetime.date.today()}")
    print(f"\nMonthly Income:    ${income:,.2f}")
    print(f"\nExpenses:")
    for cat, amount in expenses.items():
        print(f"  {cat:<20} ${amount:,.2f}")
    print(f"\nTotal Expenses:    ${total_expenses:,.2f}")
    print(f"Monthly Savings:   ${savings:,.2f}")
    print(f"Savings Rate:      {savings_rate:.1f}%")
    print(f"Status:            {category}")
    print("=" * 50)

# Main code
income = get_income()
expenses = get_expenses()
savings, total_expenses, savings_rate = calculate_savings(income, expenses)
category = categorize_savings_rate(savings_rate)
while True:
    try:
        annual_return = float(input("\nEnter expected annual return (%): "))
        if annual_return <= 0:
            print("Return must be greater than zero. Try again.")
            continue
        break
    except ValueError:
        print("Invalid input. Please enter a number. Try again.")
project_growth(savings, annual_return)
print_dashboard(income, expenses, savings, total_expenses, savings_rate, category)