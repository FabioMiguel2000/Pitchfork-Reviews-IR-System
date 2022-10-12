import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_json("../../assets/clean_reviews.json", orient='records')

genres = np.array(list(map(str, data['genre'])))
for a in np.flatnonzero(np.core.defchararray.find(genres,'|')!=-1):
    string = genres[a]
    split = np.array(string.split("|"))
    genres = np.concatenate((genres, split))
    
genress = np.take(genres, np.flatnonzero(np.core.defchararray.find(genres,'|')==-1))
unique = np.unique(genress)
amount = []
for name in unique:
    amount.append(np.count_nonzero(genress == name))
    
amount = np.array(amount)

df = pd.DataFrame({'Genres':unique, 'Number of reviews':amount})
sns.barplot(data = df, y = 'Genres', x = 'Number of reviews')
plt.savefig('Genres.png')