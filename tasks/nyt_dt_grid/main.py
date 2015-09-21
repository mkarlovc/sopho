import datetime
import snap

class Edge:
    
    # convert string to datetime
    def timeConvert(self, text):
        return datetime.datetime.strptime(text, "%d%m%Y").date()    

    def __init__(self, id1, id2, dist):
        self.id1 = id1
        self.id2 = id2
        self.dist = dist
        self.time1 = self.timeConvert(id1)
        self.time2 = self.timeConvert(id2)
        self.delta = self.time2 - self.time1

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

tg = TempGraph("Test temporal graph")

with open("testgraph.txt", "r") as ins:
    for line in ins:
        line = line.rstrip('\n')
        edg = Edge(line.split('\t')[0], line.split('\t')[1], float(line.split('\t')[2]))
        tg.addEdge(edg)

tg.createGraph(100, 0.6)
