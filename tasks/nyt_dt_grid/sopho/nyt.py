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

class Subset:
    def __init__(self, parent, rank):
        self.parent = parent
        self.rank = rank

class TempGraph:
    # constructor
    def __init__(self, name):
        self.name = name
        # list of nodes
        self.nodes = {}
        # list of edges
        self.edges = []
        # list of unique times
        self.times = {}
        # list of unique distances
        self.distances = {}

    def __del__(self):
        print "deling", self
    
    # sort distances
    def sortDistances(self, asc=True):
        if asc == True:
            self.distances = sorted(TempGraph.distances)
        else:
            self.distances = sorted(TempGraph.distances, reverse=True)

    # sort times
    def sortTimes(self, asc=True):
        if asc == True:
            self.times = sorted(TempGraph.times)
        else:
            self.times = sorted(TempGraph.times, reverse=True)  
    
    def filterEdgesDist(self, dist):
        for i,edge in enumerate(self.edges):
            if float(edge.dist) > float(dist):
                self.removeEdge(edge)
    
    def removeEdge(self, edge):
        self.edges.remove(edge)

    # Add an edge to the object
    def addEdge(self, edge):
        # insery new edge to the TempGraph class
        self.edges.append(edge)
        # update dictionary of unique times
        # and distances and update frequencies
        if not self.times.has_key(edge.delta):
            self.times[edge.delta] = 1
        else:
            self.times[edge.delta] += 1
        if not self.distances.has_key(edge.dist):
            self.distances[edge.dist] = 1
        else:
            self.distances[edge.dist] += 1

        if not self.nodes.has_key(edge.id1):
            self.nodes[edge.id1] = -1

        if not self.nodes.has_key(edge.id2):
            self.nodes[edge.id2] = -1
    
    def removeLastEdge(self):
        self.edges.pop()   
   
    # utility function to find the subset of an element i
    def find(self, parent, i):
        if parent[i] == -1:
            return i
        return self.find(parent,parent[i])
    
    def find1(self, subsets, i):
        if subsets[i].parent != i:
            subsets[i].parent = self.find1(subsets, subsets[i].parent)
        return subsets[i].parent

    # utility function to do union of two subsets   
    def union(self, parent, x, y):
        xset = self.find(parent, x)
        yset = self.find(parent, y)
        parent[xset] = yset
    
    def union1(self, subsets, x, y):
        xroot = self.find1(subsets, x)
        yroot = self.find1(subsets, y)
        if subsets[xroot].rank < subsets[yroot].rank:
            subsets[xroot].parent = yroot
        elif subsets[xroot].rank > subsets[yroot].rank:
            subsets[xroot].parent = xroot
        else:
            subsets[yroot].rank = xroot
            subsets[xroot].rank = int(subsets[xroot].rank)+1
    
    def kruskalMst(self, diff):
        V = len(self.nodes)
        mst = []
        comp = {}
        e = 0
        i = 0    
        subsets = {}
        for v,node in enumerate(self.nodes):
            subset = Subset(node,0)
            subsets[node] = subset
        
        while e < V-1 and i < len(self.edges):
            edge = self.edges[i]
            if float(edge.delta) <= float(diff):
                x = self.find1(subsets, edge.id1)
                y = self.find1(subsets, edge.id2)
                if x != y:
                    #mst.append(edge)
                    e += 1
                    comp[edge.dist] = V-e
                    self.union1(subsets, x, y)
            i += 1
        print e, V-1
        return mst,comp

    # function to check whether a given graph contains cycle or not
    def isCycle(self):
        parent = {}
        #parent[-1] = -1
        for i,n in enumerate(self.nodes):
            parent[n] = -1
        
        for i,e in enumerate(self.edges):
            x = self.find(parent, e.id1)
            y = self.find(parent, e.id2)
            if x==y:
                return True
            self.union(parent, x, y)
        return False
    
    def isCycle1(self):
        subsets = {}
        E = len(self.edges)
        V = len(self.nodes)
        
        for v,node in enumerate(self.nodes):
            subset = Subset(node,0)
            subsets[node] = subset
       
        for e,edge in enumerate(self.edges):
            x = self.find1(subsets, edge.id1)
            y = self.find1(subsets, edge.id2)
            if x == y:
                return True
            self.union1(subsets, x, y)
        return False

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
    
    # Saving dataframe
    def saveDf(self, df, path):
        df.save(path)

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
    def normalizeDfRow(slef, df):
        a = df.as_matrix()
        a = a.astype(float)
        new_matrix = np.zeros((df.columns,df.rows))
        for i, (row, row_sum, min, max) in enumerate(zip(a, row_sums, mins, maxs)):
            new_matrix[i,:] = (row-min) / (max-min)
        return pd.DataFrame(new_matrix)
    
    # Load subsets 
    def loadSubsets(self, path, d1, d2, d3, d4, header):
        subsets = {}
        with open(path, "r") as ins:
            if header:
                ins.readline()
            
            for i,line in enumerate(ins):
                node1 = line.split('\t')[d1]
                node2 = line.split('\t')[d2]
                subset = Subset(node1,0)
                subset = Subset(node2,0)
                subsets[node1] = subset
                subsets[node2] = subset
                if i%1000000==0:
                    print i
        return subsets
                
    # Load MST NYT edges
    def loadMst(self, path, subsets, diff, d1, d2, d3, d4, header):
        V = len(subsets)
        mst = []
        comp = {}
        e = 0
        i = 0
        with open(path, "r") as ins:
            if header:
                ins.readline()

            for i,line in enumerate(ins):
                line = line.rstrip('\n')
                if len(line.split('\t')) >= 4:
                    if round(float(line.split('\t')[d4]),1) <= diff:
                        edge = Edge(line.split('\t')[d1], line.split('\t')[d2], round(float(line.split('\t')[d3]),2), round(float(line.split('\t')[d4]),1))
                        x = self.find1(subsets, edge.id1)
                        y = self.find1(subsets, edge.id2)
                        if x != y:
                            #mst.append(edge) 
                            e += 1
                            comp[edge.dist] = V-e
                            self.union1(subsets, x, y)
                        if i%1000000==0:
                            print i,V-e,edge.dist
                if e > V-1:
                    break
             
        return mst,comp
        
    # Load NYT edges
    def loadEdges(self, path, d1, d2, d3, d4, header):
        with open(path, "r") as ins:
            if header:
                ins.readline()

            for i,line in enumerate(ins):
                line = line.rstrip('\n')
                if len(line.split('\t')) >= 4:
                    edg = Edge(line.split('\t')[d1], line.split('\t')[d2], round(float(line.split('\t')[d3]),2), round(float(line.split('\t')[d4]),1))
                    self.addEdge(edg)
                    if i%100000 == 0:
                        print i
