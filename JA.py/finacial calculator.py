
def Save_time_calc():
    goal = float(input("goal amount: "))
    deposit = float(input("deposit amount: "))
    def calculate_months():
        return round(goal / deposit)
    MONTHS = calculate_months()
    print(f"it will take {MONTHS} months to save ${goal:.2f}")
def tip_calc():
    bill = float(input("Bill amount: "))
    tip_percent = float(input("Tip percent: "))
    tip = bill * tip_percent / 100
    total = bill + tip
    print(f"Tip: ${tip:.2f}, Total: ${total:.2f}")
def Sale_price_calc():
    original = float(input("Original price: "))
    discount = float(input("Discount (%): "))
    final_price = original * (1 - discount / 100)
    print(f"the item now costs ${final_price:.2f}")
def budget_allocat():
    CATergories = int(input("How many budget categories? "))
    names = []
    percents = []
    for i in range(CATergories):
        names.append(input(f"Category {i+1} name: "))
    income = float(input("Monthly income: "))
    for name in names:
        percents.append(float(input(f"What percent for {name}? ")))
    for i in range(CATergories):
        amount = income * percents[i] / 100
        print(f"{names[i]}: ${amount:.2f}")
def compound_inter_calc():
    principal = float(input("starting amount: "))
    rate = float(input("interest rate: ")) / 100
    years = int(input("how many years? "))
    total = principal * (1 + rate) ** years
    print(f"After{years} years,you will have ${total:.2f}")
while True:
    print("1. Savings Calculator")
    print("2.  tip calculator")
    print("3.sale price calcualtor")
    print("4.copmpound interest calculator")
    print("5.budget allocater")
    print("6. Exit")
    choice = input("choose an option: ")
    if choice == "1":
        Save_time_calc()
    elif choice == "2":
        tip_calc()
    elif choice == "3":
        Sale_price_calc()     
    elif choice == "4":
        compound_inter_calc()
    elif choice =="5":
        budget_allocat()
        break
    else:
        print("Invalid choice")
