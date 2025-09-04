name = input("Enter a name: ")
animal = input("Enter an animal: ")
food = input("Enter a type of food: ")
verb = input("Enter a verb: ")
adjective = input("Enter an adjective: ")
print("Don't make the place specific")
place = input("Enter a place: ")

mad_lib = "One day, " + name + " went to the " + place + " and found a " + adjective + " " + animal + ". " \
          "Without thinking, " + name + " decided to " + verb + " with it. Afterwards, they both ate " + food + " and became best friends."

print("\nHere’s your Mad Lib:\n")
print(mad_lib)

