import socket
import threading
import time
from cprint import cprint

def timestamp():
    time_object = time.localtime(time.time())
    return '[{:0>2}:{:0>2}:{:0>2}]'.format(time_object[3],
              time_object[4],time_object[5])

class server():
    connections = {}
    socket = None
    
    def __init__(self, host='', port=9987, local=True):
        """__init__
        creates the server and binds it. If the port specified is
            already in use it will check the port lower than it,
            this will repeat until it binds one successfully.
        """
        cprint(' [.green]Server created!', '[.purple]' + timestamp())
        self.host = host
        self.port = port
        self.local = local
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        if local == False:
            self.host = socket.gethostbyname(socket.gethostname())

        cprint(' [.yellow]Attempting to bind to port [.bold]' + str(port),
               '[.purple]' + timestamp())
        while True:
            try:
                self.socket.bind((host, port))
            except OSError:
                port -= 1
                continue
            else:
                break
        cprint(' [.green]Port bound to [.bold]' + str(port), '[.purple]' 
               + timestamp())
        
    def listen(self, connections=10):
        """listen
        Listens for new connections then creates a threaded reciever.
        """
        cprint(' [.yellow]Listening for [.bold]' + str(connections) + 
               '[./bold] connections.', '[.purple]' + timestamp())
        self.socket.listen(connections)
        while True:
            socket, address = self.socket.accept()
            self.connections[address[1]] = (socket, address)
            rec_thread = threading.Thread(
                target=self.rec_loop,
                args=(address))
            rec_thread.daemon = True
            rec_thread.start()
        return True
    
    def rec_loop(self, address, pid):
        """rec_loop
        The recieve loop created by the listener.
        """
        cprint(' [.green]Starting recieve loop.', '[.purple]' + timestamp())
        socket = self.connections[pid][0]
        address = self.connections[pid][1]
        while True:
            try:
                recv = socket.recv(1024).decode('utf-8')
            except UnicodeDecodeError:
                cprint(' [.red]Error decoding data from [.bold]' + 
                       str(address), '[.purple]' + timestamp())
                continue
            
            split = recv.replace('\r\n', '').split(' ')
            if split[0] in ['close', 'stop', 'disconnect', 'exit', '']:
                self.close_connection(pid)
                self.popall([pid])
                break
        return 1
    
    def send(self, data):
        """send
        Sends data to all of the connections.
        """
        for pid in self.connections:
            socket = self.connections[pid][0]
            socket.send(bytes(data+'\n', 'utf-8'))
        return None
    
    def close_connection(self, pid):
        """close_connection
        Closed the connection to a specific client.
        """
        cprint(' [.red]Closing connection to [.bold]' +
               str(self.connections[pid][1]), '[.purple]' + timestamp())
        socket = self.connections[pid][0]
        socket.shutdown(2)
        socket.close()
        return None
    
    def popall(self, pids):
        """popall
        This pops the connections dict with the pid's from the pids list.
        I didn't want to use this method. I was getting errors in the other
            ways I was trying.
        """
        for pid in pids:
            self.connections.pop(pid)
        return None
        
    def shutdown(self):
        """shutdown
        Shuts down the main listener. No longer accepts connections.
        """
        cprint(' [.red]Shutting down.', '[.purple]\n' + timestamp())
        conn = self.connections
        for connection in conn:
            self.close_connection(connection)
        self.popall([c for c in self.connections])
        self.socket.close()
        return None


if __name__ == '__main__':
    server = server('', 9987)
    try:
        server.listen()
    except KeyboardInterrupt:
        server.shutdown()
