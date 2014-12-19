# -*- coding: utf-8 -*-
from packets import *

class DataReconstructor:
	def __init__(self):
		self.data = []
		self.active = False

	# @param payload: A list of data instance. 
	def add(self, payload):
		self.active = True
		self.data.extend(payload)
	# Returns: Re-constructed data. 
	def flush(self):
		self.active = False
		return self.data

	def active(self):
		return self.active

	def length(self):
		return len(self.data)

	def reset(self):
		self.data = []


class DataDeconstructor:
	def __init__(self):
		self.packets = {}

	# @param packet_size: The number of data instance per packet. 
	# @param data: The data which is to be split up into transportable packets. This
	# is must be an array of data instances. 
	# Returns: A dict of packets, representing subsets of the original 
	# data, which amount to the original data. x
	def deconstruct(self, data, packet_size, block_id, target):
		for p in range(len(data)/packet_size):
			if ((len(data)/packet_size - 1) != p):
				self.packets[p] = dataset(block_id, 
					p*packet_size, target, 
					data[p*packet_size:(p+1)*packet_size], True)
			else:
				self.packets[p] = dataset(block_id, 
					p*packet_size, target, 
					data[p*packet_size:(p+1)*packet_size], False)
		return self.packets 

