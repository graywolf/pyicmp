import struct
import socket

class Header:
	
	version_ihl = None
	type_of_service = None
	length = None
	identification = None
	flags_offset = None
	ttl = None
	protocol = None
	checksum = None
	source_ip = None
	destination_ip = None
	
	def __init__(self, data = None):
		if data is not None:
			self.unpack(data)
	
	def unpack(self, data):
		(self.version_ihl, self.type_of_service, self.length,
		self.identification, self.flags_offset, self.ttl,
		self.protocol, self.checksum) = struct.unpack('BBHHHBBH', data[:12])
		
		self.source_ip = socket.inet_ntoa(data[12:16])
		self.destination_ip = socket.inet_ntoa(data[16:20])
	
	def __repr__(self):
		return '<IP Header: from ' + self.source_ip + ' to ' + self.destination_ip + '>'
	

