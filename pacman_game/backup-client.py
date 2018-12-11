import udp_packet as udp
import tkinter
from tkinter import *
from tkinter import messagebox, simpledialog
import socket

# hows:
# different port number per client
send = udp.UDPpacket.send_data

class Client(socket.socket):
	BUFFER_SIZE = 4096
	player_name = "John Doe"
	player_type = "HOST"

	def __init__(self, host_address, port):
		socket.socket.__init__(self, type=socket.SOCK_DGRAM)		
		self.server_address = (host_address, port)
		
	def connect(self, player_name, player_type):
		self.player_name = player_name
		self.player_type = player_type
		data = ["CONNECT", self.player_name, self.player_type]
		send(self.server_address, data)

		if self.player_type == "HOST":
			self.create_room()
		elif self.player_type == "PLAYER":
			self.join()

		self.start_game("map1.txt")
		
		#data, address_info = self.recvfrom(self.BUFFER_SIZE)
		#deserialized_data = pickle.loads(data)
		#print("received: ", deserialized_data)		

	def create_room(self):	# if host
		data = ["CREATE_ROOM", self.player_name]
		send(self.server_address, data)
		
	def join(self):	# if not
		data = ["JOIN", self.player_name]
		send(self.server_address, data)
		
	def start_game(self, map_name):
		data = ["START_GAME", map_name]
		print("entered start_game")
		send(self.server_address, data)

	def move(self):
		data = ["MOVE", "UP"]
		send(self.server_address, data)
	
	def on_execute(self):
		while True:
			print("entered on exec")
			data, address_info = self.recvfrom(self.BUFFER_SIZE)
			print("address info on exec")
			print(address_info)
			deserialized_data = pickle.loads(data)
			print("received: ", deserialized_data)
			# # map_matrix = deserialized_data[1]
			# while True:
			# 	# print()
			# 	pass
			# 	render_board()
			
	def render_board(self):

		def pacman_window():
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

		def main():
			window = pacman_window()
			return window

		def game_map():
			global map_Frame
			map_Frame = Frame(window, bg="BLACK", pady=20)
			map_Frame.pack()
			create_Map()
		
		def key_listeners(event):
			print(event.keysym)

		def create_Map():
			block_height = 20 * len(self.map_matrix)
			block_width = 20 * len(self.map_matrix[0])
			global canvas
			canvas = tkinter.Canvas(map_Frame, bg="BLACK", height=block_height, width=block_width)
			canvas.pack()
			
			y_pos = 0 # starting pixel in canvas
			increment = 20 # to determine next position
			for row in range(len(self.map_matrix)):
				x_pos = 0
				for col in range(len(self.map_matrix[row])):
					if self.map_matrix[row][col] == "D":		# PAC-DOT
						block = canvas.create_oval(x_pos+8, y_pos+8, x_pos-8+increment, y_pos-8+increment, fill="WHITE", outline="")
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
						block = canvas.create_polygon(ax, ay, cx, cy, ex, ey, bx, by, dx, dy, fill="YELLOW", outline="")
					elif self.map_matrix[row][col] == "w":	# WALL
						block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLUE", outline="")
					elif self.map_matrix[row][col] == "e":	# EMPTY FLOOR
						block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="BLACK", outline="")
					elif self.map_matrix[row][col] == "P":	# PLAYER
						block = canvas.create_rectangle(x_pos, y_pos, x_pos+increment, y_pos+increment, fill="RED", outline="")
					x_pos += increment
				y_pos += increment
			
			canvas.bind_all("<KeyPress-Up>", key_listeners) # binds event listener to whole canvas
			canvas.bind_all("<KeyPress-Down>", key_listeners) # binds event listener to whole canvas
			canvas.bind_all("<KeyPress-Left>", key_listeners) # binds event listener to whole canvas
			canvas.bind_all("<KeyPress-Right>", key_listeners) # binds event listener to whole canvas
		
		window = main()
		window.resizable(width=FALSE, height=FALSE)
		game_map()

		# window.mainloop()


# send('0.0.0.0', 10939, data)