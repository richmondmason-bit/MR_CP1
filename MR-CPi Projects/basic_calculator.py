num1 = float(input("First number"))
num2 = float(input("second number"))

print ("choose between multiplication,division,subtract or add")

print("1 = add")
print("2 = subtract")
print("3 = multiply")
print("4 = divide")

choice = input("Enter choice (1/2/3/4)")

if choice == "1":
    print(f" {num1 + num2}")
elif choice == "2":
    print(f" {num1 - num2}")
elif choice == "3":
    print(f" {num1 * num2}")
elif choice == "4":
    print(f" {num1 / num2}")



