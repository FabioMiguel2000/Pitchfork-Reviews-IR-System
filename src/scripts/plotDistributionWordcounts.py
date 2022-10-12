import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_json("../../assets/clean_reviews.json", orient='records')

reviews = np.array(data['review_content'])
wordcounts = np.array([len(r.split(' ')) for r in reviews])
ratings = np.array(data['score'])
genresss = np.array(list(map(str, data['genre'])))

sns.kdeplot(wordcounts)
plt.xlabel("Wordcount")
plt.savefig("distributionWordCounts.png")

