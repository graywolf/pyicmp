import struct
import socket

"""IP Header

Representation of IP Header object, code is pretty self-explanatory."""
class Header:
	
	"""Takes data (packed ip header) as optional argument"""
	def __init__(self, data = None):
		self.version_ihl = None
		self.type_of_service = None
		self.length = None
		self.identification = None
		self.flags_offset = None
		self.ttl = None
		self.protocol = None
		self.checksum = None
		self.source_ip = None
		self.destination_ip = None
		
		if data is not None:
			self.unpack(data)
	
	"""Unpack data and fill all attributes.
	
	Converts packed IP adresses to string representations"""
	def unpack(self, data):
		(self.version_ihl, self.type_of_service, self.length,
		self.identification, self.flags_offset, self.ttl,
		self.protocol, self.checksum) = struct.unpack('BBHHHBBH', data[:12])
		
		self.source_ip = socket.inet_ntoa(data[12:16])
		self.destination_ip = socket.inet_ntoa(data[16:20])
	
	def __repr__(self):
		return '<IP Header: from ' + self.source_ip + ' to ' + self.destination_ip + '>'
	

