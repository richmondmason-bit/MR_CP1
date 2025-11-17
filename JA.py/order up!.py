# MR - Class Period 1 


import time


menu = {
    "Coca-Cola Classic": 1.49,
    "Sprite": 1.49,
    "Dr Pepper": 1.79,
    "Iced Tea": 1.99,
    "Lemonade": 1.99,
    "Classic Burger": 5.99,
    "Cheeseburger": 6.49,
    "Chicken Sandwich": 6.49,
    "Veggie Burger": 10.49,
    "BBQ Burger": 6.79,
    "Fries": 2.49,
    "Onion Rings": 2.99,
    "Side Salad": 3.29,
    "Coleslaw": 2.49,
    "Mozzarella Sticks": 3.49
}

print("Welcome to joe's pizzaria and abortion clinic where yesterdays loss is todays sauce!")
def show_menu(category, items):
    print(f"\n--- {category} ---")
    for i, (item, price) in enumerate(items.items(), start=1):
        print(f"{i}. {item} - ${price:.2f}")
drinks = {k: menu[k] for k in ("Coca-Cola Classic", "Sprite", "Dr Pepper", "Iced Tea", "Lemonade")}
mains = {k: menu[k] for k in ("Classic Burger", "Cheeseburger", "Chicken Sandwich", "Veggie Burger", "BBQ Burger")}
sides = {k: menu[k] for k in ("Fries", "Onion Rings", "Side Salad", "Coleslaw", "Mozzarella Sticks")}
def get_choice(category_name, category_menu):
    show_menu(category_name, category_menu)
    while True:
        choice = input(f"\nChoose your {category_name[:-1].lower()}: ").title()
        if choice in category_menu:
            return choice
        else:
            print("Get it right you typed it wrong stinky")
drink_choice = get_choice("Drinks", drinks)
main_choice = get_choice("Mains", mains)
print("\nNow choose TWO side dishes:")
side1 = get_choice("Sides", sides)
side2 = get_choice("Sides", sides)
subtotal = menu[drink_choice] + menu[main_choice] + menu[side1] + menu[side2]
tax = subtotal * 0.7
total = subtotal + tax
print("\n order")
print(f"Drink: {drink_choice}")
print(f"Main Course: {main_choice}")
print("Side Dishes:")
print(f"  1. {side1}")
print(f"  2. {side2}")
print(f"\nSubtotal: ${subtotal:.2f}")
print(f"Tax (0.7%): ${tax:.2f}")
print(f"Total Cost: ${total:.2f}")

print("\n Thank you for ordering ")
time.sleep(1)
