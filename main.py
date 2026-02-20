import file_handling

def main():
    print("Document Manager")
    
    filename = input("Enter the file")
    
    try:
        text, count = file_handling.get_file_data(filename)
        print(f"\nCurrent Word Count: {count}")
        print(f"Content:\n{text}\n")
        
        new_content = input("Enter the new text for the document: ")
        
        file_handling.update_file(filename, new_content)
        print("\nSuccess, file updated")
        
    except FileNotFoundError:
        print("Error,It dont exist pluh")

main()