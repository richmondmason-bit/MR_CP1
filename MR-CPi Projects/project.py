# FL class Shopping List Manager

#Put your shopping list variable here

while True:
    print("\nWhat do you want in your shopping list?")
    print("1 = add")
    print("2 = remove")
    print("3 = select")
    print("4 = quit")

    choice = input("Enter choice (1/2/3/4): ")

    if choice == "4":
        print("Goodbye!")
        break
    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice, try again.")
        continue
    elif choice == 1:
        task = input("Enter task to add")
        choice.append(task)
        print("task added")
    elif choice == 2:
        task = input("Enter to remove task")
        if task in choice


        




 


    
