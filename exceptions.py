

class EmptyQueueException( Exception ):
	def __init__( self, message ):
		super( EmptyQueueException, self ).__init__( message )