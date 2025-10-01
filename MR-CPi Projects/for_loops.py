nums = [4,654,136,84,651,86,42,1,564,3,4894]

for num in nums:
    num /= 2
    if num > 100:
        print(f"{num} is only half of {num*2}. it is a large number")
    else:
        print(num)