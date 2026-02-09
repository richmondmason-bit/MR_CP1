import csv
import os
import sys

FILENAME = "Movies list - Sheet1 (1) (1).csv"

def load_data(filename):
    """Loads CSV and normalizes data into a list of dictionaries."""
    movies = []
    
    if not os.path.exists(filename):
        print(f"[Error] File '{filename}' not found.")
        print("Please make sure the CSV file is in the same folder as this script.")
        return []

    try:
        with open(filename, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    title = row.get('Title', '').strip()
                    director = row.get('Director', '').strip()
                    rating = row.get('Rating', '').strip()
                    
                   
                    genres = [g.strip().lower() for g in row.get('Genre', '').split('/') if g.strip()]
                    
                   
                    actors = [a.strip().lower() for a in row.get('Notable Actors', '').split(',') if a.strip()]
                    
                    try:
                        length = int(row.get('Length (min)', 0))
                    except ValueError:
                        length = 0

                    if title:
                        movies.append({
                            'title': title,
                            'director': director,
                            'genres': genres,
                            'actors': actors,
                            'length': length,
                            'rating': rating,
                           
                            'display_genre': row.get('Genre', ''),
                            'display_actors': row.get('Notable Actors', '')
                        })
                except Exception:
                    continue 
    except Exception as e:
        print(f"Error reading file: {e}")
        return []
        
    return movies


def filter_genre(movies, term):
    term = term.lower().strip()
    return [m for m in movies if any(term in g for g in m['genres'])]

def filter_director(movies, term):
    term = term.lower().strip()
    return [m for m in movies if term in m['director'].lower()]

def filter_actor(movies, term):
    term = term.lower().strip()
    return [m for m in movies if any(term in a for a in m['actors'])]

def filter_length(movies, min_len=None, max_len=None):
    results = []
    for m in movies:
        if m['length'] == 0: continue
        if min_len is not None and m['length'] < min_len: continue
        if max_len is not None and m['length'] > max_len: continue
        results.append(m)
    return results


def get_recommendations(movies, filters):
    """Applies all active filters using AND logic."""
    results = movies
    
    if 'genre' in filters:
        results = filter_genre(results, filters['genre'])
    
    if 'director' in filters:
        results = filter_director(results, filters['director'])
        
    if 'actor' in filters:
        results = filter_actor(results, filters['actor'])
        
    if 'min_len' in filters or 'max_len' in filters:
        results = filter_length(results, filters.get('min_len'), filters.get('max_len'))
        
    return results



def print_full_list(movies):
    if not movies:
        print("No movies to display.")
        return
    print(f"\n FULL MOVIE LIST ({len(movies)}) ---")
    print(f"{'TITLE':<35} | {'DIRECTOR':<20} | {'LEN'}")
    
    for m in movies:
        print(f"{m['title'][:33]:<35} | {m['director'][:18]:<20} | {m['length']}")


def pretty_print_results(movies):
    if not movies:
        print("\n[!] No movies match those filters.")
        return

    print(f"\n RESULTS: {len(movies)} MOVIE(S) FOUND")
    for m in movies:
        print(f"Title:    {m['title']}")
        print(f"Director: {m['director']}")
        print(f"Genres:   {m['display_genre']}")
        print(f"Actors:   {m['display_actors']}")
        print(f"Length:   {m['length']} min")
        print("-" * 40)

def get_int(prompt):
    val = input(prompt).strip()
    if not val: return None
    try:
        return int(val)
    except ValueError:
        return None

def main():
    all_movies = load_data(FILENAME)
    
    if not all_movies:
        print("Exiting because file could not be loaded.")
        return

    while True:
        print("\n")
        print("1. Search / Get Recommendations")
        print("2. Print Full Movie List")
        print("3. Exit")
        
        choice = input("Type the number for the action: ").strip()
        
        if choice == '1':
            filters = {}
            print("\n--- CHOOSE FILTERS ---")
            print("Enter numbers separated by commas (e.g. 1,3):")
            print("1. Genre")
            print("2. Director")
            print("3. Actor")
            print("4. Length (min/max)")
            
            selection = input("Selection: ").strip()
            
            if '1' in selection:
                filters['genre'] = input("Enter genre (e.g. 'Sci-Fi'): ")
            if '2' in selection:
                filters['director'] = input("Enter director: ")
            if '3' in selection:
                filters['actor'] = input("Enter actor: ")
            if '4' in selection:
                filters['min_len'] = get_int("Enter minimum length (or blank): ")
                filters['max_len'] = get_int("Enter maximum length (or blank): ")
            
            print("\nSearching...")
            results = get_recommendations(all_movies, filters)
            pretty_print_results(results)
            
        elif choice == '2':
            print_full_list(all_movies)
            
        elif choice == '3':
            print("Goodbye.")
            break
        else:
            print("Invalid choice.")


main()