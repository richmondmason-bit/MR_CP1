while True:
    print("\nChoose between multiplication, division, subtract or add")
    print("1 = add")
    print("2 = subtract")
    print("3 = multiply")
    print("4 = divide")
    print("q = quit")

    choice = input("Enter choice (1/2/3/4/q): ")

    if choice == "q":
        print("Goodbye!")
        break

    # make sure choice is valid before asking numbers
    if choice not in ["1", "2", "3", "4"]:
        print("Invalid choice, try again.")
        continue

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice == "1":
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
    elif choice == "2":
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
    elif choice == "3":
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
    elif choice == "4":
        if num2 == 0:
            print("Error: Cannot divide by zero")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
