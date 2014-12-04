from worker import Worker
"""
Heap's internal representation is an array. 
Each item of the array contains a dict; i.e., key-value pairs, 
where the key denotes a Worker's priority, and the corresponding key
is a reference to the Worker instance. 

Whenever a Worker returns an acknwoledgement, contingent 
upon the acknwoledgement type, its position within the heap is updated. 

Acknowledgement cases:

	1. IF ( PROCESSED A FIXED AMOUNT, BUT AMOUNT PROCESSED != TOTAL NUMBER OF ITEMS ASSIGNED ):
		-> Invoke generate_key(), with the Worker that returned an acknowledgement as an argument
		   passed to the function, and store the key generated as a temporary variable. 
		-> Acquire the Worker's index in the heap, by calling get_index_in_heap() upon 
		   the Worker instance. 
		-> Using the index acquired, change the dict key to the key generated during 
		   first step, leaving the Worker instance unchanged. 
		-> Invoke the reorder() function upon the WorkerHeap, in order to reflect 
		   the changed Worker key. 
	2. IF ( PROCESSED A FIXED AMOUNT, AND AMOUNT == TOTAL NUMBER OF ITEMS ASSIGNED )
	  	-> 

"""

class WorkerHeap:
	def __init__( self, initial_capacity = 100, fixed_size = False ):
		self.heap = [ None ] * initial_capacity
		self.initialise_keys()
		self.N = 0
		self.fixed_size = fixed_size
		self.capacity = initial_capacity

	def initialise_keys( self ):
		for i in range( 0, len( self.heap ) ):
			self.heap[i] = dict([(i+10000, None)])

	def empty( self ):
		return ( self.N == 0 )

	def size( self ):
		return self.N;

	def min( self ):
		return self.heap[1]

	def resize( self, capacity ):
		assert capacity > self.N
		temp = [None] * capacity
		for i in range( 1, self.N + 1 ):
			temp[i] = self.heap[i]
		self.heap = temp

	def reorder( self ):
		i = 1;
		while ( i <= self.N ):
			if ( self.greater( i, i * 2 ) ):
				self.exch( i, i * 2 )
			if ( self.greater( i, i * 2 + 1 ) ):
				self.exch( i, i * 2 + 1 )
			i += 1

	# @param: A Worker instance. 
	# Returns: The Boolean, True, if the Worker 
	# instance passed as an argument was successfully
	# added to the heap. Otherwise, it returns False. 
	# It would return False if the heap were a fixed size 
	# and full. 
	def insert( self, worker ):
		assert( isinstance( worker, Worker ) )
		if ( self.fixed_size == False ):
			if ( self.N == len( self.heap ) - 1 ):
				self.resize( 2 * len( self.heap ) )

			self.N += 1
			if ( self.N > 1 ):
				self.heap[ self.N ] = dict( [( self.generate_key( worker ), worker )] )
				self.swim( self.N );
				assert self.is_min_heap();
			else:
				worker.set_index_in_heap( 1 )
				self.heap[ self.N ] = dict([( self.generate_key( worker ), worker )] )
			return True
		elif ( ( self.fixed_size == True ) & 
			( self.N < self.capacity ) ):
			# add to heap, but do not re-size
			self.N += 1
			if ( self.N > 1 ):
				self.heap[ self.N ] = dict( [( self.generate_key( worker ), worker )] )
				self.swim( self.N );
				assert self.is_min_heap();
			else:
				worker.set_index_in_heap( 1 )
				self.heap[ self.N ] = dict([( self.generate_key( worker ), worker )] )
			return True
		return False



	# Should only be able to 'delete'/dequeue a Worker from 
	# the WorkerHeap if:
	# a) The Worker has processed the set of data assigned to it, 
	#    and it is available to process more. 
	# b) The worker has processed the set of data assigned to it, 
	#    and it is not available to process more. 
	# c) The worker has timed-out. 
	# The function below needs to be modified to reflect the comment above. 
	# It's important to note that what is being deleted is not, 
	# directly, a Worker instance, but rather a key-value pair, where
	# the key is an int representing a Worker instance's priority
	# and the value is the corresponding Worker instance. 
	def delete_min( self ):
		if ( self.empty() ):
			raise Exception( "No elements remaining." )

		self.exch( 1, self.N )
		min = self.heap[ self.N ]
		self.N -= 1
		self.sink( 1 )
		self.heap[self.N+1] = None
		if ( self.fixed_size == False ):
			if ( ( self.N > 0 ) & ( self.N == ( len( self.heap ) -1 )/4 ) ):
				self.resize( len( self.heap )/2 )
		assert self.is_min_heap()
		return min

	# Returns: Worker instance reference. 
	def dequeue( self ):
		should_return = False
		i = 0
		while ( ( i <= self.size() ) & ( self.empty() == False ) ):
			temp = self.delete_min()
			key = temp.keys()[0]
			if ( temp[key].is_busy() ):
				self.insert( temp )
			elif ( temp[key].is_connected() == True ):
				return temp[key] 
			elif ( i > self.size() ):
				i += 1
		return None



	def swim( self, k ):
		while ( k > 1 & self.greater( k/2, k ) ):
			self.exch( k, k/2 )
			k = k/2

	def sink( self, k ):
		while ( 2 * k <= self.N ):
			j = 2 * k
			if ( (j < self.N) & (self.greater( j, j+1 )) ):
				j += 1
			if ( ( self.greater( k, j ) == False ) ):
				break
			self.exch( k, j )
			k = j  

	def greater( self, i, j ):
		return self.heap[i].keys()[0] > self.heap[j].keys()[0]

	def exch( self, i, j ):
		temp = self.heap[i]
		if ( self.heap[i][ self.heap[i].keys()[0] ] != None ):
			self.heap[i][ self.heap[i].keys()[0] ].set_index_in_heap( j )
		if ( self.heap[j][ self.heap[j].keys()[0] ] != None ):
			self.heap[j][ self.heap[j].keys()[0] ].set_index_in_heap( i )
		self.heap[i] = self.heap[j]
		self.heap[j] = temp

	def is_min_heap( self ):
		return self.is_min_heap_recursive( 1 )

	def is_min_heap_recursive( self, k ):
		if ( ( k > self.N ) | ( 2 * k >= self.N) ):
			return True
		left = 2 * k
		right = 2 * k + 1
		if ( (left <= self.N) & (self.greater( k, left )) ):
			return False
		if ( (right <= self.N) & (self.greater( k, right )) ):
			return False
		return self.is_min_heap_recursive( left ) & self.is_min_heap_recursive( right )


	def get_capacity( self ):
		return self.capacity

	def generate_key( self, worker ):
		if ( worker.items_processed == 0 ):
			return worker.get_items_assigned()
		return worker.get_items_assigned() / worker.items_processed()



if __name__ == "__main__":
	# Just testing functionality. 
	heap_test = WorkerHeap()
	worker_1 = Worker( 1, 1, 40 )
	worker_2 = Worker( 2, 2, 50 )
	worker_3 = Worker( 3, 3, 40 )
	worker_4 = Worker( 4, 4, 30 )
	heap_test.insert( worker_1 )
	heap_test.insert( worker_2 )
	heap_test.insert( worker_3 )
	heap_test.insert( worker_4 )
	print( "Before: " )
	print( heap_test.heap[0] )
	print( heap_test.heap[1] )
	print( heap_test.heap[2] )
	print( heap_test.heap[3] )
	print( heap_test.heap[4] )
	#print( "\nAfter: " )
	#heap_test.reorder()
	#print( heap_test.heap[0] )
	#print( heap_test.heap[1][40].get_index_in_heap() )
	#print( heap_test.heap[2][40].get_index_in_heap() )
	#print( heap_test.heap[3][50].get_index_in_heap() )
	#print( heap_test.heap[4][60].get_index_in_heap() )

