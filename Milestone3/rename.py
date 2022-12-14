import pandas as pd

df = pd.read_json('reviews_CleanContent_with_CleanKeywords.json', orient='records')

df = df.rename(columns={"score": "rating_score"} )

df.to_json('reviews_CleanContent_with_CleanKeywords.json', orient='records')