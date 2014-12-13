# -*- coding: utf-8 -*-
from socket import *
from thread import * 
from socket import socket
from socket import AF_INET
from threading import Thread
from thread import * 
from Queue import * 
from thread_comm import * 
from worker_queue import *
#from database import Database
from json import *
from packet_pool import *
from database import Database
from socket import error as SocketError
from worker_heap import WorkerHeap
from packets import *
from packet_constructors import DataDeconstructor

# Wrapper for server
class Server(Thread):
	DATA_INSTANCES_PER_PACKET = 1000
	def __init__(self, address, port, backlog):
		Thread.__init__(self)
		self.sock = socket(AF_INET, SOCK_STREAM)
		self.sock.bind((address,port))
		self.sock.listen(5)
		self.sock.setblocking(1)
		self.backlog = backlog
		self.address = address
		self.port = port 
		self.inbox = Queue()
		self.outbox = Queue()	# May be able to remove this.
		self.threads = Queue()	# I have no idea why this is here. 
		self.worker_pool = WorkerHeap()
		self.worker_buffer = WorkerHeap(10)
		self.packet_pool = PacketQueue()
		self.db = Database() #self.db = Database()
		filename = "names.txt"
		self.db._init_(filename)
		self.db.read_into_db(filename) #self.db.read_into_db(filename)
		self.worker_acceptor = IncomingConnectionAcceptor(self.sock, self)
		self.worker_acceptor.start()
		self.matches = {}
		self.worker_revitaliser = WorkerRevitaliser(self, 
			self.worker_pool, self.worker_buffer)
		self.worker_revitaliser.start()

	def run_server(self):
		"""
		while True:
			# Repeatedly accept incoming connections from clients
			conn, addr = self.sock.accept()
			print 'Connected with ' + addr[0] + ':' + str( addr[1])
			self.worker_pool.insert( ThreadComm(conn, addr, this) )
			self.worker_pool.just_inserted().start()
		"""
		# while self.db.data_available(): # must change this to an executable once db
		while ( self.db.data_available() | ( self.packet_pool.size() > 0 ) ):
	
			# Only assign tasks to worker in buffer; that is, 
			# "workers" that are not currently working.
			if ( self.worker_buffer.size() > 0 ):
				temp = self.worker_buffer.dequeue()
				if ( self.packet_pool.size() > 0 ):
					temp.say(self.packet_pool.dequeue())
					temp.set_availability(False)
					self.worker_pool.insert(temp)
				else:
					deconstructor = DataDeconstructor()
					data_from_database = self.db.get_data()
					packets = deconstructor.deconstruct(data_from_database["data"], self.DATA_INSTANCES_PER_PACKET,
						data_from_database["id"], "ciaran")
					temp.set_availability(False)
					self.worker_pool.insert(temp)
					for packet in packets:
						temp.say(packet)
					
					"""
					OMITTED:
					temp.set_availability(False)	# to be omitted
					self.worker_pool.insert(temp)	# to be omitted
					temp.say(dataset(0, 0, 'ciaran', self.db.get_data('0')))	# to be omitted
					"""
		self.worker_revitaliser.set_finished(True)

	def run(self):
		self.run_server()

	def get_address(self):
		return self.address

	def get_port(self):
		return self.port 

	def get_worker_pool(self):
		return self.worker_pool

	def get_database(self):
		return self.db 

	# May need to check the types with Ciaran. 
	def set_match(self, block_id, pos):
		self.matches[str(block_id )] = pos

	def get_packet_pool(self):
		return self.packet_pool

	def get_worker_buffer(self):
		return self.worker_buffer

class IncomingConnectionAcceptor(Thread):
	def __init__(self, socket, server):
		Thread.__init__(self)
		self.socket = socket 
		self.server = server

	def run(self):
		while True:
			conn, addr = self.socket.accept()
			#self.server.get_worker_pool().insert(ThreadComm(conn, addr, self))
			print "connection accepted: " + str( addr )
			temp = Worker(conn, addr, None, self.server)
			if ( self.server.get_worker_buffer().size() < 10 ):
				# We want the local worker to begin listening out for packets from
				# the corresponding remote worker immediately, 
				self.server.get_worker_buffer().insert(temp)
			else:
				self.server.get_worker_pool().insert(temp)
			# We want the local worker to begin listening out for packets from
			# the corresponding remote worker immediately. The local 
			# worker runs in the background. 
			temp.start()

class WorkerRevitaliser(Thread):
	def __init__(self, server, worker_pool, worker_buffer):
		Thread.__init__(self)
		self.server = server
		self.finished = False
		self.worker_pool = worker_pool
		self.worker_buffer = worker_buffer

	def run(self):
		while (self.finished == False):
			if ( self.worker_pool.size() > 0 ):
				dequeued_worker = self.worker_pool.dequeue()
				if ( dequeued_worker.is_available() & 
					dequeued_worker.is_connected() ):
					print "worker freed"
					if ( self.worker_buffer.size() < 10 ):
						self.worker_buffer.insert( dequeued_worker )
					else:
						self.worker_pool.insert( dequeued_worker )
				elif ( dequeued_worker.is_connected() ):
					self.worker_pool.insert( dequeued_worker )
				else:
					pass
					# don't re-queue the Worker, as it has disconnected 


	def set_finished(self, finished):
		self.finished = finished

