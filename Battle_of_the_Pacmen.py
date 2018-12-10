# import backend_chat
import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
from tcp_packet_pb2 import TcpPacket
from player_pb2 import Player
from Banner.banner import Banner
import select
import socket

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
def ConnectPlayerToServer(player, connectPacket, lobby_id):
	#connectPacket = packet.ConnectPacket()

	#connectPacket.type = TcpPacket.ERR_LDNE
	#assume first that the connectPacket type is error packet so that all can be put inside a try catch
	#and loop until the lobby chosen is existing or is not full
	
	# lobby_id = input("Enter lobby id: ") 
	connectPacket.type = TcpPacket.CONNECT
	connectPacket.lobby_id = lobby_id
	connectPacket.player.name = player.name
	#Send connect packet to server
	socket.send(connectPacket.SerializeToString()) 
	#Receive broadcasted data from server
	connect_data = bytearray(socket.recv(1024)) # receive response from server
	
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


def pacman_window():
	tk_window = tkinter.Tk()
	tk_window.title("BATTLE OF THE PACMEN")
	w = 700 # height for tk_window
	h = 700 # height for tk_window
	x = (tk_window.winfo_screenwidth()/2) - (w/2) # calculate x and y coordinates for tk_window
	y = (tk_window.winfo_screenheight()/2) - (h/2)
	# set the dimensions of the screen and where it is placed
	tk_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	tk_window.configure(bg="BLACK", padx=50, pady=50)
	return tk_window

def main():
	window = pacman_window()
	return window

def show_About():
	messagebox.showinfo("ABOUT", "This game is brought to you by:\n\n Trixia Belleza\n Jesi Musngi\n Mark Mataya\n Kianne Luna\n\nAll rights reserved.2018")

def show_Mechanics():
	messagebox.showinfo("MECHANICS", "  At the start of the game, all pacmen are placed at the corners of the map. The pacmen can move using the up, down, left, and right arrow keys. The pacmen will run through the maze to eat pac-dots and pac-stars. One pac-star will appear every 15 seconds after one pac-star has been eaten. If a pacman gets to eat a pac-star, he will be given a temporary ability to eat the other pacmen. The amount of time a pacman can have this ability is only 5 seconds. The pacman that has been eaten will be revived at the middle of the map. However, he will not be able to move for the first 3 seconds upon revival. When the game is over, the pacman that has the most number of pac-points wins. Players can chat during the game.")

def exit_Game():
	prompt = messagebox.askyesno("EXIT", "Are you sure you want to exit? No data will be saved.")
	if prompt == True:
		window.destroy()

# GETS PLAYER'S NAME ================================================================================================
def getPlayerType():
	player_type = messagebox.askquestion("USER TYPE", "Are you the host?\nPress YES if you are the host. NO if you're just a player.")
	if player_type == "yes":
		player_type = "h"
	else:
		player_type = "p"
	return player_type

def btn_ok(event=None):
	if name_Entry.get().isalnum():
		player =  InstantiatePlayer(name_Entry.get()) 		# instantiate player
		packet = TcpPacket() 		# instantiate packet

		# HOST ==========================================
		if getPlayerType() == "h":
			max_players = simpledialog.askinteger("Max Players", "Enter max number of players", parent=name_Frm)
			connectPacket =  ConnectHostToServer(player,packet,max_players)
			lobby_id = connectPacket.lobby_id

		# NOT HOST ========================================
		else:
			connectPacket = packet.ConnectPacket()
			connectPacket.type = 5
			L = Label()
			while connectPacket.type==5 or connectPacket.type==6: 

				lobby_id = simpledialog.askstring("Lobby ID", "Enter lobby ID", parent=name_Frm)
				connectPacket =  ConnectPlayerToServer(player, connectPacket, lobby_id)
				L.destroy()

				# Lobby does not exist
				if connectPacket.type==5:
					L = Label(name_Frm, text="Lobby does not exist!", bg="BLACK", fg="RED")
					L.grid(column=0, row=3, columnspan=2)

				# Lobby full
				if connectPacket.type==6:
					L = Label(name_Frm, text="Lobby full!", bg="BLACK", fg="RED")
					L.grid(column=0, row=3, columnspan=2)

			print('Received from server: ' + str(connectPacket))  # show in terminal
			print(connectPacket.player.name + " has entered the chat room.")		

		game_map(chosen_map, player, packet, lobby_id, connectPacket) 	# show game
		name_Frm.pack_forget()
	else:
		L = Label(name_Frm, text="Invalid name. Must consist of \nletters and numbers only.", bg="BLACK", fg="RED")
		L.grid(column=0, row=3, columnspan=2)

