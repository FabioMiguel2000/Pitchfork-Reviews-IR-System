FROM solr:8.10

COPY reviews_CleanContent_with_CleanKeywords.json /data/reviews.json

COPY extended_schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
