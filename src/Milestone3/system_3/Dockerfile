FROM solr:8.10

COPY reviews_OriginalContent_with_OriginalKeywords.json /data/reviews.json

COPY extended_schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
