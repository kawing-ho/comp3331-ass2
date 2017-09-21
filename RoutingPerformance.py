#!/usr/bin/python
#COMP3331 Assignment2 
#z5087077 Ka Wing Ho 
#z5113471 Andy Yang 

import sys, re

#Code referrenced from: http://www.bogotobogo.com/python/python_graph_data_structures.php
#Graph has nodes / Nodes have edges / Edges have Capacity + Prop Delay tuple


#Graph stores 
# - List of nodes (each node will know about its neighbours)
# - List of edges (no duplicates) , (edges will have Dprop,MaxCap,CurrCap)

class Vertex:
    def __init__(self, node):
        self.id = node
        self.neighbours = []

    def __str__(self):
        return str(self.id) + ' neighbours: ' + str([x.id for x in self.neighbours])

    def addNeighbour(self, neighbour):
    	if neighbour not in self.neighbours: self.neighbours.append(neighbour)

    def getNeighbours(self): return self.neighbours
    def getID(self): return self.id

class Edge:
	def __init__(self,node1,node2,delay,max):
		self.node1 = node1
		self.node2 = node2
		self.delay = delay
		self.maxCapacity = max
		self.load = 0

	def isFull(self):
		return (self.maxCapacity == self.load)

	def addLoad(self,load):
		if(not isFull(self)): self.load = self.load + load

	def reduceLoad(self,load):
		if(self.load > 0): self.load = self.load - load

	def availableSpace(self):
		return (self.maxCapacity - self.load)

	def getDelay(self): return self.delay
	def getLoad(self): return self.load
	def getMaxCapacity(self): return self.maxCapacity
	def getNode1(self): return self.node1
	def getNode2(self): return self.node2

	def isNode(self,node): return ((node == self.node1) or (node == self.node2))


class Graph:
    def __init__(self):
        self.edges = []
        self.vertices = []

    def addVertex(self, node):
        new = Vertex(node)

        #Check if the same node exists in the list or not
        for v in self.vertices:
        	if(v.getID() == node): return new

        self.vertices.append(new)
        return new

    def addNeighbour(self, vertex, neighbour):   #?

    	node1 = self.getVertex(vertex)
    	node2 = self.getVertex(neighbour)
    	for v in self.vertices:
    		if(v.getID() == node1.getID()):
    			v.addNeighbour(node2)
    		if(v.getID() == node2.getID()):
    			v.addNeighbour(node1)

    def getVertex(self, n):
        for v in self.vertices:
            if (v.getID() == n): return v

        return None

    def addEdge(node1, node2, delay, max):
        if frm not in self.vert_dict:
            self.add_vertex(frm)
        if to not in self.vert_dict:
            self.add_vertex(to)

        self.vert_dict[frm].add_neighbor(self.vert_dict[to], cost)
        self.vert_dict[to].add_neighbor(self.vert_dict[frm], cost)

    def getVertices(self):
    	ret = [];
    	for v in self.vertices:
    		ret.append(v.getID());
        return ret

    def show(self):
    	print "Vertices :" + str(self.getVertices())
    	print "Edges    :" + str(self.edges)

#Just some simple error-checking in args
if(len(sys.argv) != 6): print "Usage: python RoutingPerformance.py <CIRCUIT/PACKET> <SHP/SDP/LLP> <topology-file> <workload-file> <rate>"; exit()
if(sys.argv[1] != "CIRCUIT") and (sys.argv[1] != "PACKET"): print "Incorrect Network Scheme"; exit();
if(sys.argv[2] != "SHP") and (sys.argv[2] != "SDP") and (sys.argv[2] != "LLP"): print "Incorrect Router Scheme"; exit();
if(int(sys.argv[5]) < 1): print "Rate must be positive non-zero integer"; exit()

#try opening the files
try:
	top = open(sys.argv[3])
	work = open(sys.argv[4])
except Exception as e: print str(e); exit()


#Graph initialization
g = Graph()
for line in top.readlines():
	match = re.search("([A-Z]) ([A-Z]) (\d+) (\d+)",line)
	
	node1 = match.group(1)  #just a character like "A"
	node2 = match.group(2)  #just a character like "B" 
	dprop = match.group(3)
	maxCapacity = match.group(4)

	#Add node to graph if it doesn't exist
	g.addVertex(node1); g.addVertex(node2)

	#Add edge in the graph
	#g.addEdge(node1,node2,dprop,maxCapacity)

	#Add to each other's neighbours
	g.addNeighbour(node1,node2)

	#According to the format of the sample the input won't have duplicates so all good

#Finish graph initialization
g.show()
top.close()

#Parse workload file 
for line in work.readlines():
	match = re.search("(\d+) ([A-Z]) ([A-Z]) (\d+)",line)

	time = match.group(1)
	requester = match.group(2)
	recipient = match.group(3)
	duration = match.group(4)

#the type of network scheme defines the behaviour of the algorithms ? 

#Choose which routing algorithm to run


work.close()

