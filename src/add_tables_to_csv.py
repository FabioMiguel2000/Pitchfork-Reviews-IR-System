from tkinter.ttk import Separator
import pandas as pd
import sqlite3
import numpy as np

reviews = pd.read_csv("../assets/reviews.csv")

conn = sqlite3.connect("../assets/database.sqlite")
cursor = conn.cursor()
cursor.execute('SELECT reviewid FROM reviews;')
ids = np.array(cursor.fetchall())
genres = []
years = []
labels = []
contents = []
artists = []

for id in ids[:, 0]:
    cursor.execute(f'SELECT genre FROM genres WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    genres.append( '|'.join(str(x) for x in rows[:,0]))
    cursor.execute(f'SELECT year FROM years WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    years.append( '|'.join(str(x) for x in rows[:,0]))
    cursor.execute(f'SELECT label FROM labels WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    labels.append( '|'.join(str(x) for x in rows[:,0]))
    #cursor.execute(f'SELECT content FROM content WHERE reviewid = {id};')
    #rows = np.array(cursor.fetchall())
    #contents.append( '|'.join(str(x) for x in rows[:,0]))
    cursor.execute(f'SELECT artist FROM artists WHERE reviewid = {id};')
    rows = np.array(cursor.fetchall())
    artists.append( '|'.join(str(x) for x in rows[:,0]))

dfGenres = pd.DataFrame(list(zip(ids[:, 0], genres, years, labels, artists)), columns=['reviewid', 'genre', 'year', 'label', 'artist'])

reviews = pd.merge(reviews, dfGenres, how='inner', on = 'reviewid')
reviews.to_csv('../assets/reviewsCompleteTablesWithoutContents.csv', index = False)

