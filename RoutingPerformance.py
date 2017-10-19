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

#returns the correct order of edge eg. "AB" -> "AB" , "BA" -> "AB"
def reorder(one,two): return (one + two) if (ord(one) < ord(two)) else (two + one);

#return list of edges that involve that node
def getEdges(node,g): return [edge for edge in g if node in edge]

#return neighbours of a node
def getNeighbours(node,g):
	return None

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

#SHP algorithm
#All weights = 1 since only hops counted (same for all edges)
def ShortestHop():
	print("Shortest Hop Path !")

#SDP algorithm
#Weight = delay of that edge (constant but different for every edge)
def ShortestDelay():
	print("Shortest Delay Path !")

#LLP algorithm
#Weight = Load of that edge (very volatile as it can change in the middle of a connection)
def LeastLoad():
	print("Least Load Path !")

def SDPTest(graph):
	print "Testing SDP"
	print "graph is <",graph,">"
	print json.dumps(graph, indent=4)
	print "\n========A to D=============="
	print str(dijkstraSDP('A', 'D', Graph, algorithm))
	print "\n========A to F=============="
	print str(dijkstraSDP('A', 'F', Graph, algorithm))
	exit(1)

#input: edges
#output: sorts edges according to delay time
def sortDelay(graph, edges):
	newEdges = {}
	delaytime = getDelayTime(graph)
	for value in delaytime:
		edge,delay = value
		if(edge in edges):
			newEdges[edge] = delay
	#LOL THIS ISNT THE WAY I WANT TO DO THIS
	#newEdges = sorted(newEdges.iteritems(), key=lambda (k,v): (v,k))
	return newEdges

#returns an dictionary of delay from the graph sorted in accenditing
#order from lower delay time to highest delay time
def getDelayTime(graph):
	if graph == None: return None
	delaytime = {}
	for edge in graph:
		delaytime[edge] = int(graph[edge]['delay'])
	delaytime = sorted(delaytime.iteritems(), key=lambda (k,v): (v,k))
	return delaytime


# input : Source, Dest, Graph, algo
# output: Path as a list from Src -> Dest but using the shortest delay time
def dijkstraSDP(source, dest, graph, algorithm):
	if(source not in getNodes(graph) or dest not in getNodes(graph)): return None
	path = {}						#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];   #PQ stores tuple of (node,distanceFromSource)
	delay = {}
	visited = set()
	neighbours = set()
	nodes = getNodes(graph)
	delay[source] = 0

	while True:
		(currentNode, currentDistance) = PriorityQueue.pop(0) #Take of first element
		visited.add(currentNode)
		if(currentNode == dest):							# Check if node is destination
			print("Found destination !")
			break
		edges = getEdges(currentNode, graph)
		edges = sortDelay(graph, edges)
		for edge,time in sorted(edges.iteritems(), key=lambda (k,v): (v,k)):
			for node in edge:
				neighbours.add(node)
		print "edges is |", edges
		print "neighbours is |", neighbours
		for neighbour in neighbours:
			if neighbour in visited:
				continue
			else:
				visited.add(neighbour)
			currentEdge = reorder(neighbour,currentNode)
			weight = 1
			print "Adding " + neighbour + " " + str(currentDistance + weight) + " to PriorityQueue "
			PriorityQueue.append((neighbour,currentDistance + weight))
			path[neighbour] = currentNode
			tempdelay= graph[currentEdge]["delay"]
			delay[neighbour] = delay[currentNode] + int(tempdelay)
		print "path is |",path
		print "delay is |",delay
		print str(PriorityQueue)    #before
		PriorityQueue.sort(distance_compare)
		print str(PriorityQueue)    #after

		res = []
		node = dest
		while True:
			res = [node] + res
			if node in path:
				node = path[node]
			else:
				break
		print "----"
		print res
	return res


# input : Source, Dest, Graph, algo
# output: Path as a list from Src -> Dest
def dijkstra(source, dest, graph, algorithm):
	if(source not in getNodes(graph) or dest not in getNodes(graph)): return None
	path = {}						#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];   #PQ stores tuple of (node,distanceFromSource)
	visited = set()
	neighbours = set()
	nodes = getNodes(graph)

	while True:

		currentNode, currentDistance = PriorityQueue.pop(0)		#get node from PQ
		#print "Just popped off " + currentNode + " " + str(currentDistance)
		visited.add(currentNode)								#add node to visited

		#if node is GOAL, fill out path and break
		if(currentNode == dest):
			print("Found destination !")
			break


		# I don't know how to do the triangulation thing where if A->C = 7 but A->B->C = 5 then change 7 to 5
		# will look into that later as well ...

		# look at neighbours and consider weights
		for edge in getEdges(currentNode, graph):
			for node in edge: neighbours.add(node)

		for neighbour in neighbours:
			if neighbour in visited: continue					#if neighbour in visited skip
			else: visited.add(neighbour)
			currentEdge = reorder(neighbour,currentNode)
			weight = 1 											#in the case of SHP weight = 1 for each edge
			print "Adding " + neighbour + " " + str(currentDistance + weight) + " to PQ "
			PriorityQueue.append((neighbour,currentDistance + weight))


			#default behaviour: path[neighbour] = currentNode
			path[neighbour] = currentNode
			#advanced behaviour: triangulation will alter the path to something else if needed

		#reshuffle PQ (sort by distance)
		print str(PriorityQueue)    #before
		PriorityQueue.sort(distance_compare)
		print str(PriorityQueue)    #after


	#deconstruct / reconstruct path :
	# eg. path[dest] = mid, path[mid] = source,
	# res = []
	# res = dest + []
	# res = mid + dest + []
	# res = source + mid + dest

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

