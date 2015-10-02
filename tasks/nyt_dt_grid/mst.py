from sopho import nyt
import time
import sys
import pandas
import sys

path = sys.argv[1]
sys.path.append(".")

t1 = time.time()

print "creating temporal graph object..."

print "load graph once"
tg = nyt.TempGraph("Test temporal graph")
tg.loadEdges(path)

N = len(tg.nodes)
print N
mst = tg.KruskalMst()
t2 = time.time()
for e in mst[0]:
    print e.id1, e.id2, e.dist
print N
print len(mst[0])
print mst[1]


print (t2-t1)/(60)
