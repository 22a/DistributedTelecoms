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
	return json.dumps(packet_contents)

def completed(block_id):
	packet_contents = { 'type'		: 'COMPLETED', 
						'block_id'	: block_id }
	return json.dumps(packet_contents)

# Currently busy processing block block_id
def busy(block_id):
	packet_contents = { 'type'		: 'BUSY', 
						'block_id'	: block_id }
	return json.dumps(packet_contents)

def dataset(block_id, start_index, target, payload):
	packet_contents = { 'type'			: 'DATA', 
						'block_id'		: block_id,
						'start_index'	: start_index, 
						'target'		: target,
						'payload'		: payload }
	return json.dumps(packet_contents)

# Sent from a Client (@ id) to the Server/Coordinator, 
# informing it (the Server) whether it is available to process data
def available(id, availability):
	packet_contents = { 'type'		: 'STATUS', 
						'id'		: id, 
						'available'	: availability }
	return json.dumps(packet_contents)


# Sent from the Server/Coordinator to an arbitrary client
def available():
	packet_contents = { 'available'		: 'AVAILABILITY' }
	return json.dumps(packet_contents)





