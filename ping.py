import handler
import messages
import datetime
import sys
import socket

"""Class for pinging IP adress.

Because it is supposed to be used in data collection etc, there is no
reason to fool around with output etc. It just collects data, how you
use them is up to you.

If you run directly this script, it just prints out everything it knows.

Attributes:
	ip			target ip
	repeat		how many time repeat Echo request
	
	times		list with how long each ping took
	avg_time	calculated average time per ping
	max_time	maximum time for ping
	min_time	minimum time for ping
	mdev		mean deviation of times per ping
	packet_loss	packet loss: packet_wrong/packet_total
	responses	list with all response packets
"""
class Ping:
	
	ip = None
	on = False
	repeat = 10
	
	times = []
	avg_time = None
	max_time = None
	min_time = None
	mdev = None
	packet_loss = 0
	responses = []
	ip_headers = []
	
	"""Init class
	
	args:
		ip	ip adress of target
		run	True for auto run, if False you must call do_ping() to collect data
	
	You will use run = False mostly if you want to change repeat value (how
	many times repeat the measurement)."""
	def __init__(self, ip, run = True):
		self.ip = ip
		if run:
			self.do_ping()
	
	"""Do the ping. self.ip must be setted."""
	def do_ping(self):
		#do the job repeat-times
		for i in range(0, self.repeat):
			#reply type & timing
			reply, delta, ip_header = handler.handle_packet(self.ip, messages.EchoRequest())
			#was Echo request a success?
			if type(reply) == messages.EchoReply:
				#target is out there
				self.on = True
				#convert delta to microseconds and append to list with times
				microseconds = delta.seconds * 1000000 + delta.microseconds
				self.times.append(microseconds)
				
				#set/update min&max times
				try:
					if self.max_time < microseconds:
						self.max_time = microseconds
				except TypeError:
					self.max_time = microseconds
				
				try:
					if self.min_time > microseconds:
						self.min_time = microseconds
				except TypeError:
					self.min_time = microseconds
			#could not get through, increase packet loss
			else:
				self.packet_loss += 1
			#log response
			self.ip_headers.append(ip_header)
			self.responses.append(reply)
		
		#number of successes
		ok = self.repeat - self.packet_loss
		#if at least one packet was ok
		if ok != 0:
			#calculate mean deviation
			mean = sum([float(x) for x in self.times]) / len(self.times)
			self.mdev = sum([abs(x - mean) for x in self.times]) / len(self.times)
			#calculate average time
			self.avg_time = sum(self.times) / len(self.times)
		#convert #packet loss to [0;1] percentage value
		self.packet_loss /= self.repeat

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: ' + sys.argv[0] + ' IP|hostname')
	else:
		p = Ping(socket.gethostbyname(sys.argv[1]))
		
		print ('Reachable:', p.on)
		print ('Average time:', p.avg_time, 'µs')
		print ('Maximum time:', p.max_time, 'µs')
		print ('Minimum time:', p.min_time, 'µs')
		print ('MDev:', p.mdev, 'µs')
		print ('Packet loss:', p.packet_loss)
		
		print ('\nTimes:', p.times, 'µs')
		print ('\nResponses:', [x.__class__.__name__ for x in p.responses])
		print ('\nIP Headers:', [x for x in p.ip_headers])

