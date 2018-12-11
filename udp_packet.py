import socket
import pickle

class UDPpacket():

	packet_type = ""
	player = None
	lobby_id_udp = ''
	map_matrix = [] 
	movement = ''
	player_count = 0
	player_position = () #x,y
	map_file = ''
	
	def __init__(self, packet_type):
		self.packet_type = packet_type

	# def send_data(address, data):
	# 	sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	# 	sock.sendto(pickle.dumps(data), address)
	