

# The Coordinator must satisfy the following:
# 	1. It must contain a packet pool/queue, representing
#      packets that need to be sent. 
#   2. It must keep track of all worker nodes, which include:
#		-> Worker nodes currently processing data;
#		-> Worker nodes currently not processing data (unavailable)
#		-> Worker nodes currently not processing data (available)

"""
At any given time, a worker node is either processing data or it is not. 
Worker nodes must have time-outs configured for them. 
'Heart-beat' messages/pings are received from the client, both 
synchronously and asynchronously. Type of messages from the client include:
	- Connection established; 
	- Acknowledgement per 1000 info. datums processed, or if packet
	  contains data less than length 1000, acknowledgement per length of
	  packet data;
	- Match found;
	- Complete; i.e., no longer available to process data. 
	- Available - hey! pick me, pick me! 

"""

class Coordinator:
	def __init__( self ):

# Special function that re-packetises -- I've got a time-out from a worker - don't give __init__
# any more data. 
