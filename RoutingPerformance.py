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
# I wanna shorten this later lol
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
#Weight = 1 (same across all edges)
#input : Source, Dest, Graph
#output: Path as a list from Src -> Dest
def ShortestHop(source, dest, graph):
	path = {}						#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];   #PQ stores tuple of (node,distanceFromSource)
	visited = set()
	neighbours = set()
	nodes = getNodes(graph)

	while True:

		currentNode, currentDistance = PriorityQueue.pop(0)		#get node from PQ
		visited.add(currentNode)								#add node to visited

		if(currentNode == dest): break							#break if goal found

		# look at neighbours and consider weights
		for neighbour in getNeighbours(currentNode,graph):
			if neighbour in visited: continue					#skip if seen neighbour before
			else: visited.add(neighbour)

			currentEdge = reorder(neighbour,currentNode)
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
def ShortestDelay():
	return None

#LLP algorithm
#Weight = Load of that edge (very volatile as it can change in the middle of a connection)
def LeastLoad():
	return None

def SHPTest(graph):
	print "=== Testing out SHP with A and D ==="
	print str(ShortestHop('A', 'D', graph))

	print "=== Testing out SHP A and B ==="
	print str(ShortestHop('A', 'B', graph))
	print "=== Testing out SHP D and C ==="
	print str(ShortestHop('D', 'C', graph))
	print "=== Testing out SHP D and A ==="
	print str(ShortestHop('D', 'A', graph))

	if('G' not in getNodes(graph)): return
	print " *** Topology.txt ***"
	print "=== Testing out SHP G and I ==="
	print str(ShortestHop('G', 'I', graph))
	print "=== Testing out SHP I and G ==="
	print str(ShortestHop('I', 'G', graph))
	print "=== Testing out SHP D and O ==="
	print str(ShortestHop('D', 'O', graph))
	print "=== Testing out SHP M and E ==="
	print str(ShortestHop('M', 'E', graph))


def SDPTest(graph):
	print "Testing SDP"
	print "graph is <",graph,">"
	print json.dumps(graph, indent=4)
	print "\n========A to D=============="
	print str(dijkstraSDP('A', 'D', graph))
	print "\n========A to F=============="
	print str(dijkstraSDP('A', 'F', graph))
	print "\n========A to E=============="
	print str(dijkstraSDP('A', 'E', graph))
	print "\n========F to C=============="
	print str(dijkstraSDP('F', 'C', graph))
	print "\n========E to C=============="
	print str(dijkstraSDP('E', 'C', graph))
	print "\n========A to A=============="
	print str(dijkstraSDP('A', 'A', graph))

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

#Prototype for SDP
#input : Source, Dest, Graph
#output: Path as a list from Src -> Dest but using the shortest delay time
def dijkstraSDP(source, dest, graph):
	if(source not in getNodes(graph) or dest not in getNodes(graph)): return None
	path = {}						#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];   #PQ stores tuple of (node,distanceFromSource)
	delay = {}
	visited = set()
	neighbours = set()
	nodes = getNodes(graph)
#	for i in nodes:
#		delay[i] = 0
	delay[source] = 0

	while True:
		(currentNode, currentDistance) = PriorityQueue.pop(0) #Take of first element
		visited.add(currentNode)

		if(currentNode == dest): break			# Check if node is destination
			
		edges = getEdges(currentNode, graph)
		edges = sortDelay(graph, edges)
		for edge,time in sorted(edges.iteritems(), key=lambda (k,v): (v,k)):
			for node in edge:
				neighbours.add(node)
		print "edges is |", edges
		print "neighbours is |", neighbours
		for neighbour in neighbours:
			if (neighbour in visited):
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
		print str(PriorityQueue)

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
print "It takes ",time.time()-startOfProgram,"to finish initialization"

startTime = time.time()
#Parse workload file
for count,line in enumerate(work.readlines()):
    match = re.search("([\d\.]+) ([A-Z]) ([A-Z]) ([\d\.]+)",line)
    if(match is None): continue

    Wingstime = match.group(1)
    targetEdge = reorder(match.group(2), match.group(3))
    duration = match.group(4)

    print "Line " + str(count) + " / Current time is", time.time() - startTime

    #Choose which routing algorithm to run
    if(algorithm == "SHP"):
    	#SHPTest(Graph)
        #ShortestHop()
        continue
    elif(algorithm == "SDP"):
    	#SDPTest(Graph)
        #ShortestDelay()
        continue
    else:
        LeastLoad()

#Finish parsing workload file
work.close()

#Testing area
if(algorithm == "SHP"): SHPTest(Graph)
elif(algorithm == "SDP"): SDPTest(Graph)
print "End of Prog --> " + str(time.time()-startOfProgram)



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
