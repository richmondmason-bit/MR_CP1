# MR 
import statistics
def flexible_calculator(*args, operation="sum"):
    if len(args) == 0:
        return "Error: No numbers provided."
    if operation == "sum":
        return sum(args)
    elif operation == "average":
        return statistics.mean(args)
    elif operation == "max":
        return max(args)
    elif operation == "min":
        return min(args)
    elif operation == "product":
        product = 1
        for num in args:
            product *= num
        return product
    else:
        return "Error: Unknown operation."
def get_numbers_from_user():
    numbers = []
    print("\nEnter numbers (type 'done' when finished):")
    while True:
        user_input = input("Number: ")
        if user_input.lower() == "done":
            break
        try:
            number = float(user_input)
            numbers.append(number)
        except ValueError:
            print("Please enter a valid number or 'done'.")
    return numbers
def main():
    print("Welcome to the Flexible Calculator!")
    while True:
        operation = input("\nWhich operation would you like to perform? ").lower()
        numbers = get_numbers_from_user()
        print(f"\nCalculating {operation} of: {', '.join(str(n) for n in numbers)}")
        result = flexible_calculator(*numbers, operation=operation)
        print("Result:", result)
        again = input("\nWould you like to perform another calculation? (yes/no) ").lower()
        if again != "yes":
            break
    print("\nThank you for using the Flexible Calculator!")
main()
