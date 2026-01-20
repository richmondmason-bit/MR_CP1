#Mr 1st period dictoniaries notes


person = {
#key:value
"name": "Xavier",
"age": 22,
"job":"Maverik",
"sibling":["alex","katie"]

}

print(f"Name is {person["name"]}")
print(person.keys())
for key in person.keys():
    if key == "sibling":
        for name in person[key]:
            print(f"{person[name]} has a sibling named {name}")
        print(f"{key} is {person[key]}")
    else:
        print(f"{key} is {person[key]}")