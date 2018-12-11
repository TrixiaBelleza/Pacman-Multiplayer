'''
Coding scheme:
	Camel case beginning with an UPPERCASE letter for functions ThisIsCamelCase
	Camel case beginning with a lowercase letter for packets like connectPacket, lobbyPacket, etc.
	Snake case for variables	this_is_snake_case
'''
import socket
import sys
import select
from tcp_packet_pb2 import TcpPacket
from player_pb2 import Player

<<<<<<< HEAD
#Connect to socket to server address
server_address = ('202.92.144.45', 80) 	#address = (hostname, port)
socket = socket.socket()  # instantiate socket
socket.connect(server_address)  # connect to the server using address 

def CreateLobby(packet):
=======
def ConnectToServer():
	#Connect to socket to server address
	global socket
	server_address = ('202.92.144.45', 80) 	#address = (hostname, port)
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate socket
	socket.connect(server_address)  # connect to the server using address 
	print("Socket connected to server!")
	return socket
def CreateLobby(packet, max_players):
>>>>>>> ced8a96107c626e978a6abfc44b6c04b213c84f8
	#CREATE LOBBY

	#Instantiate Create Lobby using the packet.type = CREATE_LOBBY from TcpPacket, which is 2. (check tcp_packet.proto)
	lobbyPacket = packet.CreateLobbyPacket()
	lobbyPacket.type = TcpPacket.CREATE_LOBBY
<<<<<<< HEAD
	lobbyPacket.max_players = int(input("Enter max number of players: "))
=======
	lobbyPacket.max_players = max_players
>>>>>>> ced8a96107c626e978a6abfc44b6c04b213c84f8
	
	#Send the lobbyPacket to server
	socket.send(lobbyPacket.SerializeToString()) 
	
	#Receive lobby id from server
	data = bytearray(socket.recv(1024)) # receive response from server
	lobbyPacket.ParseFromString(data)
	print('Received from server: ' + lobbyPacket.lobby_id)  # show in terminal
	lobby_id = lobbyPacket.lobby_id

	return lobby_id

def InstantiatePlayer(player_name):
	player = Player()
	player.name = player_name
	return player

<<<<<<< HEAD
#Connect players (including host) to server using connectPacket	
def ConnectPlayerToServer(player, packet):
	connectPacket = packet.ConnectPacket()

	role = input("Are you a HOST(H) or a PLAYER(P)? : ").lower()

	if role == "h":
		connectPacket.type = TcpPacket.CONNECT
		lobby_id = CreateLobby(packet)
		connectPacket.lobby_id = lobby_id
		connectPacket.player.name = player.name
		#Send connect packet to server
		socket.send(connectPacket.SerializeToString()) 

		#Receive broadcasted data from server
		connect_data = bytearray(socket.recv(1024)) # receive response from server
		connectPacket.ParseFromString(connect_data)
	else:
		connectPacket.type = TcpPacket.ERR_LDNE
		#assume first that the connectPacket type is error packet so that all can be put inside a try catch
		#and loop until the lobby chosen is existing or is not full
		while connectPacket.type == TcpPacket.ERR_LDNE or connectPacket.type == TcpPacket.ERR_LFULL:
			try:
				lobby_id = input("Enter lobby id: ") 
				connectPacket.type = TcpPacket.CONNECT
				connectPacket.lobby_id = lobby_id
				connectPacket.player.name = player.name
				#Send connect packet to server
				socket.send(connectPacket.SerializeToString()) 
				#Receive broadcasted data from server
				connect_data = bytearray(socket.recv(1024)) # receive response from server
				connectPacket.ParseFromString(connect_data)
				#if the received response from the server is ERR_LFULL, 
				#parsing connect_data will NOT result to exception
				if connectPacket.type == TcpPacket.ERR_LFULL:
					print("Lobby is full!\n")
				#if the received response from server is ERR_LDNE, 
				#parsing connect_data will result to an exception hence going inside except block
			except:
				if connectPacket.type == TcpPacket.ERR_LDNE:
					print("Lobby does not exist!\n")
	print('Received from server: ' + str(connectPacket))  # show in terminal
	return connectPacket

