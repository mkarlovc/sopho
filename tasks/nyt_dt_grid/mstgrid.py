from sopho import nyt
import time
import sys
import pandas
import sys
import matplotlib.pyplot as plt
import numpy as np

path = sys.argv[1]
sys.path.append(".")

t1 = time.time()

print "creating temporal graph object..."

print "load graph..."

tg = nyt.TempGraph("Test temporal graph")
tg.loadEdges(path,0,1,3,4,True)
N = len(tg.nodes)
print N
print (time.time()-t1)/(60)

print "computing msti..."

rows = {}
for i in range(0, 180, 1):
    window = 180-i
    print "window", window
    comp = tg.KruskalMst(window)[1]
    rows[window] = comp
    print (time.time()-t1)/(60)

print "creating df..."

columnindex = sorted(rows.keys())
rowindex = sorted(rows[180].keys())
print columnindex
print rowindex
df = pandas.DataFrame(columns=columnindex, index=rowindex)
for r in rows:
    vals = []
    prev = 0
    for k in rowindex:
        if not rows[r].has_key(k):
            vals.append(prev)
        else:
            vals.append(rows[r][k])
            prev = rows[r][k]
    print rowindex, vals
    df[r] = vals

print "saving..."

t2 = time.time()
print (t2-t1)/(60)
print df
df.save("df")
df1 = tg.normalizeDf(df)
df1.save("df1")
