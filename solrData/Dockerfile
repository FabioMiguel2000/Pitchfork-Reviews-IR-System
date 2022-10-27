FROM solr:8.10

COPY clean_reviews.json /data/clean_reviews.json

COPY schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["/scripts/startup.sh"]
