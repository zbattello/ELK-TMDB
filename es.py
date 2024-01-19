from datetime import datetime
from elasticsearch import Elasticsearch
import csv

ELASTIC_PASSWORD = "6pl0rnxHKe82IPkf5+EA"

#disable certificate
es = Elasticsearch(hosts="https://localhost:9200", basic_auth=("elastic", ELASTIC_PASSWORD), verify_certs=False)








doc = {
    'ID': 315946 ,
    'Title': 'Passage of Venus',
    'Vote Average': '6.2',
    'Date': '1874-12-09',
    'Original Langage': 'fr',
    'Genre IDs': '[99]',
    'IsMovie': 'True'

}





def parse_csv(file_path):
    N = 1
    with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            resp = es.index(index=f"index{N}", id=1, document=row)
            es.indices.refresh(index=f"index{N}")
            N=N+1
            if N > 200000:
                break


parse_csv("media_list.csv")

resp = es.search(index="index35080", query={"match_all": {}})
print("Got %d Hits:" % resp['hits']['total']['value'])
for hit in resp['hits']['hits']:
    print("%(ID)s %(Title)s: %(Vote Average)s %(Date)s" % hit["_source"])