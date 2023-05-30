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
insert_query_for_parents = "INSERT INTO goly.parents (trove_id,title,url,contributors,date,format,pages) VALUES (?,?,?,?,?,?,?)"
create_table_query_parents= "CREATE TABLE goly.parents (\
    title text,\
    url text,\
    contributors text,\
    date text,\
    format text,\
    trove_id text PRIMARY KEY,\
    pages int\
);"
# Prepare the insert statement
insert_statement = session.prepare(insert_query_for_parents)

#STEP 1: Find parents and add them to goly.parents table:
while True:
    res = es.search(
        index=index_name,
        body={
            'query': {
        "bool": {
            "must": [
                {
                    "exists": {
                        "field": "children"
                    }
                },
                {
                    "bool": {
                        "must_not": [
                            {
                                "term": {
                                    "children": ""
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
            row = (doc['trove_id'], doc['title'], doc['url'], doc['contributors'], doc['date'], doc['format'], int(doc['pages']))
            session.execute(insert_statement, row)
            print(f"{i} docs added to goly.parents.", end="\r")
    else:
        break

print(f"\nTotal parents documents:{i}\n")


