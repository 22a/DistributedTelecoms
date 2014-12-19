from database import Database
from threading import *
from Queue import *

class DatabaseAccessRegulator(Thread):
	def __init__(self, filename):
		Thread.__init__(self)
		self.filename = filename
		self.db = None
		self.db_queue = DatabaseQueue(self)
		self.data_queue = Queue()

	def run(self):
		self.db = Database()
		self.db._init_(self.filename)
		self.db.read_into_db(self.filename)
		while True:
			if ( self.db_queue.qsize() > 0 ):
				item = self.db_queue.get()
				self.db.update_state(item[0], item[1])

			if ( self.data_queue.qsize() <= 100 ):
			 	if ( self.db.data_available() ):
			 		temp = self.db.get_data()
			 		self.data_queue.put(temp)

	def update_state(self, block_id, pos):
		self.db_queue.insert(block_id, pos)

	def read_into_db(self):
		self.db.read_into_db(filename)

	def data_available(self):
		if ( self.data_queue.qsize() > 0 ):
			return True
		else:
			return False

	def get_data(self):
		return self.data_queue.get()



class DatabaseQueue:
	def __init__(self, db_access_regulator):
		self.queue = Queue()
		self.db_access_regulator = db_access_regulator

	def insert(self, block_id, pos):
		self.queue.put((block_id, pos))

	def qsize(self):
		return self.queue.qsize()

	def get(self):
		return self.queue.get()


class ThreadedClass(Thread):
	def __init__(self, db_regulator):
		Thread.__init__(self)
		self.regulator = db_regulator

	def run(self):
		for i in range(20):
			self.regulator.update_state(i,1000)



if __name__ == "__main__":
	db_regulator = DatabaseAccessRegulator("names.txt")
	db_regulator.start()



