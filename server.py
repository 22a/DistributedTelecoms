# -*- coding: utf-8 -*-
from threading import * 
from socket import *
from socket import *
from thread import * 
from Queue import * 
#from worker_queue import *
from json import *
from packet_pool import *
from database import Database
from socket import error as SocketError
from worker_heap import WorkerHeap
from packets import *
from packet_constructors import DataDeconstructor
from db_regulator import *
import time
import sys
import webbrowser, os
from flask import Flask, render_template, jsonify
from errors import EmptyQueueException
import logging

# SOME FILTHY GLOBAL VARIABLES
bPool = 2000
bPro = 10
wPool = 0
fProg = 0

class Server(Thread):
	def __init__(self, ip, port, target_name):
		Thread.__init__(self)
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.UDP_IP = ip
		self.UDP_PORT = port
		self.sock.bind((self.UDP_IP, self.UDP_PORT))
		self.sock.setblocking(0)
		self.connection_acceptor = IncomingConnectionAcceptor(self.sock, self)
		self.connection_acceptor.start()
		self.worker_pool = WorkerHeap()
		self.matches = {}
		self.db_access_regulator = DatabaseAccessRegulator("names.txt")
		self.db_access_regulator.start()
		self.packet_pool = PacketQueue()
		self.worker_revitaliser = WorkerRevitaliser(self)
		self.worker_revitaliser.start()
		#self.default_listener = DefaultListener(self.sock, self)
		#self.default_listener.start()
		self.reading_in = True
		self.block_count = 0
		self.target_name = target_name
		# socket.sendto(string, flags, address) or socket.sendto(string, flags)


	def listen(self):
		while True:
			time.sleep(0.001)
			while (self.db_access_regulator.data_available() |
				(self.packet_pool > 0)):
				time.sleep(0.01)

	
	def run_server(self):
		while True:
			time.sleep(0.01)
			while (self.db_access_regulator.data_available() | 
				(self.packet_pool.size() > 0)):
				time.sleep(0.01)
				if (self.worker_pool.size() > 0):
					wPool = self.worker_pool.size()
					print("worker_pool.size(): " + str(self.worker_pool.size()))
					try:
						worker_copy = self.worker_pool.dequeue()
					except EmptyQueueException:
						pass
					if not(worker_copy.is_engaged()):
						if (self.packet_pool.size() > 0):
							pass
						else:
							data_from_server = json.loads(self.db_access_regulator.get_data())
							packets = DataDeconstructor().deconstruct(
								data_from_server[1]["data"], 250, 
								data_from_server[0]["id"], self.target_name)
							worker_copy.set_packets(packets)
							worker_copy.send(available(len(worker_copy.get_packets())))
					self.reading_in = self.db_access_regulator.is_reading_in()
					self.worker_pool.insert(worker_copy)
					#print("BLOCKS_PROCESSED: " + str(self.get_block_count()))
					#print("MATCHES: " + str(self.matches))

			self.worker_revitaliser.set_finished(True)

	def run(self):
		self.run_server()

	def send(self, packet, worker, timeout = None):
		self.sock.sendto(packet, worker.address())
		if (timeout != None):
			pass

	def get_worker(self, key):
		return self.worker_pool[key]

	def get_workers(self):
		return self.worker_pool

	# @param 'block_id' (type: string): Block id. in which a match
	# was found for the specified target. 
	# @param 'index' (type: string): Index in corresponding block. 
	def set_match(self, block_id, index):
		self.matches[block_id] = index

	# Returns: Key-value dict of matches, where each key
	# denotes the block in which a match was found, and
	# each value is the corresponding index within the block. 
	def get_matches(self):
		return self.matches

	def is_reading_in(self):
		return self.reading_in

	def worker_pool_size(self):
		return self.worker_pool.size()

	def blocks_processed(self):
		return self.block_count

	def set_block_count(self, count):
		bPro = count
		self.block_count = count

	def get_block_count(self):
		return self.block_count

class DefaultListener(Thread):
	def __init__(self, socket, server):
		Thread.__init__(self)
		self.sock = socket
		self.server = server


	def run(self):
		while True:
			time.sleep(0.01)
			skip = True
			try:
				packet, addr = self.sock.recvfrom(16384)
				skip = False
			except Exception:
				pass
			if (skip == False):
				if (packet != ""):
					packet = json.loads(packet)
					if (packet['type'] == "MATCH"):
						self.server.set_match(packet['block_id'], packet['index'])

class IncomingConnectionAcceptor(Thread):
	def __init__(self, socket, server):
		Thread.__init__(self)
		self.sock = socket
		self.server = server

	def run(self):
		while True:
			time.sleep(0.0001)
			skip = True
			try:
				packet, addr = self.sock.recvfrom(16384)
				skip = False
			except Exception:
				pass
			if (skip == False):
				print("Connection accepted")
				if (packet != ""):
					packet = json.loads(packet)
					if (packet['type'] == "INCOMING_CONNECTION"):
						worker = Worker(self.server, addr, None)
						worker.initialise_window(20)
						self.server.get_workers().insert(worker)
					elif(packet['type'] == "MATCH"):
						print( "MATCH!")




