#Instantiate socket as attribute
# attribute niya yung server address 
#socket.setblocking(0)
from Banner.banner import Banner
import socket
import pacman
import pickle
import udp_packet as UDPpacket
import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
from tcp_packet_pb2 import TcpPacket
from player_pb2 import Player
from sprites.Pacman.yellow import Yellow
from sprites.Pacman.blue import Blue
from sprites.Pacman.purple import Purple
from sprites.Pacman.green import Green
import select


#############################################################################################

class Client():
	socket = None
	BUFFER_SIZE = 4096
	server_address = ('0.0.0.0', 10939)
	hostname = '127.0.0.1'
	port = ''
	client_addr = ''
	map_matrix = []
	window = ''
	canvas = ''
	selected_map = ''
	main_frame = ''
	player_name = ''
	player_type = ''


	def __init__(self):
		self.render_window()


	#Connect Client to Server
	def connect(self):
		print("jere")
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.client_addr = (self.hostname, self.port)
		self.socket.bind(self.client_addr)

		# self.socket.setblocking(0)
	
		#Always create a UDPpacket first! before sending to server.
		#Kasi mas madali iaccess and mas organized, madaling i-trace  
		#send connect packet to server
		connectPacket = UDPpacket.UDPpacket("CONNECT")
		connectPacket.player = self.player
		self.socket.sendto(pickle.dumps(connectPacket), self.server_address)


	def create_room(self):
		createroomPacket = UDPpacket.UDPpacket("CREATE_ROOM")
		createroomPacket.player = self.player
		self.socket.sendto(pickle.dumps(createroomPacket), self.server_address)

		#Receive response lobby id from server
		data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		loaded_data = pickle.loads(data)
		print("LOBBY ID FROM SERVER: ")
		print(loaded_data.lobby_id_udp)
		#return lobby id
		return(loaded_data.lobby_id_udp)

	def join(self, lobby_id_udp):
		joinPacket = UDPpacket.UDPpacket("JOIN")
		joinPacket.player = self.player
		joinPacket.lobby_id_udp = lobby_id_udp
		self.socket.sendto(pickle.dumps(joinPacket), self.server_address)

		data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		loaded_data = pickle.loads(data)
		if loaded_data.packet_type == "VALID_LOBBY_ID":
			return True
		else:
			return False

	def recvNumOfPlayers(self):
		getPlayerCountPacket = UDPpacket.UDPpacket("PLAYER_COUNT")
		self.socket.sendto(pickle.dumps(getPlayerCountPacket), self.server_address)	

		#Receive player count from server
		data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		loaded_data = pickle.loads(data)

		return(loaded_data.player_count)

	def startGame(self):
		startGamePacket =  UDPpacket.UDPpacket("START_GAME")
		self.socket.sendto(pickle.dumps(startGamePacket), self.server_address)	

		#Receive game map
		#Receive player count from server
		data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		loaded_data = pickle.loads(data)

		self.map_matrix = loaded_data.map_matrix

		# if self.selected_map == 1:
		# 	self.selected_map = "map1.txt"
		# if self.selected_map == 2:
		# 	self.selected_map = "map2.txt"
		# if self.selected_map == 3:
		# 	self.selected_map = "map3.txt"

		# mapPacket = UDPpacket.UDPpacket("MAP_PACKET")
		# mapPacket.map_file = self.selected_map
		# self.socket.sendto(pickle.dumps(mapPacket), self.server_address)

		self.game_map()

	def move(self, movement): 
		movementPacket = UDPpacket.UDPpacket("MOVE")
		movementPacket.movement = movement
		movementPacket.player = self.player
		self.socket.sendto(pickle.dumps(movementPacket), self.server_address)

		#Receive player count from server
		data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		loaded_data = pickle.loads(data)

		self.map_matrix = loaded_data.map_matrix
		self.renew_map()

	def render_window(self):
		self.window = self.pacman_window()
		self.window.resizable(width=FALSE, height=FALSE)

		title_frame = Frame(self.window, bg="BLACK", padx=30, pady=30)
		title_frame.pack_propagate(True)
		title_frame.pack()

		self.main_frame = Frame(self.window, bg="BLACK", padx=50, pady=50)
		self.main_frame.pack_propagate(False)
		self.main_frame.pack()

		title = Banner(title_frame)

		# MAIN WINDOW WIDGETS ===============================================================================================

		PickLbl = Label(self.main_frame, text="Please choose a game map", bg="BLACK", fg="#e07b6a", font=("Arial Bold",14))
		PickLbl.grid(column=0, row=0, padx=10, pady=10, ipadx=30, ipady=10, columnspan=3)
		game_map1btn = Button(self.main_frame, bg='#80dba6', fg="#302727", text="Map 1", command=lambda main_frame=1:self.get_name(self.main_frame))
		game_map2btn = Button(self.main_frame, bg='#80dba6', fg="#302727", text="Map 2", command=lambda main_frame=2:self.get_name(self.main_frame))
		game_map3btn = Button(self.main_frame, bg='#80dba6', fg="#302727", text="Map 3", command=lambda main_frame=3:self.get_name(self.main_frame))
		game_map1btn.grid(column=0, row=2, padx=1, pady=10, ipadx=9, ipady=10)
		game_map2btn.grid(column=1, row=2, padx=1, pady=10, ipadx=9, ipady=10)
		game_map3btn.grid(column=2, row=2, padx=1, pady=10, ipadx=9, ipady=10)

		about_btn = Button(self.main_frame, text="About", command=self.show_About)
		about_btn.grid(column=0, row=3, padx=10, ipadx=5, pady=25, ipady=6)

		how_btn = Button(self.main_frame, text="Mechanics", command=self.show_Mechanics)
		how_btn.grid(column=1, row=3, padx=10, ipadx=5, pady=25, ipady=6)

		exit_btn = Button(self.main_frame, text="Exit", command=self.exit_Game)
		exit_btn.grid(column=2, row=3, padx=10, ipadx=10, pady=25, ipady=6)

		
		self.window.mainloop()
		# while True:
		# 	self.window.update_idletasks()
		# 	self.window.update()

		# 	updatePacket = UDPpacket.UDPpacket("UPDATE_PACKET")
		# 	self.socket.sendto(pickle.dumps(updatePacket), self.server_address)
		# 	data, addr = self.socket.recvfrom(self.BUFFER_SIZE)
		# 	loaded_data = pickle.loads(data)

		# 	self.map_matrix = loaded_data.map_matrix


	def pacman_window(self):
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

	def show_About(self):
		msg = "This is a Pacman-inspired multiplayer game brought to you by:\n\n Trixia Belleza\n Jesi Musngi\n Mark Mataya\n Kianne Luna\n\nCMSC 137 CD-4L | A.Y. 2018-2019\nAll rights reserved.2018"
		messagebox.showinfo("ABOUT", msg)

	def show_Mechanics(self):
		messagebox.showinfo("MECHANICS", "  At the start of the game, all pacmen are placed at the corners of the map. The pacmen can move using the up, down, left, and right arrow keys. The pacmen will run through the maze to eat pac-dots and pac-stars. One pac-star will appear every 15 seconds after one pac-star has been eaten. If a pacman gets to eat a pac-star, he will be given a temporary ability to eat the other pacmen. The amount of time a pacman can have this ability is only 5 seconds. The pacman that has been eaten will be revived at the middle of the map. However, he will not be able to move for the first 3 seconds upon revival. When the game is over, the pacman that has the most number of pac-points wins. Players can chat during the game.\n\n1 pac-dot : 1pt\n1 eaten pacman : 3pts")

	def exit_Game(self):
		prompt = messagebox.askyesno("EXIT", "Are you sure you want to exit? No data will be saved.")
		if prompt == True:
			self.window.destroy()

	def game_map(self):
		global map_Frame
		map_Frame = Frame(self.window, bg="BLACK", pady=20)
		map_Frame.pack()
		self.create_Map()

		# MENU BOX FRAME ----------------------------------------------------------
		global optionsFrm
		optionsFrm = Frame(self.window, bg="BLACK")

		lobby_id_lbl = Label(optionsFrm, text="Lobby ID: "+self.lobby_id_udp, bg="BLACK", fg="WHITE")
		lobby_id_lbl.grid(column=0, row=0, padx=40)

		map_name_lbl = Label(optionsFrm, text="Map 1", bg="#80dba6", padx=15)
		map_name_lbl.grid(column=1, row=0, padx=40)	
		
		global Back_btn
		Back_btn = Button(optionsFrm, text="Exit Game",bg="sky blue", padx=15, pady=0, command=self.exit)
		Back_btn.grid(column=2, row=0, padx=40)	

		optionsFrm.pack()


		# INSTRUCTION AND SCOREBOARD -------------------------------------------------
		grp_Frm = Frame(self.window, bg="BLACK")
		grp_Frm.pack(fill=X)

		# INSTRUCTIONS LABEL FRAME -------------------------------------------------
		inst_Frm = LabelFrame(grp_Frm,text = "INSTRUCTIONS", bg = "BLACK", fg = "WHITE", font="ARIAL")
		inst_Frm.pack(side=LEFT, ipadx=50, padx=10)

		up_Arrow = Label(inst_Frm, text = "Up Arrow Key - Go Up", bg = "BLACK", fg = "WHITE")
		up_Arrow.pack()
		down_Arrow = Label(inst_Frm, text = "Down Arrow Key - Go Down", bg = "BLACK", fg = "WHITE")
		down_Arrow.pack()
		right_Arrow = Label(inst_Frm, text = "Right Arrow Key - Go Right", bg = "BLACK", fg = "WHITE")
		right_Arrow.pack()
		left_Arrow = Label(inst_Frm, text = "Left Arrow Key - Go Left", bg = "BLACK", fg = "WHITE")
		left_Arrow.pack()

		# SCOREBOARD -------------------------------------------------------------
		score_Frm = LabelFrame(grp_Frm,text = "SCOREBOARD", bg = "BLACK", fg = "RED", height=50, width=200, font="ARIAL")
		score_Frm.pack(side=LEFT, ipadx=50)

		x1 = Label(score_Frm, text = "Up Arrow Key - Go Up", bg = "BLACK", fg = "WHITE")
		x1.pack()
		x2 = Label(score_Frm, text = "Down Arrow Key - Go Down", bg = "BLACK", fg = "WHITE")
		x2.pack()
		x3 = Label(score_Frm, text = "Up Arrow Key - Go Up", bg = "BLACK", fg = "WHITE")
		x3.pack()
		x4 = Label(score_Frm, text = "Down Arrow Key - Go Down", bg = "BLACK", fg = "WHITE")
		x4.pack()

		separator = Frame(height=2, bd=1, relief=SUNKEN)
		separator.pack(fill=X, padx=5, pady=5)
	
	def key_listeners(self, event):
		print(event.keysym)
		self.move(event.keysym)

	def create_Map(self):
		block_height = 20 * len(self.map_matrix)
		block_width = 20 * len(self.map_matrix[0])
		self.canvas = tkinter.Canvas(map_Frame, bg="BLACK", height=block_height, width=block_width)
		self.canvas.pack()
		
		y_pos = 0 # starting pixel in self.canvas
		increment = 20 # to determine next position
		for row in range(len(self.map_matrix)):
			x_pos = 0
			for col in range(len(self.map_matrix[row])):
				if self.map_matrix[row][col] == "D":		# PAC-DOT
					block = self.canvas.create_oval(x_pos+8, y_pos+8, x_pos-8+increment, y_pos-8+increment, fill="WHITE", outline="")
				elif self.map_matrix[row][col] == "s":	# STAR
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
					block = self.canvas.create_polygon(ax, ay, cx, cy, ex, ey, bx, by, dx, dy, fill="YELLOW", outline="")
				elif self.map_matrix[row][col] == "w":	# WALL
					block = self.canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLUE", outline="")
				elif self.map_matrix[row][col] == "e":	# EMPTY FLOOR
					block = self.canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLACK", outline="")
				elif self.map_matrix[row][col] == "P":	# PLAYER
					block = Yellow(map_Frame,self.canvas,x_pos+increment-8,y_pos+increment-8,"Right")
				x_pos += increment
			y_pos += increment
		
		self.canvas.bind_all("<KeyPress-Up>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Down>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Left>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Right>", self.key_listeners) # binds event listener to whole self.canvas

	def renew_map(self):
		block_height = 20 * len(self.map_matrix)
		block_width = 20 * len(self.map_matrix[0])
		self.canvas.pack_forget()
		self.canvas = tkinter.Canvas(map_Frame, bg="BLACK", height=block_height, width=block_width)
		self.canvas.pack()
		
		y_pos = 0 # starting pixel in self.canvas
		increment = 20 # to determine next position
		for row in range(len(self.map_matrix)):
			x_pos = 0
			for col in range(len(self.map_matrix[row])):
				if self.map_matrix[row][col] == "D":		# PAC-DOT
					block = self.canvas.create_oval(x_pos+8, y_pos+8, x_pos-8+increment, y_pos-8+increment, fill="WHITE", outline="")
				elif self.map_matrix[row][col] == "s":	# STAR
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
					block = self.canvas.create_polygon(ax, ay, cx, cy, ex, ey, bx, by, dx, dy, fill="YELLOW", outline="")
				elif self.map_matrix[row][col] == "w":	# WALL
					block = self.canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLUE", outline="")
				elif self.map_matrix[row][col] == "e":	# EMPTY FLOOR
					block = self.canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLACK", outline="")
				elif self.map_matrix[row][col] == "P":	# PLAYER
					block = Yellow(map_Frame,self.canvas, x_pos+increment-8, y_pos+increment-8, "Right")
				x_pos += increment
			y_pos += increment
		
		self.canvas.bind_all("<KeyPress-Up>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Down>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Left>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Right>", self.key_listeners) # binds event listener to whole self.canvas
		

	# GETS PLAYER'S NAME ================================================================================================

	def getPlayerType(self):
		player_type = messagebox.askquestion("USER TYPE", "Are you the host?\nPress YES if you are the host. NO if you're just a player.")
		if player_type == "yes":
			player_type = "h"
		else:
			player_type = "p"
		return player_type


	def btn_ok(self, event=None):
		if name_Entry.get().isalnum():
			self.player_name = name_Entry.get()
			# player =  InstantiatePlayer(name_Entry.get()) 		# instantiate player
			# packet = TcpPacket() 		# instantiate packet

			self.player_type = self.getPlayerType()
			self.player = pacman.Player(self.player_name, self.player_type)
			port = simpledialog.askstring("Port Number", "Enter port number", parent=name_Frm)
			self.port = int(port)
			self.connect()
			# HOST ==========================================
			if self.player_type == "h":
				self.lobby_id_udp = self.create_room()
				# max_players = simpledialog.askinteger("Max Players", "Enter max number of players", parent=name_Frm)
				# connectPacket =  ConnectHostToServer(player,packet,max_players)
				# lobby_id = connectPacket.lobby_id

			# NOT HOST ========================================
			else:
				lobby_id = simpledialog.askstring("Lobby ID", "Enter lobby ID", parent=name_Frm)
				self.lobby_id_udp = lobby_id

				# connectPacket = packet.ConnectPacket()
				# connectPacket.type = 5
				# L = Label()
				# while connectPacket.type==5 or connectPacket.type==6: 

				# 	lobby_id = simpledialog.askstring("Lobby ID", "Enter lobby ID", parent=name_Frm)
				# 	connectPacket =  ConnectPlayerToServer(player, connectPacket, lobby_id)
				# 	L.destroy()

				# 	# Lobby does not exist
				# 	if connectPacket.type==5:
				# 		L = Label(name_Frm, text="Lobby does not exist!", bg="BLACK", fg="RED")
				# 		L.grid(column=0, row=3, columnspan=2)

				# 	# Lobby full
				# 	if connectPacket.type==6:
				# 		L = Label(name_Frm, text="Lobby full!", bg="BLACK", fg="RED")
				# 		L.grid(column=0, row=3, columnspan=2)

				# print('Received from server: ' + str(connectPacket))  # show in terminal
				# print(connectPacket.player.name + " has entered the chat room.")
			if self.join(self.lobby_id_udp) == True:
				while True:
					num_of_players = self.recvNumOfPlayers()
					print(num_of_players)
					if num_of_players == 3:
						name_Frm.pack_forget()
						self.startGame()
						break		

			# game_map(chosen_map, player, packet, lobby_id, connectPacket) 	# show game
			# self.game_map()
		else:
			L = Label(name_Frm, text="Invalid name. Must consist of \nletters and numbers only.", bg="BLACK", fg="RED")
			L.grid(column=0, row=3, columnspan=2)

	def btn_cancel(self):
		name_Frm.pack_forget()
		self.main_frame.pack()

	# Name of chosen map
	def get_name(self, map_selected):
		global chosen_map
		chosen_map = map_selected
		self.selected_map = map_selected

		self.main_frame.pack_forget()

		global name_Frm
		name_Frm = Frame(self.window, bg="BLACK", pady=100)

		# Ask for player's name
		L = Label(name_Frm, text="Please enter your name", bg="BLACK", fg="WHITE", pady=20)
		L.grid(column=0, row=0, columnspan=2)
		global name_Entry
		name_Entry = Entry(name_Frm, width=20)
		name_Entry.grid(column=0, row=1, columnspan=2)
		w = Button(name_Frm, text="Proceed", width=10, command=self.btn_ok)
		w.grid(column=0, row=2, padx=5, pady=20)
		w = Button(name_Frm, text="Cancel", width=10, command=self.btn_cancel)
		w.grid(column=1, row=2, padx=5, pady=20)
		name_Entry.focus_set()
		name_Entry.bind("<Return>", self.btn_ok)

		name_Frm.pack()
