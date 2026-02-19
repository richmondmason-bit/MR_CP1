import datetime

def process_file(filename):
    
    with open(filename, 'r') as f:
        content = f.read()
    
   
    words = content.split()
    return content, len(words)

def write_to_file(filename, new_text):
    timestamp = datetime.datetime.now()

    with open(filename, 'w') as f:
        f.write(new_text + "\n\nAdded on: " + timestamp)