def btn_cancel():
	name_Frm.pack_forget()
	main_frame.pack()

# Name of chosen map
def get_name(map_selected):
	global chosen_map
	chosen_map = map_selected

	main_frame.pack_forget()

	global name_Frm
	name_Frm = Frame(window, bg="BLACK", pady=100)

	# Ask for player's name
	L = Label(name_Frm, text="Please enter your name", bg="BLACK", fg="WHITE", pady=20)
	L.grid(column=0, row=0, columnspan=2)
	global name_Entry
	name_Entry = Entry(name_Frm, width=20)
	name_Entry.grid(column=0, row=1, columnspan=2)
	w = Button(name_Frm, text="Proceed", width=10, command=btn_ok)
	w.grid(column=0, row=2, padx=5, pady=20)
	w = Button(name_Frm, text="Cancel", width=10, command=btn_cancel)
	w.grid(column=1, row=2, padx=5, pady=20)
	name_Entry.focus_set()
	name_Entry.bind("<Return>", btn_ok)

	name_Frm.pack()


# GAME ENVIRONMENT ==================================================================================================

def game_map(chosen_map, player, packet, lobby_id, connectPacket):

	# MAP FRAME ---------------------------------------------------------------
	global map_Frame
	map_Frame = Frame(window, bg="BLACK", pady=20)
	
	map_template = None
	if chosen_map == 1:
		map_template = open("map1.txt", "r")
		map_name = "Map 1"
	if chosen_map == 2:
		map_template = open("map2.txt", "r")
		map_name = "Map 2"
	if chosen_map == 3:
		map_template = open("map3.txt", "r")
		map_name = "Map 3"

	if map_template == None:
		messagebox.showerror("ERROR", "File not found.")
		return

	global map_matrix
	map_matrix = []
	
	for lines in map_template:
		line = []
		line[0:len(lines)] = iter(lines)
		map_matrix.append(line)	

	main_frame.pack_forget()
	title_frame.pack_forget()
	create_Map()

	# MENU BOX FRAME ----------------------------------------------------------
	global optionsFrm
	optionsFrm = Frame(window, bg="BLACK")

	map_name_lbl = Label(optionsFrm, text=map_name, bg="#80dba6", padx=15)
	map_name_lbl.grid(column=0, row=0, padx=40)	
	
	global Back_btn
	Back_btn = Button(optionsFrm, text="Exit Game",bg="sky blue", padx=15, pady=0, command=exit)
	Back_btn.grid(column=1, row=0, padx=40)	
		
	# CHAT HISTORY FRAME ------------------------------------------------------
	global chat_history_Frm
	chat_history_Frm = Frame(window, bg="WHITE", height=50)
	chat_history()

	# CHAT ENTRY FRAME --------------------------------------------------------
	global entry_Frm
	entry_Frm = Frame(window, bg="BLACK", height=50)
	chat_entry(player, packet, lobby_id, connectPacket)
	optionsFrm.pack()
	map_Frame.pack()
	chat_history_Frm.pack(fill=X)
	entry_Frm.pack(fill=X)	
	map_template.close()

	separator = Frame(height=2, bd=1, relief=SUNKEN)
	separator.pack(fill=X, padx=8, pady=8)

	# INSTRUCTIONS LABEL FRAME -------------------------------------------------
	inst_Frm = LabelFrame(window,text = "INSTRUCTIONS", bg = "BLACK", fg = "WHITE")
	inst_Frm.pack(fill=X)

	up_Arrow = Label(inst_Frm, text = "Up Arrow Key - Go Up", bg = "BLACK", fg = "WHITE")
	up_Arrow.pack()
	down_Arrow = Label(inst_Frm, text = "Down Arrow Key - Go Down", bg = "BLACK", fg = "WHITE")
	down_Arrow.pack()
	right_Arrow = Label(inst_Frm, text = "Right Arrow Key - Go Right", bg = "BLACK", fg = "WHITE")
	right_Arrow.pack()
	left_Arrow = Label(inst_Frm, text = "Left Arrow Key - Go Left", bg = "BLACK", fg = "WHITE")
	left_Arrow.pack()

