docker build . -t meic_solr_advanced
docker run --name my_solr -p 8984:8984 meic_solr