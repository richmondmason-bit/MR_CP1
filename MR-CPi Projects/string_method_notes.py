#string_method

subject = "Computer Programming 1!"

#print(subject.upper().center(100))

#color = input("What is your favorite color?").strip().lower()
#print("That is cool. i like" + color + "Too")

#Stupid/idiot Proofing Inputs

#color = input("What is your favorite color?").strip().lower()
#print("That is cool. i like" + color + "Too")

word = "jumps"
sentence = "The quick brown fox jumps over the lazy dog"
length = len("lazy")
print(sentence[start:start+length])
start = sentence.index(word)
print(sentence.find(word))