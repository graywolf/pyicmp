from threading import Lock
from . import ping
import time
import socket

class Handler:
	
	identifier = 0
	ports = []
	l = Lock()

	#this should be enough port, app will likely never use so many threads anyway
	max_ports = 1024

	def __init__(self, port = 33438):
		self.start_port = port
	
	def do_ping(self, ip, ttl = 64):
		#get identifier for this serie of packet
		with self.l:
			i = self.identifier
			self.identifier += 1
		#get free port to use
		while True:
			self.l.acquire()
			if len(self.ports) >= self.max_ports:
				self.l.release()
				time.sleep(0.1)
			else:
				port = None
				for port in range(self.start_port, self.start_port + self.max_ports):
					if port not in self.ports:
						self.ports.append(port)
						break
				self.l.release()
				break
		#now do actuall ping
		p = ping.Ping(ip = ip, port = port, identifier = i, sequence = 0, ttl = 64)
		with self.l:
			self.ports.remove(port)
		return p.result
	
	def do_trace(self, ip):
		result = []
		#get identifier for this serie of packet
		with self.l:
			i = self.identifier
			self.identifier += 1
		#get free port to use
		while True:
			self.l.acquire()
			if len(self.ports) >= self.max_ports:
				self.l.release()
				time.sleep(0.1)
			else:
				port = None
				for port in range(self.start_port, self.start_port + self.max_ports):
					if port not in self.ports:
						self.ports.append(port)
						break
				self.l.release()
				break
		#now do actuall trace
		sequence = 0
		ttl = 1
		on = False
		while not on and ttl < 128:
			p = ping.Ping(ip = ip, port = port, identifier = i, sequence = sequence, ttl = ttl, repeat = 1)
			sequence += 1
			ttl += 1
			on = p.result['on']
			try:
				result.append((p.result['responses'][0][0].source_ip, socket.gethostbyaddr(p.result['responses'][0][0].source_ip)))
			#no PTR record
			except socket.herror:
				result.append((p.result['responses'][0][0].source_ip, None))
			#no response from this step, ignore, useless for traceroute
			except IndexError:
				pass
		with self.l:
			self.ports.remove(port)
		result = {
			'ip': ip,
			'steps': result
		}
		return result

