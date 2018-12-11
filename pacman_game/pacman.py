class Player():
	address_info = ()
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
		self.player_counter += 1

		if self.player_counter == 1:
			new_player.current_pos = (1,1)
		elif self.player_counter == 2:
			new_player.current_pos = (9,9)
		elif self.player_counter == 3:
			new_player.current_pos = (9,1)
		elif self.player_counter == 4:
			new_player.current_pos = (1,9)

		self.clients.append(new_player)


class GameMap():

	def __init__(self, map_name, clients):
		self.map_name = map_name
		self.map_matrix = []
		self.clients = clients
		
		with open(map_name, "r") as map_file:
			for lines in map_file:
				line = []
				line[0:len(lines)] = iter(lines)
				self.map_matrix.append(line)

		for client in self.clients :
			row, col = client.current_pos
			self.map_matrix[row][col] = "P"
		# print(self.map_matrix)

	def move(self, player, movement):
		#print(movement)
		for client in self.clients :
			if player.name == client.name :
				row, col = client.current_pos
				self.map_matrix[row][col] = "e"

				if movement == "Left":
					if self.map_matrix[row][col-1] == "D" or self.map_matrix[row][col-1] == "s" or self.map_matrix[row][col-1] == "e":
						self.map_matrix[row][col-1] = "P"
						client.current_pos = (row,col-1)

				if movement == "Right":
					if self.map_matrix[row][col+1] == "D" or self.map_matrix[row][col+1] == "s" or self.map_matrix[row][col+1] == "e":
						self.map_matrix[row][col+1] = "P"
						client.current_pos = (row,col+1)
				
				if movement == "Up":
					if self.map_matrix[row-1][col] == "D" or self.map_matrix[row-1][col] == "s" or self.map_matrix[row-1][col] == "e":
						self.map_matrix[row-1][col] = "P"
						client.current_pos = (row-1,col)

				if movement == "Down":
					if self.map_matrix[row+1][col] == "D" or self.map_matrix[row+1][col] == "s" or self.map_matrix[row+1][col] == "e":
						self.map_matrix[row+1][col] = "P"
						client.current_pos = (row+1,col)

