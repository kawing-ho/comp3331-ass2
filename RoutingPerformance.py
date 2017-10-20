#!/usr/bin/python
#COMP3331 Assignment2
#z5087077 Ka Wing Ho
#z5113471 Andy Yang

'''
References :
(1)> List-sorting with tuples in them: https://stackoverflow.com/a/36075587
(2)> ...
'''

import sys, re
import time, math, threading, json
from collections import defaultdict

#returns the correct order of edge eg. "AB" -> "AB" , "BA" -> "AB"
def reorder(one,two): return (one + two) if (ord(one) < ord(two)) else (two + one)

#return list of edges that involve that node
def getEdges(node,g): return [edge for edge in g if node in edge]

#return neighbours of a node (not including itself)
def getNeighbours(myNode,g):
	neighbours = set()
	for edge in getEdges(myNode,g):
		[neighbours.add(node) for node in edge if (node != myNode)]
	return sorted(list(neighbours))

#return list of nodes in the graph
def getNodes(g):
	nodes = set()
	for edge in g.keys():
		[nodes.add(node) for node in edge]
	return sorted(list(nodes))

#comparator function for sorting PQ
#-------(See reference (1))--------
def distance_compare(a, b):
	if a[1] < b[1]: return -1
	elif a[1] == b[1]:
		if a[0] > b[0]: return 1
		else: return -1
	else: return 1
#-----------------------------------

#check if a path has already been computed before for two nodes
#input: a two-letter route (eg. AG , BC , etc ...)
#output: None if not found or Path as a list from Src->Dest
def checkSaved(route):
	if(algorithm == "LLP") or (route not in routes.keys()): return None
	else: return routes[route]


#SHP algorithm 
#Weight = 1 (same across all edges)
#input : Source, Dest, Graph
#output: Path as a list from Src -> Dest
def shortestHop(source, dest, graph):
	path = {}						#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];   #PQ stores tuple of (node,distanceFromSource)
	visited = set()

	while True:

		currentNode, currentDistance = PriorityQueue.pop(0)		#get node from PQ
		visited.add(currentNode)								#add node to visited

		if(currentNode == dest): break							#break if goal found

		# look at neighbours and consider weights
		for neighbour in getNeighbours(currentNode,graph):
			if neighbour in visited: continue					#skip if seen neighbour before
			else: visited.add(neighbour)

			PriorityQueue.append((neighbour,currentDistance + 1)) #weight = 1 for all edges in SHP

			path[neighbour] = currentNode

		#reshuffle PQ (sort by distance)
		PriorityQueue.sort(distance_compare)

	res = []
	node = dest
	while True:
		res = [node] + res
		if node in path: node = path[node]
		else : break


	return res

#SDP algorithm
#Weight = delay of that edge (constant but different for every edge)
def shortestDelay():
	return None

#LLP algorithm
#Weight = Load of that edge (very volatile as it can change in the middle of a connection)
def leastLoad():
	return None

def SHPTest():
	print "=== Testing out SHP with A and D ==="
	print str(shortestHop('A', 'D', Graph))
	print "=== Testing out SHP A and B ==="
	print str(shortestHop('A', 'B', Graph))
	print "=== Testing out SHP D and C ==="
	print str(shortestHop('D', 'C', Graph))
	print "=== Testing out SHP D and A ==="
	print str(shortestHop('D', 'A', Graph))


	if('G' not in getNodes(Graph)): return
	print " *** Topology.txt ***"
	print "=== Testing out SHP G and I ==="
	print str(shortestHop('G', 'I', Graph))
	print "=== Testing out SHP I and G ==="
	print str(shortestHop('I', 'G', Graph))
	print "=== Testing out SHP D and O ==="
	print str(shortestHop('D', 'O', Graph))
	print "=== Testing out SHP M and E ==="
	print str(shortestHop('M', 'E', Graph))


def SDPTest():
	print "Testing SDP"
	print "graph is <",Graph,">"
	print json.dumps(Graph, indent=4)
	print "\n========A to D=============="
	print str(dijkstraSDP('A', 'D', Graph))
	print "\n========A to F=============="
	print str(dijkstraSDP('A', 'F', Graph))
	print "\n========A to E=============="
	print str(dijkstraSDP('A', 'E', Graph))
	print "\n========F to C=============="
	print str(dijkstraSDP('F', 'C', Graph))
	print "\n========E to C=============="
	print str(dijkstraSDP('E', 'C', Graph))
	print "\n========A to A=============="
	print str(dijkstraSDP('A', 'A', Graph))

