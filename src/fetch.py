from bs4 import BeautifulSoup
import json
import bs4
import requests

f = open('../assets/reviews.json')

dataset = json.load(f)

reviews = []

for review in dataset:
    if 'review_content' in review:
        continue

    result = requests.get(review['url'])

    print(review['reviewid'])

    doc = BeautifulSoup(result.text, "html.parser")

    html_content = doc.find("div", {"class": "body__inner-container"})

    if(html_content == None):
        html_content = doc.find("div", {"class": "contents dropcap"})
    
        if(html_content == None): # Most likely due to content not found
            review_content = {"review_content": "None"}
            review.update(review_content)
            j = json.dumps(dataset)

            with open("../assets/reviews.json", "w") as f:
                f.write(j)
            continue

    for child in html_content:
        if isinstance(child, bs4.Tag):
            
            # print(child.text)
            review_content = {"review_content":child.text}
            review.update(review_content)

    j = json.dumps(dataset)

    with open("../assets/reviews.json", "w") as f:
        f.write(j)

f.close()






