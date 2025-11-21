# first factorial program

#print instructions 
# ask the user to enter a whole number less than 11
#list = [1,2,3,4,5,6,7,8,9,10]
#user(input) # ask for number
#if input less than 10:
    #print that the input works 
#if input more than 10: print error 
    #then returns to input 
#if input != list():
    #return 
#for list in input:
    #math.factorial(number)
# print(f"original:input factorial:math.factorial(number))

import math

print("Welcome to factorial calculator")
print("please enter a whole number thats 1-10")
try:
    user_number = int(input("Please enter an integer: "))
except ValueError:
    print("Invalid input. Please enter a whole number.")
print(f"Orginal:{print(user_number)}New Number:{math.factorial(user_number)}")