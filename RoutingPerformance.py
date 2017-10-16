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


'''