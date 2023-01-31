FROM solr:8.10

COPY reviews_EmptyContent_with_EmptyKeywords.json /data/reviews.json

COPY extended_schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
