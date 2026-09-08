# Compound Intrest Calculator
# Asks for principal, rate, and years
# Outputs a year-by-year growth table and final summary

principal = float(input("Enter your starting principal ($): "))
rate = float(input("Enter your annual intrest rate (%): "))
years = int(input("Enter number of years: "))
rate = rate/100

print(f"\nYear | Starting Balance | Interest Earned | Ending Balance")
print("-" * 60)

balance = principal
for year in range(1, years+1):
    starting_balance = balance
    interest_earned = balance * rate
    balance = balance + interest_earned
    print(f"{year:<5} | ${starting_balance:>15,.2f} | ${interest_earned:>14,.2f} | ${balance:>14,.2f}")
          
total_interest = balance - principal
rule_of_72 = 72 / (rate * 100)

print("-" * 60)
print(f"\nFinal Summary:")
print(f"Starting Principal:  ${principal:,.2f}")
print(f"Final Value:         ${balance:,.2f}")
print(f"Total Interest:      ${total_interest:,.2f}")
print(f"Years to double:     {rule_of_72:.1f} years (Rule of 72)")