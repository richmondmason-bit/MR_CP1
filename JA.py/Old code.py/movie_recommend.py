import csv
import random

def load_movies(filename='movies list.csv'):
    movies = []
    try:
        with open(filename, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                # skip header if present
                if row[0].strip().lower() == 'title':
                    continue
                # ensure at least 6 columns
                row = (row + [''] * 6)[:6]
                title, director, genre, rating, length, actors = [c.strip() for c in row]
                movies.append({
                    'title': title,
                    'director': director,
                    'genre': genre,
                    'rating': rating,
                    'length': length,
                    'actors': [a.strip() for a in actors.split(',') if a.strip()]
                })
    except FileNotFoundError:
        print(f"File not found: {filename}")
    return movies

def list_movies(movies):
    if not movies:
        print("No movies loaded.")
        return
    for i, m in enumerate(movies, 1):
        print(f"{i}. {m['title']} ({m['genre']}) - {m['length']} min")

def show_movie(m):
    print(f"Title: {m['title']}")
    print(f"Director: {m['director']}")
    print(f"Genre: {m['genre']}")
    print(f"Rating: {m['rating']}")
    print(f"Length: {m['length']} min")
    print("Actors:", ", ".join(m['actors']) if m['actors'] else "N/A")
    print("-" * 30)

def recommend_by_genre(movies, genre):
    return [m for m in movies if genre.lower() in m['genre'].lower()]

def recommend_random(movies, count=3):
    return random.sample(movies, min(count, len(movies)))

def main():
    movies = load_movies()
    if not movies:
        return
    while True:
        print("\nMenu:")
        print("1. List all movies")
        print("2. Recommend by genre")
        print("3. Random recommendations")
        print("4. Show movie details by number")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            list_movies(movies)
        elif choice == "2":
            g = input("Enter genre: ").strip()
            results = recommend_by_genre(movies, g)
            if not results:
                print("No movies found for that genre.")
            else:
                for m in results:
                    show_movie(m)
        elif choice == "3":
            for m in recommend_random(movies, 3):
                show_movie(m)
        elif choice == "4":
            try:
                idx = int(input("Movie number: ").strip())
                show_movie(movies[idx - 1])
            except (ValueError, IndexError):
                print("Invalid number.")
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid option. Enter 1-5.")

if __name__ == "__main__":
    main()
