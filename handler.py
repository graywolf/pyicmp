import socket
import messages
import datetime

default_port = 33434

"""Function to send ICMP packet and receive answer (if one is expected).

args:
	ip			ip adress of target
	inp			input message (some of messages.*) -> .pack() is used
	outp		true if function should try to read output/return value from
				socket
	force_port	for usage of specific port

returns:
	output == False
		nothing
	
	output == True
		tuple (response packet, time it took)
"""
def handle_packet(ip, inp, output = True, force_port = None):
	if force_port is not None:
		port = force_port
	else:
		port = default_port
	
	outs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
	ins = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
	
	ins.bind(("", port))
	
	if output:
		start = datetime.datetime.now()
	
	outs.sendto(inp.pack(), (ip, port))
	
	if output:
		a = ins.recvfrom(1024)[0]
		end = datetime.datetime.now()
		a = a[20:]
		outp = messages.types[a[0]]()
		outp.unpack(a)
	
	ins.close()
	outs.close()
	
	if output:
		delta = end - start
		return (outp, delta)

