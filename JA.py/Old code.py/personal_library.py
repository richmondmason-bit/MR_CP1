library_books = []
def add_book():
    title = input("Enter book title: ").strip()
    if not title:
        print("Title cannot be empty.")
        return
    author = input("Enter author name: ").strip()
    library_books.append({"title": title, "author": author})
    print("Book added.")
def display_books():
    if not library_books:
        print("Library is empty.")
        return
    for i, book in enumerate(library_books, 1):
        print(f"{i}. {book['title']} by {book['author']}")
def remove_book():
    title = input("Enter title to remove: ").strip().lower()
    for i, book in enumerate(library_books):
        if book["title"].lower() == title:
            removed = library_books.pop(i)
            print(f"Removed: {removed['title']} by {removed['author']}")
            return
    print("Book not found.")
    return

def search_books():
    query = input("Enter search term (title or author): ").strip().lower()
    if not query:
        print("Search term cannot be empty.")
        return
    results = [
        book for book in library_books
        if query in book["title"].lower() or query in book["author"].lower()
    ]
    if not results:
        print("No books found.")
        return
    for i, book in enumerate(results, 1):
        print(f"{i}. {book['title']} by {book['author']}")

def main():
    while True:
        print("\nMenu:")
        print("1. Add book")
        print("2. Display books")
        print("3. Remove book")
        print("4. Search books")
        print("5. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            add_book()
        elif choice == "2":
            display_books()
        elif choice == "3":
            remove_book()
        elif choice == "4":
            search_books()
        elif choice == "5":
            print("Exiting.")
            break
        else:
            print("Invalid option. Please enter 1-5.")
while True:
    main()
