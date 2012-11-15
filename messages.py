"""
Most names are self-explaining and all is defined in RFC 792, I do not
see reason to write it all here. If you want to know details, read rfc.
It's not so long.
"""


import struct
import os
import datetime

identifier = os.getpid()
sequence = 0

"""Skeleton message class

Basic attributes and needed method, setting unified API for all
messages."""
class Message:
	
	packed = ''
	
	ptype = 0
	code = 0
	checksum = 0
	identifier = 0
	sequence = 0
	
	def __init__(self):
		global sequence
		sequence = sequence + 1
		self.identifier = identifier
		self.sequence = sequence
	
	"""Function packing data into bytes.
	
	Inheriting class MUST override this if is expected to send data
	(e.g. Echo request)."""
	def pack(self):
		pass
	
	"""Function unpacking data from bytes.
	
	Inheriting class MUST override this if is expected to receive data
	(e.g. Echo reply).
	
	args:
		data	should by data directly from socket
	"""
	def unpack(self, data):
		pass
	
	def _carry_around_add(self, a, b):
		c = a + b
		return (c & 0xffff) + (c >> 16)
	
	def _calcchecksum(self, msg):
		s = 0
		for i in range(0, len(msg), 2):
			w = msg[i] + (msg[i+1] << 8)
			s = self._carry_around_add(s, w)
		return ~s & 0xffff
	
	def __repr__(self):
		return "<Message: type: %d, code: %d, idf: %d, seq: %d>" % (self.ptype, self.code, self.identifier, self.sequence)

class DestinationUnreachable(Message):
	
	NET_UNREACHABLE = 0
	HOST_UNREACHABLE = 1
	PROTOCOL_UNREACHABLE = 2
	PORT_UNREACHABLE = 3
	FRAGMENTATION_NEEDED = 4
	SOURCE_ROUTE_FAILED = 5
	
	def __init__(self):
		del self.identifier
		del self.sequence
	
	def __repr__(self):
		return "<" + self.self.__class__.__name__ + ": type: %d, code: %d>" % (self.ptype, self.code)
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum) = struct.unpack('BBH', data[0:4])

class TimeExceeded(Message):
	
	TIME_TO_LIVE_EXCEEDED_IN_TRANSIT = 0
	FRAGMENT_REASSEMBLY_TIME_EXCEEDED = 1
	
	def __init__(self):
		del self.identifier
		del self.sequence
	
	def __repr__(self):
		return "<" + self.self.__class__.__name__ + ": type: %d, code: %d>" % (self.ptype, self.code)
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum) = struct.unpack('BBH', data[0:4])

class ParameterProblem(Message):
	
	def __init__(self):
		del self.identifier
		del self.sequence
	
	def __repr__(self):
		return "<" + self.self.__class__.__name__ + ": type: %d, pointer: %d>" % (self.ptype, self._pointer)
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum, self._pointer) = struct.unpack('BBHB', data[0:5])

class SourceQuench(Message):
	
	def __init__(self):
		del self.identifier
		del self.sequence
	
	def __repr__(self):
		return "<" + self.self.__class__.__name__ + ": type: %d, code: %d>" % (self.ptype, self.code)
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum) = struct.unpack('BBH', data[0:4])

class Redirect(Message):
	
	REDIRECT_DATAGRAMS_FOR_THE_NETWORK = 0
	REDIRECT_DATAGRAMS_FOR_THE_HOST = 1
	REDIRECT_DATAGRAMS_FOR_THE_TYPE_OF_SERVICE_AND_NETWORK = 2
	REDIRECT_DATAGRAMS_FOR_THE_TYPE_OF_SERVICE_AND_HOST = 3
	
	def __init__(self):
		del self.identifier
		del self.sequence
	
	def __repr__(self):
		return "<" + self.self.__class__.__name__ + ": type: %d, code: %d, gateway: %d>" % (self.ptype, self.code, self._gateway)
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum) = struct.unpack('BBHI', data[0:4])
		self._gateway = socket.inet_ntoa(data[4:4])

class Timestamp(Message):
	
	ptype = 13
	receive_timestamp = 0
	transmit_timestamp = 0
	
	def pack(self):
		date = datetime.date.today()
		delta = datetime.datetime.now() - datetime.datetime(date.year, date.month, date.day)
		self.originate_timestamp = round(delta.seconds + delta.microseconds/1000)
		self.packed = struct.pack('BBHHHIII', self.ptype, self.code, self.checksum, self.identifier, self.sequence, self.originate_timestamp, self.receive_timestamp, self.transmit_timestamp)
		self.checksum = self._calcchecksum(self.packed)
		self.packed = struct.pack('BBHHHIII', self.ptype, self.code, self.checksum, self.identifier, self.sequence, self.originate_timestamp, self.receive_timestamp, self.transmit_timestamp)
		return self.packed

class TimestampReply(Message):
	
	def __init__(self):
		del self.identifier
		del self.sequence
	
	def __repr__(self):
		return "<" + self.self.__class__.__name__ + ": type: %d, code: %d>" % (self.ptype, self.code)
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum, self.identifier, self.sequence, self.originate_timestamp, self.receive_timestamp, self.transmit_timestamp) = struct.unpack('BBHHHIII', data)

class InformationRequest(Message):
	
	ptype = 15
	
	def pack(self):
		self.packed = struct.pack('BBHHH', self.ptype, self.code, self.checksum, self.identifier, self.sequence)
		self.checksum = self._calcchecksum(self.packed)
		self.packed = struct.pack('BBHHH', self.ptype, self.code, self.checksum, self.identifier, self.sequence)
		return self.packed

class InformationReply(Message):
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum, self.identifier, self.sequence) = struct.unpack('BBHHH', data)

"""Echo Request message

Ping - request"""
class EchoRequest(Message):
	
	ptype = 8
	
	def pack(self):
		self.packed = struct.pack('BBHHH', self.ptype, self.code, self.checksum, self.identifier, self.sequence)
		self.checksum = self._calcchecksum(self.packed)
		self.packed = struct.pack('BBHHH', self.ptype, self.code, self.checksum, self.identifier, self.sequence)
		return self.packed

"""Echo Reply message

Ping - reply"""
class EchoReply(Message):
	
	def unpack(self, data):
		(self.ptype, self.code, self.checksum, self.identifier, self.sequence) = struct.unpack('BBHHH', data)


types = {
	3: DestinationUnreachable,
	11: TimeExceeded,
	12: ParameterProblem,
	4: SourceQuench,
	5: Redirect,
	8: EchoRequest,
	0: EchoReply,
	13: Timestamp,
	14: TimestampReply,
	15: InformationRequest,
	16: InformationReply,
}
