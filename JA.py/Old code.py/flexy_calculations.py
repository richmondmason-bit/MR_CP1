
# - define apply_round(value, **kwargs):
#     - get "round" from kwargs
#     - if provided, return rounded value to that many decimals, else return value
# - define sum_numbers(*nums, **kwargs): return apply_round(sum(nums), **kwargs)
# - define avg_numbers(*nums, **kwargs): return apply_round(sum(nums)/len(nums), **kwargs) if any nums else None
# - define max_number(*nums, **kwargs): return apply_round(max(nums), **kwargs) if any nums else None
# - define min_number(*nums, **kwargs): return apply_round(min(nums), **kwargs) if any nums else None
# - define prod_numbers(*nums, **kwargs): multiply all nums and return apply_round(product, **kwargs)
# - build OPS mapping of operation names to functions
# - print welcome and list available operations
# - loop:
#     - ask user which operation; normalize and validate against OPS
#     - if invalid, notify and continue loop
#     - collect numbers from user until 'done', parsing floats and handling invalid input
#     - if no numbers entered, notify and continue loop
#     - ask for rounding decimals (optional), validate integer input if provided
#     - call selected operation with numbers and rounding kwargs
#     - print result
#     - ask if user wants to run again; break loop unless user answers "yes"

def apply_round(value, **kwargs):
    r = kwargs.get("round")
    return round(value, int(r)) if r is not None else value
def sum_numbers(*nums, **kwargs):
    return apply_round(sum(nums), **kwargs)
def avg_numbers(*nums, **kwargs):
    return apply_round(sum(nums)/len(nums), **kwargs) if nums else None
def max_number(*nums, **kwargs):
    return apply_round(max(nums), **kwargs) if nums else None
def min_number(*nums, **kwargs):
    return apply_round(min(nums), **kwargs) if nums else None
def prod_numbers(*nums, **kwargs):
    p = 1
    for n in nums: p *= n
    return apply_round(p, **kwargs)
OPS = {
    "sum": sum_numbers,
    "average": avg_numbers,
    "max": max_number,
    "min": min_number,
    "product": prod_numbers,
}
print("Welcome to the flexy calculations!!!\n")
print("Available flexy operations:", ", ".join(OPS.keys()))
while True:
    op = input("\nWhich flexy calculation do you want to calculate? ").strip().lower()
    if op not in OPS:
        print("Hey dummy type it right ")
        continue
    nums = []
    print("\nEnter numbers (type 'done' when finished):")
    while True:
        n = input("Number: ").strip()
        if n.lower() == "done":
            break
        try:
            nums.append(float(n))
        except ValueError:
            print("STUPID")
    if not nums:
        print("Put numbers in you dummy")
        continue
    print(f"\nCalculating {op} of: {', '.join(map(str, nums))}")
    dec = input("Round decimals? (leave blank for none): ").strip()
    kwargs = {}
    if dec:
        try: kwargs["round"] = int(dec)
        except ValueError: print("Invalid round value; ignoring")
    result = OPS[op](*nums, **kwargs)
    print(f"Result: {result}\n")
    again = input("You wanna do the flexy calcualtions again? ").strip().lower()
    if again != "yes":
        print("Goodbye hope I flexy calculated you!")
        break


#MS LAROSe you must be proud of me because this one time I did pseudocode 