class WorkerRevitaliser(Thread):
	def __init__(self, server):
		Thread.__init__(self)
		self.server = server
		self.finished = False


	def run(self):
		while True:
			time.sleep(0.01)
			if (self.server.worker_pool.size() > 0):
				try:
					dequeued_worker = self.server.worker_pool.dequeue()
				except EmptyQueueException:
					pass
				if (dequeued_worker.is_connected() == True):
					if (dequeued_worker.is_engaged() == False):
						dequeued_worker.send(ping())
					self.server.worker_pool.insert(dequeued_worker)
			

	def set_finished(self, finished):
		self.finished = finished

class Worker(Thread):
	def __init__(self, server, addr, packets):
		Thread.__init__(self)
		self.window = []
		self.packets = packets 
		self.address = addr
		self.server = server 
		self.engaged = False
		self.connected = True
		self.started = False

	def reenable(self):
		self.started = True
		while True:
			time.sleep(0.001)
			all_processed = True
			for value in self.window:
				if (value == False):
					all_processed = False
			if (all_processed == True):
				self.engaged = False
				self.window = []
				self.initialise_window(len(self.packets))

	def run(self):
		self.reenable()



	def send(self, packet):
		sock = socket(AF_INET, SOCK_DGRAM)
		sock.sendto(packet, self.address)
		sock.settimeout(2.0)
		hasReceived = False
		attempts = 0

		while ((hasReceived == False) & (attempts < 3)):
			try:
				packet, addr = sock.recvfrom(16384)
				packet = json.loads(packet)
				#print( "Worker.packet: " + str( packet ))
				if (packet['type'] == "PROCESSING_STATUS_UPDATE"):
					if (packet['payload'] == "COMPLETE"):
						self.engaged = False
						self.block_id = packet['block_id']
						print("COMPLETE MESSAGE RECEIVED FROM CLIENT")
					else:
						self.server.get_database().update_state(
							str(packet['block_id']), packet['payload'])
				elif (packet['type'] == "POS_DATA_ACK"):
					if not(self.started):
						self.start()
					#print("Data acknwoledgement from client: " + str( 
					#	packet['start_index']/250))
					self.set_window(packet['start_index']/250)
					self.server.set_block_count(int(packet['block_id']))
					if (packet['block_id'] == 19):
						self.send(match_request())
				elif (packet['type'] == "REQUEST_ACCEPTED"):
					for index in self.get_packets():
						self.send(self.get_packets()[index])
						self.engaged = True
					#print("REQUEST_ACCEPTED")

				elif (packet['type'] == "REQUEST_REJECTED"):
					self.set_availability(False)
				elif (packet['type'] == "ALIVE"):
					self.connected = True
				elif (packet['type'] == "MATCH_FOUND"):
					self.server.matches.update(packet['matches'])



				hasReceived = True
			except timeout:
				attempts = attempts + 1

		if (hasReceived == False):
			self.connected = False

	def initialise_window(self, length):
		for i in range(length):
			self.window.append(False)

	def set_window(self, index):
		self.window[index] = True

	def set_packets(self, packets):
		self.packets = packets 

	def get_packet(self, index):
		return self.packets[index]

	def get_packets(self):
		return self.packets

	def get_address(self):
		return self.address

	def is_engaged(self):
		return self.engaged

	def is_connected(self):
		return self.connected

	def set_connected(self, connected):
		self.connected = connected

#These function can be merged into server.py, that way we can jsonify the simple returns 
#from the db and various pools


app = Flask(__name__)
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)



@app.route('/_return_bPool')
def return_bPool():
  global bPool
  bPool = bPool -1
  return jsonify(result=bPool) #values are hardcoded for display purposes, they will call a function that returns an int size

@app.route('/_return_bPro')
def return_bPro():
  global bPro
  bPro = bPro + 1
  return jsonify(result=bPro)

@app.route('/_return_wPool')
def return_wPool():
  
  return jsonify(result=wPool)

@app.route('/_return_fProg')
def return_fProg():
  global fProg
  fProg = fProg + 9
  return jsonify(result=fProg%100)

@app.route('/_return_fCread')
def return_fCread():
  ## we should have a var here that is 1 if we're reading in a file, 0 otherwise
  global fProg
  test = 1
  if fProg%90==0:     ##for display purposes hides loading bar every 5 seconds
    test = 0
  return jsonify(result=test)

@app.route('/addWorker')
def return_AddWorker():
  os.system("python client.py")
  return
    
@app.route("/")
def hello():
  return render_template('index.html')

class ConcurrentGui(Thread):
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		webbrowser.open('127.0.0.1:5000')
		app.run()


if __name__ == "__main__":
	name = raw_input("Enter the name you wish to search from: ")
	"""
	webbrowser.open('127.0.0.1:5000')
	app.run()
	"""
	browser_gui = ConcurrentGui()
	browser_gui.start()

	print("should be executed")
	server = Server('localhost', 24069, name)
	server.start()
	#app.debug = True
	#b = webbrowser.get('firefox')
	#b.open_new('127.0.0.1:5000')      #using webbrowser to automatically open the ui