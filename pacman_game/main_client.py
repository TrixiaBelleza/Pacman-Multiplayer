# import backend_chat
import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
from tcp_packet_pb2 import TcpPacket
from player_pb2 import Player
from Banner.banner import Banner
from sprites.Pacman.yellow import Yellow
from sprites.Pacman.blue import Blue
from sprites.Pacman.purple import Purple
from sprites.Pacman.green import Green
import select
import socket
import client

# global socket
server_address = ('202.92.144.45', 80) 	#address = (hostname, port)
socket = socket.socket()  # instantiate socket
socket.connect(server_address)  # connect to the server using address 

################ BACKEND ################################################

def ConnectToServer():
	#Connect to socket to server address
	global socket
	server_address = ('202.92.144.45', 80) 	#address = (hostname, port)
	socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # instantiate socket
	socket.connect(server_address)  # connect to the server using address 
	print("Socket connected to server!")
	return socket
def CreateLobby(packet, max_players):
	#CREATE LOBBY

	#Instantiate Create Lobby using the packet.type = CREATE_LOBBY from TcpPacket, which is 2. (check tcp_packet.proto)
	lobbyPacket = packet.CreateLobbyPacket()
	lobbyPacket.type = TcpPacket.CREATE_LOBBY
	lobbyPacket.max_players = max_players
	
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

# Connect host to server using connectPacket	
def ConnectHostToServer(player, packet, max_players):
	connectPacket = packet.ConnectPacket()

	connectPacket.type = TcpPacket.CONNECT
	lobby_id = CreateLobby(packet, max_players)
	connectPacket.lobby_id = lobby_id
	connectPacket.player.name = player.name
	socket.send(connectPacket.SerializeToString()) 	# Send connect packet to server

	# Receive broadcasted data from server
	connect_data = bytearray(socket.recv(1024)) # receive response from server
	connectPacket.ParseFromString(connect_data)

	print('Received from server: ' + str(connectPacket))  # show in terminal
	return connectPacket

# Connect players (including host) to server using connectPacket	
def ConnectPlayerToServer(player, connectPacket, lobby_id):
	
	connectPacket.type = TcpPacket.CONNECT
	connectPacket.lobby_id = lobby_id
	connectPacket.player.name = player.name
	socket.send(connectPacket.SerializeToString()) 		# Send connect packet to server
	
	# Receive broadcasted data from server
	connect_data = bytearray(socket.recv(1024)) 	# Receive response from server
	
	try:
		connectPacket.ParseFromString(connect_data)
	except:
		return connectPacket	
		
	#if the received response from the server is ERR_LFULL, 
	#parsing connect_data will NOT result to exception
	
	#if the received response from server is ERR_LDNE, 
	#parsing connect_data will result to an exception hence going inside except block
		
	
	return connectPacket

#############################################################################################



name = input("Enter your name: ")
ptype = input("Enter your type: ")
port = int(input("Enter port: "))
# hostname = input("Enter hostname: ")
# c = client.Client(name, ptype)
c = client.Client()

hostname = '127.0.0.1'

c.hostname = hostname
c.port = port

c.connect()

if c.player.player_type == "HOST" :
	lobby_id = c.create_room()
else :
	lobby_id = input("Enter lobby_id: ")
	
if c.join(lobby_id) == True:
	while True:
		num_of_players = c.recvNumOfPlayers()
		print(num_of_players)
		if num_of_players == 3:
			game_state = c.startGame()
			break
