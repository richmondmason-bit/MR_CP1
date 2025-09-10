import random

# List of stats
stats = ["Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

# Generate 7 sets of random stats
for i in range(1, 8):
    print(f"\nCharacter {i}'s stats:")
    for stat in stats:
        value = random.randint(1, 20)
        print(f"{stat}: {value}")

