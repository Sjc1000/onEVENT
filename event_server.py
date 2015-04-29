import socket
from pprint import pprint
import threading

class server():
	port = None
	host = None
	connections = {}
	def __init__(self, host='', port=9987, local=1):
		pprint('Attempting to create server on', 'yellow')
		if local:
			pprint('Setting up in local mode.', 'yellow')
			self.host = host
		else:
			pprint('Setting up in global mode.', 'yellow')
			self.host = socket.getaddrinfo(host, port)[0][4][0]
		pprint('Host\t\t: ' + self.host , 'yellow')
		pprint('Port\t\t: ' + str(port) , 'yellow')
		self.port = port
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		pprint('Binding server.')
		
		while port != 0:
			try:
				self.socket.bind((self.host,self.port))
			except OSError:
				self.port = self.port - 1
			else:
				break
		pprint('Bound on', 'green')
		pprint('Host\t\t: ' + self.host, 'green')
		pprint('Port\t\t: ' + str(self.port) , 'green')
	
	def recv_loop(self, socket, address):
		while True:
			recv = socket.recv(1024)
			if recv == b'':
				pprint('Closing connection to ' + str(address[0]) )
				self.connections.pop(address[1])
				break
		return None
	
	def connection_loop(self, accept=5):
		self.socket.listen(accept)
		pprint('Listening for ' + str(accept) + ' connections.')
		pprint('Good to connect!', 'green')
		while True:
			new_connection = self.socket.accept()
			self.connections[new_connection[1][1]] = new_connection
			pprint('New connection : ' + str(new_connection[1]))
			recv_thread = threading.Thread(target=self.recv_loop, args=(new_connection))
			recv_thread.daemon = True
			recv_thread.start()
		return None
	
	def send(self, data):
		for id in self.connections:
			connection = self.connections[id]
			socket = connection[0]
			socket.send(bytes(data+'\r\n', 'utf-8'))
		return None
	
	def shutdown(self):
		print('') # Forces a newline in the terminal window. So the next data is displayed on a newline.
		pprint('Shutting down server.', 'red')
		self.socket.shutdown(socket.SHUT_RDWR)
		pprint('Closing connection.', 'red')
		self.socket.close()
		return None


if __name__ == '__main__':
	server = server()
	
	try:
		server.connection_loop()
	except (KeyboardInterrupt, OSError):
		server.shutdown()
