
#csv_file = 'C:/Users/AhmaDGoly/Desktop/Arshad/TERM 2/Big Data/ElasticSearch/Tamrin 9/books_info.csv'
#json_file = 'C:/Users/AhmaDGoly/Desktop/Arshad/TERM 2/Big Data/ElasticSearch/Tamrin 9/data.json'
from elasticsearch import Elasticsearch
import csv
es = Elasticsearch(hosts=['http://localhost:9200'])

index_name = 'my_index3'
file_path = 'C:/Users/AhmaDGoly/Desktop/Arshad/TERM 2/Big Data/ElasticSearch/Tamrin 9/books_info.csv'

file=open(file_path, 'r', encoding='utf-8')
i=0
def counter():
    global i
    i=i+1
    return i

reader = csv.DictReader(file)
my_body=[]
for row in reader:
    my_body.append({ "index" : {"_index":index_name, "_id":counter()}})
    my_body.append(dict(row))

print(len(my_body))
print(my_body[0])
print(my_body[1])
print(my_body[2])
print(my_body[3])

response = es.bulk(body=my_body)
#print(response)

#helpful link: https://www.elastic.co/guide/en/elasticsearch/reference/current/docs-bulk.html
#helpful link: https://coralogix.com/blog/42-elasticsearch-query-examples-hands-on-tutorial/