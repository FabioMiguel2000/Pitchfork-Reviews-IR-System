import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_json("../../assets/clean_reviews.json", orient='records')


reviews = np.array(data['review_content'])
wordcounts = np.array([len(r.split(' ')) for r in reviews])
ratings = np.array(data['score'])

wordcount = wordcounts[wordcounts > 200]
rating = ratings[wordcounts > 200]
rating = rating[wordcount < 1500]
wordcount = wordcount[wordcount < 1500]


scores = np.round(wordcount.astype(int)/200)*200
unique = np.unique(scores)
amount = [np.count_nonzero(wordcounts <= 200)]
r = [np.average(ratings[wordcounts <= 200])]
for i in unique:
    amount.append(np.count_nonzero(scores == i))
    r.append(np.average(rating[scores == i]))


amount.append(np.count_nonzero(wordcounts >= 1500))
r.append(np.average(ratings[wordcounts >= 1500]))
amount = np.array(amount)
unique = np.concatenate((np.array([0.0]), unique))
unique = np.concatenate((unique, np.array([">1500.0"])))

df = pd.DataFrame({'Wordcount':unique, 'y':amount, 'Score':r })
sns.barplot(data = df, x = 'Wordcount', y = 'Score')

plt.savefig("WordCountsXScore.png")