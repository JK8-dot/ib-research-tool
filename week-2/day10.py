import csv
import datetime
import os
import random

# Business Idea Tracker
# Log business ideas with ratings to a CSV file
# View and rank ideas by score

def log_idea():
    print("\n--- Log New Idea ---")
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

    date = datetime.date.today()
    score = round((market_size + personal_edge + ease) / 3, 2)
    
    with open("ideas.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([date, name, problem, customer, revenue, market_size, personal_edge, ease, score])
    
    print(f"\nIdea logged! Score: {score}/5")

def view_ideas():
    if not os.path.exists("ideas.csv"):
        print("\nNo ideas logged yet. Log your first idea!")
        return
    
    with open("ideas.csv", "r") as f:
        reader = csv.reader(f)
        ideas = list(reader)
    
    if len(ideas) == 0:
        print("\nNo ideas logged yet. Log your first idea!")
        return
    
    ideas.sort(key=lambda x: float(x[8]), reverse=True)
    
    print(f"\n{'Rank':<5} | {'Idea':<20} | {'Score':<6} | {'Date':<12}")
    print("-" * 50)
    
    for rank, idea in enumerate(ideas, 1):
        print(f"{rank:<5} | {idea[1]:<20} | {float(idea[8]):<6.2f} | {idea[0]:<12}")
    
    print(f"\nTop Idea: {ideas[0][1]}")
    print(f"Problem:  {ideas[0][2]}")
    print(f"Customer: {ideas[0][3]}")
    print(f"Revenue:  {ideas[0][4]}")

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

# Main menu
print("=" * 40)
print("BUSINESS IDEA TRACKER")
print("=" * 40)

while True:
    print("\n1. Log a new idea")
    print("2. View all ideas")
    print("3. Random idea prompt")
    print("4. Exit")
    
    choice = input("\nSelect an option (1-4): ")
    
    if choice == "1":
        log_idea()
    elif choice == "2":
        view_ideas()
    elif choice == "3":
        random_prompt()
    elif choice == "4":
        print("Goodbye.")
        break
    else:
        print("Invalid option. Please enter 1, 2, 3, or 4.")