# GAME FUNCTIONS ====================================================================================================

def get_Player_pos():
	global player_xpos
	global player_ypos
	for row in range(len(map_matrix)):
		for col in range(len(map_matrix[row])):
			if map_matrix[row][col] == "P":	# PLAYER
				player_xpos = row
				player_ypos = col

def create_Map():
	block_height = 20 * len(map_matrix)
	block_width = 20 * len(map_matrix[0])
	global canvas
	canvas = tkinter.Canvas(map_Frame, bg="BLACK", height=block_height, width=block_width)
	canvas.pack()
	
	y_pos = 0 # starting pixel in canvas
	increment = 20 # to determine next position
	for row in range(len(map_matrix)):
		x_pos = 0
		for col in range(len(map_matrix[row])):
			if map_matrix[row][col] == "D":		# PAC-DOT
				block = canvas.create_oval(x_pos+8, y_pos+8, x_pos-8+increment, y_pos-8+increment, fill="WHITE", outline="")
			elif map_matrix[row][col] == "s":	# STAR
				ax = x_pos+(increment/2), 
				ay = y_pos
				bx = x_pos+1
				by = y_pos+(increment/3)
				cx = x_pos+(increment/5)
				cy = y_pos+increment
				dx = x_pos+(increment/5)*4
				dy = y_pos+increment
				ex = x_pos+increment
				ey = y_pos+(increment/3)
				block = canvas.create_polygon(ax, ay, cx, cy, ex, ey, bx, by, dx, dy, fill="YELLOW", outline="")
			elif map_matrix[row][col] == "w":	# WALL
				block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLUE", outline="")
			elif map_matrix[row][col] == "e":	# EMPTY FLOOR
				block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLACK", outline="")
			elif map_matrix[row][col] == "P":	# PLAYER
				block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="RED", outline="")
			x_pos += increment
		y_pos += increment
	
	canvas.bind_all("<KeyPress-Up>", key_listeners) # binds event listener to whole canvas
	canvas.bind_all("<KeyPress-Down>", key_listeners) # binds event listener to whole canvas
	canvas.bind_all("<KeyPress-Left>", key_listeners) # binds event listener to whole canvas
	canvas.bind_all("<KeyPress-Right>", key_listeners) # binds event listener to whole canvas

def key_listeners(event):
	get_Player_pos()

	if event.keysym == "Left":
		if map_matrix[player_xpos][player_ypos-1] == "D" or map_matrix[player_xpos][player_ypos-1] == "s" or map_matrix[player_xpos][player_ypos-1] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos][player_ypos-1] = "P"
			block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
			block = canvas.create_rectangle((player_ypos-1)*20, player_xpos*20, (player_ypos-1)*20+20, player_xpos*20+20, fill="RED", outline="")
	elif event.keysym == "Right":
		if map_matrix[player_xpos][player_ypos+1] == "D" or map_matrix[player_xpos][player_ypos+1] == "s" or map_matrix[player_xpos][player_ypos+1] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos][player_ypos+1] = "P"
			block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
			block = canvas.create_rectangle((player_ypos+1)*20, player_xpos*20, (player_ypos+1)*20+20, player_xpos*20+20, fill="RED", outline="")
	elif event.keysym == "Up":
		if map_matrix[player_xpos-1][player_ypos] == "D" or map_matrix[player_xpos-1][player_ypos] == "s" or map_matrix[player_xpos-1][player_ypos] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos-1][player_ypos] = "P"
			block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
			block = canvas.create_rectangle(player_ypos*20, (player_xpos-1)*20, player_ypos*20+20, (player_xpos-1)*20+20, fill="RED", outline="")
	elif event.keysym == "Down":
		if map_matrix[player_xpos+1][player_ypos] == "D" or map_matrix[player_xpos+1][player_ypos] == "s" or map_matrix[player_xpos+1][player_ypos] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos+1][player_ypos] = "P"
			block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
			block = canvas.create_rectangle(player_ypos*20, (player_xpos+1)*20, player_ypos*20+20, (player_xpos+1)*20+20, fill="RED", outline="")


