FROM solr:8.10

COPY ProcessedData/reviews_CleanContent_with_CleanKeywords.json /data/clean_reviews.json

COPY schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
