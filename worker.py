# Still uncertain about how this will work, so 
# the ADT is subject to change. 

class Worker:
	def __init__( self, id, block_id, items_assigned ):
		self.id = id
		self.block_id = block_id
		self.items_assigned = items_assigned
		self.connected = None
		self.completed = None
		self.available = None
		self.busy = None
		self.items_processed = 0
		self.index_in_heap = -1
		self.packet = None

	def set_block_id( self, id ):
		self.block_id = id

	def get_block_id( self ):
		return self.block_id

	def set_items_assigned( self, items_assigned ):
		self.items_assigned = items_assigned

	def get_items_assigned( self ):
		return self.items_assigned

	def is_connected( self ):
		return self.connected

	def is_available( self ):
		return self.available

	def is_busy( self ):
		return self.busy

	def items_processed( self ):
		return self.items_processed

	def get_id( self ):
		return self.id

	def set_index_in_heap( self, index ):
		assert( index > 0 )
		self.index_in_heap = index

	def get_index_in_heap( self ):
		return self.index_in_heap

	def has_timed_out( self ):
		return self.packet.has_timed_out()

	def set_packet( self, packet ):
		self.packet = packet

	def set_connected( self, connected ):
		self.connected = connected

	def set_busy( self, busy ):
		self.busy = busy






#piece of data returned 

#sending
#sent 
#block id
#data
