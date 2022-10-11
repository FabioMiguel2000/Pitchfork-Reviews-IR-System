import pandas as pd

import json

df = pd.read_json('reviews.json', orient='records')

df.drop(['artist_y', 'best_new_music', 'author_type', 'pub_weekday', 'pub_day', 'pub_month', 'pub_year', 'url'], inplace=True, axis=1)

df = df.rename(columns={"pub_date": "review_publication_date", "year": "song_release_year", "label": "record_label", "content":"review_content", "artist_x": "artist"})

df['review_publication_date'] = pd.to_datetime(df['review_publication_date'], format='%Y-%m-%d')

df.loc[df['review_content'] != ''] 

data = df.to_json('clean_reviews.json', orient='records')