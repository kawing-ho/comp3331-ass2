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
def tuple_compare(a, b):
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
		PriorityQueue.sort(tuple_compare)

	res = []
	node = dest
	while True:
		res = [node] + res
		if node in path: node = path[node]
		else : break


	return res


#Main algorithm for computing routes (depending on algorithm)
#input : Source, Dest, Graph, algorithm
#output: Path as a list from Src -> Dest
def dijkstra(source, dest, graph):
	path = {}								#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];			#PQ stores tuple of (node,totalWeightFromSource)
	visited = set()

	while PriorityQueue:

		#Get node + weight so far from top of PQ
		currentNode, weightToCurrentNode = PriorityQueue.pop(0)

		#Get neighbours of this node, also compute the proper weightages
		for neighbour in getNeighbours(currentNode,graph):
			if neighbour in visited: continue		#prevent looping / backtracking

			currentEdge = reorder(currentNode,neighbour)

			#choose weight of edge depending on what algo is running
			if  (algorithm == "SDP"): currentWeight = getDelayOfEdge(currentEdge)
			elif(algorithm == "LLP"): currentWeight = getLoadOfEdge(currentEdge)
			else               : currentWeight = 1  #for SHP

			#print neighbour,":Considering",currentEdge,"->",currentWeight,"from",currentNode,"with",weightToCurrentNode

			comparativeWeight = currentWeight + weightToCurrentNode  	#value to compare with one on the queue
			originalWeight = dict(PriorityQueue).get(neighbour, None)  	#value found on the queue (if any)

			#if that node is already in the PriorityQueue do triangulation
			if(originalWeight is not None):

				#don't have to change anything if the originalWeight is less 
				if(comparativeWeight < originalWeight):

					#Change the originalWeight in PQ to the comparativeWeight
					PriorityQueue.remove((neighbour,originalWeight))		#tuples can't be edited
					PriorityQueue.append((neighbour,comparativeWeight))		#so have to remove and re-add again

					#Change path to pass through current node instead
					path[neighbour] = currentNode

			else:
				PriorityQueue.append((neighbour,weightToCurrentNode + currentWeight))
				path[neighbour] = currentNode

		PriorityQueue.sort(tuple_compare)			#reshuffle the PQ (sort by propDelay)
		visited.add(currentNode)					#add currentNode to finished list

	#reconstruct the path into a list
	res = []
	node = dest
	while True:
		res = [node] + res
		if node in path: node = path[node]
		else : break

	return res


def SHPTest():
	print "=== Testing out SHP with A and D ==="
	#print str(shortestHop('A', 'D', Graph))
	print str(dijkstra('A', 'D', Graph))
	print "=== Testing out SHP A and B ==="
	#print str(shortestHop('A', 'B', Graph))
	print str(dijkstra('A', 'B', Graph))
	print "=== Testing out SHP D and C ==="
	#print str(shortestHop('D', 'C', Graph))
	print str(dijkstra('D', 'C', Graph))
	print "=== Testing out SHP D and A ==="
	#print str(shortestHop('D', 'A', Graph))
	print str(dijkstra('D', 'A', Graph))


	if('G' not in getNodes(Graph)): return
	print " *** Topology.txt ***"
	print "=== Testing out SHP G and I ==="
	#print str(shortestHop('G', 'I', Graph))
	print str(dijkstra('G', 'I', Graph))
	print "=== Testing out SHP I and G ==="
	#print str(shortestHop('I', 'G', Graph))
	print str(dijkstra('I', 'G', Graph))
	print "=== Testing out SHP D and O ==="
	#print str(shortestHop('D', 'O', Graph))
	print str(dijkstra('D', 'O', Graph))
	print "=== Testing out SHP M and E ==="
	#print str(shortestHop('M', 'E', Graph))
	print str(dijkstra('M', 'E', Graph))

