
Seems like my concept of capacity was wrong (This is what a tutor said):
- Capacity of 20 means can support 20 connections simultaneously
- If the link was completely empty then you could send 20 packets through it where each packet would take 0.5s (if PacketRate was 2)
- However if there were other connections going through it like maybe 6 then you would only have 14
- packets are sent one at a time and everytime before sending we check the availability of the link
- When a packet is sent the capacity goes down by 1 and after 0.5 second it goes back up by 1
- If a packet tries to get sent while theres no more capacity then it's counted as BLOCKED
- In circuit a blocked packet would never occur midway as the whole connection would have been blocked since the beginning



### Pseudocode for packet handling:

```python
request = work.readline()              <-- start off by reading the very first line
readyForNextLine = FALSE               <-- boolean flag which sees if the next line is ready to be read
timeOfNextRequest = getTime(request)




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
```