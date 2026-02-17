import csv
import os

FIELDS = ["title", "creator", "year", "genre"]

def load_data(path):
    if not os.path.exists(path):
        return [], False
    try:
        with open(path, "r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = [row for row in reader if all(k in row for k in FIELDS)]
        return data, False
    except:
        print("Warning: Could not read file.")
        return [], False

def save_data(path, data):
    try:
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=FIELDS)
            writer.writeheader()
            writer.writerows(data)
        print("Saved.")
        return False
    except:
        print("Error saving to file.")
        return True

def show_list(data, full=False):
    if not data:
        print("Library is empty.")
        return
    for i, item in enumerate(data, 1):
        if full:
            details = " | ".join(f"{k}: {v}" for k, v in item.items())
            print(f"[{i}] {details}")
        else:
            print(f"[{i}] {item['title']} - {item['creator']}")

def add_item(data):
    item = {}
    for f in FIELDS:
        val = ""
        while not val:
            val = input(f"{f.capitalize()}: ").strip()
        item[f] = val
    data.append(item)
    return True

def update_item(data):
    show_list(data)
    try:
        idx = int(input("Item number to update: ")) - 1
        if 0 <= idx < len(data):
            for f in FIELDS:
                new = input(f"New {f} (leave blank to keep '{data[idx][f]}'): ").strip()
                if new:
                    data[idx][f] = new
            return True
        else:
            print("Invalid index.")
    except ValueError:
        print("Enter a number.")
    return False

def delete_item(data):
    show_list(data)
    try:
        idx = int(input("Item number to delete: ")) - 1
        if 0 <= idx < len(data):
            data.pop(idx)
            print("Deleted.")
            return True
    except ValueError:
        print("Invalid input.")
    return False

# Main program flow
file_path = input("File path [library.csv]: ").strip() or "library.csv"
library_data, has_changes = load_data(file_path)

while True:
    print("\n1. List (Simple)\n2. List (Detailed)\n3. Add\n4. Update\n5. Delete\n6. Save\n7. Reload\n8. Exit")
    cmd = input("> ")

    if cmd == "1":
        show_list(library_data, False)
    elif cmd == "2":
        show_list(library_data, True)
    elif cmd == "3":
        if add_item(library_data):
            has_changes = True
    elif cmd == "4":
        if update_item(library_data):
            has_changes = True
    elif cmd == "5":
        if delete_item(library_data):
            has_changes = True
    elif cmd == "6":
        has_changes = save_data(file_path, library_data)
    elif cmd == "7":
        library_data, has_changes = load_data(file_path)
    elif cmd == "8":
        if has_changes:
            if input("Save changes? (y/n): ").lower() == "y":
                save_data(file_path, library_data)
        break
    else:
        print("Try again.")