def SDPTest():
	print "************Testing SDP******************"
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
	print "\n========F to O=============="
	print str(dijkstraSDP('F', 'O', Graph))
	print "\n========K to L=============="
	print str(dijkstraSDP('K', 'L', Graph))
	print "\n========I to G=============="
	print str(dijkstraSDP('I', 'G', Graph))
	print "\n========M to A=============="
	print str(dijkstraSDP('M', 'A', Graph))
	print "\n========E to I=============="
	print str(dijkstraSDP('E', 'I', Graph))

	print "***************Testing dijkstra**************"
	print "\n========A to D=============="
	print str(dijkstra('A', 'D', Graph))
	print "\n========A to F=============="
	print str(dijkstra('A', 'F', Graph))
	print "\n========A to E=============="
	print str(dijkstra('A', 'E', Graph))
	print "\n========F to C=============="
	print str(dijkstra('F', 'C', Graph))
	print "\n========E to C=============="
	print str(dijkstra('E', 'C', Graph))
	print "\n========A to A=============="
	print str(dijkstra('A', 'A', Graph))
	print "\n========F to O=============="
	print str(dijkstra('F', 'O', Graph))
	print "\n========K to L=============="
	print str(dijkstra('K', 'L', Graph))
	print "\n========I to G=============="
	print str(dijkstra('I', 'G', Graph))
	print "\n========M to A=============="
	print str(dijkstra('M', 'A', Graph))
	print "\n========E to I=============="
	print str(dijkstra('E', 'I', Graph))

def LLPTest():
	return None


def getDelayOfEdge(edge): return int(Graph[edge]['delay'])
def getLoadOfEdge(edge): return int(Graph[edge]['load'])

def increaseLoad(edge): Graph[edge]["load"]+= 1
def decreaseLoad(edge):	Graph[edge]["load"]-= 1

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
	path = {}								#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];			#PQ stores tuple of (node,totalDelayFromSource)
	visited = set()

	while PriorityQueue:

		#Get node + delay so far from top of PQ
		currentNode, delayToCurrentNode = PriorityQueue.pop(0)

		#Get neighbours of this node, also compute the proper weightages
		for neighbour in getNeighbours(currentNode,graph):
			if neighbour in visited: continue		#prevent looping / backtracking

			currentEdge = reorder(currentNode,neighbour)
			currentDelay = getDelayOfEdge(currentEdge)

			#print neighbour,":Considering",currentEdge,"->",currentDelay,"from",currentNode,"with",delayToCurrentNode

			comparativeDelay = currentDelay + delayToCurrentNode  		#value to compare with one on the queue
			originalDelay = dict(PriorityQueue).get(neighbour, None)  	#value found on the queue (if any)

			#if that node is already in the PriorityQueue do triangulation
			if(originalDelay is not None):

				#don't have to change anything if the originalDelay is less 
				if(comparativeDelay < originalDelay):

					#Change the originalDelay in PQ to the comparativeDelay
					PriorityQueue.remove((neighbour,originalDelay))			#tuples can't be edited
					PriorityQueue.append((neighbour,comparativeDelay))		#so have to remove and re-add again

					#Change path to pass through current node instead
					path[neighbour] = currentNode

			else:
				PriorityQueue.append((neighbour,delayToCurrentNode + currentDelay))
				path[neighbour] = currentNode

		PriorityQueue.sort(tuple_compare)			#reshuffle the PQ (sort by propDelay)
		visited.add(currentNode)					#add currentNode to finished list

	#reconstruct the path into a list
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
	duration = match.group(4)

	#print "Line",str(count),"/ Current time is", time.time() - startTime

	#==============================================
	continue    #leave this uncommented for testing
	#==============================================

	#grab a saved path or run the algorithm if not found
	path = checkSaved(reorder(source,dest))
	if(path is None):
		path = dijkstra(source, dest, Graph)	#algorithm is global so no need to pass in
		routes[reorder(source,dest)] = path
	else:
		print "Used a saved path !"

	#convert nodes across path into edges
	# update = []
	# for index, node in enumerate(path):
	# 	if(node == path[-1]): continue 	#skip last element
	# 	update.append(reorder(node,path[index+1]))

	# #do the actual updating to the graph
	# [increaseLoad(edge) for edge in update]

#Finish parsing workload file
work.close()





#Testing area
if(algorithm == "SHP"): SHPTest()
elif(algorithm == "SDP"): SDPTest()
else: LLPTest()
print "End of Prog -->",str(time.time()-startOfProgram)
