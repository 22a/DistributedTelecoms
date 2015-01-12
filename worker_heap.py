from Queue import Queue
#from server_test import *
from errors import *

class WorkerHeap:
	def __init__(self, capacity = 10000):
		self.capacity = capacity
		self.queue = Queue()

	# Returns: True if the queue does not contain
	# any queued packets. 
	def empty( self ):
		return self.queue.empty()

	# @param: A packet to be added to the packet queue. 
	# Behaviour: Adds a packet to the packet queue. 
	def insert( self, queued_worker ):
		self.queue.put( queued_worker )

	# Returns: A packet. 
	# Throws: User-defined EmptyQueueException
	# if the packet queue does not contain any packets. 
	# Behaviour: Dequeues packets in F.I.F.O. order. 
	def dequeue( self ):
		if ( self.size() > 0 ):
			return self.queue.get()
		else:
			raise EmptyQueueException( "No elements in packet queue." )

	# Returns: Size of packet queue. 
	def size( self ):
		return self.queue.qsize()

	def capacity(self):
		return self.capacity
