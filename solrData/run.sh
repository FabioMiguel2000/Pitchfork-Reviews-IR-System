docker build . -t meic_solr_advanced
docker run --name my_solr -p 8982:8982 meic_solr_advanced