# -*- coding: utf-8 -*-

from json import JSONDecoder;
import sys
from socket import *
from thread import * 
from socket import socket
from socket import AF_INET
import threading
import json
from packets import *
from packet_constructors import DataReconstructor

class RemoteWorker(threading.Thread):
	def __init__(self, server_address, server_port):
		threading.Thread.__init__(self)
		self.sock = socket(AF_INET, SOCK_STREAM)
		#self.sock.bind((server_address,server_port))
		self.sock.connect((server_address, server_port))
		print "connection established"
		self.server_address = server_address
		self.server_port = server_port
		#self.sock.listen(1)
		#self.run() # probably should omit this!
		self.id = id
		self.block_id = -1
		self.index_in_heap = -1
		self.items_assigned = -1 # The number of items that has been assigned to a worker
		self.items_processed = -1 # The number of those items assigned that have been processed
		self.start_index = 0
		self.busy = False


	def run(self):
		reconstructor = DataReconstructor()
		while True:
			#conn, addr = self.sock.accept()
			# having received something from the server, tell the server
			# that you have received their message
			#conn, addr = self.sock.accept()
			#received = conn.recv(1024)
			#data = conn.recv(1024)
			#print( "received from server: ", data )
			#conn.send( "Client: Received message from the Server." )
			raw_from_server = self.sock.recv(65536)
			if (raw_from_server != ""):
				packets_conjoined = False
				conjoined_packets = []
				try:
					decoded_message = json.loads(raw_from_server)
				except ValueError, e:
					index_from = 0
					more_index = 0
					while ( raw_from_server.find( "{\"type\": \"DATA\"}", index_from ) != -1 ):
						packets_conjoined = True
						more_index = raw_from_server.find( "more", index_from ) 
						next_packet_start_index = raw_from_server.find( "[", more_index )

						if ( next_packet_start_index != -1 ):
							conjoined_packets.append( raw_from_server[index_from:next_packet_start_index])
							index_from = next_packet_start_index
						else:
							conjoined_packets.append( raw_from_server[index_from:])
							index_from = more_index
					print( "Error/exception message: " + str( e ) + ". Clean-up ops. performed." )

				if ( packets_conjoined == True ):
					if ( len( conjoined_packets ) > 0 ):
						for packet in conjoined_packets:
							if ( self.busy == False ):
								#print "sys.getsizeof( packet ): " + str( sys.getsizeof( packet ) )
								#print "packet: " + str( packet )
								decoded_message = json.loads(packet)
								self.block_id = decoded_message[1]['block_id']
								if ( self.start_index == 0 ):
									self.start_index = decoded_message[2]['start_index']
								reconstructor.add(decoded_message[4]['payload'])
								items_assigned = reconstructor.length()
								if (decoded_message[5]['more'] == False):
									self.search(decoded_message[3]['target'], reconstructor.flush())
									reconstructor.reset()
							else:
								busy(self.block_id)

				elif (decoded_message[0]['type'] == "DATA"):
					if ( self.busy == False ):
						self.block_id = decoded_message[1]['block_id']
						if ( self.start_index == 0 ):
							self.start_index = decoded_message[2]['start_index']
						#items_assigned = len(decoded_message['payload']) #decomm
						# May need to thread this method
						reconstructor.add(decoded_message[4]['payload'])
						items_assigned = reconstructor.length() 
						if (decoded_message[5]['more'] == False):
							self.search(decoded_message[3]['target'], reconstructor.flush())
							reconstructor.reset()
						# self.search(decoded_message['target'], decoded_message['payload']) # decomm
					else:
						busy(self.block_id)
				# Request for a status update, essentially
				elif (decoded_message['type'] == "AVAILABILITY"):
					available(self.id, self.busy)
				else:
					raise Exception("This exception should not have been raised!")
		conn.close() # this may be the cause of an error. 
		self.sock.close()

	def set_block_id(self,id):
		self.block_id = id

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

	def say(self, packet):
		self.sock.send(packet)


	def search(self, name, names):
		self.busy = True
		for index, name in enumerate(names):
			if ( name == 'name' ):
				# found(id, index) returns a json 
				# packet that is to be sent to the
				# Server/Coordinator, informing 
				# it that a match has been found (id == 'MATCH')
				self.say(found(self.block_id, ( self.start_index + index)))
			# I'm unsure whether this should ping the Server per 1000 
			# names processed, or per 1/5 of items_assigned that have 
			# been processed - I guess that per 1000 is sufficient. 
			if ( ( (index + self.start_index) % 1000 == 0 ) & ( ( self.start_index + index ) != 0 ) ):
				# processed_section() returns a packet
				# that is to be sent to the Server/Coordinator, 
				# informing it that a match has been found (id == 'PROCESSED_1000')
				self.items_processed = ( index + self.start_index )
				self.say(processed_section(self.block_id, (index + self.start_index)))

		# complete(id) returns a json packet
		# that is to be sent to the Server/Coordinator,
		# informing it that all of the items in the 
		# assigned dataset have been searched (id == 'COMPLETE')
		# Flush
		self.say(complete(self.block_id))

		# Some clean-up actions
		self.start_index = 0
		self.items_processed = -1
		self.busy = False
		self.items_assigned = -1
		self.block_id = -1


if __name__ == "__main__":
	host = 'localhost'
	port = 24069
	worker = RemoteWorker(host, port)
	worker.start()
