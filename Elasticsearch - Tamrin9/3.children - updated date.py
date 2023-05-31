from elasticsearch import Elasticsearch
from cassandra.cluster import Cluster
from cassandra.query import BatchStatement

es = Elasticsearch(hosts=['http://localhost:9200'])
print("Elasticsearch is ready.")
cluster = Cluster(['localhost'])
session = cluster.connect()
print("Cassandra is ready.\n")

#ElasticSearch settings:
index_name = 'my_index3'
batch_size = 1000
sort_field = '_doc'
sort_order = 'asc'
i=0
search_after = None

#Cassandra Settings:
insert_query_for_children = "INSERT INTO goly.children (trove_id,title,url,contributors,date,format,pages) VALUES (?,?,?,?,?,?,?)"
create_table_query_children= "CREATE TABLE goly.children (\
    title text,\
    url text,\
    contributors text,\
    date text,\
    format text,\
    trove_id text PRIMARY KEY,\
    pages int\
);"
# Prepare the insert statement
insert_statement = session.prepare(insert_query_for_children)

#STEP 1: Find children and add them to goly.children table:
while True:
    res = es.search(
        index=index_name,
        body={
            'query': {
        "bool": {
            "must": [
                {
                    "exists": {
                        "field": "parent"
                    }
                },
                {
                    "bool": {
                        "must_not": [
                            {
                                "term": {
                                    "parent": ""
                                }
                            }
                        ]
                    }
                }
            ]
        }
    },
            'sort': [{sort_field: sort_order}],
            'size': batch_size,
            'search_after': search_after
        }
    )

    if res['hits']['hits']:
        last_hit = res['hits']['hits'][-1]
        search_after = last_hit['sort']
        
        for hit in res['hits']['hits']:
            doc_id = hit['_id']
            doc = hit['_source']
            i=i+1
            # Perform any necessary data transformations or mappings here
            datecache = doc['date']
            if len(datecache)<=4:
                row = (doc['trove_id'], doc['title'], doc['url'], doc['contributors'], datecache, doc['format'], int(doc['pages']))
            else:
                row = (doc['trove_id'], doc['title'], doc['url'], doc['contributors'], datecache[5:], doc['format'], int(doc['pages']))
            session.execute(insert_statement, row)
            print(f"{i} docs added to goly.children.", end="\r")
    else:
        break

print(f"\nTotal child documents:{i}\n")
