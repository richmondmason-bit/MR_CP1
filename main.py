import file_handling

def main():
    print("--- Document Log Manager ---")
    
    while True:
        filename = input("\nEnter file name (or 'q' to quit): ").strip()
        if filename.lower() in ('q', 'quit'):
            break

        while True:
            # Get the display text and the 'Clean' word count
            content, count = file_handling.get_file_data(filename)
            
            
            print(f"FILE: {filename} | WORD COUNT: {count}")
          
            print(content)
            
            prompt = "\nType to ADD text (':f' for new file, ':q' to quit): "
            user_input = input(prompt).strip()

            if user_input == ':q':
                return
            if user_input == ':f':
                break

            
            if user_input:
                file_handling.update_file(filename, user_input)
                print("Entry saved!")
            else:
                print("Skipped (empty input).")

if __name__ == "__main__":
    main()