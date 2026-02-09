import csv

with open("notes_firest/sampe.csv", 'a', newline='') as csvfile:
    fieldnames = ['username', 'color']
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writerow({'username':'aUser','color':'pink'})
    