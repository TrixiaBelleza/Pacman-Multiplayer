import socket
import pickle
import Pacman
import UdpPacket as UdpPacket

class Server():
	BUFFER_SIZE = 4096
	DEFAULT_PORT = 10939
	DEFAULT_HOST = '0.0.0.0'
	def __init__(self, port):
		self.port = port 
		self.room = {}
		self.client_list = []
		self.player_number = 1

	def run(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.bind((self.DEFAULT_HOST,self.DEFAULT_PORT))
		print("Server Started.")

		while True:
			data, addr = sock.recvfrom(self.BUFFER_SIZE)
			deserialized_data = pickle.loads(data)