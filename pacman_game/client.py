#Instantiate socket as attribute
# attribute niya yung server address 
#socket.setblocking(0)
import socket
import pacman
import pickle
import udp_packet as UDPpacket
import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog

class Client():
	socket = None
	BUFFER_SIZE = 4096
	server_address = ('0.0.0.0', 10939)
	hostname = ''
	port = ''
	client_addr = ''
	map_matrix = []
	window = ''
	canvas = ''
	#Bale gagawin natin na equivalent si CLIENT and PLAYER
	def __init__(self, player_name, player_type):
		self.player = pacman.Player(player_name, player_type)

	#Connect Client to Server
	def connect(self):
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
		print(loaded_data.lobby_id)
		#return lobby id
		return(loaded_data.lobby_id)

	def join(self, lobby_id):
		joinPacket = UDPpacket.UDPpacket("JOIN")
		joinPacket.player = self.player
		joinPacket.lobby_id = lobby_id
		self.socket.sendto(pickle.dumps(joinPacket), self.server_address)	

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
		self.render_window()

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
		self.game_map()
		self.window.mainloop()

	def pacman_window(self):
		tk_window = tkinter.Tk()
		tk_window.title("BATTLE OF THE PACMEN")
		w = 500 # height for tk_window
		h = 600 # height for tk_window
		x = (tk_window.winfo_screenwidth()/2) - (w/2) # calculate x and y coordinates for tk_window
		y = (tk_window.winfo_screenheight()/2) - (h/2)
		# set the dimensions of the screen and where it is placed
		tk_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
		tk_window.configure(bg="BLACK", padx=50, pady=50)
		return tk_window

	def game_map(self):
		global map_Frame
		map_Frame = Frame(self.window, bg="BLACK", pady=20)
		map_Frame.pack()
		self.create_Map()
	
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
					block = self.canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="RED", outline="")
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
					block = self.canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="RED", outline="")
				x_pos += increment
			y_pos += increment
		
		self.canvas.bind_all("<KeyPress-Up>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Down>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Left>", self.key_listeners) # binds event listener to whole self.canvas
		self.canvas.bind_all("<KeyPress-Right>", self.key_listeners) # binds event listener to whole self.canvas
		


