FROM solr:8.10

COPY reviews_CleanContent_with_CleanKeywords.json /data/reviews.json

COPY synonyms_schema.json /data/schema.json

COPY synonyms_en.txt /data/synonyms.txt

COPY startup.sh /scripts/startup.sh

ENTRYPOINT ["sh","/scripts/startup.sh"]
