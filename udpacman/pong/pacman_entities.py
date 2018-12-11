import pygame
from pygame.math import Vector2
import tkinter
from tkinter import *
<<<<<<< HEAD
=======
import pacmanclient.pacman_main
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e
# from tkinter import messagebox

class World():
	WIDTH = 500
	HEIGHT = 500
<<<<<<< HEAD

=======
	map_matrix = []
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e
	def __init__(self, filename):
		self.filename = filename
		self.game_map()

	def pacman_window(self):
		window = tkinter.Tk()
		window.title("BATTLE OF THE PACMEN")
		w = 500 # width for tk_window
		h = 500 # height for tk_window
		x = (window.winfo_screenwidth()/2) - (w/2) # calculate x and y coordinates for tk_window
		y = (window.winfo_screenheight()/2) - (h/2)
		# set the dimensions of the screen and where it is placed
		window.geometry('%dx%d+%d+%d' % (w, h, x, y))
		window.configure(bg="BLACK", padx=50, pady=50)
		return window

	def draw_map(self):
		block_height = 20 * len(self.map_matrix)
		block_width = 20 * len(self.map_matrix[0])
		self.canvas = tkinter.Canvas(self.map_Frame, bg="BLACK", height=block_height, width=block_width)
		self.canvas.pack()
		
		y_pos = 0 # starting pixel in canvas
		increment = 20 # to determine next position

		for row in range(len(self.map_matrix)):
			print("Entered here")
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

<<<<<<< HEAD
		# surface = pygame.Surface(500,500)
		# return pygame.rect(surface, (0,255,255), [0,0,10,10])

=======
		self.canvas.bind_all("<KeyPress-Up>", pacmanclient.pacman_main.key_listeners) # binds event listener to whole canvas
		self.canvas.bind_all("<KeyPress-Down>", pacmanclient.pacman_main.key_listeners) # binds event listener to whole canvas
		self.canvas.bind_all("<KeyPress-Left>", pacmanclient.pacman_main.key_listeners) # binds event listener to whole canvas
		self.canvas.bind_all("<KeyPress-Right>", pacmanclient.pacman_main.key_listeners) # binds event listener to whole canvas

		# surface = pygame.Surface(500,500)
		# return pygame.rect(surface, (0,255,255), [0,0,10,10])

	def set_canvas(self,a,b,c,d, color):
		block = self.canvas.create_rectangle(a,b,c,d, fill=color, outline="")
	
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e

	def game_map(self):
		window = self.pacman_window()
		self.map_Frame = Frame(window, bg="BLACK", pady=20)
		
		map_template = open(self.filename, "r")
		map_name = "Map 1"

		if map_template == None:
			print("file not found")

		self.map_matrix = []
		for lines in map_template:
			line = []
			line[0:len(lines)] = iter(lines)
			self.map_matrix.append(line)
		
		self.map_Frame.pack()
		self.draw_map()

<<<<<<< HEAD
	def get_map_matrix():
=======
	def get_map_matrix(self):
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e
		return self.map_matrix

	def insert_object_to_map_matrix(self,xPos,yPos, entity):
		self.map_matrix[xPos][yPos] = entity
<<<<<<< HEAD
		block = self.canvas.create_rectangle(yPos*20, xPos*20, yPos*20+20, xPos*20+20, fill="BLACK", outline="")
		block = self.canvas.create_rectangle(yPos*20, (xPos+1)*20, yPos*20+20, (xPos+1)*20+20, fill="RED", outline="")
=======
		block = self.canvas.create_rectangle(yPos*20, xPos*20, yPos*20+20, xPos*20+20, fill="RED", outline="")
		# block = self.canvas.create_rectangle(yPos*20, (xPos+1)*20, yPos*20+20, (xPos+1)*20+20, fill="RED", outline="")
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e

class GameEntity():
	world = None

	def __init__(self, location=None):
		if self.world is None:
		   super().__init__()
		else:
		   super().__init__(GameEntity.world)    # Place this in the world automatically

class Pacman(GameEntity):
<<<<<<< HEAD
=======
	xPos=1
	yPos=1
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e
	def __init__(self, color, player_name, world):
		self.world = world
		self.color = color
		self.player_name = player_name
		if self.color == "yellow":
			self.xPos = 1
<<<<<<< HEAD
			self.yPos = 1

		world.insert_object_to_map_matrix(self.xPos,self.yPos,"P")

		def get_xPos(self):
			return self.xPos
		def get_yPos(self):
			return self.yPos
=======
			self.yPos = 3

		world.insert_object_to_map_matrix(self.xPos,self.yPos,"P")

	def get_xPos(self):
		return self.xPos
	def get_yPos(self):
		return self.yPos
>>>>>>> a0fef4317ce4d9a25f687f0f1ab8d469c581373e

# world = World("map1.txt")
# window = world.pacman_window()
# window.resizable(width=FALSE, height=FALSE)
# pacman = Pacman("yellow", "player", world)


<<<<<<< HEAD
# window.mainloop()
=======
# window.mainloop()
>>>>>>> 99fec82637b17bcd512f51a9a57b546361bc3fd5
