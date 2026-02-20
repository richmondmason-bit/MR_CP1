import time_handling

def get_file_data(filename):
    """Reads the file and only counts words on lines starting with '>'."""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        full_display = "".join(lines)
        
        # Only count words in lines that start with '>'
        actual_content = [line[1:] for line in lines if line.startswith(">")]
        word_count = len(" ".join(actual_content).split())
        
        return full_display, word_count
    except FileNotFoundError:
        return "[New File]", 0

def update_file(filename, new_entry):
    """Adds a clean header and marks user text with '>' for easy counting."""
    timestamp = time_handling.get_clean_time()
    
    with open(filename, 'a', encoding='utf-8') as f:
        # 1. Add a visual separator
        f.write(f"\n\n--- ENTRY: {timestamp} ---\n")
        # 2. Add the marker '>' so the code knows this is user text
        f.write(f">{new_entry}\n")
        f.write("-" * 30)