from packet_pool import PacketQueue
from worker_pool import WorkerHeap
from database import Database 
from worker import Worker

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
		self.worker_buffer = WorkerHeap( 10, True )
		self.packet_pool = PacketQueue() # Packet pool should serve as a buffer
		self.worker_pool = WorkerHeap()

	# -- START HELPER FUNCTION SECTION -- #
	def worker_available( self ):
		if ( self.worker_buffer.size() > 0 ):
			return True
		return False
	def get_worker( self ):
		return self.worker_buffer.delete_min()

	# This function should be invoked
	# before invoking the proceeding function, 
	# get_packet(). 
	def packet_available( self ):
		if ( packet_pool.size() > 0 ):
			return True
		return False
	def get_packet( self ):
		return self.packet_pool.dequeue()
	# -- END HELPER FUNCTION SECTION -- #

	def fill_worker_buffer( self ):
		if ( ( self.worker_pool.empty() == False ) & 
			( self.worker_buffer.size() < self.worker_buffer.get_capacity() ) ):
			min = self.worker_pool.dequeue()
			print( "min: " + str( min ) )
			if ( min != None ):
				self.worker_buffer.insert( min )




# Special function that re-packetises -- I've got a time-out from a worker - don't give __init__
# any more data. 

if __name__ == "__main__":
	# Just testing functionality. 
	coordinator_instance = Coordinator()
	# Just to assist prototyping; not the actual database!
	database = Database()
	worker_1 = Worker( 1, 1, 40 )
	worker_1.set_connected( True )
	worker_1.set_busy( False )
	worker_2 = Worker( 2, 2, 50 )
	worker_3 = Worker( 3, 3, 40 )
	worker_4 = Worker( 4, 4, 30 )
	print( "coorinator: " + str( coordinator_instance ) )
	worker_pool = coordinator_instance.worker_pool
	worker_pool.insert( worker_1 )
	worker_pool.insert( worker_2 )
	worker_pool.insert( worker_3 )
	worker_pool.insert( worker_4 )

	coordinator_instance.fill_worker_buffer()
	print( "Worker buffer: " + str( coordinator_instance.worker_buffer ) )





