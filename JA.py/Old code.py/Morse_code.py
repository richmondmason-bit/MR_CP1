# PSEUDOCODE
# store english letters and morse code symbols
# create function to change english into morse
# create function to change morse into english
# keep showing menu until user chooses to exit
# get user input and translate based on choice


english_chars = (
    'a','b','c','d','e','f','g','h','i','j','k','l','m',
    'n','o','p','q','r','s','t','u','v','w','x','y','z',
    '0','1','2','3','4','5','6','7','8','9',' '
)

morse_chars = (
    '.-','-...','-.-.','-..','.','..-.','--.','....','..',
    '.---','-.-','.-..','--','-.','---','.--.','--.-','.-.',
    '...','-','..-','...-','.--','-..-','-.--','--..',
    '-----','.----','..---','...--','....-','.....',
    '-....','--...','---..','----.','/'
)


def english_to_morse(message):
    message = message.lower()
    translated = ""

    for char in message:
        if char in english_chars:
            index = english_chars.index(char)
            translated += morse_chars[index] + " "
        else:
            translated += "? "

    return translated.strip()


def morse_to_english(message):
    translated = ""
    morse_letters = message.split(" ")

    for symbol in morse_letters:
        if symbol in morse_chars:
            index = morse_chars.index(symbol)
            translated += english_chars[index]
        else:
            translated += "?"

    return translated


def main():
    print("\nWelcome to the Morse Code Translator!")
    print("Translate between English and Morse Code.\n")

    while True:
        print("\nMAIN MENU:")
        print("1. Translate from Morse Code to English")
        print("2. Translate from English to Morse Code")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == "1":
            print("\nMORSE CODE TO ENGLISH:")
            morse_message = input("What is the code you need translated?\n\n")
            result = morse_to_english(morse_message)
            print("\nYour message says:\n")
            print(result)

        elif choice == "2":
            print("\nENGLISH TO MORSE CODE:")
            english_message = input("What is the message you need translated?\n\n")
            result = english_to_morse(english_message)
            print("\nYour message says:\n")
            print(result)

        elif choice == "3":
            print("\nThank you for using the Morse Code Translator. Goodbye!")
            break

        else:
            print("\nInvalid choice. Please select 1, 2, or 3.")
while True:
    main()
