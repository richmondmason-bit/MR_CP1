import file_handling

def start():
    
    name = input("Enter file name (e.g. data.txt): ")
    
   
    text, count = file_handling.process_file(name)
    print(f"Word Count: {count}")
    print(f"Current Text: {text}")
    
    
    update = input("\nType new text to overwrite the file: ")
    file_handling.write_to_file(name, update)
    print("Done! File updated with a timestamp.")

start()