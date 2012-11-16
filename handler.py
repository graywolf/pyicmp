import socket
import messages
import datetime
import ip as ip_m

default_port = 33434

"""Function to send ICMP packet and receive answer (if one is expected).

args:
	ip			ip adress of target
	inp			input message (some of messages.*) -> .pack() is used
	outp		true if function should try to read output/return value from
				socket
	force_port	for usage of specific port
	ttl			socket TTL, None meaning default

returns:
	output == False
		nothing
	
	output == True
		tuple (response packet, time it took)
"""
def handle_packet(ip, inp, output = True, force_port = None, ttl = None):
	if force_port is not None:
		port = force_port
	else:
		port = default_port
	
	outs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
	ins = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
	
	ins.bind(("", port))
	
	if output:
		start = datetime.datetime.now()
	
	if ttl is not None:
		outs.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
	outs.sendto(inp.pack(), (ip, port))
	
	if output:
		a = ins.recvfrom(1024)[0]
		end = datetime.datetime.now()
		ip_header = ip_m.Header(a[:20])
		outp = messages.types[a[20]]()
		outp.unpack(a[20:])
	
	ins.close()
	outs.close()
	
	if output:
		delta = end - start
		return (outp, delta, ip_header)

