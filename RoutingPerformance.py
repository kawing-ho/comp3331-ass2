#!/bin/usr/python
#COMP3331 Assignment2 
#z5087077 Ka Wing Ho 
#z5113471 Andy Yang 

import sys, re

#Just some simple error-checking in args
if(len(sys.argv) != 6): print "Usage: python RoutingPerformance.py <CIRCUIT/PACKET> <SHP/SDP/LLP> <topology-file> <workload-file> <rate>"; exit()
if(sys.argv[1] != "CIRCUIT") and (sys.argv[1] != "PACKET"): print "Incorrect Network Scheme"; exit();
if(sys.argv[2] != "SHP") and (sys.argv[2] != "SDP") and (sys.argv[2] != "LLP"): print "Incorrect Router Scheme"; exit();
if(int(sys.argv[5]) < 1): print "Rate must be positive non-zero integer"; exit()

#try opening the files
try:
	top = open(sys.argv[3]);	work = open(sys.argv[4])
except Exception as e: print str(e); exit()

#the type of network scheme defines the behaviour of the algorithms ? 


#Model data structure from contents of "topology"


#Extract data from "workload"


#Choose which routing algorithm to run



top.close()
work.close()