# CHAT FUNCTIONALITIES ==============================================================================================

def chat_history():
	global chat_history_Txt
	chat_scrollbar = Scrollbar(chat_history_Frm)
	chat_history_Txt = Text(chat_history_Frm, height=5)
	chat_scrollbar.pack(side=RIGHT, fill=Y)
	chat_history_Txt.pack(side=LEFT, fill=X)
	chat_scrollbar.config(command=chat_history_Txt.yview)
	chat_history_Txt.config(yscrollcommand=chat_scrollbar.set)
	chat_history_Txt.config(state=DISABLED)

def process(data):
    print("processing: {0}".format(data))

def entry_callback(event):
    print("entry")
    process(event.widget.get())

def chat_process(player, packet, lobby_id, connectPacket):
	sockets_list = [sys.stdin, socket] 
	chatPacket = packet.ChatPacket() 	# Instantiate chat packet 
	disconnectPacket = packet.DisconnectPacket() 	# Instantiate disconnect packet
	disconnectPacket.type = TcpPacket.DISCONNECT

	# ON-GOING CHAT -----------------------------------------------------------
	read_sockets,write_socket,error_socket = select.select(sockets_list,[],[],0)
	for socks in read_sockets: 

		packet_received = bytearray(socket.recv(2048))
		packet.ParseFromString(packet_received)
		packet_type = packet.type 

		if packet_type == 0:
			disconnectPacket.ParseFromString(packet_received)
			if disconnectPacket.player.name == "":
				if disconnectPacket.update == 0: 		# if the disconnection is normal
					print("You left the chat room.")
				else:
					print("Unknown error occured.\nYou have been disconnected from the chat room.")
				socket.close()
				sys.exit()
			else :
				# broadcast disconnected player
				print(disconnectPacket.player.name + " has left the chat room.")
				chat_history_Txt.config(state=NORMAL)
				chat_history_Txt.insert(END, disconnectPacket.player.name + " has left the chat room." + '\n')
				chat_history_Txt.see("end")
				chat_history_Txt.config(state=DISABLED)

		# Connect packet type
		if packet_type == 1:
			connectPacket.ParseFromString(packet_received)
			print(connectPacket.player.name + " has entered the chat room." + '\n')

			chat_history_Txt.config(state=NORMAL)
			chat_history_Txt.insert(END, connectPacket.player.name + " has entered the chat room." + '\n')
			chat_history_Txt.see("end")
			chat_history_Txt.config(state=DISABLED)

		# Chat packet type
		if packet_type == 3:

			# Receive broadcasted data from server
			chatPacket.ParseFromString(packet_received)
			print(chatPacket.player.name+": "+ chatPacket.message) 

			chat_history_Txt.config(state=NORMAL)
			chat_history_Txt.insert(END, chatPacket.player.name+ ':' + chatPacket.message + '\n')
			chat_history_Txt.see("end")
			chat_history_Txt.config(state=DISABLED)
			
		# Exit Chat
		if chatPacket.message.strip() == "bye" and chatPacket.player.name == player.name:
			disconnectPacket.type = TcpPacket.DISCONNECT
			disconnectPacket.player.name = player.name
			socket.send(disconnectPacket.SerializeToString())

		chat_entry.delete(0,len(chat_entry.get()))

	window.after(100,chat_process,player, packet, lobby_id, connectPacket)


