from tkinter.ttk import Separator
import pandas as pd
import sqlite3
import numpy as np

conn = sqlite3.connect("../assets/database.sqlite")
reviews = pd.read_sql('SELECT * FROM reviews;', conn)

cursor = conn.cursor()
cursor.execute('SELECT reviewid FROM reviews;')
ids = np.array(cursor.fetchall())
genres = []
years = []
labels = []
artists = []

for id in ids[:, 0]:
    cursor.execute(f'SELECT genre FROM genres WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    genres.append( ','.join(str(x) for x in rows[:,0]))
    cursor.execute(f'SELECT year FROM years WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    years.append( ','.join(str(x) for x in rows[:,0]))
    cursor.execute(f'SELECT label FROM labels WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    labels.append( ','.join(str(x) for x in rows[:,0]))
    cursor.execute(f'SELECT artist FROM artists WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    artists.append( ','.join(str(x) for x in rows[:,0]))

dfGenres = pd.DataFrame(list(zip(ids[:, 0], genres, years, labels, artists)), columns=['reviewid', 'genre', 'year', 'label', 'artist'])
reviews = pd.merge(reviews, dfGenres, how='inner', on = 'reviewid')


cursor.execute('SELECT * FROM content;')
contents = np.array(cursor.fetchall())

dfContents = pd.DataFrame(contents, columns=['reviewid', 'content'])
dfContents['reviewid'] = dfContents['reviewid'].astype(int)

allData = pd.merge(reviews, dfContents, how='inner', on = 'reviewid')
allData.to_json('../assets/reviews.json', orient ='records')
