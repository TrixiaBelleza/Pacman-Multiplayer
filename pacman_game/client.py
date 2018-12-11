#Instantiate socket as attribute
# attribute niya yung server address 
#socket.setblocking(0)
import socket
import pacman
import pickle
import udp_packet as UDPpacket
class Client():
	socket = None
	BUFFER_SIZE = 4096
	server_address = ('0.0.0.0', 10939)
	hostname = ''
	port = ''
	client_addr = ''
	#Bale gagawin natin na equivalent si CLIENT and PLAYER
	def __init__(self, player_name, player_type):
		self.player = pacman.Player(player_name, player_type)

	#Connect Client to Server
	def connect(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.client_addr = (self.hostname, self.port)
		self.socket.bind(self.client_addr)
		# self.socket.setblocking(0)
	
		#Always create a UDPpacket first! before sending to server.
		#Kasi mas madali iaccess and mas organized, madaling i-trace  
		#send connect packet to server
		connectPacket = UDPpacket.UDPpacket("CONNECT")
		connectPacket.player = self.player
		self.socket.sendto(pickle.dumps(connectPacket), self.server_address)

	def create_room(self):
		createroomPacket = UDPpacket.UDPpacket("CREATE_ROOM")
		createroomPacket.player = self.player
		self.socket.sendto(pickle.dumps(createroomPacket), self.server_address)

		#Receive response lobby id from server
		data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		loaded_data = pickle.loads(data)
		print("LOBBY ID FROM SERVER: ")
		print(loaded_data.lobby_id)

	def join(self, lobby_id):
		joinPacket = UDPpacket.UDPpacket("JOIN")
		joinPacket.player = self.player
		joinPacket.lobby_id = lobby_id
		self.socket.sendto(pickle.dumps(joinPacket), self.server_address)	



