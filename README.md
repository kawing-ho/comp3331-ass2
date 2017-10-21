
### Notes for time simulation

* Treat time as iteration(s)
* startTime = 0.000000
* every iteration we add one to startTime

* each Task from workload file would have their own
	* requestStart = x
	* requestEnd = x + (duration)

* between time (think iterations) requestStart and requestEnd, some edges will have y load
* after that the y load is removed

* so we need to have a job queue
* read lines from workload.txt and add all of them to the queue
* then at the start of each loop we check 
	* first item in the queue (is it time yet ?)
	* if its time what should we do ?
		* if its start then try to establish connection (pass = fine) (fail = block)
		* if its end then free up resources

* need some data structure to store all the active connections 
	* every (1 / packetRate) seconds (again think iterations) we need to add 1 to their packetCount
	* collect statistics (maybe there might be a more efficient way)

* how do we know when to stop ? 
* I guess when theres no more jobs left and the active connection dataStructure list is empty

* after everything is done we just calculate the statistics and print ?? should be okay right
