#!/usr/bin/python
#COMP3331 Assignment2 
#z5087077 Ka Wing Ho 
#z5113471 Andy Yang 

import sys, re

#Code referrenced from: http://www.bogotobogo.com/python/python_graph_data_structures.php
#Graph has nodes / Nodes have edges / Edges have Capacity + Prop Delay tuple

'''
So I decided its better to not make a separate Graph object because dealing with duplicates is a pain in the ass
Instead I propose we use this way of using graphs instead 
- Dictionary of dictionaries to represent fields in edges  (edges are the keys)
- eg.  Graph = {}
       Graph["AB"] = {"delay":10,"max",5,"load",0}

       then we can access these fields easily 
       if we want to get/set the load of edge AB just do 

       ABLoad = Graph["AB"]["load"]
       or  Graph["AB"]["load"] = newABLoad

       if we need to add new fields simply do

       Graph["AB"]["newFIeld"] = newValue 

Some issues that we have to deal with (but should be easily done)
Edges may come in wrong order eg. AB or BA (but we can have some convention like stricly sorted alphabetically edges)

How do we find edges based on vertex ? eg. given C I need to consider all edges like AC , CD , CE,  FC .... (again see above)
- to solve this we can just write a function to do Graph.keys() and return a list of all keys which contain "C" 
'''

#returns the correct order of edge eg. "AB" -> "AB" , "BA" -> "AB"
def reorder(one,two): return (one + two) if (ord(one) < ord(two)) else (two + one);

#return list of edges that involve that node
def getEdges(node,g): return [edge for edge in g if node in edge]

#SHP algorithm
def ShortestHop():
	print("Shortest Hop Path !")

#SDP algorithm
def ShortestDelay():
	print("Shortest Delay Path !")

#LLP algorithm 
def LeastLoad():
	print("Least Load Path !")



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

print "\nCan we find C ?"      # ------------------------
myList = getEdges("C",Graph.keys())   #  EXAMPLE , DELETE LATER
print myList				   # ------------------------


#Parse workload file 
for line in work.readlines():
	match = re.search("(\d+) ([A-Z]) ([A-Z]) (\d+)",line)

	time = match.group(1)
	targetEdge = reorder(match.group(2), match.group(3))
	duration = match.group(4)

	#the type of network scheme defines the behaviour of the algorithms ?  (not sure yet tbh)

	#Choose which routing algorithm to run
	if(algorithm == "SHP"): 
		ShortestHop()
	elif(algorithm == "SDP"): 
		ShortestDelay()
	else:
		LeastLoad()


work.close()
