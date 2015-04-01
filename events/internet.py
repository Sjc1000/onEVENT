import socket

def internet(host='www.google.com'):
	'''internet
	Checks if you have connection to the internet by trying to connect to a host.
	params:
		- host - The host to connect to, defaults to www.google.com
	'''
	try:
		hostname = socket.gethostbyname(host)
		sock = socket.create_connection((host, 80), 2)
		return (1, hostname)
	except:
		pass
	return (0, 'None')

if __name__ == '__main__':
	help(internet)
