from threading import * 
from socket import * 
from packets import * 

class Client(Thread):
	def __init__(self, ip, port):
		Thread.__init__(self)
		self.server_ip = ip
		self.server_port = port
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.task = None
		self.packets = []
		self.processing = False
		self.expected_packet_count = -1
		self.expected_instance_per_packet = -1
		self.target = ""
		self.matches = {}
		self.engaged = False	# It is necessary to set an 
								# engagement record. Otherwise, the 
								# Server may send another packet to 
								# the Client, while the Client has 
								# already agreed to process a previous request. 
	def run(self):
		while True:
			#print("self.ready_to_process(): " + str(self.ready_to_process()))
			if (self.ready_to_process() == True):
				dataset = []
				for instance in range( len( self.packets ) ):
					#print("instance: " + str(self.packets[instance]))
					dataset.extend(self.packets[instance])

				self.task = ConcurrentTask(self.target, "1", dataset, self)
				self.task.start()

			packet, addr = self.sock.recvfrom(16384)
			packet = json.loads(packet)
			self.server_ip = addr[0]
			self.server_port = addr[1]

			if (packet['type'] == "AVAILABLE"):
				if (self.task != None):
					if not(self.task.is_processing()):
						self.engaged = True
						self.send(request_accepted(), addr)
						self.packets = initialise_list(self.packets, packet['packet_count'], None)
						self.expected_packet_count = packet['packet_count']
					else:
						self.send(available(False), addr)
				else:
					self.engaged = True
					self.send(request_accepted(), addr)
					self.packets = initialise_list(self.packets, packet['packet_count'], None)
					self.expected_packet_count = packet['packet_count']
					print( "request accepted sent")
				
			elif (packet['type'] == "DATA"):
				#print(" -- DATA RECEIVED -- ")
				self.packets[packet['start_index']/len(packet['payload'])] = packet['payload']
				self.target = packet['target']
				self.send(positive_data_acknowledgement(packet['block_id'], packet['start_index']), addr)
			
			elif (packet['type'] == "PROCESSING"):
				self.send(processed_section(self.task.get_dataset_id(),
					self.task.processed_to()), addr)

			elif (packet['type'] == "PING"):
				self.send(alive())

			elif (packet['type'] == "MATCH_REQUEST"):
				self.send(match_found(self.get_matches()))
				self.reset_matches()

	def ready_to_process(self):
		if (len(self.packets) > 0):
			for value in self.packets:
				if (value == None):
					return False
			return True
		return False

	def send(self, packet, dest = None):
		if (dest == None):
			self.sock.sendto(packet,(self.server_ip, self.server_port))
		else:
			self.sock.sendto(packet, dest)

	def add_match(self, block_id, index):
		self.matches[block_id] = index

	def get_matches(self):
		return self.matches

	def reset_matches(self):
		self.matches = {}

# Assumed structure of a Server-Client data packet:
# 	-> 'type'			:	'DATA'
# 	-> 'block_id'		: 	'block_id'
# 	-> 'start_index' 	: 	start_index of target, relative to block(int)
#	-> 'target'			: 	target (string)
#	-> 'payload'		: 	payload (list of string values)
# 	-> 'more'			:	boolean (True or False)


class ConcurrentTask(Thread):
	def __init__(self, target, dataset_id, dataset, client):
		Thread.__init__(self)
		self.target = target
		self.dataset = dataset
		self.dataset_id = dataset_id
		self.processed_to = 0
		self.processing = False
		self.client = client 

	def run(self):
		self.processing = True
		index = 0
		for instance in self.dataset:
			if (instance == self.target):
				#self.client.send(found(self.dataset_id, index))
				self.client.add_match(self.dataset_id, index)
			if ((index % 1000 == 0) & (index != 0)):
				self.client.send(processed_section(self.dataset_id, index)) 
				self.processed_to = index
			index = index + 1
		self.client.send(complete(self.dataset_id))
		self.processing = False

	def get_dataset_id(self):
		return self.dataset_id

	def is_processing(self):
		return self.processing 

	def processed_to(self):
		return self.processed_to

def insertion_sort(array):
	for i in range(len(array)):
		j = i 
		while ((j>0) & (array[j-1] > array[j])):
			array = swap(array, j, j-1)
			j -= 1
	return array

def swap(array, i, j):
	temp = array[i]
	array[i] = array[j]
	array[j] = temp
	return array

def initialise_list(array, length, value):
	for i in range(length):
		array.append(value)
	return array
if __name__ == "__main__":
	client = Client('localhost', 24069)
	client.start()
	client.send(connect(1))