Graph = {} #Graph is a dict containing dicts
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

    print str(edge) + " -> " + str(Graph[edge])  #EXAMPLE , DELETE LATER

#Finish graph initialization
top.close()


print "It takes ",time.time()-startOfProgram,"to finish initialization"
print "\nCan we find C ?"             # ------------------------
myList = getEdges("C",Graph.keys())   #  EXAMPLE , DELETE LATER
print myList				          # ------------------------

startTime = time.time()
#Parse workload file
for line in work.readlines():
    match = re.search("([\d\.]+) ([A-Z]) ([A-Z]) ([\d\.]+)",line)
    if(match is None): continue

    Wingstime = match.group(1)
    targetEdge = reorder(match.group(2), match.group(3))
    duration = match.group(4)

    #the type of network scheme defines the behaviour of the algorithms ?  (not sure yet tbh)
    print "Current time is", time.time() - startTime
    #Choose which routing algorithm to run
    if(algorithm == "SHP"):
        ShortestHop()
    elif(algorithm == "SDP"):
        ShortestDelay()
    else:
        LeastLoad()


work.close()


if algorithm == "SDP": SDPTest(Graph)
print time.time()-startOfProgram
print "=== Testing out Dijkstra with A and D ==="
print str(dijkstra('A', 'D', Graph, algorithm))

print "=== Testing out Dijkstra A and B ==="
print str(dijkstra('A', 'B', Graph, algorithm))
print "=== Testing out Dijkstra D and C ==="
print str(dijkstra('D', 'C', Graph, algorithm))
print "=== Testing out Dijkstra D and A ==="
print str(dijkstra('D', 'A', Graph, algorithm))

print " *** Topology.txt ***"
print "=== Testing out Dijkstra G and I ==="
print str(dijkstra('G', 'I', Graph, algorithm))
print "=== Testing out Dijkstra I and G ==="
print str(dijkstra('I', 'G', Graph, algorithm))
print "=== Testing out Dijkstra D and O ==="
print str(dijkstra('D', 'O', Graph, algorithm))

'''
Seems like my concept of capacity was wrong (This is what a tutor said):
- Capacity of 20 means can support 20 connections simultaneously
- If the link was completely empty then you could send 20 packets through it where each packet would take 0.5s (if PacketRate was 2)
- However if there were other connections going through it like maybe 6 then you would only have 14
- packets are sent one at a time and everytime before sending we check the availability of the link
- When a packet is sent the capacity goes down by 1 and after 0.5 second it goes back up by 1
- If a packet tries to get sent while theres no more capacity then it's counted as BLOCKED
-
- In circuit a blocked packet would never occur midway as the whole connection would have been blocked since the beginning
'''

'''
request = work.readline()              <-- start off by reading the very first line
readyForNextLine = FALSE               <-- boolean flag which sees if the next line is ready to be read
timeOfNextRequest = getTime(request)

===============================
Pseudocode for packet handling:
===============================

start = time.time()
while True:                             <---- no time restriction on this outer loop, whereas time restrictions happen INSIDE
	currentTime = time.time() - start   <---- get Time of current loop iteration

	if(readyForNextLine):
		request = work.readline()
		if(request is None):            <---- no more requests
			readyForNextLine = FALSE
			timeOfNextRequest = -1
		else:
			timeOfNextRequest = getTime(request)  <---- update the time of the next request so it knows when to start the next connection


	#Processing new request  <-- this part runs when the timeOfNextRequest >= currentTime
								 (however this will produce inaccurate timing , need to refine somehow)

	if(timeOfNextRequest >= currentTime):
		readyForNextLine = TRUE

		source = getSource(request)
		dest = getDest(request)
		duration = getDuration(request)

		#compute shortest path while ignoring capacities of links

		if algorithm == "SHP": shortestPath = SHP(source,dest,graph)  <-- Note that the graph must be kept updated at all times
		elif algorithm == "SDP": shortestPath = SDP(source,dest,graph)
		else: shortestPath = LLP(source,dest,graph)


		#note that each new request has to go through this step so techincally you wouldn't have any cases
		#where a block would happen midway for any two requests

		if(capacity of shortestPath can accomodate the request):

			add to list/queue/whatever of existing requests as standard procedure


		else: block all packets for this request




	#Processing existing requests (happens every 1/PacketRate seconds , default would be every 0.5 seconds)

	pauseTime  <-- to simulate simultaneous use of connections across all requests
	           <-- basically the following block of code runs while time is paused
	           <-- and then at the end 1/PacketRate seconds is added to the timer
	           <-- in real life it would probably take a lot longer
	           <-- since there could be dozens of events each taking 1/PacketRate seconds to run
	               (but in reality we want all of them to run at the same time)

	for each existing request:         <-- this loop only sends one packet per request per iteration of OUTER LOOP
	                                   <-- hope you get this part lol coz i find it hard to explain

		if request is done (reached end of duration or can't send anymore packets):
				remove it from list/queue/whatever

		process request
			increment capacity
			do stuff like send a packet
			decrement capacity
			....

		repeat across all existing/unfulfilled requests


	resumeTime


	> need to maintain tiny bit of state across time frames
	-> eg. at time 0.5 connection A uses up capacity (1) , at time 1.0 A releases (1) capacity but also decides to use capacity (1) again for another packet cycle
	-> at time 1.5 connection A has reached its duration then it releases capacity (1) and doesn't reuse again
	-> at time 0.5 other connections will know that connection A is using (1) capacity, and also at time 1.0, finally at time 1.5 the other connections will
	   know that connection A has released its (1) capacity,

	->but the problem is that the code to release A at time 1.5 is in the same time frame as the other connections checking for open connections, this would cause
	  inconsistensies / race conditions :(  , unless I put the code for releasing outside the for loop ?

	  -> will think more about it tomorrow ...


'''
