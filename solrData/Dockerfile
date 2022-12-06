FROM solr:8.10

COPY ProcessedData/reviews_OriginalData.json /data/clean_reviews.json

COPY basic_schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
