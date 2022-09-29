from bs4 import BeautifulSoup
import json
import bs4
import requests

f = open('../assets/reviews.json')

dataset = json.load(f)

for review in dataset:
    result = requests.get(review['url'])

    doc = BeautifulSoup(result.text, "html.parser")

    review_content = doc.find("div", {"class": "body__inner-container"})

    for child in review_content:
        if isinstance(child, bs4.Tag):
            print(child.text)

f.close()






