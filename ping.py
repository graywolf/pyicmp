import handler
import messages
import datetime
import sys
import socket

"""Class for pinging IP adress.

Because it is supposed to be used in data collection etc, there is no
reason to fool around with output etc. It just collects data, how you
use them is up to you"""
class Ping:
	
	ip = None
	on = False
	repeat = 10
	
	avg_time = 0
	max_time = None
	min_time = None
	packet_loss = 0
	responses = []
	
	def __init__(self, ip, run = True):
		self.ip = ip
		if run:
			self.do_ping()
	
	def do_ping(self):
		for i in range(0, self.repeat):
			try:
				#consider moving time measuring into handle_packet for
				#removing measuring func calling cost
				reply, delta = handler.handle_packet(self.ip, messages.EchoRequest())
				if type(reply) == messages.EchoReply:
					self.on = True
					microseconds = delta.seconds * 1000000 + delta.microseconds
					self.avg_time += microseconds
					
					try:
						if self.max_time < microseconds:
							self.max_time = microseconds
					except TypeError as e:
						self.max_time = microseconds
					
					try:
						if self.min_time > microseconds:
							self.min_time = microseconds
					except TypeError as e:
						self.min_time = microseconds
				else:
					self.packet_loss += 1
				self.responses.append(reply)
			except Exception as e:
				raise
		
		self.avg_time /= self.repeat - self.packet_loss
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
		print ('Packet loss:', p.packet_loss)