def chat_entry(player, packet, lobby_id, connectPacket):
	global chat_entry
	chat_entry = Entry(entry_Frm, width=67)
	chat_entry.focus_set()
	chat_entry.bind("<Return>", lambda x: get_chat_entry(player,packet,lobby_id, connectPacket))
	
	chat_entry.grid(column=0, row=0)

	enter_chat_btn = Button(entry_Frm, text="Enter", command=lambda x : get_chat_entry(player,packet,lobby_id, connectPacket), pady=0)

	enter_chat_btn.grid(column=1, row=0)
	chat_process(player, packet, lobby_id, connectPacket)

	chat_history_Txt.config(state=NORMAL)
	chat_history_Txt.insert(END, "You entered the chat room." + '\n')
	chat_history_Txt.see("end")
	chat_history_Txt.config(state=DISABLED)
	
def get_chat_entry(player, packet, lobby_id, connectPacket, event=None):
	# maintains a list of possible input streams 
	sockets_list = [sys.stdin, socket]
	chatPacket = packet.ChatPacket()

	chatPacket.type = TcpPacket.CHAT
	chatPacket.message = chat_entry.get()
	chatPacket.player.name = player.name
	chatPacket.lobby_id = lobby_id
	
	socket.send(chatPacket.SerializeToString())

	return chat_entry.get()

# BACK TO MAIN MENU PROMPT ==========================================================================================
def back():
	prompt = messagebox.askyesno("ARE YOU SURE YOU WANT TO EXIT?", "Once you leave, your game will be lost.")
	if prompt == True:
		map_Frame.destroy()
		optionsFrm.destroy()
		chat_history_Frm.destroy()
		entry_Frm.destroy()
		main_frame.pack()

# MAIN ==============================================================================================================

window = main()
window.resizable(width=FALSE, height=FALSE)
title_frame = Frame(window, bg="BLACK", padx=30, pady=30)
title_frame.pack_propagate(True)
title_frame.pack()

main_frame = Frame(window, bg="BLACK", padx=50, pady=50)
main_frame.pack_propagate(False)
main_frame.pack()

title = Banner(title_frame)

# MAIN WINDOW WIDGETS ===============================================================================================

PickLbl = Label(main_frame, text="Please choose a game map", bg="BLACK", fg="#e07b6a", font=("Arial Bold",14))
PickLbl.grid(column=0, row=0, padx=10, pady=10, ipadx=30, ipady=10, columnspan=3)
game_map1btn = Button(main_frame, bg='#80dba6', fg="#302727", text="Map 1", command=lambda main_frame=1:get_name(main_frame))
game_map2btn = Button(main_frame, bg='#80dba6', fg="#302727", text="Map 2", command=lambda main_frame=2:get_name(main_frame))
game_map3btn = Button(main_frame, bg='#80dba6', fg="#302727", text="Map 3", command=lambda main_frame=3:get_name(main_frame))
game_map1btn.grid(column=0, row=2, padx=1, pady=10, ipadx=9, ipady=10)
game_map2btn.grid(column=1, row=2, padx=1, pady=10, ipadx=9, ipady=10)
game_map3btn.grid(column=2, row=2, padx=1, pady=10, ipadx=9, ipady=10)

about_btn = Button(main_frame, text="About", command=show_About)
about_btn.grid(column=0, row=3, padx=10, ipadx=5, pady=25, ipady=6, sticky=SE)
how_btn = Button(main_frame, text="Mechanics", command=show_Mechanics)
how_btn.grid(column=1, row=3, padx=10, ipadx=5, pady=25, ipady=6, sticky=SE)
exit_btn = Button(main_frame, text="Exit", command=exit_Game)
exit_btn.grid(column=2, row=3, padx=10, ipadx=10, pady=25, ipady=6, sticky=SE)

#====================================================================================================================

window.mainloop()

# FOR REFERENCE, PLEASE READ:
# Shipman, John W. "Tkinter 8.5 reference: a GUI for." 31 December 2013. New Mexico Tech Computer Center. Web / PDF.