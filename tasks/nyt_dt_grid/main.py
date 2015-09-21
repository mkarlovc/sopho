import datetime
import snap
import pickle
import os
import time

class Edge:
    
    # convert string to datetime
    def timeConvert(self, text):
        return datetime.datetime.strptime(text, "%d%m%Y").date()    

    def __init__(self, id1, id2, dist, delta):
        self.id1 = id1
        self.id2 = id2
        self.dist = dist
        self.delta = delta

class TempGraph:
    
    edges = []    
 
    def __init__(self, name):
        self.name = name

    # add an edge to the object
    def addEdge(self, edge):
        TempGraph.edges.append(edge)
    
    # iterate all edges and create snap graph with edges
    # that satisfy tide difference and distance tresholds
    def createGraph(self, time, dist):
        g = snap.TNGraph.New()
        nodes = {}
        nodes_rev = {}
        nodesCount = 0
        for i,e in enumerate(self.edges):
            if e.delta.days <= time and e.dist <= dist:
                n1 = -1
                n2 = -1
                if (not nodes.has_key(e.id1)):
                    n1 = nodesCount
                    nodes[e.id1] = n1
                    g.AddNode(n1)
                    nodes_rev[n1] = e.id1
                    nodesCount += 1
                else:
                    n1 = nodes[e.id1]

                if (not nodes.has_key(e.id2)):
                    n2 = nodesCount
                    nodes[e.id2] = n2
                    g.AddNode(n2)
                    nodes_rev[n2] = e.id2
                    nodesCount += 1
                else:
                    n2 = nodes[e.id2]
                
                g.AddEdge(n1, n2)
        return (g,nodes_rev)

    # with one pass create bunch of graph
    def createGraphGrid(self):
        grid = {}
        map = {}
        nodes = 0
        for i,e in enumerate(self.edges):
            key = str(round(float(e.delta)/120,1))+'_'+str(round(e.dist,1))            
            if not grid.has_key(key):
                g = snap.TNGraph.New()
                grid[key] = g
            else:
                g = grid[key]
            
            n1 = -1
            n2 = -1

            if not map.has_key(e.id1):
                map[e.id1] = nodes
                n1 = nodes
                nodes += 1
            else:
                n1 = map[e.id1]
 
            if not map.has_key(e.id2):
                map[e.id2] = nodes
                n2 = nodes
                nodes += 1
            else:
                n2 = map[e.id2]
                        
            if g.IsNode(n1) == False:
                g.AddNode(n1)
            
            if g.IsNode(n2) == False:
                g.AddNode(n2)

            g.AddEdge(n1, n2)
  
        return (grid,map)

t1 = time.time()

tg = TempGraph("Test temporal graph")

with open("/media/mario/My Book/mario/sopho/nyt/nyt/graph/nyt-06-fast/graph.txt", "r") as ins:
    ins.readline()
    for line in ins:
        line = line.rstrip('\n')
        edg = Edge(line.split('\t')[0], line.split('\t')[1], float(line.split('\t')[2]), float(line.split('\t')[4]))
        tg.addEdge(edg)

# calculate grid
obj = tg.createGraphGrid()
grid = obj[0]
map = obj[1]

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# calculate dataframe
columns = {}
index = {}


for g in grid:
    columns[float(g.split('_')[0])] = 1
    index[float(g.split('_')[1])] = 1

columns = columns.keys()
index = index.keys()
df = pd.DataFrame(index=sorted(index), columns=sorted(columns))
df = df.fillna(0)

for g in grid:
    col = float(g.split('_')[0])
    ind = float(g.split('_')[1])
    graph = grid[g]
    Components = snap.TCnComV()
    snap.GetWccs(graph,Components)
    df[col][ind] = Components.Len()

plt.pcolor(df)
plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
plt.show()

# save grid
if not os.path.exists("./grid/"):
    os.makedirs("./grid/")

for g in grid:
    FOut = snap.TFOut("grid/g_"+g.replace('.',''))
    grid[g].Save(FOut)

t2 = time.time()

print t2-t1
