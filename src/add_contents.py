from tkinter.ttk import Separator
import pandas as pd
import sqlite3
import numpy as np

reviews = pd.read_csv("../assets/reviewsCompleteTablesWithoutContents.csv")

conn = sqlite3.connect("../assets/database.sqlite")
reviews = pd.read_sql('SELECT * FROM reviews;', conn)
print(reviews.head)



