from . import ping
from . import handler
import sys
import socket
import copy

"""This class performs trace route.

Because it is supposed to be used in data collection etc, there is no
reason to fool around with output etc. It just collects data, how you
use them is up to you.

If you run directly this script, it just prints out everything it knows.

attributes:
	ip			target ip
	max_hops	maximum number of hops to the target (target beeing 60th)
	ping_repeat	repeat attribute of ping
	timeout		socket timeout (default 5 sec, 'cause ping over 5s is way too big)
	detailed	after tracing do ping for each routing point
"""
class TraceRoute:
	
	def __init__(self, ip, run = True, detailed = True, handler = handler.Handler()):
		self.ip = ip
		
		self.max_hops = 60
		self.ping_repeat = 1
		self.timeout = 2
		self.reached = False
		self.detailed = detailed
		self.handler = handler
		
		self.pings = []
		
		if run:
			self.do_trace()
	
	def do_trace(self):
		ttl = 1
		while True:
			p = ping.Ping(self.ip, run = False, handler = self.handler)
			p.ttl = ttl
			p.repeat = 1
			p.timeout = self.timeout
			try:
				p.do_ping()
			except socket.timeout:
				pass
			
			self.pings.append(p)
			
			try:
				if self.pings[-1].responses[-1].__class__.__name__ == 'EchoReply':
					self.reached = True
					break
			except:
				pass
			
			if ttl == self.max_hops:
				break
			
			ttl += 1
		
		if self.detailed:
			ps = []
			for p in self.pings:
				try:
					ip = p.ip_headers[0].source_ip
					p.reset()
					p.ip = ip
					p.sleep = 0
					p.do_ping()
					ps.append(p)
				except Exception as e:
					ps.append(p)
			self.pings = ps
	

