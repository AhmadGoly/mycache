from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.metadata import KeyspaceMetadata
cluster = Cluster(['localhost'])
session = cluster.connect()

def baseNum_to_base (baseNum):
    if baseNum==0:
        return "B02617"
    if baseNum==1:
        return "B02598"
    if baseNum==2:
        return "B02682"
    if baseNum==3:
        return "B02764"
    if baseNum==4:
        return "B02512"

week1_groupby=list(session.execute('SELECT basenumerical,COUNT(*) FROM goly.cache2 WHERE datetimeseconds >= 0 AND datetimeseconds < 604800 GROUP BY basenumerical ALLOW FILTERING;'))
week2_groupby=list(session.execute('SELECT basenumerical,COUNT(*) FROM goly.cache2 WHERE datetimeseconds >= 604800 AND datetimeseconds < 1209600 GROUP BY basenumerical ALLOW FILTERING;'))
week3_groupby=list(session.execute('SELECT basenumerical,COUNT(*) FROM goly.cache2 WHERE datetimeseconds >= 1209600 AND datetimeseconds < 1814400 GROUP BY basenumerical ALLOW FILTERING;'))
week4_groupby=list(session.execute('SELECT basenumerical,COUNT(*) FROM goly.cache2 WHERE datetimeseconds >= 1814400 AND datetimeseconds < 2419200 GROUP BY basenumerical ALLOW FILTERING;'))
week5_groupby=list(session.execute('SELECT basenumerical,COUNT(*) FROM goly.cache2 WHERE datetimeseconds >= 2419200 GROUP BY basenumerical ALLOW FILTERING;'))

print("1st Week:")
for row in week1_groupby:
    row=list(row)
    print(f"Base {baseNum_to_base(row[0])} Total Ubers: {row[1]}")

print("2nd week:")
for row in week2_groupby:
    row=list(row)
    print(f"Base {baseNum_to_base(row[0])} Total Ubers: {row[1]}")

print("3rd Week:")
for row in week3_groupby:
    row=list(row)
    print(f"Base {baseNum_to_base(row[0])} Total Ubers: {row[1]}")

print("4th Week:")
for row in week4_groupby:
    row=list(row)
    print(f"Base {baseNum_to_base(row[0])} Total Ubers: {row[1]}")

print("5th Week:")
for row in week5_groupby:
    row=list(row)
    print(f"Base {baseNum_to_base(row[0])} Total Ubers: {row[1]}")