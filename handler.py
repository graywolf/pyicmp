import socket
import messages
import datetime
import ip as ip_m
import os, pwd, grp

default_port = 33434

class Handler:
	
	def __init__(self, port = default_port, user = 'paladin', group = 'users', output = True):
		
		self.port = port
		self.output = output
		self.ttl = 64
		
		self.ins = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
		self.outs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
		try:
			os.setgid(grp.getgrnam(group).gr_gid)
			os.setuid(pwd.getpwnam(user).pw_uid)
		except:
			pass
		
		self.timeout = self.ins.gettimeout()
	
	"""Function to send ICMP packet and receive answer (if one is expected).
	
	args:
		ip			ip adress of target
		inp			input message (some of messages.*) -> .pack() is used
		outp		true if function should try to read output/return value from
					socket
		force_port	for usage of specific port
		ttl			socket TTL, None meaning default
		timeout		socket timeout
	
	returns:
		output == False
			nothing
		
		output == True
			tuple (response packet, time it took, ip header)
	"""
	def do(self, packet):
		self.ins.bind(("", self.port))
		
		if self.output:
			start = datetime.datetime.now()
		
		if self.ttl is not None:
			self.outs.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
		if self.timeout is not None:
			self.ins.settimeout(self.timeout)
			
		self.outs.sendto(packet.pack(), (self.ip, self.port))
		
		if self.output:
			a = self.ins.recvfrom(1024)[0]
			end = datetime.datetime.now()
			ip_header = ip_m.Header(a[:20])
			outp = messages.types[a[20]]()
			outp.unpack(a[20:])
			
			delta = end - start
			return (outp, delta, ip_header)
	
	def __del__(self):
		self.ins.close()
		self.outs.close()
	

