from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.metadata import KeyspaceMetadata
cluster = Cluster(['localhost'])
session = cluster.connect()
result=list(session.execute('SELECT prediction,COUNT(*) FROM goly.cache WHERE datetimeseconds >= 1987200 GROUP BY prediction ALLOW FILTERING;'))
for i in range(0,len(result)):
    result[i]=list(result[i])
result = sorted(result, key=lambda x: x[1], reverse=True)
print("Sorted Clusters:")
for row in result:
    print(f"Cluster {row[0]} has {row[1]} rows in last week.")