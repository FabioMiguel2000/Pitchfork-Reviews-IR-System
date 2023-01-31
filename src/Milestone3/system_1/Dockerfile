FROM solr:8.10

COPY reviews_OriginalData.json /data/reviews.json

COPY basic_schema.json /data/schema.json

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
