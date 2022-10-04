import sqlite3
import collections
import json

# Create a SQL connection to our SQLite database

con = sqlite3.connect("../assets/database.sqlite")

cur = con.cursor()


data = cur.execute('SELECT * FROM reviews;')
rows = cur.fetchall()

rowarray_list = []
for row in rows:
    t = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
    rowarray_list.append(t)
j = json.dumps(rowarray_list)


# Convert query to objects of key-value pairs
objects_list = []
count = 0
for row in rows:
    d = collections.OrderedDict()
    d["reviewid"] = row[0]
    d["title"] = row[1]
    d["artist"] = row[2]
    d["url"] = row[3]
    d["score"] = row[4]
    d["best_new_music"] = row[5]
    d["author"] = row[6]
    d["author_type"] = row[7]
    d["author_date"] = row[8]
    objects_list.append(d)
    count += 1
    if(count == 50):
        break



j = json.dumps(objects_list)
with open("../assets/mini_reviews.json", "w") as f:
    f.write(j)

# Be sure to close the connection
con.close()