alphabet = "abcdefghijklmnopqrstuvwxyz"
def shift_letter(letter, key):
    # Keep spaces unchanged
    if letter == " ":
        return " "
 
    if letter in alphabet:
        position = 0
        while position < 26:
            if alphabet[position] == letter:
                break
            position = position + 1

        new_position = (position + key) % 26
        return alphabet[new_position]
    else:
     
        return letter
def caesar_cipher(text, key, mode):
    result = ""

    if mode == "d":
        key = -key

    i = 0
    while i < len(text):
        letter = text[i]
        new_letter = shift_letter(letter, key)
        result = result + new_letter
        i = i + 1

    return result

print(" Simple Caesar Cipher ")
text = input("Enter the text: ").lower()
key_input = input("Enter the key (1-26): ")
mode = input("Type 'e' to encode or 'd' to decode: ").lower()

if not key_input.isdigit():
    print("Key must be a number!")
else:
    key = int(key_input)
    if key < 1 or key > 26:
        print("Key must be between 1 and 26!")
    elif len(text) == 0:
        print("Text cannot be empty!")
    elif mode not in ["e", "d"]:
        print("Mode must be 'e' or 'd'!")
    else:
        result = caesar_cipher(text, key, mode)
        print("Result:", result)



   
    