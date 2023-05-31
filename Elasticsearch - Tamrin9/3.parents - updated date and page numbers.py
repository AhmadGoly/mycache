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

#page number calculator for parents:
def pageNumberCalculator(es,index_name,trove_id):
    query = {
    "query": {
        "bool": {
            "must": [
                {
                    "term": {
                        "parent": {
                            "value": trove_id
                        }
                    }
                },
                {
                    "exists": {
                        "field": "pages"
                    }
                }
            ]
        }
    },
    "aggs": {
        "total_pages": {
            "sum": {
                "field": "pages"
            }
        }
    }
    }
    response = es.search(index=index_name, body=query)
    return response["aggregations"]["total_pages"]["value"]

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
            #Add page Number to parents based on data on elasticsearch

            # Perform any necessary data transformations or mappings here

            pagenumber = pageNumberCalculator(es,index_name,doc['trove_id'])
            datecache = doc['date']
            if len(datecache)<=4:
                row = (doc['trove_id'], doc['title'], doc['url'], doc['contributors'], datecache, doc['format'], int(pagenumber))
            else:
                row = (doc['trove_id'], doc['title'], doc['url'], doc['contributors'], datecache[5:], doc['format'], int(pagenumber))
            session.execute(insert_statement, row)
            print(f"{i} docs added to goly.parents.", end="\r")
    else:
        break

print(f"\nTotal parents documents:{i}\n")