def getDelayOfEdge(graph,edge): return int(graph[edge]['delay'])

#input: edges
#output: sorts edges according to delay time
def sortDelay(graph, edges):
	newEdges = {}
	delaytime = getDelayTime(graph)
	for edge,delay in delaytime:
		if(edge in edges):
			newEdges[edge] = delay

	return newEdges

#returns a dictionary of delay from the graph sorted
#from lowest delay time to highest delay time   eg.  {"AB":5 ,"BD":10, "CB":30}
def getDelayTime(graph):
	delaytime = {}
	for edge in graph:
		delaytime[edge] = getDelayOfEdge(graph,edge)
	delaytime = sorted(delaytime.iteritems(), key=lambda (k,v): (v,k))
	return delaytime

#Prototype for SDP
#input : Source, Dest, Graph
#output: Path as a list from Src -> Dest but using the shortest delay time
def dijkstraSDP(source, dest, graph):
	if(source not in getNodes(graph) or dest not in getNodes(graph)): return None
	path = {}						#Path is dict going backwards eg. path[B] = A
	delay = {}
	queue = [source];
	visited = set()

	delay[source] = 0

	while True:
	#while queue:
		currentNode = queue.pop(0)
		print "--- current node is ",currentNode,"---"
		visited.add(currentNode)

		print "visited  |\t",list(visited)
		if(currentNode == dest): 				# Check if node is destination
			sys.stdout.write("Found destination ! Path is ")
			break				


		#edges = getEdges(currentNode, graph)
		#edges = sortDelay(graph, edges)

		for neighbour in getNeighbours(currentNode,graph):

			currentEdge = reorder(neighbour,currentNode)

			if (neighbour in visited):
				if(getDelayOfEdge(graph,currentEdge) + delay[currentNode] > delay[neighbour]):
					continue
			else:
				visited.add(neighbour)

			queue.append(neighbour)
			path[neighbour] = currentNode
			delay[neighbour] = delay[currentNode] + getDelayOfEdge(graph,currentEdge)

		print "path is  |\t",path
		print "delay is |\t",delay
		print "queue is |\t",str(queue)

	res = []
	node = dest
	while True:
		res = [node] + res
		if node in path: node = path[node]
		else : break

	return res


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

Graph = {} 						   #Graph is a dict containing dicts
routes = {}						   #route is a dict containing pre-computed paths for chosen source/dest nodes
scheme = sys.argv[1]
algorithm = sys.argv[2]
rate = int(sys.argv[5])            # eg. if rate = 2 it means 2 packets/s
packetTime = float(1.0 / rate)	   # that means each packet takes 0.5 s to transmit
startOfProgram = time.time()


#Graph initialization
for line in top.readlines():
    match = re.search("([A-Z]) ([A-Z]) (\d+) (\d+)",line)

    edge = reorder(match.group(1), match.group(2))
    propDelay = match.group(3)
    maxCapacity = match.group(4)

    Graph[edge] = {"delay":propDelay, "max":maxCapacity, "load":0}

#Finish graph initialization
top.close()

print json.dumps(Graph, indent=4)
print "It takes",time.time()-startOfProgram,"to finish initialization"

startTime = time.time()
#Parse workload file
for count,line in enumerate(work.readlines()):
    match = re.search("([\d\.]+) ([A-Z]) ([A-Z]) ([\d\.]+)",line)
    if(match is None): continue

    fileTime = match.group(1)
    source = match.group(2)
    dest = match.group(3)
    #targetEdge = reorder(match.group(2), match.group(3))
    duration = match.group(4)

    print "Line",str(count),"/ Current time is", time.time() - startTime

    #Choose which routing algorithm to run
    if(algorithm == "SHP"):

    	#----------------------------------------------
        continue    #leave this uncommented for testing
        #----------------------------------------------

        #grab path from saved values or run algorithm if not found
        path = checkSaved(reorder(source,dest))
        if(path is None):
        	path = shortestHop(source, dest, Graph)
        	routes[reorder(source,dest)] = path
        	print "Ran algo !"
        else:
        	print "Found a saved path!",reorder(source,dest)


    elif(algorithm == "SDP"):
        #ShortestDelay()
        continue
    else:
        LeastLoad()

#Finish parsing workload file
work.close()

#Testing area
if(algorithm == "SHP"): SHPTest()
elif(algorithm == "SDP"): SDPTest()
print "End of Prog -->",str(time.time()-startOfProgram)
