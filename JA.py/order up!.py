import time

# 🧾 MS LAROSE LOOK HERE — order 500 Cigarettes for a secret message!

menu = {
    # 🍔 BURGERS
    "Classic Burger": 5.99,
    "Cheeseburger": 6.49,
    "Bacon Burger": 6.99,
    "Double Burger": 7.99,
    "Veggie Burger": 5.49,
    "BBQ Burger": 6.79,
    "Mushroom Swiss Burger": 7.49,
    "Spicy Jalapeno Burger": 7.29,
    "Avocado Burger": 7.29,
    "Blue Cheese Burger": 7.49,
    "Hawaiian Burger": 7.99,
    "Guacamole Burger": 7.79,
    "Teriyaki Burger": 7.99,
    "Truffle Burger": 8.99,
    "Fried Egg Burger": 7.49,
    "Mac & Cheese Burger": 8.49,
    "Breakfast Burger": 7.29,
    "Vegan Black Bean Burger": 6.49,
    "Impossible Burger": 8.49,

    # 🍗 CHICKEN
    "Chicken Sandwich": 6.49,
    "Spicy Chicken Sandwich": 6.79,
    "Buffalo Chicken Sandwich": 7.29,
    "Chicken Nuggets": 4.99,
    "Chicken Tenders": 5.99,
    "Popcorn Chicken": 4.79,
    "Buffalo Wings": 7.99,
    "Honey BBQ Wings": 8.49,
    "Grilled Chicken Salad": 6.99,
    "Crispy Chicken Wrap": 5.99,
    "Chicken Caesar Wrap": 6.49,
    "Teriyaki Chicken Wrap": 6.79,
    "Spicy Chicken Wrap": 6.79,
    "Korean Fried Chicken": 9.49,
    "Chicken Quesadilla": 6.99,
    "Chicken Burrito": 7.49,
    "Chicken Nachos": 6.49,
    "Chicken Parmesan Sandwich": 7.99,
    "Buffalo Chicken Pizza Slice": 3.49,

    # 🌭 HOTDOGS
    "Classic Hotdog": 3.49,
    "Chili Dog": 4.49,
    "Cheese Dog": 4.29,
    "Bacon-Wrapped Dog": 5.49,
    "Footlong Hotdog": 6.49,
    "Spicy Sausage Dog": 5.99,
    "Chicago-Style Hotdog": 5.99,
    "Coney Island Dog": 5.49,
    "Bratwurst": 6.49,
    "Hotdog Combo (Fries + Drink)": 7.99,

    # 🍕 PIZZA
    "Cheese Pizza": 7.99,
    "Pepperoni Pizza": 8.99,
    "BBQ Chicken Pizza": 9.49,
    "Veggie Pizza": 8.49,
    "Meat Lovers Pizza": 9.99,
    "Hawaiian Pizza": 8.79,
    "Four Cheese Pizza": 9.29,
    "Supreme Pizza": 10.49,
    "Buffalo Chicken Pizza": 9.79,
    "Margherita Pizza": 8.29,
    "Spinach & Feta Pizza": 8.79,
    "Sausage & Mushroom Pizza": 9.29,
    "Pineapple & Ham Pizza": 8.79,
    "BBQ Pulled Pork Pizza": 10.29,
    "Chicken Alfredo Pizza": 9.49,
    "Vegan Pizza": 9.99,
    "Extra Cheese Pizza": 9.29,
    "Deep Dish Pepperoni Pizza": 11.49,

    # 🌮 MEXICAN
    "Taco": 2.49,
    "Soft Taco": 2.79,
    "Beef Taco": 2.99,
    "Chicken Taco": 2.99,
    "Shrimp Taco": 3.49,
    "Burrito": 6.49,
    "Beef Burrito": 6.79,
    "Chicken Burrito": 6.79,
    "Veggie Burrito": 6.29,
    "Quesadilla": 5.99,
    "Cheese Quesadilla": 5.79,
    "Chicken Quesadilla": 6.29,
    "Beef Quesadilla": 6.49,
    "Nachos": 4.99,
    "Loaded Nachos": 6.49,
    "Supreme Nachos": 7.49,
    "Churros": 2.99,
    "Guacamole": 3.49,
    "Salsa & Chips": 2.49,
    "Fajita Wrap": 6.99,
    "Enchiladas": 7.49,
    "Tamales": 6.99,
    "Chimichanga": 7.49,

    # 🍣 JAPANESE
    "Sushi Roll": 7.99,
    "Tempura Shrimp": 6.99,
    "Ramen Bowl": 8.49,
    "Miso Soup": 2.49,
    "Teriyaki Chicken": 8.99,
    "Salmon Sashimi": 9.99,
    "California Roll": 7.49,
    "Spicy Tuna Roll": 7.99,
    "Udon Noodles": 8.29,
    "Nigiri Combo": 9.49,
    "Dragon Roll": 10.49,
    "Philadelphia Roll": 8.49,
    "Rainbow Roll": 10.49,
    "Shrimp Tempura Roll": 9.49,
    "Vegetable Roll": 6.99,
    "Tofu Teriyaki Bowl": 7.99,

    # 🥞 BREAKFAST
    "Pancakes": 4.99,
    "Chocolate Chip Pancakes": 5.49,
    "French Toast": 4.99,
    "Cinnamon French Toast": 5.29,
    "Breakfast Burrito": 5.99,
    "Egg Muffin": 3.99,
    "Omelette": 6.49,
    "Cheese Omelette": 6.79,
    "Avocado Toast": 5.49,
    "Bagel with Cream Cheese": 2.99,
    "Waffles": 5.49,
    "Strawberry Waffles": 5.99,
    "Breakfast Sandwich": 4.49,
    "Hash Brown Plate": 3.49,
    "Croissant": 2.99,
    "Chocolate Croissant": 3.29,
    "Breakfast Platter": 7.99,
    "English Muffin": 2.49,

    # 🍟 SIDES
    "Fries": 2.49,
    "Curly Fries": 2.79,
    "Onion Rings": 2.99,
    "Mozzarella Sticks": 3.49,
    "Loaded Fries": 3.99,
    "Hash Browns": 2.29,
    "Side Salad": 3.29,
    "Coleslaw": 2.49,
    "Sweet Potato Fries": 3.49,
    "Garlic Bread": 2.99,
    "Fried Pickles": 3.49,
    "Potato Wedges": 3.29,
    "Mac & Cheese Bites": 4.49,
    "Cheese Curds": 4.29,
    "Mini Corn Dogs": 3.99,

    # 🍰 DESSERTS & ICE CREAM (Brands + Variations)
    "Oreo Ice Cream Cup": 2.99,
    "Ben & Jerry's Chocolate Fudge Brownie": 4.99,
    "Häagen-Dazs Vanilla": 4.49,
    "Häagen-Dazs Chocolate": 4.49,
    "Magnum Classic": 3.49,
    "Magnum Almond": 3.79,
    "Magnum Double Caramel": 3.99,
    "Breyers Cookies & Cream": 3.99,
    "Breyers Vanilla": 3.49,
    "Nestle Drumstick": 2.49,
    "Ice Cream Sundae": 3.49,
    "Banana Split": 3.99,
    "Chocolate Lava Cake": 4.49,
    "Brownie": 2.49,
    "Apple Pie": 2.99,
    "Cheesecake Slice": 3.99,
    "Donut": 1.49,
    "Cupcake": 2.19,
    "Chocolate Chip Cookie": 1.29,
    "Macaron": 2.49,
    "Fruit Tart": 3.99,
    "Crepe": 4.29,
    "Gelato Cup": 4.49,
    "Gelato Cone": 3.99,
    "Soft Serve Vanilla": 2.99,
    "Soft Serve Chocolate": 2.99,
    "McFlurry Oreo": 3.49,
    "McFlurry M&M's": 3.49,
    "Dairy Queen Blizzard": 4.49,
    "Dairy Queen Reese's Blizzard": 4.99,
    "Frosty Chocolate": 2.99,
    "Frosty Vanilla": 2.99,

    # 🥤 DRINKS (Sodas, Monster, Red Bull, Coffee, Tea, Bubble Tea)
    "Coca-Cola Classic": 1.49,
    "Coca-Cola Zero Sugar": 1.49,
    "Diet Coke": 1.49,
    "Cherry Coke": 1.49,
    "Vanilla Coke": 1.49,
    "Pepsi": 1.49,
    "Diet Pepsi": 1.49,
    "Pepsi Zero Sugar": 1.49,
    "Cherry Pepsi": 1.49,
    "Mountain Dew": 1.49,
    "Mountain Dew Voltage": 1.79,
    "Mountain Dew Baja Blast": 1.79,
    "Mountain Dew Code Red": 1.79,
    "Mountain Dew Live Wire": 1.79,
    "Dr Pepper": 1.79,
    "Diet Dr Pepper": 1.79,
    "Dr Pepper Cherry": 1.79,
    "Dr Pepper Vanilla Float": 1.99,
    "Fanta Orange": 1.49,
    "Fanta Strawberry": 1.49,
    "Fanta Grape": 1.49,
    "Fanta Pineapple": 1.49,
    "Sprite": 1.49,
    "Sprite Zero": 1.49,
    "A&W Root Beer": 1.79,
    "Barq's Root Beer": 1.79,
    "Mug Root Beer": 1.79,
    "Lemonade": 1.99,
    "Pink Lemonade": 1.99,
    "Iced Tea": 1.99,
    "Sweet Tea": 1.99,
    "Peach Iced Tea": 1.99,
    "Coffee": 1.99,
    "Iced Coffee": 2.49,
    "Latte": 3.29,
    "Cappuccino": 3.29,
    "Espresso": 2.49,
    "Americano": 2.49,
    "Hot Chocolate": 2.49,
    "Chai Latte": 3.99,
    "Matcha Latte": 4.29,
    "Monster Energy Original": 3.49,
    "Monster Energy Ultra": 3.49,
    "Monster Energy Ultra Sunrise": 3.49,
    "Monster Energy Ultra Red": 3.49,
    "Monster Energy Ultra White": 3.49,
    "Monster Energy Mango Loco": 3.49,
    "Monster Energy Pipeline Punch": 3.49,
    "Monster Energy Pacific Punch": 3.49,
    "Monster Energy Rehab Lemon Tea": 3.49,
    "Monster Energy Rehab Peach Tea": 3.49,
    "Monster Energy Java Monster": 3.99,
    "Red Bull": 3.49,
    "Red Bull Sugarfree": 3.49,
    "Red Bull Tropical": 3.49,
    "Red Bull Watermelon": 3.49,
    "Bottled Water": 1.29,
    "Sparkling Water": 1.99,
    "Coconut Water": 2.49,
    "Fruit Juice": 2.49,
    "Mango Lassi": 3.49,
    "Milk": 1.49,
    "Chocolate Milk": 1.79,
    "Strawberry Milk": 1.79,
    "Milk Tea": 2.99,
    "Bubble Tea": 3.49,
    "Smoothie Strawberry": 3.49,
    "Smoothie Mango": 3.49,
    "Protein Shake": 4.49,
    "Frappuccino": 3.99,
    "Caramel Macchiato": 4.29,

    # 🚬 SECRET ITEM
    "Cigarette": 2.00
}
print(" WELCOME TO BURGER SHACK ULTRA ")
print("\n--- MENU ---")
for item, price in menu.items():
    print(f"{item}: ${price:.2f}")
order = {}
while True:
    item = input("\nEnter item to order (or 'done' to finish): ").title()
    if item == "Done":
        break
    if item in menu:
        qty = int(input(f"How many {item}s? "))
        order[item] = order.get(item, 0) + qty
        if item == "Cigarette" and qty >= 500:
            print("\n🚬🚬 500 CIGARETTES ALERT 🚬🚬\n")
            for _ in range(20):
                print("🚬 " * 80)
                time.sleep(0.05)
            print("\n You really went all-in on those cigarettes \n")
    else:
        print(" Not on the menu.")
if not order:
    print("No order. Goodbye!")
    exit()

subtotal = sum(menu[i] * q for i, q in order.items())
tax = subtotal * 0.07
tip = float(input("Tip: $") or 0)
total = subtotal + tax + tip

print("\n--- RECEIPT ---")
for i, q in order.items():
    print(f"{i} x{q} = ${menu[i] * q:.2f}")
print(f"\nSubtotal: ${subtotal:.2f}")
print(f"Tax: ${tax:.2f}")
print(f"Tip: ${tip:.2f}")
print(f"Total: ${total:.2f}")
print("\nThank you for ordering at Burger Shack Ultra! 🍔✨")