class Worker(Thread):
	COMMUNICATION_TIMEOUT = 30.0
	def __init__(self, conn, addr, id, server_reference):
		Thread.__init__(self)
		self.conn = conn
		self.addr = addr 
		self.index_in_heap = -1
		self.id = id 
		self.block_id = -1
		self.items_assigned = -1
		self.available = True 
		self.items_processed = -1
		self.start_index = -1
		self.server_reference = server_reference
		self.packets = None
		self.t = None # Timer which handles timeouts on task(s) assigned to the Worker
		self.connected = True

	def run(self):
		self.hear() # listening, bitches!

	def hear(self):
		while True:
			raw_data_from_client = self.conn.recv(512)
			decoded_message = json.loads(raw_data_from_client)
			if (decoded_message['type'] == "1000_PROCESSED"):
				print "decoded_message['block_id']: " + str( decoded_message['block_id'] )
				print "decoded_message['position']: " + str( decoded_message['position'] )
				self.server_reference.get_database().update_state(
					str( decoded_message['block_id'] ), decoded_message['position'] )
				self.items_processed = decoded_message['position']
				# Once 1000 have been processed, we do not
				# want to re-process the already-processed 1000. 
				if ( len(self.packets) > 0 ):
					self.packets.pop(len(self.packets))

				if ( self.t != None ):
					self.t.cancel()	# Cancel timer task
				# In this case, we would want to reset the timer task. Only once
				# the Server has received a packet of type 'COMPLETED' from 
				# the Worker should the timer object not be immediately re-scheduled/set
				"""
				COMMENTED-OUT BECAUSE I WAS UNSURE WHY IT EXISTED
				self.t = Timer(30.0, self.dataset_timeout)
				self.t.start()
				"""
			elif (decoded_message['type'] == "MATCH"):
				self.server_reference.set_match(decoded_message['block_id'], 
					decoded_message['index'])
				# In this case, we would want to reset the timer task. Only once
				# the Server has received a packet of type 'COMPLETED' from 
				# the Worker should the timer object not be immediately re-scheduled/set
				if ( self.t != None ):
					self.t.cancel() # Cancel timer task
				"""
				COMMENTED-OUT BECAUSE I WAS UNSURE WHY IT EXISTED
				self.t = Timer(30.0, self.dataset_timeout)
				self.t.start()
				"""
			# This may be redundant, but I'm not certain, yet. 
			elif (decoded_message['type'] == "COMPLETED"):
				print "completed executed"
				try:
					self.t.cancel() # Cancel timer task
					self.set_availability(True)
					# Reset packets - clean-up operation
					self.packets = {}
					print "made available"
					print "worker_buffer.size(): " + str( self.server_reference.get_worker_buffer().size() )
					print "worker_pool.size(): " + str( self.server_reference.get_worker_pool().size() )
				except Exception:
					print("An active Timer task does not exist on the Timer object.")
				# Not sure whether we should do anything!?
			elif (decoded_message['type'] == "BUSY"):
				# Not sure whether we should do anything!?
				# I guess that it depends on the context -- may 
				# need to further explore this. 
				try:
					# In this case, we would want to reset the timer task. Only once
					# the Server has received a packet of type 'COMPLETED' from 
					# the Worker should the timer object not be immediately re-scheduled/set
					if ( self.t != None ):
						self.t.cancel() # Cancel timer task
					self.t = Timer(30.0, self.dataset_timeout)
					self.t.start()
				except Exception:
					print("An active Timer task does not exist on the Timer object.")


			#self.say('Hello, there, friendly client.')

	# @param: A json packet object. 
	def say(self, packet):
		# Need to set timeouts for this, particularly 
		# if the packet being sent contains a names payload. 
		self.packets[len(self.packets)] = packet # Temporary copy of the packet sent to the Worker is stored on the server-side. 
		# That way, if a time-out occurs, we can add the packet to the Server's packet pool. 
		try:
			self.conn.send(packet)
		except SocketError:
			self.is_connected = False
		# Start timer once packet has been sent to the Worker
		decoded_packet = json.loads(packet)

		if (decoded_packet['type'] == "DATA"):	
			self.set_availability(False)		
			self.t = Timer(self.COMMUNICATION_TIMEOUT, self.dataset_timeout)	# May need to change this to just 'COMMUNICATION_TIMEOUT'
			self.t.start()
		elif (decoded_packet['type'] == "AVAILABILITY"):
			self.t = Timer(self.COMMUNICATION_TIMEOUT, self.connected_timeout)
			selt.t.start 
			# Not sure what we should do here. 


	def set_block_id(self,id):
		self.block_id = id

	def set_connected(self, connected):
		self.connected = connected

	def dataset_timeout(self):
		for packet in self.packets:
			self.server_reference.get_packet_pool().put(packet)
		#self.server_reference.get_packet_pool().put(self.packet) # decomm

	def connected_timeout(self):
		self.connected = False

	def get_block_id(self):
		return self.block_id

	def set_items_assigned(self, items_assigned):
		self.items_assigned = items_assigned

	def get_items_assigned(self):
		return self.items_assigned

	def is_available(self):
		return self.available

	def get_items_processed(self):
		return self.items_processed

	def get_id(self):
		return self.id 

	def set_index_in_heap(self, index):
		self.index_in_heap = index

	def set_availability(self, availability):
		self.available = availability

	def is_connected(self):
		return self.connected



if __name__ == "__main__":
	host = 'localhost'
	port = 24069
	server = Server(host, port, 100)
	# Begin accepting client connections. 
	#server.run_server() # Replaced with 
	server.start()
