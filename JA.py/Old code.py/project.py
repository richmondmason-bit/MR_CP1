# FL class Shopping List Manager

# Initialize your shopping list variable
shopping_list = []

while True:
    print("\nWhat do you want to do with your shopping list?")
    print("1 = Add item")
    print("2 = Remove item")
    print("3 = Show list")
    print("4 = Quit")

    choice = input("Enter choice (1/2/3/4): ")

    if choice == "4":
        print("Goodbye!")
        break
    elif choice not in ["1", "2", "3"]:
        print("Invalid choice, try again.")
        continue

    elif choice == "1":
        item = input("Enter item to add: ")
        shopping_list.append(item)
        print(f"'{item}' added to the list.")

    elif choice == "2":
        item = input("Enter item to remove: ")
        if item in shopping_list:
            shopping_list.remove(item)
            print(f"'{item}' removed from the list.")
        else:
            print(f"'{item}' not found in the list.")

    elif choice == "3":
        if shopping_list:
            print("\nYour shopping list:")
            for i, item in enumerate(shopping_list, start=1):
                print(f"{i}. {item}")
        else:
            print("Your shopping list is empty.")



        




 


    
        




 


    