def Chat(player, packet, lobby_id, connectPacket):
	#on-going chat room
	packet_type = 0
	while True:
		# maintains a list of possible input streams 
		sockets_list = [sys.stdin, socket] 
		'''
		" There are two possible input situations. Either the 
		user wants to give manual input to send to other people, 
		or the server is sending a message to be printed on the 
		screen. Select returns from sockets_list, the stream that 
		is reader for input. So for example, if the server wants 
		to send a message, then the if condition will hold true 
		below.If the user wants to send a message, the else 
		condition will evaluate as true"
		'''
		#Instantiate chat packet 
		chatPacket = packet.ChatPacket()
		#Instantiate disconnect packet
		disconnectPacket = packet.DisconnectPacket()
		disconnectPacket.type = TcpPacket.DISCONNECT
		read_sockets,write_socket,error_socket = select.select(sockets_list,[],[])
		for socks in read_sockets: 
			if socks == socket: 
				packet_received = bytearray(socket.recv(2048))
				packet.ParseFromString(packet_received)
				packet_type = packet.type 
				#Disconnect packet type
				if packet_type == 0:
					disconnectPacket.ParseFromString(packet_received)
					if disconnectPacket.player.name == "":
						#if the disconnection is normal
						if disconnectPacket.update == 0:
							print("You left the game.")
						else:
							print("Unknown error occured.\nYou have been disconnected from the game")
						sys.exit()
					else :
						print(disconnectPacket.player.name + " has left the game.")
				#Connect packet type
				if packet_type == 1:
					connectPacket.ParseFromString(packet_received)
					print(connectPacket.player.name + " has entered the game")
				#Chat packet type
				if packet_type == 3:
					#Receive broadcasted data from server
					chatPacket.ParseFromString(packet_received)
					print(chatPacket.player.name+": "+ chatPacket.message) 
			else: 
				# #Write your message here
				chatPacket.type = TcpPacket.CHAT
				chatPacket.message = sys.stdin.readline()
				chatPacket.player.name = player_name
				chatPacket.lobby_id = lobby_id
			
				socket.send(chatPacket.SerializeToString())

				if chatPacket.message.strip() == "bye":
					disconnectPacket.type = TcpPacket.DISCONNECT

					disconnectPacket.player.name = player_name
					socket.send(disconnectPacket.SerializeToString())
=======

#Connect host to server using connectPacket	
def ConnectHostToServer(player, packet, max_players):
	connectPacket = packet.ConnectPacket()

	connectPacket.type = TcpPacket.CONNECT
	lobby_id = CreateLobby(packet, max_players)
	connectPacket.lobby_id = lobby_id
	connectPacket.player.name = player.name
	#Send connect packet to server
	socket.send(connectPacket.SerializeToString()) 

	#Receive broadcasted data from server
	connect_data = bytearray(socket.recv(1024)) # receive response from server
	connectPacket.ParseFromString(connect_data)

	print('Received from server: ' + str(connectPacket))  # show in terminal
	return connectPacket

#Connect players (including host) to server using connectPacket	
def ConnectPlayerToServer(player, packet, lobby_id):
	connectPacket = packet.ConnectPacket()

	connectPacket.type = TcpPacket.ERR_LDNE
	#assume first that the connectPacket type is error packet so that all can be put inside a try catch
	#and loop until the lobby chosen is existing or is not full
	while connectPacket.type == TcpPacket.ERR_LDNE or connectPacket.type == TcpPacket.ERR_LFULL:
		try:
			# lobby_id = input("Enter lobby id: ") 
			connectPacket.type = TcpPacket.CONNECT
			connectPacket.lobby_id = lobby_id
			connectPacket.player.name = player.name
			#Send connect packet to server
			socket.send(connectPacket.SerializeToString()) 
			#Receive broadcasted data from server
			connect_data = bytearray(socket.recv(1024)) # receive response from server

			time.sleep(3)
			connectPacket.ParseFromString(connect_data)
			#if the received response from the server is ERR_LFULL, 
			#parsing connect_data will NOT result to exception
			if connectPacket.type == TcpPacket.ERR_LFULL:
				print("Lobby is full!\n")
			#if the received response from server is ERR_LDNE, 
			#parsing connect_data will result to an exception hence going inside except block
		except:
			if connectPacket.type == TcpPacket.ERR_LDNE:
				print("Lobby does not exist!\n")
	print('Received from server: ' + str(connectPacket))  # show in terminal
	return connectPacket

# #Connect players (including host) to server using connectPacket	
# def ConnectHostToServer(player, packet, max_players):
# 	connectPacket = packet.ConnectPacket()
	
# 	connectPacket.type = TcpPacket.CONNECT
# 	lobby_id = CreateLobby(packet)
# 	connectPacket.lobby_id = lobby_id
# 	connectPacket.player.name = player.name
# 	#Send connect packet to server
# 	socket.send(connectPacket.SerializeToString()) 

# 	#Receive broadcasted data from server
# 	connect_data = bytearray(socket.recv(1024)) # receive response from server
# 	connectPacket.ParseFromString(connect_data)

# def ConnectPlayerToServer(player, packet, role):


# 	if role == "h":
		
