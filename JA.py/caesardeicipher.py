alphabet = " abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyz"
get_letter, keyword = 0, []

text = input("Enter the text: ").strip().lower()
key_input = input("Enter the key: ")


if not key_input.isdigit():
    print("Key must be a number between 1 and 26!")
else:
    key = int(key_input)
    if 1 <= key <= 26:
        if len(text) == 0:
            print("Text cannot be empty!")
        else:
            for letter in text:
                if letter in alphabet:
                    get_letter = alphabet.index(letter) + key	
                    keyword.append(alphabet[get_letter])
                else:
                    keyword.append(letter)  
            print("".join(keyword))
    else:
        print("STUPID NICOMPOOP")


   
    