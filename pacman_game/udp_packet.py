import socket
import pickle

class UDPpacket():

	# packet_type = ""
	# client
	# lobby_id
	# state
	# movement
	# position

	def __init__(self, packet_type):
		self.packet_type = packet_type

	def send_data(host_address, data):
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto(pickle.dumps(data), host_address)
	