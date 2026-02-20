import time_handling

def get_file_data(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Cleaning: split() removes extra whitespace/newlines for an accurate count
    word_count = len(content.split())
    return content, word_count

def update_file(filename, new_text):
    """Overwrites file with new text and adds the word count/timestamp."""
    # Get word count of the NEW text
    count = len(new_text.split())
    timestamp = time_handling.get_time()
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_text)
        f.write(f"\n\n--- Document Stats ---")
        f.write(f"\nWord Count: {count}")
        f.write(f"\nLast Updated: {timestamp}")