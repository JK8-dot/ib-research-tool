import datetime

# Personal Finance Dashboard
# Takes income and expenses as input
# Calculates savings rate, categorizes it, and projects compound growth

income = float(input("Enter your monthly take-home income ($): "))

expenses = {}

print("\nEnter your expense categories and amounts.")
print("Type 'done' when finished.\n")

while True:
    category = input("Enter expense category (or 'done' to finish): ")
    if category.lower() == "done":
        break
    amount = float(input(f"Enter amount for {category}: $"))
    expenses[category] = amount

total_expenses = sum(expenses.values())
savings = income - total_expenses
savings_rate = (savings / income) * 100

if savings_rate < 10:
    category = "Critical — below survival threshold"
elif savings_rate < 20:
    category = "Minimal — reduce expenses or increase income"
elif savings_rate < 35:
    category = "Healthy — on track"
else:
    category = "Strong — wealth-building pace"

annual_return = float(input("\nEnter expected annual return (%): "))
monthly_return = annual_return / 100 / 12

print("\nCompound Growth Projection:")
print(f"{'Years':<10} | {'Final Value':>15}")
print("-" * 30)

for years in [5, 10, 20, 30]:
    months = years * 12
    future_value = savings * (((1 + monthly_return) ** months - 1) / monthly_return)
    print(f"{years:<10} | ${future_value:>14,.2f}")

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