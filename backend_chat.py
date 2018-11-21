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

#Connect to socket to server address
server_address = ('202.92.144.45', 80) 	#address = (hostname, port)
socket = socket.socket()  # instantiate socket
socket.connect(server_address)  # connect to the server using address 

#Instantiate packet
packet = TcpPacket()

player_name = input("Enter name: ")
#instantiate player 
player = Player()
player.name = player_name
role = input("Are you a HOST(H) or a PLAYER(P)? : ").lower()
lobby_id = "" #initialize lobby_id
if role == 'h': #Host
	#CREATE LOBBY

	#Instantiate Create Lobby using the packet.type = CREATE_LOBBY from TcpPacket, which is 2. (check tcp_packet.proto)
	lobbyPacket = packet.CreateLobbyPacket()
	lobbyPacket.type = TcpPacket.CREATE_LOBBY
	lobbyPacket.max_players = int(input("Enter max number of players: "))
	
	#Send the lobbyPacket to server
	socket.send(lobbyPacket.SerializeToString()) 
	
	#Receive lobby id from server
	data = bytearray(socket.recv(1024)) # receive response from server
	lobbyPacket.ParseFromString(data)
	print('Received from server: ' + lobbyPacket.lobby_id)  # show in terminal
	lobby_id = lobbyPacket.lobby_id

	
else:	#Player (NOT HOST)
	#Input lobby id
	lobby_id = input("Enter lobby id: ") 

#Connect players (including host) to server using connectPacket
#Instantiate connectPacket 
connectPacket = packet.ConnectPacket()
connectPacket.type = TcpPacket.CONNECT
connectPacket.lobby_id = lobby_id
connectPacket.player.name = player_name
#Send connect packet to server
socket.send(connectPacket.SerializeToString()) 

#Receive broadcasted data from server
connect_data = bytearray(socket.recv(1024)) # receive response from server
connectPacket.ParseFromString(connect_data)
print('Received from server: ' + str(connectPacket))  # show in terminal

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
	read_sockets,write_socket,error_socket = select.select(sockets_list,[],[])
	for socks in read_sockets: 
		if socks == socket: 
			packet_received = bytearray(socket.recv(2048))
			packet.ParseFromString(packet_received)
			packet_type = packet.type 
			if packet_type == 0:
				disconnect_data = bytearray(socket.recv(1024))
				disconnectPacket.ParseFromString(disconnect_data)
				print(disconnectPacket.player.name + " has disconnected")
				sys.exit()
			if packet_type == 1:
				connectPacket.ParseFromString(packet_received)
				print(connectPacket.player.name + " has entered the game")
			if packet_type == 3:
				#Receive broadcasted data from server
				chatPacket.ParseFromString(packet_received)
				print("Chat packet broadcasted: " + chatPacket.message) 	
		else: 

			# #Write your message here
			chatPacket.type = TcpPacket.CHAT
			chatPacket.message = sys.stdin.readline()
			chatPacket.player.name = player_name
			chatPacket.lobby_id = lobby_id
		
			socket.send(chatPacket.SerializeToString())

			if chatPacket.message.strip() == "bye":
				disconnectPacket.type = TcpPacket.DISCONNECT
				socket.send(disconnectPacket.SerializeToString())
			
socket.close() 
