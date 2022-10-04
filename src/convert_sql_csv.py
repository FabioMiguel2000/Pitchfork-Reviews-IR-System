import csv
import sqlite3

conn = sqlite3.connect("../assets/database.sqlite")
cursor = conn.cursor()
cursor.execute('SELECT * FROM reviews;')
with open("../assets/reviews.csv", 'w',newline='') as csv_file: 
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow([i[0] for i in cursor.description]) 
    csv_writer.writerows(cursor)
conn.close()