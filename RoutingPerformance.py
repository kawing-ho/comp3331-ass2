#!/usr/bin/python
#COMP3331 Assignment2
#z5087077 Ka Wing Ho
#z5113471 Andy Yang

import sys, re
import time, math, threading

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

# input : Source, Dest, Graph, algo
# output: Path as a list from Src -> Dest
def dijkstra(source, dest, graph, algorithm):
	path = {}						#Path is dict going backwards eg. path[B] = A
	PriorityQueue = [(source,0)];   #PQ stores tuple of (node,distanceFromSource)
	visited = set()
	neighbours = set()
	nodes = getNodes(graph)

	while true:

		currentNode, currentDistance = PriorityQueue.pop(0)		#get node from PQ
		visited.add(currentNode)								#add node to visited

		#if node is GOAL, fill out path and break
		if(currentNode == dest):
			print("Found destination !")
			break


		# I don't know how to do the triangulation thing where if A->C = 7 but A->B->C = 5 then change 7 to 5
		# will look into that later as well ...
		
		# look at neighbours and consider weights
		for edge in currentNode.getEdges:
			for node in edge: neighbours.add(node)

		for neighbour in neighbours:
			if neighbour in visited: continue					#if neighbour in visited skip
			currentEdge = reorder(neighbour,currentNode)
			weight = 1 											#in the case of SHP weight = 1 for each edge
			PriorityQueue.append((neighbour,currentDistance + weight))
		

			#default behaviour: path[neighbour] = currentNode
			path[neighbour] = currentNode
			#advanced behaviour: triangulation will alter the path to something else if needed

		#reshuffle PQ (sort by distance)
		print str(PriorityQueue)    #before

		print str(PriorityQueue)    #after


	#deconstruct / reconstruct path :
	# eg. path[dest] = mid, path[mid] = source,
	# res = []
	# res = dest + []
	# res = mid + dest + []
	# res = source + mid + dest

	res = []
	node = dest
	while (node != source):
		res = [node] + res
		node = path[node]

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


print time.time()-startOfProgram
print getNodes(Graph)



'''
Similarities and Differences of Virtual Circuit / Virtual Packet

- Number of requests = number of lines in workload file
- When a path is determined, the whole path is reserved for that time frame (eg. A->B->D for time 0-0.5 load increase by 1)
- In some cases even though the packets are blocked the reservation still happens and the request is still counted (I'll look more into this later)*
- once the path has been chosen and if we encounter that one of the links is fully occupied, either that individual packet is dropped (for VP) or the whole
  request is dropped (for VC)
-


- in VC algorithm only needs to be run once
- in VP algorithm needs to be run once for each packet (and the scenarios (aka load) may change in between runs)

'''

'''
Cases to consider:
- Have to keep track of dozens of individual durations and start/end times
- Only have one single unified timer 
- Time doesn't wait for us when we are doing calculations (especially if we're trying to be precise)


How I'd like to do it:
- List/Dict of connections indexed by start time (as time moves forward we grab the first element off the list)
   eg.  Connections[]
        Connections[0.1234] = {edge, duration}
        Connections[0.3456] = {edge, duration}
- That would be the connection we are interested in at the moment, do whatever we need to do with it, and then delete the list element when we're done

Problems of doing it this way:
- If we delete it how do we know where to free up the connection from when the pakcets are sent 
- Spec says we need to do it line by line from workload file, this method wouldn't really work properly if we did that 
- 


- We have a global variable to indicate the next "CloseConnectionEvent", every loop we check for this Event 
  eg. if the very first connection starts at 0.1 and lasts for 12 seconds then the first CloseConnectionEvent will be at 12.1s
  in between now and then we can either wait or do other things , once the time hits 


- The way the spec wants us to do it is 
   - for each line in workload file
   - read , parse , chuck it into the algorithm 
   - algorithm determines what path to take
   - network scheme determines the timing for the packet(s) as well as how many times the algorithm will run
   - duration of which resource is consumed 

   - move on to next line

'''