#initialize host and port sa constructor
#initialize socket as attrib
#create socket sa run
import pickle
import socket
import pacman
import udp_packet as UDPpacket
class Server():
	BUFFER_SIZE = 4096
	socket = None
	hostname = ''
	port = ''
	room = ''

	def __init__(self, hostname, port):
		self.hostname = hostname
		self.port = port

	def run(self):
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		server_addr = (self.hostname, self.port)
		self.socket.bind(server_addr)
		
		print("Hosting at: ", self.hostname)

		while True:
			data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
			loaded_data = pickle.loads(data)
			packet_type = loaded_data.packet_type

			if packet_type == "CONNECT":
				print("{} succesfully connected to server!".format(loaded_data.player.name))

			if packet_type == "CREATE_ROOM":
				#generate a lobby_id
				lobby_id = "JK898"
				#create room using pacman.Room(lobby_id)
				self.room = pacman.Room(lobby_id)
			
				#Send lobby_id to client 
				sendLobbyIdPacket = UDPpacket.UDPpacket("SEND_LOBBY_ID") 
				sendLobbyIdPacket.lobby_id = lobby_id
				
				self.socket.sendto(pickle.dumps(sendLobbyIdPacket), addr)

			if packet_type == "JOIN":
				#Add client to room 
				self.room.add_client(loaded_data.player)
				print("ADDED " + loaded_data.player.name)
	
			if packet_type == "PLAYER_COUNT":
				#send room to client
				sendRoomPacket = UDPpacket.UDPpacket("SEND_ROOM") 
				sendRoomPacket.player_count = self.room.player_counter
			
				self.socket.sendto(pickle.dumps(sendRoomPacket), addr)

			if packet_type == "START_GAME":
				game_map = pacman.GameMap("map1.txt")

				#Send gamemap
				sendGameMapPacket =  UDPpacket.UDPpacket("SEND_GAMEMAP") 
				sendGameMapPacket.map_matrix = game_map.map_matrix
				self.socket.sendto(pickle.dumps(sendGameMapPacket), addr)
