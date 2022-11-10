docker build . -t meic_solr
docker run --name my_solr -p 8983:8983 meic_solr