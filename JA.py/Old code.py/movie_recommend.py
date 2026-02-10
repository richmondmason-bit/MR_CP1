import csv
import os

FILE_NAME = "Movies list - Sheet1 (1) (1).csv"

def normalize(text):
    if text is None:
        return ""
    return text.strip().lower()

def parse_movies():
    movies = []

    if not os.path.exists(FILE_NAME):
        print("Movie file not found.")
        return movies

    with open(FILE_NAME, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            try:
                title = row.get("title", "").strip()
                year = row.get("year", "").strip()

                genres_raw = row.get("genres", "")
                genres = []
                for g in genres_raw.split("|"):
                    g = g.strip().lower()
                    if g:
                        genres.append(g)

                director = normalize(row.get("director", ""))

                actors_raw = row.get("actors", "")
                actors = []
                for a in actors_raw.split("|"):
                    a = a.strip().lower()
                    if a:
                        actors.append(a)

                length_text = row.get("length", "")
                if length_text.isdigit():
                    length = int(length_text)
                else:
                    length = None

                movie = {
                    "title": title,
                    "year": year,
                    "genres": genres,
                    "director": director,
                    "actors": actors,
                    "length": length
                }

                movies.append(movie)

            except:
                continue

    return movies

def filter_by_genre(movies, genre):
    genre = normalize(genre)
    results = []

    for movie in movies:
        for g in movie["genres"]:
            if genre in g:
                results.append(movie)
                break

    return results

def filter_by_director(movies, director):
    director = normalize(director)
    results = []

    for movie in movies:
        if director in movie["director"]:
            results.append(movie)

    return results

def filter_by_actor(movies, actor):
    actor = normalize(actor)
    results = []

    for movie in movies:
        for a in movie["actors"]:
            if actor in a:
                results.append(movie)
                break

    return results

def filter_by_length(movies, min_len, max_len):
    results = []

    for movie in movies:
        length = movie["length"]

        if length is None:
            continue

        if min_len is not None and length < min_len:
            continue

        if max_len is not None and length > max_len:
            continue

        results.append(movie)

    return results

def apply_filters(movies, filters):
    results = movies

    for f in filters:
        results = f(results)

    return results

def print_movie(movie, number=None):
    if number:
        prefix = str(number) + ". "
    else:
        prefix = ""

    print(
        prefix +
        'Title: "' + movie["title"] + '" — Year: ' + movie["year"] +
        ' — Genres: ' + "|".join(movie["genres"]) +
        ' — Director: ' + movie["director"] +
        ' — Actors: ' + ", ".join(movie["actors"]) +
        ' — Length: ' + str(movie["length"]) + ' min'
    )

def print_results(movies):
    if len(movies) == 0:
        print("\nNo movies match those filters.")
        print("Try removing one filter or widening the length range.\n")
        return

    for i in range(len(movies)):
        print_movie(movies[i], i + 1)

def print_all_movies(movies):
    for i in range(len(movies)):
        print_movie(movies[i], i + 1)

def search_menu(movies):
    print("\nChoose filters to apply (comma separated):")
    print("1 Genre")
    print("2 Director")
    print("3 Actor")
    print("4 Length")

    selected = input("Selected filters: ").split(",")

    filters = []

    if "1" in selected:
        genre = input("Enter genre: ")
        def g_filter(m):
            return filter_by_genre(m, genre)
        filters.append(g_filter)

    if "2" in selected:
        director = input("Enter director: ")
        def d_filter(m):
            return filter_by_director(m, director)
        filters.append(d_filter)

    if "3" in selected:
        actor = input("Enter actor: ")
        def a_filter(m):
            return filter_by_actor(m, actor)
        filters.append(a_filter)

    if "4" in selected:
        min_text = input("Enter minimum length (blank for none): ")
        max_text = input("Enter maximum length (blank for none): ")

        if min_text.isdigit():
            min_len = int(min_text)
        else:
            min_len = None

        if max_text.isdigit():
            max_len = int(max_text)
        else:
            max_len = None

        def l_filter(m):
            return filter_by_length(m, min_len, max_len)
        filters.append(l_filter)

    results = apply_filters(movies, filters)

    print("\nResults:\n")
    print_results(results)

def main():
    print("Movie Search Program")
    print("Search movies by genre, director, actor, and length.")
    print("The program runs until you choose to exit.\n")

    movies = parse_movies()

    while True:
        print("\nMAIN MENU")
        print("1 Search / Get Recommendations")
        print("2 Print Full Movie List")
        print("3 Exit")

        choice = input("Type the number for the action you would like to perform: ")

        if choice == "1":
            search_menu(movies)

        elif choice == "2":
            print_all_movies(movies)

        elif choice == "3":
            print("Goodbye.")
            break

        else:
            print("Invalid input.")

main()
