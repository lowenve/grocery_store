from elasticsearch import Elasticsearch

es = Elasticsearch(['192.168.105.28:9200'])
print(es.ping())