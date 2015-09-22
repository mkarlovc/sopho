import datetime
import snap
import pickle
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    # list of edges
    edges = []    
    # list of unique times
    times = {}
    # list of unique distances
    distances = {}
    # constructor
    def __init__(self, name):
        self.name = name

    # sort distances
    def sortDistances(self, asc=True):
        if asc == True:
            TempGraph.distances = sorted(TempGraph.distances)
        else:
            TempGraph.distances = sorted(TempGraph.distances, reverse=True)

    # sort times
    def sortTimes(self, asc=True):
        if asc == True:
            TempGraph.times = sorted(TempGraph.times)
        else:
            TempGraph.times = sorted(TempGraph.times, reverse=True)  

    # Add an edge to the object
    def addEdge(self, edge):
        # insery new edge to the TempGraph class
        TempGraph.edges.append(edge)
        # update dictionary of unique times
        # and distances and update frequencies
        if not TempGraph.times.has_key(edge.delta):
            TempGraph.times[edge.delta] = 1
        else:
            TempGraph.times[edge.delta] += 1
        if not TempGraph.distances.has_key(edge.dist):
            TempGraph.distances[edge.dist] = 1
        else:
            TempGraph.distances[edge.dist] += 1
 
    # Iterate all edges and create snap graph with edges
    # that satisfy tide difference and distance tresholds
    # No Null Nodes
    def createGraphNNN(self, time, dist):
        g = snap.TNGraph.New()
        nodes = {}
        nodes_rev = {}
        nodesCount = 0
        for i,e in enumerate(self.edges):
            go = False
            if logAnd == True:
                if e.delta <= time and e.dist > dist:
                    go = True
            else:
                if e.delta <= time or e.dist > dist:   
                    go = False

            if go:
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
        return g

    # Iterate all edges and create snap graph with edges
    # that satisfy tide difference and distance tresholds
    # With null nodes
    def createGraph(self, time, dist, logAnd=True):
        g = snap.TNGraph.New()
        nodes = {}
        nodes_rev = {}
        nodesCount = 0
        for i,e in enumerate(self.edges):
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

            if logAnd == True:
                if e.delta <= time and e.dist > dist:
                    g.AddEdge(n1, n2)
            else:
                if e.delta <= time or e.dist > dist:
                    g.AddEdge(n1, n2)

        return g

    # with one pass create bunch of graph
    def frequenciesGrid(self):
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
  
        return grid

    # Saving graphs
    def saveGraphs(self, grid, path):
        # create directory
        if not os.path.exists(path):
            os.makedirs(path)

        # save all graph from the grid into the directory
        for g in grid:
            FOut = snap.TFOut(path+"/g_"+g.replace('.',''))
            grid[g].Save(FOut)
    
    # Compute and output grid in form of graphs dictionary 
    def computeGrid(self, logAnd):
        grid = {}
        for t in TempGraph.times:
            for d in TempGraph.distances:
                grid[str(t)+"_"+str(d)] = self.createGraph(t,d,logAnd)
        
        self.sortTimes()
        self.sortDistances()

        return grid
    
    # Compute and output dataframe of connected components 
    def getWccsDf(self, grid):
        df = pd.DataFrame(index=self.distances, columns=self.times)
        df = df.fillna(0)
        for g in grid:
            col = float(g.split('_')[0])
            ind = float(g.split('_')[1])
            graph = grid[g]
            Components = snap.TCnComV()
            snap.GetWccs(graph,Components)
            df[col][ind] = float(Components.Len())
        return df
    
    # Plot dataframe
    def plotDf(self, df):
        plt.pcolor(df)
        plt.yticks(np.arange(0.5, len(df.index), 1), df.index)
        plt.xticks(np.arange(0.5, len(df.columns), 1), df.columns)
        plt.show()

    # Normalize DataFrame
    def normalizeDf(self, df):
        a = df.as_matrix()
        a = a.astype(float)
        row_sums = a.sum(axis=1)
        new_matrix = a / row_sums[:, np.newaxis]
        return pd.DataFrame(new_matrix)
    
    # Normalize row spec
    '''
    def normalizeDfRow(slef, df):
        a = df.as_matrix()
        a = a.astype(float)
        new_matrix = np.zeros((df.columns,df.rows))
        for i, (row, row_sum, min, max) in enumerate(zip(a, row_sums, mins, maxs)):
            new_matrix[i,:] = (row-min) / (max-min)
        return pd.DataFrame(new_matrix)
    '''

    # Load NYT edges
    def loadEdges(self, path):
        with open(path, "r") as ins:
            ins.readline()
            for line in ins:
                line = line.rstrip('\n')
                #edg = Edge(line.split('\t')[0], line.split('\t')[1], round(float(line.split('\t')[2]),1), round(float(line.split('\t')[4])/60,1))
                edg = Edge(line.split('\t')[0], line.split('\t')[1], round(float(line.split('\t')[2]),1), round(float(line.split('\t')[4]),0))
                self.addEdge(edg)