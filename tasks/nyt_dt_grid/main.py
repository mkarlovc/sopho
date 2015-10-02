from sopho import nyt
import time
import sys

sys.path.append(".")

t1 = time.time()

print "creating temporal graph object..."
tg = nyt.TempGraph("Test temporal graph")

print "loading edges..."
tg.loadEdges("/media/mario/My Book/mario/sopho/nyt/nyt/graph/nyt-06-fast/graph1M.txt")

print "computing grid..."
grid = tg.computeGrid(True)

print "saving grid..."
tg.saveGraphs(grid,"gridnew")

print "creating weakly connected components dataframe..."
df = tg.getWccsDf(grid)

print "saving dataframe..."
tg.saveDf(df, "df")

t2 = time.time()

print t2-t1

print "plotting df"
tg.plotDf(df)

print "normalizing dataframe..."
df1 = tg.normalizeDf(df)

print "saving dataframe..."
tg.saveDf(df1, "df1")

print "plotting dataframe"
tg.plotDf(df1)

print "computing OR grid..."
grid1 = tg.computeGrid(False)

print "creating wcc dataframe"
df2 = tg.getWccsDf(grid1)

print "saving dataframe..."
tg.saveDf(df2, "df2")

print "plotting"
tg.plotDf(df2)

