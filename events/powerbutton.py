import socket

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock.connect('/var/run/acpid.socket')

def powerbutton():
	'''powerbutton
	Returns true if the power button has been pressed. False if it hasn't.
	
	Note: Due to the way this finds the power button press it may miss a press. I haven't had it miss one yet, but it may be possible. If it does, decrease the time on the delay section.
	'''
	sock.settimeout(0.1)
	try:
		e = sock.recv(1024)
	except socket.timeout:
		return (0, 'None')
	if e.split(b' ')[0] == b'button/power':
		return (1, 'Power')
	return (0, 'None')
