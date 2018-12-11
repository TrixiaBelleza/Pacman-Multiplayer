import threading
import socket

class PacmanServer(threading.Thread, socket.socket):
	BUFFER_SIZE = 4096
	DEFAULT_PORT = 5000
	COMMAND_CLIENT_CONNECT = 'pacman_connect'
	
	def __init__(self, port=None):
		threading.Thread.__init__(self, name="Server thread")
		socket.socket.__init__(self, socket.AF_INET, type=socket.SOCK_DGRAM)

		self.port = self.DEFAULT_PORT if port is None else port
		self.bind(('', self.port))
		self.clients = []
		self.player_addresses = dict()	#Dictionary of player_addresses
		self._current_player_to_assign = 1
		self.client_handlers = []

		#generate map
		#self.pacman_world = pacman.game.Pacman() 
	def run(self):
		print('Hosting at:', self.getsockname())
		print('Starting server.')

		for i in range(3):
			player_number = i + 1

			print('Waiting for client #{}'.format(player_number))
			c = self.wait_client() #get client
			self.clients.append(c) #append the client to list of clients

			#send player number
			print('Sending player number {} to {}'.format(player_number,c))
			self.send_player_number(c,player_number)

		print('Starting game.')

		while True:
			print("on-going")
		return

	def wait_client(self, return_queue=None):
		#Step 1 : Wait for a client to connect

		data, address_info = self.recvfrom(self.BUFFER_SIZE)
		print('data:', data, 'address_info:', address_info)

		if data:
			decoded = data.decode('utf-8')
			if decoded != self.COMMAND_CLIENT_CONNECT:
				raise ValueError('Expecting "{}", but got "{}"'.format(self.COMMAND_CLIENT_CONNECT, decoded))
			return address_info

	def send_player_number(self, client_address, player_number):
		#Step 2 : Create a client handler object to send the player number to the connected client"
		ch = ClientHandler(self.port + self._current_player_to_assign, client_address, player_number, self)
		self.client_handlers.append(ch)
		self._current_player_to_assign += 1
		ch.start()

		self.player_addresses[player_number] = client_address

	def join(self, timeout=None):
		super().join()
		self.close()

class ClientHandler(threading.Thread, socket.socket):
	def __init__(self, port, client_address, player_number, server):
		socket.socket.__init__(self, type=socket.SOCK_DGRAM)
		threading.Thread.__init__(self, name='ClientHandler')
		self.bind(('localhost', port))
		self.setDaemon(True)
		self.player_number = player_number
		self.client_address = client_address
		self.server = server

		self.send_player_number()

	def send_player_number(self):
		self.sendto(str(self.player_number).encode('utf-8'), self.client_address)

	def run(self):
		while True:
			print("client handler")

	def join(self, timeout=None):
		self.close()
