import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
data = pd.read_json("../../assets/clean_reviews.json", orient='records')

scores = np.round(np.array(data['score']))

amount = []
for i in range(11):
    amount.append(np.count_nonzero(scores == i))

ide = np.array([i for i in range(11)])

df = pd.DataFrame({'Score':ide, 'Number of reviews':amount})
sns.barplot(data = df, x = 'Score', y = 'Number of reviews')
plt.savefig("Scores.png")