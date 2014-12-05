class EmptyQueueException( Exception ):
	def __init__( self, message ):
		super( EmptyQueueException, self ).__init__( message )

class WorkerUnavailableException( Exception ):
	def __init__( self, message ):
		super( WorkerUnavailableException, self ).__init__( message )
