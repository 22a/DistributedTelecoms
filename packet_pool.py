from Queue import Queue
from errors import EmptyQueueException


class PacketQueue:
	# @param: Initial size of queue (defaults to 0). 
	def __init__( self, size = 0 ):
		self.packet_queue = Queue()

	# Returns: True if the queue does not contain
	# any queued packets. 
	def empty( self ):
		return self.packet_queue.empty()

	# @param: A packet to be added to the packet queue. 
	# Behaviour: Adds a packet to the packet queue. 
	def enqueue( self, queued_packet ):
		self.packet_queue.put( queued_packet )

	# Returns: A packet. 
	# Throws: User-defined EmptyQueueException
	# if the packet queue does not contain any packets. 
	# Behaviour: Dequeues packets in F.I.F.O. order. 
	def dequeue( self ):
		if ( self.size() > 0 ):
			return self.packet_queue.get()
		else:
			raise EmptyQueueException( "No elements in packet queue." )

	# Returns: Size of packet queue. 
	def size( self ):
		return self.packet_queue.qsize()

if __name__ == "__main__":	
	# Rudimentary, informal tests. 
	a_queue = PacketQueue()
	try:
		a_queue.enqueue( 1 )
		a_queue.enqueue( 2 )
	except NameError, e:
		print str( e )
	else:
		pass
	finally:
		pass
	
	try:
		a_queue.dequeue()
		a_queue.dequeue()
		a_queue.dequeue()
	except EmptyQueueException, e:
		print str( e )
	else:
		pass
	finally:
		pass
	
