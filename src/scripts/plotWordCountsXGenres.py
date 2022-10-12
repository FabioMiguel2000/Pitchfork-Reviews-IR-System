import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_json("../../assets/clean_reviews.json", orient='records')

reviews = np.array(data['review_content'])
wordcounts = np.array([len(r.split(' ')) for r in reviews])
ratings = np.array(data['score'])

genresss = np.array(list(map(str, data['genre'])))

wordcount = wordcounts[wordcounts > 200]
rating = ratings[wordcounts > 200]
genres = genresss[wordcounts > 200]
rating = rating[wordcount < 1500]
genres = genres[wordcount < 1500]
wordcount = wordcount[wordcount < 1500]

count = list(wordcount)
for a in np.flatnonzero(np.core.defchararray.find(genres,'|')!=-1):
    string = genres[a]
    split = np.array(string.split("|"))
    genres = np.concatenate((genres, split))
    for i in split:
        count.append(count[a])
    
counts = np.array(count)
count = np.take(counts, np.flatnonzero(np.core.defchararray.find(genres,'|')==-1))
genress = np.take(genres, np.flatnonzero(np.core.defchararray.find(genres,'|')==-1))
unique = np.unique(genress)
amount = []


for name in unique:
    amount.append(np.average(count[genress == name]))
    
amount = np.array(amount)


df = pd.DataFrame({'Genres':unique, 'Wordcount':amount})
sns.barplot(data = df, y = 'Genres', x = 'Wordcount')
plt.savefig('WordCountXGenres.png')