# 	else:
# 		connectPacket.type = TcpPacket.ERR_LDNE
# 		#assume first that the connectPacket type is error packet so that all can be put inside a try catch
# 		#and loop until the lobby chosen is existing or is not full
# 		while connectPacket.type == TcpPacket.ERR_LDNE or connectPacket.type == TcpPacket.ERR_LFULL:
# 			try:
# 				lobby_id = input("Enter lobby id: ") 
# 				connectPacket.type = TcpPacket.CONNECT
# 				connectPacket.lobby_id = lobby_id
# 				connectPacket.player.name = player.name
# 				#Send connect packet to server
# 				socket.send(connectPacket.SerializeToString()) 
# 				#Receive broadcasted data from server
# 				connect_data = bytearray(socket.recv(1024)) # receive response from server
# 				connectPacket.ParseFromString(connect_data)
# 				#if the received response from the server is ERR_LFULL, 
# 				#parsing connect_data will NOT result to exception
# 				if connectPacket.type == TcpPacket.ERR_LFULL:
# 					print("Lobby is full!\n")
# 				#if the received response from server is ERR_LDNE, 
# 				#parsing connect_data will result to an exception hence going inside except block
# 			except:
# 				if connectPacket.type == TcpPacket.ERR_LDNE:
# 					print("Lobby does not exist!\n")
# 	print('Received from server: ' + str(connectPacket))  # show in terminal
# 	return connectPacket

def Chat(player, packet, lobby_id, connectPacket):
	#on-going chat room
	packet_type = 0
	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, socket] 
	'''
	" There are two possible input situations. Either the 
	user wants to give manual input to send to other people, 
	or the server is sending a message to be printed on the 
	screen. Select returns from sockets_list, the stream that 
	is reader for input. So for example, if the server wants 
	to send a message, then the if condition will hold true 
	below.If the user wants to send a message, the else 
	condition will evaluate as true"
	'''
	#Instantiate chat packet 
	chatPacket = packet.ChatPacket()
	#Instantiate disconnect packet
	disconnectPacket = packet.DisconnectPacket()
	disconnectPacket.type = TcpPacket.DISCONNECT
	read_sockets,write_socket,error_socket = select.select(sockets_list,[],[])
	for socks in read_sockets: 
		if socks == socket: 
			packet_received = bytearray(socket.recv(2048))
			packet.ParseFromString(packet_received)
			packet_type = packet.type 
			#Disconnect packet type
			if packet_type == 0:
				disconnectPacket.ParseFromString(packet_received)
				if disconnectPacket.player.name == "":
					#if the disconnection is normal
					if disconnectPacket.update == 0:
						print("You left the game.")
					else:
						print("Unknown error occured.\nYou have been disconnected from the game")
					sys.exit()
				else :
					print(disconnectPacket.player.name + " has left the game.")
			#Connect packet type
			if packet_type == 1:
				connectPacket.ParseFromString(packet_received)
				print(connectPacket.player.name + " has entered the game")
			#Chat packet type
			if packet_type == 3:
				#Receive broadcasted data from server
				chatPacket.ParseFromString(packet_received)
				print(chatPacket.player.name+": "+ chatPacket.message) 
		else: 
			# #Write your message here
			chatPacket.type = TcpPacket.CHAT
			chatPacket.message = sys.stdin.readline()
			chatPacket.player.name = player_name
			chatPacket.lobby_id = lobby_id
		
			socket.send(chatPacket.SerializeToString())

			if chatPacket.message.strip() == "bye":
				disconnectPacket.type = TcpPacket.DISCONNECT

				disconnectPacket.player.name = player_name
				socket.send(disconnectPacket.SerializeToString())
>>>>>>> ced8a96107c626e978a6abfc44b6c04b213c84f8

#######################################################################
#								MAIN                				  #
#######################################################################

<<<<<<< HEAD
#Instantiate packet
packet = TcpPacket()

#Instantiate player
player_name = input("Enter name: ")
player = InstantiatePlayer(player_name)

connectPacket = ConnectPlayerToServer(player, packet)
Chat(player, packet, connectPacket.lobby_id, connectPacket)
socket.close() 
=======
# ConnectToServer()
# # Instantiate packet
# packet = TcpPacket()

# #Instantiate player
# player_name = input("Enter name: ")
# player = InstantiatePlayer(player_name)
# role = input("Are you a HOST(H) or a PLAYER(P)? : ").lower()

# connectPacket = ConnectPlayerToServer(player, packet, role)
# while True:
# 	Chat(player, packet, connectPacket.lobby_id, connectPacket)
# socket.close() 
>>>>>>> ced8a96107c626e978a6abfc44b6c04b213c84f8
