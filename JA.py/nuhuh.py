# compliment_generator_weird.py
import random
import json
import os

# --- Absurd and Silly Adjectives ---
ADJECTIVES = [
    "fluffy", "crispy", "soggy", "chaotic", "sparkly", "unreasonably round",
    "mildly confused", "deliciously awkward", "existential", "derpy",
    "ferociously polite", "slightly radioactive", "emotionally stable",
    "overcaffeinated", "suspiciously smooth", "musically gifted", "arguably moist",
    "dramatic", "hauntingly fabulous", "confusedly majestic", "extra toasty",
    "dangerously glittery", "uncomfortably enthusiastic", "hyperactive",
    "aesthetically wobbly", "loudly invisible", "thoroughly bewildered",
    "surprisingly crunchy", "cosmically tired", "ethically sparkly",
    "socially exhausted", "questionably sentient", "vibrationally chaotic",
    "spiritually bouncy", "digitally moist", "heroically bland", "mysteriously sticky",
    "philosophically spicy", "overly dramatic", "weirdly confident"
]

# --- Ridiculous and Random Nouns ---
NOUNS = [
    "toaster", "spaghetti tornado", "penguin overlord", "potato waffle",
    "bagel wizard", "enchanted burrito", "keyboard gremlin", "rubber duck army",
    "glitter bomb", "banana whisperer", "muffin knight", "sock monster",
    "emotional cactus", "space llama", "taco crusader", "marshmallow samurai",
    "quantum donut", "friendly ghost", "cosmic pancake", "bubble philosopher",
    "chair goblin", "jellybean prophet", "pickle bard", "snack dragon",
    "sandwich sorcerer", "moon hamster", "celestial noodle", "dramatic walrus",
    "enchanted onion", "wizard toaster", "interdimensional raccoon",
    "mystical beanbag", "psychic potato", "dancing mushroom", "sentient pretzel",
    "galactic otter", "haunted waffle", "hyper banana", "sarcastic burrito",
    "frog diplomat", "tech-support unicorn", "invisible crab", "angsty eggplant",
    "philosopher donut", "robot frog", "vampire bagel", "musical trash panda",
    "emotional pizza", "overthinking cupcake"
]

# --- Favorites file ---
FAVS_FILE = "weird_compliment_favorites.json"


def make_compliment():
    """Generate a random weird compliment."""
    adj = random.choice(ADJECTIVES)
    noun = random.choice(NOUNS)
    return f"You are a {adj} {noun}!"


def load_favorites():
    if os.path.exists(FAVS_FILE):
        with open(FAVS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_favorites(favs):
    with open(FAVS_FILE, "w", encoding="utf-8") as f:
        json.dump(favs, f, ensure_ascii=False, indent=2)


def main():
    print("💫 Weird Compliment Generator 💫")
    print("Press [Enter] for a new compliment, 'f' to favorite, 'v' to view favorites, 'q' to quit.")

    favorites = load_favorites()
    last = None

    while True:
        cmd = input("\nCommand: ").strip().lower()

        if cmd == "q":
            print("\n👋 Farewell, you magnificent bagel wizard!\n")
            break

        elif cmd == "f":
            if last:
                favorites.append(last)
                save_favorites(favorites)
                print("❤️ Favorited that nonsense!")
            else:
                print("You haven’t generated any weirdness yet!")

        elif cmd == "v":
            if favorites:
                print("\n🌈 Your Favorite Weird Compliments 🌈")
                for i, c in enumerate(favorites, 1):
                    print(f"{i}. {c}")
            else:
                print("No favorites yet! Go make something weird!")

        else:  # generate new compliment
            last = make_compliment()
            print("\n✨ " + last)


if __name__ == "__main__":
    main()
