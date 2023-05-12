from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.metadata import KeyspaceMetadata
cluster = Cluster(['localhost'])
session = cluster.connect()
results=list(session.execute('SELECT lat,lon FROM goly.cache WHERE datetimeseconds >= 1728000 ALLOW FILTERING;'))
#result=list(session.execute('SELECT prediction,COUNT(*) FROM goly.cache WHERE datetimeseconds >= 1987200 GROUP BY prediction ALLOW FILTERING;'))

for i in range (0,len(results)):
    results[i]=list(results[i])
    results[i][0]=round(results[i][0], 2)
    results[i][1]=round(results[i][1], 2)

counts = {}
for point in results:
    if tuple(point) in counts:
        counts[tuple(point)] += 1
    else:
        counts[tuple(point)] = 1

sorted_counts = sorted(counts.items(), key=lambda x: x[1], reverse=True)
for point, count in sorted_counts:
    if count > 1:
        print("Point", point, "occurs", count, "times in the results list.")