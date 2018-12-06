class Player():

	# current_pos
	# direction

	def __init__(self, name, player_type):
		self.name = name
		self.player_type = player_type
		self.current_pos = ()

class Room():
	def __init__(self, lobby_id):
		# self.hostname = hostname
		self.lobby_id = lobby_id
		self.clients = []
		self.player_counter = 0

	def add_client(self, new_player):
		self.clients.append(new_player)
		self.player_counter += 1

		if self.player_counter == 1:
			self.current_pos = (1,1)
		elif self.player_counter == 2:
			self.current_pos = (9,9)
		elif self.player_counter == 3:
			self.current_pos = (9,1)
		elif self.player_counter == 4:
			self.current_pos = (1,9)

class GameMap():

	def __init__(self, map_name):
		self.map_name = map_name
		self.map_matrix = []
		
		with open(map_name, "r") as map_file:
			for lines in map_file:
				line = []
				line[0:len(lines)] = iter(lines)
				self.map_matrix.append(line)

		# print(self.map_matrix)

		def move(self, player, movement):
			print(movement)
