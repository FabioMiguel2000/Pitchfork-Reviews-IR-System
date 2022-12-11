FROM solr:8.10

COPY reviews_with_only_keywords25_new.json /data/clean_reviews.json

COPY schema_synonyms.json /data/schema.json

COPY synonyms_en.txt /data/synonyms.txt

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
