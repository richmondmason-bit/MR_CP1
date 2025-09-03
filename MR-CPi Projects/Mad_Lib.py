import random


name = input("Enter a name: ")
animal = input("Enter an animal: ")
food = input("Enter a type of food: ")
verb = input("Enter a verb: ")
adjective = input("Enter an adjective: ")
print("Dont make the place specific")
place = input("Enter a place: ")


stories = [
    f"One day, {name} went to the {place} and found a {adjective} {animal}. "
    f"Without thinking, {name} decided to {verb} with it. Afterwards, they both ate {food} and became best friends.",

    f"In the middle of the {place}, a {adjective} {animal} stole {name}'s {food}. "
    f"To get it back, {name} had to {verb} faster than ever before!",

    f"{name} was having a normal day until a {adjective} {animal} appeared at the {place}. "
    f"It asked for {food} politely, but {name} just wanted to {verb} instead."]


mad_lib = random.choice(stories)
print(mad_lib)
