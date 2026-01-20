#Create a list of numbers with at least 20 values.
# Use the map() function to square each value in the list.
# Convert the map object into a list of squared numbers.
# Loop through the numbers using an index.
# For each index:
#Get the original number from the numbers list.
#Get the squared number from the squared list.
#Print both values in a readable format.

numbers = [3, 7, 12, 25, 30, 45, 50, 65, 70, 85,
           90, 105, 110, 125, 130, 145, 150, 165,
           170, 185, 190, 205, 210, 225, 230, 245,
           250, 265, 270, 285]

squared_numbers = list(map(lambda x: x ** 2, numbers))

for i in range(len(numbers)):
    print(f"Original: {numbers[i]}, Squared: {squared_numbers[i]}")