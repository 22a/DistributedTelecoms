# -*- coding: utf-8 -*-
import json
# packet modules

def found(block_id, index):
	packet_contents = { 'type'		: 'MATCH', 
						'block_id'	: block_id, 
						'index'		: index }
	return json.dumps(packet_contents)

def processed_section(block_id, position):
	packet_contents = { 'type'		: '1000_PROCESSED', 
						'block_id'	: block_id,
						'position'	: position }
	return json.dumps(packet_contents, separators=(',', ': '))

def complete(block_id):
	packet_contents = { 'type'		: 'COMPLETE', 
						'block_id'	: block_id }
	return json.dumps([packet_contents])

# Currently busy processing block block_id
def busy(block_id):
	packet_contents = { 'type' : 'BUSY', 
						'block_id' : block_id } 
	return json.dumps(packet_contents, sort_keys = True)


def dataset(block_id, start_index, target, payload, more):
	packet_contents = {	'type' : 'DATA', 
						'block_id' : block_id, 
						'start_index' : start_index, 
						'target' : target, 
						'payload' : payload, 
						'more' : more }
	return json.dumps(packet_contents, sort_keys = True, ensure_ascii = True)


# Sent from a Client (@ id) to the Server/Coordinator, 
# informing it (the Server) whether it is available to process data

def request_accepted():
	packet_contents = { 'type'		: "REQUEST_ACCEPTED" }
	return json.dumps(packet_contents)

def available(id, availability):
	packet_contents = { 'type'		: 'STATUS', 
						'id'		: id, 
						'available'	: availability }
	return json.dumps(packet_contents)


# Sent from the Server/Coordinator to an arbitrary client
def available(packet_count):
	packet_contents = { 'type'		: 'AVAILABLE', 
						'packet_count'	: packet_count }
	return json.dumps(packet_contents)

def connect(id):
	packet_contents = { 'type'		: 'INCOMING_CONNECTION', 
						'id'		: id }
	return json.dumps(packet_contents)


def positive_data_acknowledgement(block_id, start_index):
	packet_contents = { 'type'			: 'POS_DATA_ACK', 
						'block_id'		: block_id, 
						'start_index'	: start_index }
	return json.dumps(packet_contents)

def ping():
	packet_contents = { 'type'			: 'PING' }
	return json.dumps(packet_contents)

def alive():
	packet_contents = { 'type'			: 'ALIVE' }
	return json.dumps(packet_contents)

def match_request():
	packet_contents = { 'type'			: 'MATCH_REQUEST'}
	return json.dumps(packet_contents)

def match_found(matches):
	packet_contents = { 'type'			: 'MATCH_FOUND', 
						'matches'		: matches }
	return json.dumps(packet_contents)


