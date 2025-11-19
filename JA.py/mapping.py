numbers = [123,234,345,456,567,678,789,890]
new_nums = []
for number in numbers:
    new_nums.append(number/3)

print(new_nums)

def divide(num):
    return num/3

new_nums = map(divide, numbers)
print(new_nums)

for num in new_nums:
    print(num)
    new_nums = map(lambda num: num/3,numbers )