import time, datetime
import socket
from . import messages
from . import ip as ip_m

icmp = socket.getprotobyname('icmp')

class Ping:
	
	def __init__(self, ip, port, identifier, sequence, ttl, timeout = 5, repeat = 4, sleep = 0.25):
		#init result
		self.result = {
			'ip' : ip,
			'on' : False,
			'hostname' : None,
			'times' : [],
			'mdev' : 0,
			'avg_time' : 0,
			'packet_loss' : 0,
			'ttl': ttl,
			'responses' : []
		}
		#do pings
		for x in range(0, repeat):
			self.one_ping(ip, port, identifier, sequence, ttl, timeout)
			sequence += 1
			if x != repeat -1:
				time.sleep(sleep)
		#count packet loss
		self.result['packet_loss'] /= repeat
		#try to get hostname
		try:
			self.result['hostname'] = socket.gethostbyaddr(ip)[0]
		except socket.herror:
			self.result['hostname'] = None
		#calculate averate time
		if len(self.result['times']) != 0:
			self.result['avg_time'] = sum(self.result['times']) / len(self.result['times'])
			#and calculate mdev
			mean = sum([float(x) for x in self.result['times']]) / len(self.result['times'])
			self.result['mdev'] = sum([abs(x - mean) for x in self.result['times']]) / len(self.result['times'])

	
	def one_ping(self, ip, port, identifier, sequence, ttl, timeout):
		#prepare result dict
		result = {'error': None}
		
		#create sockets
		ins = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		outs = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
		#bind and set timeout for IN socket
		ins.bind(("", port))
		ins.settimeout(timeout)
		#set TTL for OUT socket
		outs.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
		
		#create packet and send it
		#print('sending to', ip, 'packet with', identifier, sequence)
		packet = messages.EchoRequest(identifier = identifier, sequence = sequence)
		outs.sendto(packet.pack(), (ip, port))
		
		#get answer and time it
		start = datetime.datetime.now()
		try:
			s = time.time()
			while time.time() - s < timeout:
				a  = ins.recvfrom(1024)[0]
				ip_header = ip_m.Header(a[:20])
				outp = messages.types[a[20]]()
				outp.unpack(a[20:])
				#print('received from', ip, 'packet', type(outp), 'with', outp.identifier, outp.sequence, 'policy:', type(outp) in messages.reply_messages and identifier == outp.identifier and sequence == outp.sequence, 'result so far:', result)
				if (
					(
						#handle errors
						type(outp) in messages.error_messages and
						#cover not specification complient routers
						outp.original_message is not None and
						identifier == outp.original_message.identifier and
						sequence == outp.original_message.sequence
					)
					or
					(
						#handle normal responses
						type(outp) in messages.reply_messages and
						identifier == outp.identifier and
						sequence == outp.sequence
					)
				):
					if type(outp) == messages.EchoReply:
						self.result['on'] = True
					delta = datetime.datetime.now() - start
					self.result['times'].append(delta.seconds * 1000000 + delta.microseconds)
					self.result['responses'].append((ip_header, outp))
					break
		except socket.timeout as e:
			self.result['packet_loss'] += 1

