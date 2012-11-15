import socket
import messages

port = 33434

"""Function to send ICMP packet and receive answer (if one is expected).

args:
	inp		input message (some of messages.*) -> .pack() is used
	outp	true if function should try to read output/return value from
			socket
"""
def handle_packet(inp, output = True):
	outs = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
	ins = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.getprotobyname('icmp'))
	
	ins.bind(("", port))
	
	outs.sendto(inp.pack(), ('77.93.223.198', port))
	
	if output:
		a = ins.recvfrom(1024)[0]
		a = a[20:]
		outp = messages.types[a[0]]()
		outp.unpack(a)
	
	ins.close()
	outs.close()
	
	if output:
		return outp

