import ping
import sys
import socket

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
	
	def __init__(self, ip, run = True):
		self.ip = ip
		
		self.max_hops = 60
		self.ping_repeat = 1
		self.timeout = 5
		self.reached = False
		self.detailed = True
		
		self.pings = []
		
		if run:
			self.do_trace()
	
	def do_trace(self):
		ttl = 1
		while True:
			p = ping.Ping(self.ip, run = False)
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
					ps.append(ping.Ping(p.ip_headers[0].source_ip))
				except:
					ps.append(p)
			self.pings = ps
	

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print('Usage: ' + sys.argv[0] + ' IP|hostname')
	else:
		print('Traceroute-ing', sys.argv[0])
		t = TraceRoute(socket.gethostbyname(sys.argv[1]))
		i = 1
		for p in t.pings:
			try:
				print(i, p.host[0], '(' + p.ip_headers[0].source_ip + ')', 'avg:', p.avg_time, 'µs')
			except:
				print(i, '* * *')
			i += 1

