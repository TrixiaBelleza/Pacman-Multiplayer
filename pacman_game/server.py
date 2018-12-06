import socket
import pickle
import pacman
import udp_packet as udp

send = udp.UDPpacket.send_data

class Server(socket.socket):
	BUFFER_SIZE = 4096
	DEFAULT_PORT = 10939
	
	def __init__(self, port):
		self.port = port
		self.room = []
		self.client_list = []

	def run(self):
		socket.socket.__init__(self, type=socket.SOCK_DGRAM)
		self.bind(('', self.port))
		self.host_address = self.getsockname()[0]

		print('Hosting at:', self.host_address)

		while True:

			data, address_info = self.recvfrom(self.BUFFER_SIZE)
			deserialized_data = pickle.loads(data)
			packet_type = deserialized_data[0]

			if packet_type == "CONNECT":

				player_name = deserialized_data[1]
				player_type = deserialized_data[2]
				
				print("{} {} connected from {}".format(player_type, player_name, address_info))

				player = pacman.Player(player_name, player_type)
				self.client_list.append(player)

				send(address_info, address_info[1])

			elif packet_type == "CREATE_ROOM":

				player = deserialized_data[1]
				lobby_id = "JK898"

				print("{} created room in lobby {}".format(player, lobby_id))

				self.room = pacman.Room(lobby_id)
				for client in self.client_list:
					if client.name == player:
						self.room.add_client(client)

			elif packet_type == "JOIN":

				player = deserialized_data[1]

				print("{} joined lobby {}".format(player, lobby_id))

				for client in self.client_list:
					if client.name == player:
						self.room.add_client(client)

			elif packet_type == "START_GAME":
 
				if self.room.player_counter == 1003 or self.room.player_counter == 1004:
					print("hello")
					map_name = deserialized_data[1]
					
					map_state = pacman.GameMap(map_name)

					# print(map_state.map_matrix)

					# send to client, after client receive: on_execute(matrix)
					# for client in self.room.clients:
					# 	send(self._address, )


			elif packet_type == "MOVE":

				movement = deserialized_data[1]
				game.move(movement)

			else:
				print("[ERROR] Packet type: {} not recognized".format(packet_type))
