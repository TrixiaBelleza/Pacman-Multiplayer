import UdpPacket as UdpPacket
class Client():
	BUFFER_SIZE = 4096
	player_name = "John Doe"
	player_type = "HOST"
	

	def __init__(self, host_address, server_port):
		self.server_address = (host_address, port)

	def connect(self, player_name, player_type):
		self.player_name = player_name
		self.player_type = player_type

		#create udp connect packet
		connectPacket = UdpPacket()
		connectPacket.packet_type = "CONNECT"
		connectPacket.player_name = self.player_name
		connectPacket.player_type = self.player_type

		
		