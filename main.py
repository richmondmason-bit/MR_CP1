import file_handling
from datetime import datetime

def main():
    print("Document Manager")
    while True:
        filename = input("\nEnter the CSV file to open (or 'q' to quit): ").strip()
        if filename.lower() in ('q', 'quit', 'exit'):
            print("Exiting.")
            break

        try:
            while True:
                text, count = file_handling.get_file_data(filename)
                print(f"\nCurrent Word Count: {count}")
                print(f"Content:\n{text}\n")

                prompt = ("Enter the new text for the document (leave empty to skip).\n"
                          "Special commands: ':exit' to choose another file, ':quit' to exit program.\n"
                          "Input: ")
                new_content = input(prompt)

                if new_content == ':quit':
                    print("Exiting.")
                    return
                if new_content == ':exit':
                    print(f"Closing file {filename}.")
                    break  # back to file selection

                if new_content:
                    file_handling.update_file(filename, new_content)
                    print(f"Success, file updated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                else:
                    print("No changes made.")

                # Ask whether to continue editing the same file or exit it
                cont = input("\nContinue editing this file? (y to continue / any other to exit file): ").strip().lower()
                if cont not in ('y', 'yes'):
                    print(f"Closing file {filename}.")
                    break

        except FileNotFoundError:
            print("Error: file not found.")
        # Loop will go back to file selection

if __name__ == "__main__":
    main()