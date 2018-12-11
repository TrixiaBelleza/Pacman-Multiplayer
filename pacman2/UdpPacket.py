class UDPpacket():
	packet_type = ""
	player_name = ""
	player_id = ""
	map_state = [] 
	player_position = () #x,y

	def __init__(self, packet_type):
		self.packet_type = packet_type
