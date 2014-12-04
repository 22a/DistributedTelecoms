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

	def set_block_id( self, id ):
		self.block_id = id

	def get_block_id( self ):
		return self.block_id

	def set_items_assigned( self, items_assigned ):
		self.items_assigned = items_assigned

	def get_items_assigned( self ):
		return self.items_assigned

	def connected( self ):
		return self.connected

	def available( self ):
		return self.available

	def busy( self ):
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




#piece of data returned 

#sending
#sent 
#block id
#data
