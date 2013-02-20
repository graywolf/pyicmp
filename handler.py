from . import ip as ip_m
from . import messages
import socket
import datetime
import os, pwd, grp
import time
import random
import struct

class TimeoutException(Exception):
	pass

class Handler:
	
	default_port = 33434
	
	def __init__(self, port = default_port, user = 'paladin', group = 'users', output = True, looptime = 30):
		self.port = port
		self.output = output
		self.ttl = 64
		self.looptime = looptime
		
		self.ins = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
		self.outs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
		
		self.port = Handler.default_port
		self.ins.bind(("", self.port))
		
		try:
			#os.setgid(grp.getgrnam(group).gr_gid)
			#os.setuid(pwd.getpwnam(user).pw_uid)
			pass
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
		packet.sequence = random.randrange(1, 65535)
		packet.identifier = os.getpid()
		if self.ttl is not None:
			self.outs.setsockopt(socket.SOL_IP, socket.IP_TTL, self.ttl)
		if self.timeout is not None:
			self.ins.settimeout(self.timeout)
		
		self.outs.sendto(packet.pack(), (self.ip, self.port))
		
		if self.output:
			
			s = time.time()
			#while loop with timeout
			while time.time() - s < self.looptime:
				start = datetime.datetime.now()
				try:
					a = self.ins.recvfrom(1024)[0]
				#packet lost, try again
				except socket.timeout:
					raise TimeoutException
				end = datetime.datetime.now()
				ip_header = ip_m.Header(a[:20])
				outp = messages.types[a[20]]()
				outp.unpack(a[20:])
				
				if (
						(
							#handle errors
							type(outp) in messages.error_messages and
							os.getpid() == outp.original_message.identifier and
							packet.sequence == outp.original_message.sequence
						)
						or
						(
							#handle normal responses
							type(outp) in messages.reply_messages and
							os.getpid() == outp.identifier and
							packet.sequence == outp.sequence
						)
					):
					delta = end - start
					return (outp, delta, ip_header)
				#special dirty fix for that idiotic BitDefender Firewall
				elif a.find(b"BitDefender Firewall Broadcast") != -1:
					delta = end - start
					return (outp, delta, ip_header)
				else:
					pass
			
			raise TimeoutException
	
	def __del__(self):
		try:
			self.ins.close()
		except AttributeError:
			pass
		try:
			self.outs.close()
		except AttributeError:
			pass

