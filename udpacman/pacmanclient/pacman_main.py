import pacmanserver.server
import pacmanclient.pacman_client
import random
from pygame.locals import *
import pygame
<<<<<<< HEAD

=======
import pong.pacman_entities
import tkinter
from tkinter import *

pygame.init()
>>>>>>> 668eb8a57c0825110838ccf801f22fa5b0dbf731
address = input("Server address (host:port) = ")
host, port = address.split(':')
port = int(port)

SERVER_ADDRESS = (host, port)
<<<<<<< HEAD
SCREEN_SIZE = (300, 500)

def main():
=======
# SCREEN_SIZE = (pong.pacman_entities.World.WIDTH, pong.pacman_entities.World.HEIGHT)

def key_listeners(event):
	player_xpos = pong.pacman_entities.Pacman.get_xPos(pong.pacman_entities.Pacman)
	player_ypos = pong.pacman_entities.Pacman.get_yPos(pong.pacman_entities.Pacman) 
	map_matrix = pong.pacman_entities.World.get_map_matrix(pong.pacman_entities.World)
	print("MAP MATRIX")
	print(map_matrix)
	if event.keysym == "Left":
		print("Entered left")
		if map_matrix[player_xpos][player_ypos-1] == "D" or map_matrix[player_xpos][player_ypos-1] == "s" or map_matrix[player_xpos][player_ypos-1] == "e":
			map_matrix[player_xpos][player_ypos] = "e"
			map_matrix[player_xpos][player_ypos-1] = "P"
			pong.pacman_entities.World.set_canvas(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, "BLACK")
			pong.pacman_entities.World.set_canvas((player_ypos-1)*20, player_xpos*20, (player_ypos-1)*20+20, player_xpos*20+20, "RED")
			# block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
			# block = canvas.create_rectangle((player_ypos-1)*20, player_xpos*20, (player_ypos-1)*20+20, player_xpos*20+20, fill="RED", outline="")
	# elif event.keysym == "Right":
	# 	if map_matrix[player_xpos][player_ypos+1] == "D" or map_matrix[player_xpos][player_ypos+1] == "s" or map_matrix[player_xpos][player_ypos+1] == "e":
	# 		map_matrix[player_xpos][player_ypos] = "e"
	# 		map_matrix[player_xpos][player_ypos+1] = "P"
	# 		block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
	# 		block = canvas.create_rectangle((player_ypos+1)*20, player_xpos*20, (player_ypos+1)*20+20, player_xpos*20+20, fill="RED", outline="")
	# elif event.keysym == "Up":
	# 	if map_matrix[player_xpos-1][player_ypos] == "D" or map_matrix[player_xpos-1][player_ypos] == "s" or map_matrix[player_xpos-1][player_ypos] == "e":
	# 		map_matrix[player_xpos][player_ypos] = "e"
	# 		map_matrix[player_xpos-1][player_ypos] = "P"
	# 		block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
	# 		block = canvas.create_rectangle(player_ypos*20, (player_xpos-1)*20, player_ypos*20+20, (player_xpos-1)*20+20, fill="RED", outline="")
	# elif event.keysym == "Down":
	# 	if map_matrix[player_xpos+1][player_ypos] == "D" or map_matrix[player_xpos+1][player_ypos] == "s" or map_matrix[player_xpos+1][player_ypos] == "e":
	# 		map_matrix[player_xpos][player_ypos] = "e"
	# 		map_matrix[player_xpos+1][player_ypos] = "P"
	# 		block = canvas.create_rectangle(player_ypos*20, player_xpos*20, player_ypos*20+20, player_xpos*20+20, fill="BLACK", outline="")
	# 		block = canvas.create_rectangle(player_ypos*20, (player_xpos+1)*20, player_ypos*20+20, (player_xpos+1)*20+20, fill="RED", outline="")


def main():


>>>>>>> 668eb8a57c0825110838ccf801f22fa5b0dbf731
	#Randomly generate the address for this client
	local_address = ('localhost', random.randint(10000, 20000))

	server_handler = pacmanclient.pacman_client.ServerHandler(local_address,
														SERVER_ADDRESS
														)
	server_handler.start()
<<<<<<< HEAD
	screen = pygame.display.set_mode(SCREEN_SIZE)
	pygame.display.set_caption('GUI Client')
	while True:
		for event in pygame.event.get():

			if event.type == KEYDOWN:
				print("down")
		
		#print("game begins")
=======
	

	world = pong.pacman_entities.World("map1.txt")
	window = world.pacman_window()
	window.resizable(width=FALSE, height=FALSE)
	global pacman
	pacman = pong.pacman_entities.Pacman("yellow", "player", world)
	window.mainloop()
		
>>>>>>> 668eb8a57c0825110838ccf801f22fa5b0dbf731

	return

if __name__ == '__main__':
	main()